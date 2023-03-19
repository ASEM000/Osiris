from __future__ import annotations

import functools as ft
from typing import Any, Callable

import jax
import jax.numpy as jnp
import jax.random as jr
import pytreeclass as pytc

import serket as sk
from serket.nn.callbacks import frozen_positive_int_cbs
from serket.nn.lazy_class import lazy_class
from serket.nn.utils import (
    DilationType,
    InitFuncType,
    KernelSizeType,
    PaddingType,
    StridesType,
    _act_func_map,
)

"""Defines RNN related classes."""


# =============================================== Non Spatial RNN ==================================================== #


@pytc.treeclass
class RNNState:
    hidden_state: jax.Array


@pytc.treeclass
class RNNCell:
    pass


class SimpleRNNState(RNNState):
    pass


def infer_func(self, *args, **kwargs):
    return (args[0].shape[0],)


@ft.partial(lazy_class, lazy_keywords=["in_features"], infer_func=infer_func)
@pytc.treeclass
class SimpleRNNCell(RNNCell):
    in_features: int = pytc.field(callbacks=[*frozen_positive_int_cbs])
    hidden_features: int = pytc.field(callbacks=[*frozen_positive_int_cbs])
    in_to_hidden: sk.nn.Linear
    hidden_to_hidden: sk.nn.Linear

    def __init__(
        self,
        in_features: int,
        hidden_features: int,
        *,
        weight_init_func: InitFuncType = "glorot_uniform",
        bias_init_func: InitFuncType = "zeros",
        recurrent_weight_init_func: InitFuncType = "orthogonal",
        act_func: str | Callable[[Any], Any] | None = jax.nn.tanh,
        key: jr.KeyArray = jr.PRNGKey(0),
    ):
        """Vanilla RNN cell that defines the update rule for the hidden state
        See:
            https://www.tensorflow.org/api_docs/python/tf/keras/layers/SimpleRNNCell.

        Args:
            in_features: the number of input features
            hidden_features: the number of hidden features
            weight_init_func: the function to use to initialize the weights
            bias_init_func: the function to use to initialize the bias
            recurrent_weight_init_func: the function to use to initialize the recurrent weights
            act_func: the activation function to use for the hidden state update
            key: the key to use to initialize the weights

        Example:
            >>> cell = SimpleRNNCell(10, 20) # 10-dimensional input, 20-dimensional hidden state
            >>> rnn_state = cell.init_state()
            >>> x = jnp.ones((10,)) # 10 features
            >>> result = cell(x, rnn_state)
            >>> result.hidden_state.shape  # 20 features
        """
        k1, k2 = jr.split(key, 2)

        self.in_features = in_features
        self.hidden_features = hidden_features
        self.act_func = _act_func_map.get(act_func, act_func)

        self.in_to_hidden = sk.nn.Linear(
            in_features,
            hidden_features,
            weight_init_func=weight_init_func,
            bias_init_func=bias_init_func,
            key=k1,
        )

        self.hidden_to_hidden = sk.nn.Linear(
            hidden_features,
            hidden_features,
            weight_init_func=recurrent_weight_init_func,
            bias_init_func=None,
            key=k2,
        )

    def __call__(self, x: jax.Array, state: SimpleRNNState, **k) -> SimpleRNNState:
        if not isinstance(state, SimpleRNNState):
            msg = "Expected state to be an instance of `SimpleRNNState`"
            msg += f", got {type(state).__name__}"
            raise TypeError(msg)

        h = state.hidden_state
        h = self.act_func(self.in_to_hidden(x) + self.hidden_to_hidden(h))
        return SimpleRNNState(h)

    def init_state(self) -> SimpleRNNState:
        shape = (self.hidden_features,)
        return SimpleRNNState(jnp.zeros(shape))


@pytc.treeclass
class LSTMState(RNNState):
    cell_state: jax.Array


