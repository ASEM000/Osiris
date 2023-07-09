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

from typing import Callable, Literal, Union, get_args

import jax
import jax.numpy as jnp
import pytreeclass as pytc
from jax import lax

from serket.nn.utils import IsInstance, Range, ScalarLike


class AdaptiveLeakyReLU(pytc.TreeClass):
    """Leaky ReLU activation function

    Note:
        https://arxiv.org/pdf/1906.01170.pdf.
    """

    a: float = pytc.field(default=1.0, callbacks=[Range(0), ScalarLike()])
    v: float = pytc.field(default=1.0, callbacks=[Range(0), ScalarLike()])

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        v = jax.lax.stop_gradient(self.v)
        return jnp.maximum(0, self.a * x) - v * jnp.maximum(0, -self.a * x)


class AdaptiveReLU(pytc.TreeClass):
    """ReLU activation function with learnable parameters
    Note:
        https://arxiv.org/pdf/1906.01170.pdf.
    """

    a: float = pytc.field(default=1.0, callbacks=[Range(0), ScalarLike()])

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        return jnp.maximum(0, self.a * x)


class AdaptiveSigmoid(pytc.TreeClass):
    """Sigmoid activation function with learnable `a` parameter
    Note:
        https://arxiv.org/pdf/1906.01170.pdf.
    """

    a: float = pytc.field(default=1.0, callbacks=[Range(0), ScalarLike()])

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        return 1 / (1 + jnp.exp(-self.a * x))


class AdaptiveTanh(pytc.TreeClass):
    """Tanh activation function with learnable parameters
    Note:
        https://arxiv.org/pdf/1906.01170.pdf.
    """

    a: float = pytc.field(default=1.0, callbacks=[Range(0), ScalarLike()])

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        a = self.a
        return (jnp.exp(a * x) - jnp.exp(-a * x)) / (jnp.exp(a * x) + jnp.exp(-a * x))


class CeLU(pytc.TreeClass):
    """Celu activation function"""

    alpha: float = pytc.field(default=1.0, callbacks=[ScalarLike()])

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        return jax.nn.celu(x, alpha=lax.stop_gradient(self.alpha))


class ELU(pytc.TreeClass):
    """Exponential linear unit"""

    alpha: float = pytc.field(default=1.0, callbacks=[ScalarLike()])

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        return jax.nn.elu(x, alpha=lax.stop_gradient(self.alpha))


class GELU(pytc.TreeClass):
    """Gaussian error linear unit"""

    approximate: bool = pytc.field(default=1.0, callbacks=[IsInstance(bool)])

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        return jax.nn.gelu(x, approximate=self.approximate)


class GLU(pytc.TreeClass):
    """Gated linear unit"""

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        return jax.nn.glu(x)


class HardShrink(pytc.TreeClass):
    """Hard shrink activation function"""

    alpha: float = pytc.field(default=0.5, callbacks=[Range(0), ScalarLike()])

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        alpha = lax.stop_gradient(self.alpha)
        return jnp.where(x > alpha, x, jnp.where(x < -alpha, x, 0.0))


class HardSigmoid(pytc.TreeClass):
    """Hard sigmoid activation function"""

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        return jax.nn.hard_sigmoid(x)


class HardSwish(pytc.TreeClass):
    """Hard swish activation function"""

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        return jax.nn.hard_swish(x)


class HardTanh(pytc.TreeClass):
    """Hard tanh activation function"""

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        return jax.nn.hard_tanh(x)


class LogSigmoid(pytc.TreeClass):
    """Log sigmoid activation function"""

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        return jax.nn.log_sigmoid(x)


class LogSoftmax(pytc.TreeClass):
    """Log softmax activation function"""

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        return jax.nn.log_softmax(x)


class LeakyReLU(pytc.TreeClass):
    """Leaky ReLU activation function"""

    negative_slope: float = pytc.field(default=0.01, callbacks=[Range(0), ScalarLike()])

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        return jax.nn.leaky_relu(x, lax.stop_gradient(self.negative_slope))


class ReLU(pytc.TreeClass):
    """ReLU activation function"""

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        return jax.nn.relu(x)


class ReLU6(pytc.TreeClass):
    """ReLU6 activation function"""

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        return jax.nn.relu6(x)


class SeLU(pytc.TreeClass):
    """Scaled Exponential Linear Unit"""

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        return jax.nn.selu(x)


class Sigmoid(pytc.TreeClass):
    """Sigmoid activation function"""

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        return jax.nn.sigmoid(x)


