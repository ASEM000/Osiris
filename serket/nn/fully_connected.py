# Copyright 2023 Serket authors
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

from typing import Any, Sequence

import jax
import jax.random as jr
import pytreeclass as pytc

from serket.nn.activation import ActivationType, resolve_activation
from serket.nn.initialization import InitType
from serket.nn.linear import Linear

PyTree = Any


class FNN(pytc.TreeClass):
    def __init__(
        self,
        layers: Sequence[int],
        *,
        act_func: ActivationType = "tanh",
        weight_init_func: InitType = "glorot_uniform",
        bias_init_func: InitType = "zeros",
        key: jr.KeyArray = jr.PRNGKey(0),
    ):
        """Fully connected neural network
        Args:
            layers: Sequence of layer sizes
            act_func: a single Activation function to be applied between layers or
                `len(layers)-2` Sequence of activation functions applied between layers.
            weight_init_func: Weight initializer function.
            bias_init_func: Bias initializer function. Defaults to lambda key,
                shape: jnp.ones(shape).
            key: Random key for weight and bias initialization.

        Example:
            >>> fnn = FNN([10, 5, 2])
            >>> fnn(jnp.ones((3, 10))).shape
            (3, 2)

        Note:
            - layers argument yields len(layers) - 1 linear layers with required
                `len(layers)-2` activation functions, for example, `layers=[10, 5, 2]`
                yields 2 linear layers with weight shapes (10, 5) and (5, 2)
                and single activation function is applied between them.
            - `FNN` uses python `for` loop to apply layers and activation functions.
        """

        keys = jr.split(key, len(layers) - 1)

        self.act_funcs = tuple(resolve_activation(act_func) for _ in keys[1:])

        self.layers = tuple(
            Linear(
                in_features=di,
                out_features=do,
                key=ki,
                weight_init_func=weight_init_func,
                bias_init_func=bias_init_func,
            )
            for (ki, di, do) in (zip(keys, layers[:-1], layers[1:]))
        )

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        for act, layer in zip(self.act_funcs, self.layers[:-1]):
            x = act(layer(x))
        return self.layers[-1](x)


class MLP(pytc.TreeClass):
    def __init__(
        self,
        in_features: int,
        out_features: int,
        *,
        hidden_size: int,
        num_hidden_layers: int,
        act_func: ActivationType = "tanh",
        weight_init_func: InitType = "glorot_uniform",
        bias_init_func: InitType = "zeros",
        key: jr.KeyArray = jr.PRNGKey(0),
    ):
        """Multi-layer perceptron.

        Args:
            in_features: Number of input features.
            out_features: Number of output features.
            hidden_size: Number of hidden units in each hidden layer.
            num_hidden_layers: Number of hidden layers including the output layer.
            act_func: Activation function.
            weight_init_func: Weight initialization function.
            bias_init_func: Bias initialization function.
            key: Random number generator key.

        Note:
            - MLP with `in_features`=1, `out_features`=2, `hidden_size`=4,
            `num_hidden_layers`=2 is equivalent to `[1, 4, 4, 2]` which has one input layer (1, 4),
            one intermediate  layer (4, 4), and one output layer (4, 2) = `num_hidden_layers` + 1
            - `MLP` exploits same input/out size for intermediate layers to use `jax.lax.scan`,
                which offers better compilation speed for large number of layers
                and producing a smaller `jaxpr`.
        """
        if hidden_size < 1:
            raise ValueError(f"hidden_size must be positive, got {hidden_size}")

        keys = jr.split(key, num_hidden_layers + 1)
        self.act_funcs = tuple(resolve_activation(act_func) for _ in keys[1:])

        self.layers = tuple(
            [
                Linear(
                    in_features=in_features,
                    out_features=hidden_size,
                    weight_init_func=weight_init_func,
                    bias_init_func=bias_init_func,
                    key=keys[0],
                )
            ]
            + [
                Linear(
                    in_features=hidden_size,
                    out_features=hidden_size,
                    weight_init_func=weight_init_func,
                    bias_init_func=bias_init_func,
                    key=key,
                )
                for key in keys[1:-1]
            ]
            + [
                Linear(
                    in_features=hidden_size,
                    out_features=out_features,
                    weight_init_func=weight_init_func,
                    bias_init_func=bias_init_func,
                    key=keys[-1],
                )
            ]
        )

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        def scan_func(carry, _):
            x, (l0, *lh), (a0, *ah) = carry
            return [a0(l0(x)), [*lh, l0], [*ah, a0]], None

        (l0, *lh, lf), (a0, *ah) = self.layers, self.act_funcs
        x = a0(l0(x))
        if length := len(lh):
            (x, _, _), _ = jax.lax.scan(scan_func, [x, lh, ah], None, length=length)
        return lf(x)