@ft.partial(lazy_class, lazy_keywords=["in_features"], infer_func=infer_func)
@pytc.treeclass
class LSTMCell(RNNCell):
    in_features: int = pytc.field(callbacks=[*frozen_positive_int_cbs])
    hidden_features: int = pytc.field(callbacks=[*frozen_positive_int_cbs])
    in_to_hidden: sk.nn.Linear
    hidden_to_hidden: sk.nn.Linear

    def __init__(
        self,
        in_features: int,
        hidden_features: int,
        *,
        weight_init_func: str | Callable = "glorot_uniform",
        bias_init_func: str | Callable | None = "zeros",
        recurrent_weight_init_func: str | Callable = "orthogonal",
        act_func: str | Callable[[Any], Any] | None = "tanh",
        recurrent_act_func: str | Callable[[Any], Any] | None = "sigmoid",
        key: jr.KeyArray = jr.PRNGKey(0),
    ):
        """LSTM cell that defines the update rule for the hidden state and cell state
        Args:
            in_features: the number of input features
            hidden_features: the number of hidden features
            weight_init_func: the function to use to initialize the weights
            bias_init_func: the function to use to initialize the bias
            recurrent_weight_init_func: the function to use to initialize the recurrent weights
            act_func: the activation function to use for the hidden state update
            recurrent_act_func: the activation function to use for the cell state update
            key: the key to use to initialize the weights

        See:
            https://www.tensorflow.org/api_docs/python/tf/keras/layers/LSTMCell
            https://github.com/deepmind/dm-haiku/blob/main/haiku/_src/recurrent.py
        """
        k1, k2 = jr.split(key, 2)

        self.in_features = in_features
        self.hidden_features = hidden_features
        self.act_func = _act_func_map.get(act_func, act_func)
        self.recurrent_act_func = _act_func_map.get(
            recurrent_act_func, recurrent_act_func
        )

        self.in_to_hidden = sk.nn.Linear(
            in_features,
            hidden_features * 4,
            weight_init_func=weight_init_func,
            bias_init_func=bias_init_func,
            key=k1,
        )

        self.hidden_to_hidden = sk.nn.Linear(
            hidden_features,
            hidden_features * 4,
            weight_init_func=recurrent_weight_init_func,
            bias_init_func=None,
            key=k2,
        )

    def __call__(self, x: jax.Array, state: LSTMState, **k) -> LSTMState:
        if not isinstance(state, LSTMState):
            msg = "Expected state to be an instance of `LSTMState`"
            msg += f", got {type(state).__name__}"
            raise TypeError(msg)

        h, c = state.hidden_state, state.cell_state
        h = self.in_to_hidden(x) + self.hidden_to_hidden(h)
        i, f, g, o = jnp.split(h, 4, axis=-1)
        i = self.recurrent_act_func(i)
        f = self.recurrent_act_func(f)
        g = self.act_func(g)
        o = self.recurrent_act_func(o)
        c = f * c + i * g
        h = o * self.act_func(c)
        return LSTMState(h, c)

    def init_state(self) -> LSTMState:
        shape = (self.hidden_features,)
        return LSTMState(jnp.zeros(shape), jnp.zeros(shape))


class GRUState(RNNState):
    pass


@ft.partial(lazy_class, lazy_keywords=["in_features"], infer_func=infer_func)
@pytc.treeclass
class GRUCell(RNNCell):
    in_features: int = pytc.field(callbacks=[*frozen_positive_int_cbs])
    hidden_features: int = pytc.field(callbacks=[*frozen_positive_int_cbs])
    in_to_hidden: sk.nn.Linear
    hidden_to_hidden: sk.nn.Linear

    def __init__(
        self,
        in_features: int,
        hidden_features: int,
        *,
        weight_init_func: InitFuncType = "glorot_uniform",
        bias_init_func: InitFuncType = "zeros",
        recurrent_weight_init_func: InitFuncType = "orthogonal",
        act_func: str | Callable[[Any], Any] | None = "tanh",
        recurrent_act_func: str | Callable[[Any], Any] | None = "sigmoid",
        key: jr.KeyArray = jr.PRNGKey(0),
    ):
        """GRU cell that defines the update rule for the hidden state and cell state
        Args:
            in_features: the number of input features
            hidden_features: the number of hidden features
            weight_init_func: the function to use to initialize the weights
            bias_init_func: the function to use to initialize the bias
            recurrent_weight_init_func: the function to use to initialize the recurrent weights
            act_func: the activation function to use for the hidden state update
            recurrent_act_func: the activation function to use for the cell state update
            key: the key to use to initialize the weights

        See:
            https://keras.io/api/layers/recurrent_layers/gru/
        """
        k1, k2 = jr.split(key, 2)

        self.in_features = in_features
        self.hidden_features = hidden_features
        self.act_func = _act_func_map.get(act_func, act_func)
        self.recurrent_act_func = _act_func_map[recurrent_act_func]

        self.in_to_hidden = sk.nn.Linear(
            in_features,
            hidden_features * 3,
            weight_init_func=weight_init_func,
            bias_init_func=bias_init_func,
            key=k1,
        )

        self.hidden_to_hidden = sk.nn.Linear(
            hidden_features,
            hidden_features * 3,
            weight_init_func=recurrent_weight_init_func,
            bias_init_func=None,
            key=k2,
        )

    def __call__(self, x: jax.Array, state: GRUState, **k) -> GRUState:
        if not isinstance(state, GRUState):
            msg = "Expected state to be an instance of `GRUState`"
            msg += f", got {type(state).__name__}"
            raise TypeError(msg)

        h = state.hidden_state
        xe, xu, xo = jnp.split(self.in_to_hidden(x), 3, axis=-1)
        he, hu, ho = jnp.split(self.hidden_to_hidden(h), 3, axis=-1)
        e = self.recurrent_act_func(xe + he)
        u = self.recurrent_act_func(xu + hu)
        o = self.act_func(xo + (e * ho))
        h = (1 - u) * o + u * h
        return GRUState(hidden_state=h)

    def init_state(self) -> GRUState:
        shape = (self.hidden_features,)
        return GRUState(jnp.zeros(shape, dtype=jnp.float32))


