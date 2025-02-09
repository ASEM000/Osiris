# Copyright 2024 serket authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import functools as ft
from typing import Callable

import jax
import jax.numpy as jnp
import jax.random as jr
from typing_extensions import Annotated

from serket import TreeClass
from serket._src.nn.dropout import Dropout
from serket._src.nn.linear import Linear
from serket._src.utils.lazy import maybe_lazy_call, maybe_lazy_init
from serket._src.utils.typing import DType, InitType

"""Defines attention layers."""


def split_heads(input: jax.Array, num_heads: int) -> jax.Array:
    """Splits the last dimension of the input into multiple heads."""
    return input.reshape(*input.shape[:-1], num_heads, -1)


def merge_heads(input: jax.Array) -> jax.Array:
    """Merges the last two dimensions of the input."""
    return input.reshape(*input.shape[:-2], -1)


def is_lazy_call(instance, *_, **__) -> bool:
    return getattr(instance, "q_features", False) is None


def is_lazy_init(_, num_heads, q_features, *__, **___) -> bool:
    return q_features is None


attention_updates = dict(
    q_features=lambda _1, q_input, *_2, **_3: q_input.shape[-1],
    k_features=lambda _1, _2, k_input, *_3, **_4: k_input.shape[-1],
    v_features=lambda _1, _2, _3, v_input, *_4, **__5: v_input.shape[-1],
)


def dot_product_attention(
    q_heads: Annotated[jax.Array, "..., q_length, num_heads, head_features"],
    k_heads: Annotated[jax.Array, "..., kv_length, num_heads, head_features"],
    v_heads: Annotated[jax.Array, "..., kv_length, num_heads, head_features"],
    mask: Annotated[jax.Array, "..., num_heads, q_length, kv_length"] | None,
    drop_func: Callable[[jax.Array], jax.Array],
) -> jax.Array:
    """Applies multi-head attention to the given inputs.

    Args:
        q_input: Query input. [..., q_length, num_heads, head_features]
        k_input: Key input. [..., k_length, num_heads, head_features]
        v_input: Value input. [..., v_length, num_heads, head_features]
        mask: Mask input. [..., num_heads, q_length, kv_length]. Use ``None``
            for no masking.
        drop_func: Dropout function. Takes a single input and returns a single output.
            Use ``lambda input: input`` for no dropout.

    Reference:
        - https://keras.io/api/layers/attention_layers/multi_head_attention/
        - https://flax.readthedocs.io/en/latest/_modules/flax/linen/attention.html
    """
    *_other, _length, _num_heads, k_depth = k_heads.shape
    logits = jnp.einsum("...qhd,...khd->...hqk", q_heads, k_heads)
    logits /= jnp.sqrt(k_depth)
    min_num = jnp.finfo(logits.dtype).min
    logits = logits if mask is None else jnp.where(mask, logits, min_num)
    weight = jax.nn.softmax(logits)
    attention = jnp.einsum("...hqk,...khd->...qhd", weight, v_heads)
    # avoid using Dropout layers inside functions
    return merge_heads(drop_func(attention))