class SoftPlus(pytc.TreeClass):
    """SoftPlus activation function"""

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        return jax.nn.softplus(x)


class SoftSign(pytc.TreeClass):
    """SoftSign activation function"""

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        return x / (1 + jnp.abs(x))


class SoftShrink(pytc.TreeClass):
    """SoftShrink activation function"""

    alpha: float = pytc.field(default=0.5, callbacks=[Range(0), ScalarLike()])

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        alpha = lax.stop_gradient(self.alpha)
        return jnp.where(
            x < -alpha,
            x + alpha,
            jnp.where(x > alpha, x - alpha, 0.0),
        )


class SquarePlus(pytc.TreeClass):
    """SquarePlus activation function"""

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        return 0.5 * (x + jnp.sqrt(x * x + 4))


class Swish(pytc.TreeClass):
    """Swish activation function"""

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        return jax.nn.swish(x)


class Tanh(pytc.TreeClass):
    """Tanh activation function"""

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        return jax.nn.tanh(x)


class TanhShrink(pytc.TreeClass):
    """TanhShrink activation function"""

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        return x - jax.nn.tanh(x)


class ThresholdedReLU(pytc.TreeClass):
    """Thresholded ReLU activation function."""

    theta: float = pytc.field(default=1.0, callbacks=[Range(0), ScalarLike()])

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        theta = lax.stop_gradient(self.theta)
        return jnp.where(x > theta, x, 0)


class Mish(pytc.TreeClass):
    """Mish activation function https://arxiv.org/pdf/1908.08681.pdf."""

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        return x * jax.nn.tanh(jax.nn.softplus(x))


class PReLU(pytc.TreeClass):
    """Parametric ReLU activation function"""

    a: float = pytc.field(default=0.25, callbacks=[Range(0), ScalarLike()])

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        return jnp.where(x >= 0, x, x * self.a)


class Snake(pytc.TreeClass):
    """Snake activation function

    Args:
        a: scalar (frequency) parameter of the activation function, default is 1.0.

    Note:
        https://arxiv.org/pdf/2006.08195.pdf.
    """

    a: float = pytc.field(callbacks=[Range(0), ScalarLike()], default=1.0)

    def __call__(self, x: jax.Array, **k) -> jax.Array:
        a = lax.stop_gradient(self.a)
        return x + (1 - jnp.cos(2 * a * x)) / (2 * a)


# useful for building layers from configuration text
ActivationLiteral = Literal[
    "adaptive_leaky_relu",
    "adaptive_relu",
    "adaptive_sigmoid",
    "adaptive_tanh",
    "celu",
    "elu",
    "gelu",
    "glu",
    "hard_shrink",
    "hard_sigmoid",
    "hard_swish",
    "hard_tanh",
    "leaky_relu",
    "log_sigmoid",
    "log_softmax",
    "mish",
    "prelu",
    "relu",
    "relu6",
    "selu",
    "sigmoid",
    "snake",
    "softplus",
    "softshrink",
    "softsign",
    "squareplus",
    "swish",
    "tanh",
    "tanh_shrink",
    "thresholded_relu",
]


acts = [
    AdaptiveLeakyReLU,
    AdaptiveReLU,
    AdaptiveSigmoid,
    AdaptiveTanh,
    CeLU,
    ELU,
    GELU,
    GLU,
    HardShrink,
    HardSigmoid,
    HardSwish,
    HardTanh,
    LeakyReLU,
    LogSigmoid,
    LogSoftmax,
    Mish,
    PReLU,
    ReLU,
    ReLU6,
    SeLU,
    Sigmoid,
    Snake,
    SoftPlus,
    SoftShrink,
    SoftSign,
    SquarePlus,
    Swish,
    Tanh,
    TanhShrink,
    ThresholdedReLU,
]


act_map: dict[str, pytc.TreeClass] = dict(zip(get_args(ActivationLiteral), acts))

ActivationFunctionType = Callable[[jax.typing.ArrayLike], jax.Array]
ActivationType = Union[ActivationLiteral, ActivationFunctionType]


def resolve_activation(act_func: ActivationType) -> ActivationFunctionType:
    # in case the user passes a trainable activation function
    # we need to make a copy of it to avoid unpredictable side effects
    if isinstance(act_func, str):
        if act_func in act_map:
            return act_map[act_func]()

        raise ValueError(
            f"Unknown activation function {act_func=}, "
            f"available activations are {list(act_map.keys())}"
        )
    return act_func