# =============================================== Spatial RNN ======================================================= #


@pytc.treeclass
class SpatialRNNCell:
    pass


# ------------------------------------------------- ConvLSTM RNN ----------------------------------------------------- #


@pytc.treeclass
class ConvLSTMNDState(RNNState):
    cell_state: jax.Array


@ft.partial(lazy_class, lazy_keywords=["in_features"], infer_func=infer_func)
@pytc.treeclass
class ConvLSTMNDCell(SpatialRNNCell):
    in_features: int = pytc.field(callbacks=[*frozen_positive_int_cbs])
    out_features: int = pytc.field(callbacks=[*frozen_positive_int_cbs])
    in_to_hidden: Any
    hidden_to_hidden: Any

    def __init__(
        self,
        in_features: int,
        out_features: int,
        kernel_size: KernelSizeType,
        *,
        strides: StridesType = 1,
        padding: PaddingType = "SAME",
        input_dilation: DilationType = 1,
        kernel_dilation: DilationType = 1,
        weight_init_func: InitFuncType = "glorot_uniform",
        bias_init_func: InitFuncType = "zeros",
        recurrent_weight_init_func: InitFuncType = "orthogonal",
        act_func: str | Callable[[Any], Any] | None = "tanh",
        recurrent_act_func: str | Callable[[Any], Any] | None = "hard_sigmoid",
        key: jr.KeyArray = jr.PRNGKey(0),
        conv_layer: Any = None,
        spatial_ndim: int = 1,
    ):
        """Convolution LSTM cell that defines the update rule for the hidden state and cell state
        Args:
            in_features: Number of input features
            out_features: Number of output features
            kernel_size: Size of the convolutional kernel
            strides: Stride of the convolution
            padding: Padding of the convolution
            input_dilation: Dilation of the input
            kernel_dilation: Dilation of the convolutional kernel
            weight_init_func: Weight initialization function
            bias_init_func: Bias initialization function
            recurrent_weight_init_func: Recurrent weight initialization function
            act_func: Activation function
            recurrent_act_func: Recurrent activation function
            key: PRNG key
            spatial_ndim: Number of spatial dimensions

        See: https://www.tensorflow.org/api_docs/python/tf/keras/layers/ConvLSTM1D
        """
        k1, k2 = jr.split(key, 2)

        self.in_features = in_features
        self.out_features = out_features
        self.spatial_ndim = spatial_ndim
        self.act_func = _act_func_map.get(act_func, act_func)
        self.recurrent_act_func = _act_func_map.get(recurrent_act_func, recurrent_act_func)  # fmt: skip

        self.in_to_hidden = conv_layer(
            in_features,
            out_features * 4,
            kernel_size,
            strides=strides,
            padding=padding,
            input_dilation=input_dilation,
            kernel_dilation=kernel_dilation,
            weight_init_func=weight_init_func,
            bias_init_func=bias_init_func,
            key=k1,
        )

        self.hidden_to_hidden = conv_layer(
            out_features,
            out_features * 4,
            kernel_size,
            strides=strides,
            padding=padding,
            input_dilation=input_dilation,
            kernel_dilation=kernel_dilation,
            weight_init_func=recurrent_weight_init_func,
            bias_init_func=None,
            key=k2,
        )

    def __call__(self, x: jax.Array, state: ConvLSTMNDState, **k) -> ConvLSTMNDState:
        if not isinstance(state, ConvLSTMNDState):
            msg = f"Expected state to be an instance of ConvLSTMNDState, got {type(state)}"
            raise TypeError(msg)

        h, c = state.hidden_state, state.cell_state
        h = self.in_to_hidden(x) + self.hidden_to_hidden(h)
        i, f, g, o = jnp.split(h, 4, axis=0)
        i = self.recurrent_act_func(i)
        f = self.recurrent_act_func(f)
        g = self.act_func(g)
        o = self.recurrent_act_func(o)
        c = f * c + i * g
        h = o * self.act_func(c)
        return ConvLSTMNDState(h, c)

    def init_state(self, spatial_dim: tuple[int, ...]) -> ConvLSTMNDState:
        msg = f"Expected spatial_dim to be a tuple of length {self.spatial_ndim}, got {spatial_dim}"
        assert len(spatial_dim) == self.spatial_ndim, msg
        shape = (self.out_features, *spatial_dim)
        return ConvLSTMNDState(jnp.zeros(shape), jnp.zeros(shape))