class MultiHeadAttention(TreeClass):
    """Multi-head attention module.

    The module consists of linear projections for query, key, and value
    (q, k, v), followed by the application of scaled dot-product attention
    with optional masking and dropout. It supports multi-head attention where
    the input features are divided into multiple heads to capture different
    aspects of relationships between the input vectors.


    Args:
        num_heads: Number of attention heads.
        q_features: Number of features for the query.
        k_features: Number of features for the key.
        v_features: Number of features for the value.
        out_features: Number of features for the output.
        key: Key for the random number generator.
        q_weight_init: Initializer for the query weight. Defaults to ``glorot_uniform``.
        q_bias_init: Initializer for the query bias. Defaults to zeros. use
            ``None`` to disable bias.
        q_dtype: Data type for the query. ``float32``
        k_weight_init: Initializer for the key weight. Defaults to ``glorot_uniform``.
        k_bias_init: Initializer for the key bias. Defaults to zeros. use
            ``None`` to disable bias.
        k_dtype: Data type for the key. ``float32``
        v_weight_init: Initializer for the value weight. Defaults to ``glorot_uniform``.
        v_bias_init: Initializer for the value bias. Defaults to zeros. use
            ``None`` to disable bias.
        v_dtype: Data type for the value. ``float32``
        out_weight_init: Initializer for the output weight. Defaults to ``glorot_uniform``.
        out_bias_init: Initializer for the output bias. Defaults to zeros. use
            ``None`` to disable bias.
        out_dtype: Data type for the output. ``float32``
        drop_rate: Dropout rate. defaults to 0.0.
        drop_broadcast: Whether to broadcast the dropout mask across the batch
            dimension and the heads dimension. Defaults to False.

    Example:
        >>> import serket as sk
        >>> import jax.numpy as jnp
        >>> import jax.random as jr
        >>> batch = 3
        >>> num_heads = 2
        >>> q_features = 4
        >>> k_features = 8
        >>> v_features = 6
        >>> q_length = 4
        >>> kv_length = 2
        >>> mask = jr.uniform(jr.key(0), (batch, num_heads, q_length, kv_length))
        >>> mask = (mask > 0.5).astype(jnp.float32)
        >>> k1, k2, k3, k4 = jr.split(jr.key(0), 4)
        >>> q = jr.uniform(k1, (batch, q_length, q_features))
        >>> k = jr.uniform(k2, (batch, kv_length, k_features))
        >>> v = jr.uniform(k3, (batch, kv_length, v_features))
        >>> layer = sk.nn.MultiHeadAttention(
        ...    num_heads,
        ...    q_features,
        ...    k_features,
        ...    v_features,
        ...    drop_rate=0.0,
        ...    key=k4,
        ... )
        >>> print(layer(q, k, v, mask=mask, key=jr.key(1)).shape)
        (3, 4, 4)

    Note:
        - If ``k_features``, ``v_features``, ``out_features`` are not specified,
          they are set to ``q_features``.
        - To disable attention :class:`.Dropout`, use :func:`.tree_eval` on the
          instantiated layer.

        >>> import serket as sk
        >>> layer = sk.nn.MultiHeadAttention(1, 1, key=jr.key(0))
        >>> print(repr(layer.dropout))
        Dropout(drop_rate=0.0, drop_axes=None)
        >>> print(repr(sk.tree_eval(layer).dropout))
        Identity()

    Note:
        :class:`.MultiHeadAttention` supports lazy initialization, meaning that the weights and
        biases are not initialized until the first call to the layer. This is
        useful when the input shape is not known at initialization time.

        To use lazy initialization, pass ``None`` as the ``q_features`` argument
        and use :func:`.value_and_tree` to call the layer with an input of known shape.

        >>> import jax.random as jr
        >>> import serket as sk
        >>> k1, k2, k3, k4, k5 = jr.split(jr.key(0), 5)
        >>> q = jr.uniform(k1, (3, 2, 6))
        >>> k = jr.uniform(k2, (3, 2, 6))
        >>> v = jr.uniform(k3, (3, 2, 6))
        >>> lazy = sk.nn.MultiHeadAttention(2, None, key=k4)
        >>> _, material = sk.value_and_tree(lambda lazy: lazy(q, k, v, key=k4))(lazy)
        >>> material(q, k, v, key=k5).shape
        (3, 2, 6)

    Reference:
        - https://keras.io/api/layers/attention_layers/multi_head_attention/
        - https://flax.readthedocs.io/en/latest/_modules/flax/linen/attention.html
        - https://arxiv.org/abs/1706.03762
    """

    @ft.partial(maybe_lazy_init, is_lazy=is_lazy_init)
    def __init__(
        self,
        num_heads: int,
        q_features: int,
        k_features: int | None = None,
        v_features: int | None = None,
        out_features: int | None = None,
        *,
        key: jax.Array,
        q_weight_init: InitType = "glorot_uniform",
        q_bias_init: InitType = "zeros",
        q_dtype: DType = jnp.float32,
        k_weight_init: InitType = "glorot_uniform",
        k_bias_init: InitType = "zeros",
        k_dtype: DType = jnp.float32,
        v_weight_init: InitType = "glorot_uniform",
        v_bias_init: InitType = "zeros",
        v_dtype: DType = jnp.float32,
        out_weight_init: InitType = "glorot_uniform",
        out_bias_init: InitType = "zeros",
        out_dtype: DType = jnp.float32,
        drop_rate: float = 0.0,
        drop_broadcast: bool = False,
    ):
        k_features = q_features if k_features is None else k_features
        v_features = q_features if v_features is None else v_features
        out_features = q_features if out_features is None else out_features

        if q_features % num_heads != 0:
            raise ValueError(f"{q_features=} % {num_heads=} != 0.")

        if k_features % num_heads != 0:
            raise ValueError(f"{k_features=} % {num_heads=} != 0.")

        if v_features % num_heads != 0:
            raise ValueError(f"{v_features=} % {num_heads=} != 0.")

        if out_features % num_heads != 0:
            raise ValueError(f"{out_features=} % {num_heads=} != 0.")

        head_features = q_features // num_heads
        qkey, kkey, vkey, okey = jr.split(key, 4)

        self.num_heads = num_heads
        # while dropout == 0.0 is a no-op, still instantiate a dropout layer
        # because .at[drop_rate] can be used to change the dropout rate later on.
        self.dropout = Dropout(drop_rate, (-1, -2) if drop_broadcast else None)

        self.q_projection = Linear(
            in_features=q_features,
            out_features=head_features * num_heads,
            weight_init=q_weight_init,
            bias_init=q_bias_init,
            dtype=q_dtype,
            key=qkey,
        )

        self.k_projection = Linear(
            in_features=k_features,
            out_features=head_features * num_heads,
            weight_init=k_weight_init,
            bias_init=k_bias_init,
            dtype=k_dtype,
            key=kkey,
        )

        self.v_projection = Linear(
            in_features=v_features,
            out_features=head_features * num_heads,
            weight_init=v_weight_init,
            bias_init=v_bias_init,
            dtype=v_dtype,
            key=vkey,
        )

        self.out_projection = Linear(
            in_features=head_features * num_heads,
            out_features=out_features,
            weight_init=out_weight_init,
            bias_init=out_bias_init,
            dtype=out_dtype,
            key=okey,
        )

    @ft.partial(maybe_lazy_call, is_lazy=is_lazy_call, updates=attention_updates)
    def __call__(
        self,
        q_input: Annotated[jax.Array, "..., q_length, q_features"],
        k_input: Annotated[jax.Array, "..., kv_length, k_features"],
        v_input: Annotated[jax.Array, "..., kv_length, v_features"],
        mask: Annotated[jax.Array, "..., num_heads, q_length, kv_length"] | None = None,
        *,
        key: jax.Array | None = None,
    ) -> Annotated[jax.Array, "..., q_length, out_features"]:
        """Applies multi-head attention to the given inputs.

        Args:
            q_input: Query input. [..., q_length, q_features]
            k_input: Key input. [..., kv_length, k_features]
            v_input: Value input. [..., kv_length, v_features]
            mask: Mask input. [..., num_heads, q_length, kv_length] Defaults to ``None``.
                for no masking.
            key: Key for the random number generator used for dropout.
                Defaults to ``None`` for no dropout.
        """

        # [..., q_length, q_features] -> [..., q_length, head_features, num_heads]
        q_heads = split_heads(self.q_projection(q_input), self.num_heads)
        # [..., k_length, k_features] -> [..., k_length, head_features, num_heads]
        k_heads = split_heads(self.k_projection(k_input), self.num_heads)
        # [..., v_length, v_features] -> [..., v_length, head_features, num_heads]
        v_heads = split_heads(self.v_projection(v_input), self.num_heads)

        attention = self.attention_op(
            q_heads=q_heads,
            k_heads=k_heads,
            v_heads=v_heads,
            mask=mask,
            # note that if `tree_eval` is used, self.dropout is converted to an
            # identity function, so the `key` argument is ignored.
            # one pro of this approach is that `Identity` will be displayed in
            # the repr of the layer to make it clear that dropout is disabled.
            # another pro is that no need to thread the ``training`` flag through
            # the layer.
            drop_func=lambda input: self.dropout(input, key=key),
        )

        return self.out_projection(attention)

    attention_op = staticmethod(dot_product_attention)