@pytc.treeclass
class ConvLSTM1DCell(ConvLSTMNDCell):
    def __init__(
        self,
        in_features: int,
        out_features: int,
        kernel_size: KernelSizeType,
        *,
        strides: StridesType = 1,
        padding: PaddingType = "SAME",
        input_dilation: DilationType = 1,
        kernel_dilation: DilationType = 1,
        weight_init_func: InitFuncType = "glorot_uniform",
        bias_init_func: InitFuncType = "zeros",
        recurrent_weight_init_func: InitFuncType = "orthogonal",
        act_func: str | Callable[[Any], Any] | None = "tanh",
        recurrent_act_func: str | Callable[[Any], Any] | None = "hard_sigmoid",
        key: jr.KeyArray = jr.PRNGKey(0),
    ):
        """1D Convolution LSTM cell that defines the update rule for the hidden state and cell state
        Args:
            in_features: Number of input features
            out_features: Number of output features
            kernel_size: Size of the convolutional kernel
            strides: Stride of the convolution
            padding: Padding of the convolution
            input_dilation: Dilation of the input
            kernel_dilation: Dilation of the convolutional kernel
            weight_init_func: Weight initialization function
            bias_init_func: Bias initialization function
            recurrent_weight_init_func: Recurrent weight initialization function
            act_func: Activation function
            recurrent_act_func: Recurrent activation function
            key: PRNG key
            spatial_ndim: Number of spatial dimensions.

        See: https://www.tensorflow.org/api_docs/python/tf/keras/layers/ConvLSTM1D
        """
        super().__init__(
            in_features=in_features,
            out_features=out_features,
            kernel_size=kernel_size,
            strides=strides,
            padding=padding,
            input_dilation=input_dilation,
            kernel_dilation=kernel_dilation,
            weight_init_func=weight_init_func,
            bias_init_func=bias_init_func,
            recurrent_weight_init_func=recurrent_weight_init_func,
            act_func=act_func,
            recurrent_act_func=recurrent_act_func,
            key=key,
            conv_layer=sk.nn.Conv1D,
            spatial_ndim=1,
        )


@pytc.treeclass
class ConvLSTM2DCell(ConvLSTMNDCell):
    def __init__(
        self,
        in_features: int,
        out_features: int,
        kernel_size: KernelSizeType,
        *,
        strides: StridesType = 1,
        padding: PaddingType = "SAME",
        input_dilation: DilationType = 1,
        kernel_dilation: DilationType = 1,
        weight_init_func: InitFuncType = "glorot_uniform",
        bias_init_func: InitFuncType = "zeros",
        recurrent_weight_init_func: InitFuncType = "orthogonal",
        act_func: str | Callable[[Any], Any] | None = "tanh",
        recurrent_act_func: str | Callable[[Any], Any] | None = "hard_sigmoid",
        key: jr.KeyArray = jr.PRNGKey(0),
    ):
        """2D Convolution LSTM cell that defines the update rule for the hidden state and cell state
        Args:
            in_features: Number of input features
            out_features: Number of output features
            kernel_size: Size of the convolutional kernel
            strides: Stride of the convolution
            padding: Padding of the convolution
            input_dilation: Dilation of the input
            kernel_dilation: Dilation of the convolutional kernel
            weight_init_func: Weight initialization function
            bias_init_func: Bias initialization function
            recurrent_weight_init_func: Recurrent weight initialization function
            act_func: Activation function
            recurrent_act_func: Recurrent activation function
            key: PRNG key
            spatial_ndim: Number of spatial dimensions.

        See: https://www.tensorflow.org/api_docs/python/tf/keras/layers/ConvLSTM1D
        """
        super().__init__(
            in_features=in_features,
            out_features=out_features,
            kernel_size=kernel_size,
            strides=strides,
            padding=padding,
            input_dilation=input_dilation,
            kernel_dilation=kernel_dilation,
            weight_init_func=weight_init_func,
            bias_init_func=bias_init_func,
            recurrent_weight_init_func=recurrent_weight_init_func,
            act_func=act_func,
            recurrent_act_func=recurrent_act_func,
            key=key,
            conv_layer=sk.nn.Conv2D,
            spatial_ndim=2,
        )


@pytc.treeclass
class ConvLSTM3DCell(ConvLSTMNDCell):
    def __init__(
        self,
        in_features: int,
        out_features: int,
        kernel_size: KernelSizeType,
        *,
        strides: StridesType = 1,
        padding: PaddingType = "SAME",
        input_dilation: DilationType = 1,
        kernel_dilation: DilationType = 1,
        weight_init_func: InitFuncType = "glorot_uniform",
        bias_init_func: InitFuncType = "zeros",
        recurrent_weight_init_func: InitFuncType = "orthogonal",
        act_func: str | Callable[[Any], Any] | None = "tanh",
        recurrent_act_func: str | Callable[[Any], Any] | None = "hard_sigmoid",
        key: jr.KeyArray = jr.PRNGKey(0),
    ):
        """3D Convolution LSTM cell that defines the update rule for the hidden state and cell state
        Args:
            in_features: Number of input features
            out_features: Number of output features
            kernel_size: Size of the convolutional kernel
            strides: Stride of the convolution
            padding: Padding of the convolution
            input_dilation: Dilation of the input
            kernel_dilation: Dilation of the convolutional kernel
            weight_init_func: Weight initialization function
            bias_init_func: Bias initialization function
            recurrent_weight_init_func: Recurrent weight initialization function
            act_func: Activation function
            recurrent_act_func: Recurrent activation function
            key: PRNG key
            spatial_ndim: Number of spatial dimensions.

        See: https://www.tensorflow.org/api_docs/python/tf/keras/layers/ConvLSTM1D
        """
        super().__init__(
            in_features=in_features,
            out_features=out_features,
            kernel_size=kernel_size,
            strides=strides,
            padding=padding,
            input_dilation=input_dilation,
            kernel_dilation=kernel_dilation,
            weight_init_func=weight_init_func,
            bias_init_func=bias_init_func,
            recurrent_weight_init_func=recurrent_weight_init_func,
            act_func=act_func,
            recurrent_act_func=recurrent_act_func,
            key=key,
            conv_layer=sk.nn.Conv3D,
            spatial_ndim=3,
        )


# ------------------------------------------------- ConvGRU RNN ------------------------------------------------------ #
@pytc.treeclass
class ConvGRUNDState(RNNState):
    pass


@ft.partial(lazy_class, lazy_keywords=["in_features"], infer_func=infer_func)
@pytc.treeclass
class ConvGRUNDCell(SpatialRNNCell):
    in_features: int = pytc.field(callbacks=[*frozen_positive_int_cbs])
    out_features: int = pytc.field(callbacks=[*frozen_positive_int_cbs])
    in_to_hidden: Any
    hidden_to_hidden: Any

    def __init__(
        self,
        in_features: int,
        out_features: int,
        kernel_size: int | tuple[int, ...],
        *,
        strides: StridesType = 1,
        padding: PaddingType = "SAME",
        input_dilation: DilationType = 1,
        kernel_dilation: DilationType = 1,
        weight_init_func: InitFuncType = "glorot_uniform",
        bias_init_func: InitFuncType = "zeros",
        recurrent_weight_init_func: InitFuncType = "orthogonal",
        act_func: str | Callable[[Any], Any] | None = "tanh",
        recurrent_act_func: str | Callable[[Any], Any] | None = "sigmoid",
        key: jr.KeyArray = jr.PRNGKey(0),
        conv_layer: Any = None,
        spatial_ndim: int = 1,
    ):
        """Convolution GRU cell that defines the update rule for the hidden state and cell state
        Args:
            in_features: Number of input features
            out_features: Number of output features
            kernel_size: Size of the convolutional kernel
            strides: Stride of the convolution
            padding: Padding of the convolution
            input_dilation: Dilation of the input
            kernel_dilation: Dilation of the convolutional kernel
            weight_init_func: Weight initialization function
            bias_init_func: Bias initialization function
            recurrent_weight_init_func: Recurrent weight initialization function
            act_func: Activation function
            recurrent_act_func: Recurrent activation function
            key: PRNG key
            spatial_ndim: Number of spatial dimensions.

        """
        k1, k2 = jr.split(key, 2)

        self.in_features = in_features
        self.out_features = out_features
        self.spatial_ndim = spatial_ndim
        self.act_func = _act_func_map.get(act_func, act_func)
        self.recurrent_act_func = _act_func_map.get(recurrent_act_func, recurrent_act_func)  # fmt: skip

        self.in_to_hidden = conv_layer(
            in_features,
            out_features * 3,
            kernel_size,
            strides=strides,
            padding=padding,
            input_dilation=input_dilation,
            kernel_dilation=kernel_dilation,
            weight_init_func=weight_init_func,
            bias_init_func=bias_init_func,
            key=k1,
        )

        self.hidden_to_hidden = conv_layer(
            out_features,
            out_features * 3,
            kernel_size,
            strides=strides,
            padding=padding,
            input_dilation=input_dilation,
            kernel_dilation=kernel_dilation,
            weight_init_func=recurrent_weight_init_func,
            bias_init_func=None,
            key=k2,
        )

    def __call__(self, x: jax.Array, state: ConvGRUNDState, **k) -> ConvGRUNDState:
        if not isinstance(state, ConvGRUNDState):
            msg = f"Expected state to be an instance of GRUState, got {type(state)}"
            raise TypeError(msg)

        h = state.hidden_state
        xe, xu, xo = jnp.split(self.in_to_hidden(x), 3, axis=0)
        he, hu, ho = jnp.split(self.hidden_to_hidden(h), 3, axis=0)
        e = self.recurrent_act_func(xe + he)
        u = self.recurrent_act_func(xu + hu)
        o = self.act_func(xo + (e * ho))
        h = (1 - u) * o + u * h
        return ConvGRUNDState(hidden_state=h)

    def init_state(self, spatial_dim: tuple[int, ...]) -> ConvGRUNDState:
        msg = f"Expected spatial_dim to be a tuple of length {self.spatial_ndim}, got {spatial_dim}"
        assert len(spatial_dim) == self.spatial_ndim, msg
        shape = (self.out_features, *spatial_dim)
        return ConvGRUNDState(hidden_state=jnp.zeros(shape))


@pytc.treeclass
class ConvGRU1DCell(ConvGRUNDCell):
    in_features: int = pytc.field(callbacks=[*frozen_positive_int_cbs])
    out_features: int = pytc.field(callbacks=[*frozen_positive_int_cbs])
    in_to_hidden: Any
    hidden_to_hidden: Any

    def __init__(
        self,
        in_features: int,
        out_features: int,
        kernel_size: int | tuple[int, ...],
        *,
        strides: StridesType = 1,
        padding: PaddingType = "SAME",
        input_dilation: DilationType = 1,
        kernel_dilation: DilationType = 1,
        weight_init_func: InitFuncType = "glorot_uniform",
        bias_init_func: InitFuncType = "zeros",
        recurrent_weight_init_func: InitFuncType = "orthogonal",
        act_func: str | Callable[[Any], Any] | None = "tanh",
        recurrent_act_func: str | Callable[[Any], Any] | None = "sigmoid",
        key: jr.KeyArray = jr.PRNGKey(0),
    ):
        """1D Convolution GRU cell that defines the update rule for the hidden state and cell state
        Args:
            in_features: Number of input features
            out_features: Number of output features
            kernel_size: Size of the convolutional kernel
            strides: Stride of the convolution
            padding: Padding of the convolution
            input_dilation: Dilation of the input
            kernel_dilation: Dilation of the convolutional kernel
            weight_init_func: Weight initialization function
            bias_init_func: Bias initialization function
            recurrent_weight_init_func: Recurrent weight initialization function
            act_func: Activation function
            recurrent_act_func: Recurrent activation function
            key: PRNG key
            spatial_ndim: Number of spatial dimensions.

        """
        super().__init__(
            in_features=in_features,
            out_features=out_features,
            kernel_size=kernel_size,
            strides=strides,
            padding=padding,
            input_dilation=input_dilation,
            kernel_dilation=kernel_dilation,
            weight_init_func=weight_init_func,
            bias_init_func=bias_init_func,
            recurrent_weight_init_func=recurrent_weight_init_func,
            act_func=act_func,
            recurrent_act_func=recurrent_act_func,
            key=key,
            conv_layer=sk.nn.Conv1D,
            spatial_ndim=1,
        )


@pytc.treeclass
class ConvGRU2DCell(ConvGRUNDCell):
    in_features: int = pytc.field(callbacks=[*frozen_positive_int_cbs])
    out_features: int = pytc.field(callbacks=[*frozen_positive_int_cbs])
    in_to_hidden: Any
    hidden_to_hidden: Any

    def __init__(
        self,
        in_features: int,
        out_features: int,
        kernel_size: int | tuple[int, ...],
        *,
        strides: StridesType = 1,
        padding: PaddingType = "SAME",
        input_dilation: DilationType = 1,
        kernel_dilation: DilationType = 1,
        weight_init_func: InitFuncType = "glorot_uniform",
        bias_init_func: InitFuncType = "zeros",
        recurrent_weight_init_func: InitFuncType = "orthogonal",
        act_func: str | Callable[[Any], Any] | None = "tanh",
        recurrent_act_func: str | Callable[[Any], Any] | None = "sigmoid",
        key: jr.KeyArray = jr.PRNGKey(0),
    ):
        """2D Convolution GRU cell that defines the update rule for the hidden state and cell state
        Args:
            in_features: Number of input features
            out_features: Number of output features
            kernel_size: Size of the convolutional kernel
            strides: Stride of the convolution
            padding: Padding of the convolution
            input_dilation: Dilation of the input
            kernel_dilation: Dilation of the convolutional kernel
            weight_init_func: Weight initialization function
            bias_init_func: Bias initialization function
            recurrent_weight_init_func: Recurrent weight initialization function
            act_func: Activation function
            recurrent_act_func: Recurrent activation function
            key: PRNG key
            spatial_ndim: Number of spatial dimensions.

        """
        super().__init__(
            in_features=in_features,
            out_features=out_features,
            kernel_size=kernel_size,
            strides=strides,
            padding=padding,
            input_dilation=input_dilation,
            kernel_dilation=kernel_dilation,
            weight_init_func=weight_init_func,
            bias_init_func=bias_init_func,
            recurrent_weight_init_func=recurrent_weight_init_func,
            act_func=act_func,
            recurrent_act_func=recurrent_act_func,
            key=key,
            conv_layer=sk.nn.Conv2D,
            spatial_ndim=2,
        )


@pytc.treeclass
class ConvGRU3DCell(ConvGRUNDCell):
    in_features: int = pytc.field(callbacks=[*frozen_positive_int_cbs])
    out_features: int = pytc.field(callbacks=[*frozen_positive_int_cbs])
    in_to_hidden: Any
    hidden_to_hidden: Any

    def __init__(
        self,
        in_features: int,
        out_features: int,
        kernel_size: int | tuple[int, ...],
        *,
        strides: StridesType = 1,
        padding: PaddingType = "SAME",
        input_dilation: DilationType = 1,
        kernel_dilation: DilationType = 1,
        weight_init_func: InitFuncType = "glorot_uniform",
        bias_init_func: InitFuncType = "zeros",
        recurrent_weight_init_func: InitFuncType = "orthogonal",
        act_func: str | Callable[[Any], Any] | None = "tanh",
        recurrent_act_func: str | Callable[[Any], Any] | None = "sigmoid",
        key: jr.KeyArray = jr.PRNGKey(0),
    ):
        """3D Convolution GRU cell that defines the update rule for the hidden state and cell state
        Args:
            in_features: Number of input features
            out_features: Number of output features
            kernel_size: Size of the convolutional kernel
            strides: Stride of the convolution
            padding: Padding of the convolution
            input_dilation: Dilation of the input
            kernel_dilation: Dilation of the convolutional kernel
            weight_init_func: Weight initialization function
            bias_init_func: Bias initialization function
            recurrent_weight_init_func: Recurrent weight initialization function
            act_func: Activation function
            recurrent_act_func: Recurrent activation function
            key: PRNG key
            spatial_ndim: Number of spatial dimensions.

        """
        super().__init__(
            in_features=in_features,
            out_features=out_features,
            kernel_size=kernel_size,
            strides=strides,
            padding=padding,
            input_dilation=input_dilation,
            kernel_dilation=kernel_dilation,
            weight_init_func=weight_init_func,
            bias_init_func=bias_init_func,
            recurrent_weight_init_func=recurrent_weight_init_func,
            act_func=act_func,
            recurrent_act_func=recurrent_act_func,
            key=key,
            conv_layer=sk.nn.Conv3D,
            spatial_ndim=3,
        )


# =============================================== Scanning API ======================================================= #


def infer_func(self, *args, **kwargs):
    return (args[0].shape[1],)


@pytc.treeclass
class ScanRNN:
    cell: RNNCell
    backward_cell: RNNCell

    def __init__(
        self,
        cell: RNNCell | SpatialRNNCell,
        backward_cell: RNNCell | SpatialRNNCell | None = None,
        *,
        return_sequences: bool = False,
    ):
        """Scans RNN cell over a sequence.

        Args:
            cell: the RNN cell to use
            backward_cell: the RNN cell to use for bidirectional scanning.
            return_sequences: whether to return the hidden state for each timestep

        Example:
            >>> cell = SimpleRNNCell(10, 20) # 10-dimensional input, 20-dimensional hidden state
            >>> rnn = ScanRNN(cell)
            >>> x = jnp.ones((5, 10)) # 5 timesteps, 10 features
            >>> result = rnn(x)  # 20 features
        """
        if not isinstance(cell, (RNNCell, SpatialRNNCell)):
            msg = f"Expected `cell` to be an instance of RNNCell got {type(cell)}"
            raise TypeError(msg)

        if not isinstance(backward_cell, (RNNCell, SpatialRNNCell, type(None))):
            msg = f"Expected `backward_cell` to be an instance of RNNCell, got {type(backward_cell)}"
            raise TypeError(msg)

        self.cell = cell
        self.backward_cell = backward_cell
        self.return_sequences = return_sequences

    def __call__(
        self,
        x: jax.Array,
        state: SpatialRNNCell | None = None,
        backward_state: SpatialRNNCell | None = None,
        **k,
    ) -> jax.Array:
        # check input shape
        if not isinstance(state, (RNNState, type(None))):
            msg = "Expected state to be an instance of RNNState, "
            msg += f"got {type(state).__name__}"
            raise TypeError(msg)

        if isinstance(self.cell, RNNCell):
            # non-spatial RNN
            # (time steps, in_features)
            if x.ndim != 2:
                msg = "Expected x to have 2 dimensions corresponds "
                msg += f"to (timesteps, in_features), got {x.ndim}"
                raise ValueError(msg)

            if self.cell.in_features != x.shape[1]:
                # check input shape
                msg = f"Expected x to have shape (timesteps, {self.cell.in_features})"
                msg += f", got {x.shape}"
                raise ValueError(msg)

            state = state or self.cell.init_state()

            if self.backward_cell is not None:
                backward_state = backward_state or self.backward_cell.init_state()

        else:
            # spatial RNN
            # (time steps, in_features, *spatial_dims)
            if x.ndim != self.cell.spatial_ndim + 2:
                msg = f"Expected x to have {self.cell.spatial_ndim + 2}"  # account for time and in_features
                msg += f" dimensions corresponds to (timesteps, in_features, *spatial_dims), got {x.ndim}"
                raise ValueError(msg)

            if self.cell.in_features != x.shape[1]:
                # check input shape
                msg = f"Expected x to have shape (timesteps, {self.cell.in_features}, *spatial_dims)"
                msg += f", got {x.shape}"
                raise ValueError(msg)

            state = state or self.cell.init_state(spatial_dim=x.shape[2:])

            if self.backward_cell is not None:
                backward_state = backward_state or self.backward_cell.init_state(spatial_dim=x.shape[2:])  # fmt: skip

        # computation

        if self.return_sequences is True:
            # accumulate the hidden state for each timestep
            # in essence, this means return a state along with the carry
            # in `jax.lax.scan`
            def general_scan_func(cell, carry, x):
                state = cell(x, state=carry)
                return state, state

            scan_func = ft.partial(general_scan_func, self.cell)
            result = jax.lax.scan(scan_func, state, x)[1].hidden_state

            if self.backward_cell:
                scan_func = ft.partial(general_scan_func, self.backward_cell)
                x = jnp.flip(x, axis=0)  # reverse the time axis
                back_result = jax.lax.scan(scan_func, backward_state, x)[1].hidden_state
                # reverse once again over the accumulated time axis
                back_result = jnp.flip(back_result, axis=-1)
                result = jnp.concatenate([result, back_result], axis=1)
        else:
            # no return sequences case
            # (i.e. only return the hidden state for the last timestep)
            # return carry only
            def general_scan_func(cell, carry, x):
                state = cell(x, state=carry)
                return state, None

            scan_func = ft.partial(general_scan_func, self.cell)
            result = jax.lax.scan(scan_func, state, x)[0].hidden_state

            # backward cell
            if self.backward_cell is not None:
                scan_func = ft.partial(general_scan_func, self.backward_cell)
                x = jnp.flip(x, axis=0)
                back_result = jax.lax.scan(scan_func, backward_state, x)[0].hidden_state
                result = jnp.concatenate([result, back_result], axis=0)

        return result
