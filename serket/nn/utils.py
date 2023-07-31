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

import functools as ft
import operator as op
from typing import Any, Callable, Sequence, Tuple, TypeVar, Union

import jax
import jax.numpy as jnp
import numpy as np
from typing_extensions import ParamSpec

import serket as sk

KernelSizeType = Union[int, Sequence[int]]
StridesType = Union[int, Sequence[int]]
PaddingType = Union[str, int, Sequence[int], Sequence[Tuple[int, int]]]
DilationType = Union[int, Sequence[int]]

P = ParamSpec("P")
T = TypeVar("T")


@ft.lru_cache(maxsize=128)
def calculate_transpose_padding(
    padding,
    kernel_size,
    input_dilation,
    extra_padding,
):
    """Transpose padding to get the padding for the transpose convolution.

    Args:
        padding: padding to transpose
        kernel_size: kernel size to use for transposing padding
        input_dilation: input dilation to use for transposing padding
        extra_padding: extra padding to use for transposing padding
    """
    return tuple(
        ((ki - 1) * di - pl, (ki - 1) * di - pr + ep)
        for (pl, pr), ki, ep, di in zip(
            padding, kernel_size, extra_padding, input_dilation
        )
    )


def calculate_convolution_output_shape(
    shape: tuple[int, ...],
    kernel_size: tuple[int, ...],
    padding: tuple[tuple[int, int], ...],
    strides: tuple[int, ...],
):
    """Compute the shape of the output of a convolutional layer."""
    return tuple(
        (xi + (li + ri) - ki) // si + 1
        for xi, ki, si, (li, ri) in zip(shape, kernel_size, strides, padding)
    )


def same_padding_along_dim(
    in_dim: int,
    kernel_size: int,
    stride: int,
) -> tuple[int, int]:
    # https://www.tensorflow.org/api_docs/python/tf/nn#notes_on_padding_2
    # di: input dimension
    # ki: kernel size
    # si: stride
    if in_dim % stride == 0:
        pad = max(kernel_size - stride, 0)
    else:
        pad = max(kernel_size - (in_dim % stride), 0)

    return (pad // 2, pad - pad // 2)


def resolve_tuple_padding(
    in_dim: tuple[int, ...],
    padding: PaddingType,
    kernel_size: KernelSizeType,
    strides: StridesType,
) -> tuple[tuple[int, int], ...]:
    del in_dim, strides
    if len(padding) != len(kernel_size):
        raise ValueError(f"Length mismatch {len(kernel_size)=}!={len(padding)=}.")

    resolved_padding = [[]] * len(kernel_size)

    for i, item in enumerate(padding):
        if isinstance(item, int):
            resolved_padding[i] = (item, item)  # ex: padding = (1, 2, 3)

        elif isinstance(item, tuple):
            if len(item) != 2:
                raise ValueError(f"Expected tuple of length 2, got {len(item)=}")
            resolved_padding[i] = item

    return tuple(resolved_padding)


def resolve_int_padding(
    in_dim: tuple[int, ...],
    padding: PaddingType,
    kernel_size: KernelSizeType,
    strides: StridesType,
):
    del in_dim, strides
    return ((padding, padding),) * len(kernel_size)


def resolve_string_padding(in_dim, padding, kernel_size, strides):
    if padding.lower() == "same":
        return tuple(
            same_padding_along_dim(di, ki, si)
            for di, ki, si in zip(in_dim, kernel_size, strides)
        )

    if padding.lower() == "valid":
        return ((0, 0),) * len(kernel_size)

    raise ValueError(f'string argument must be in ["same","valid"].Found {padding}')


@ft.lru_cache(maxsize=128)
def delayed_canonicalize_padding(
    in_dim: tuple[int, ...],
    padding: PaddingType,
    kernel_size: KernelSizeType,
    strides: StridesType,
):
    # in case of `str` padding, we need to know the input dimension
    # to calculate the padding thus we need to delay the canonicalization
    # until the call

    if isinstance(padding, int):
        return resolve_int_padding(in_dim, padding, kernel_size, strides)

    if isinstance(padding, str):
        return resolve_string_padding(in_dim, padding, kernel_size, strides)

    if isinstance(padding, tuple):
        return resolve_tuple_padding(in_dim, padding, kernel_size, strides)

    raise ValueError(
        "Expected padding to be of:\n"
        "* int, for same padding along all dimensions\n"
        "* str, for `same` or `valid` padding along all dimensions\n"
        "* tuple of int, for individual padding along each dimension\n"
        "* tuple of tuple of int, for padding before and after each dimension\n"
        f"Got {padding=}."
    )


def canonicalize(value, ndim, *, name: str | None = None):
    if isinstance(value, int):
        return (value,) * ndim
    if isinstance(value, jax.Array):
        return jnp.repeat(value, ndim)
    if isinstance(value, tuple):
        if len(value) != ndim:
            raise ValueError(f"{len(value)=} != {ndim=} for {name=} and {value=}.")
        return tuple(value)

    raise ValueError(f"Expected int or tuple , got {value=}.")


@sk.autoinit
class Range(sk.TreeClass):
    """Check if the input is in the range [min_val, max_val]."""

    min_val: float = -float("inf")
    max_val: float = float("inf")
    min_inclusive: bool = True
    max_inclusive: bool = True

    def __call__(self, value: Any):
        lop, ls = (op.ge, "[") if self.min_inclusive else (op.gt, "(")
        rop, rs = (op.le, "]") if self.max_inclusive else (op.lt, ")")

        if lop(value, self.min_val) and rop(value, self.max_val):
            return value

        raise ValueError(f"Not in {ls}{self.min_val}, {self.max_val}{rs} got {value=}.")


@sk.autoinit
class IsInstance(sk.TreeClass):
    """Check if the input is an instance of expected_type."""

    predicted_type: type | Sequence[type]

    def __call__(self, value: Any):
        if isinstance(value, self.predicted_type):
            return value
        raise TypeError(f"Expected {self.predicted_type}, got {type(value).__name__}")


class ScalarLike(sk.TreeClass):
    """Check if the input is a scalar"""

    def __call__(self, value: Any):
        if isinstance(value, (float, complex)):
            return value
        if (
            isinstance(value, (jax.Array, np.ndarray))
            and np.issubdtype(value.dtype, np.inexact)
            and value.shape == ()
        ):
            return value
        raise ValueError(f"Expected inexact type got {value=}")


def canonicalize_cb(value, ndim, name: str | None = None):
    # in essence this is a type check that allows for int, tuple, and jax.Array
    # canonicalization is done by converting to a tuple of length ndim
    if isinstance(value, int):
        return (value,) * ndim
    if isinstance(value, jax.Array):
        return jnp.repeat(value, ndim)
    if isinstance(value, tuple):
        if len(value) != ndim:
            raise ValueError(f"{len(value)=} != {ndim=}.")
        return tuple(value)

    raise ValueError(f"Expected int/tuple for {name=} and {value=}.")


def positive_int_cb(value):
    """Return if value is a positive integer, otherwise raise an error."""
    if not isinstance(value, int):
        raise ValueError(f"value must be an integer, got {type(value).__name__}")
    if value <= 0:
        raise ValueError(f"{value=} must be positive.")
    return value


def positive_int_or_none_cb(value):
    """Return if value is a positive integer, otherwise raise an error."""
    if value is None:
        return value
    if not isinstance(value, int):
        raise ValueError(f"value must be an integer, got {type(value).__name__}")
    if value <= 0:
        raise ValueError(f"{value=} must be positive.")
    return value


def recursive_getattr(obj, attr: Sequence[str]):
    return (
        getattr(obj, attr[0])
        if len(attr) == 1
        else recursive_getattr(getattr(obj, attr[0]), attr[1:])
    )


def validate_spatial_ndim(func: Callable[P, T], attribute_name: str) -> Callable[P, T]:
    """Decorator to validate spatial input shape."""
    attribute_list: Sequence[str] = attribute_name.split(".")

    def check_spatial_in_shape(x, spatial_ndim: int) -> None:
        if x.ndim != spatial_ndim + 1:
            spatial = {", ".join(("rows", "cols", "depths")[:spatial_ndim])}
            raise ValueError(
                f"Input should satisfy:\n"
                f"- {spatial_ndim+1=} dimension, got {x.ndim=}.\n"
                f"- shape of (in_features, {spatial}), got {x.shape=}.\n"
                + (
                    # maybe the user apply the layer on a batched input
                    "To apply on batched input, use `jax.vmap(...)(input)`."
                    if x.ndim == spatial_ndim + 2
                    else ""
                )
            )
        return x

    @ft.wraps(func)
    def wrapper(self, array, *a, **k):
        array = check_spatial_in_shape(array, recursive_getattr(self, attribute_list))
        return func(self, array, *a, **k)

    return wrapper


def validate_axis_shape(
    func: Callable[P, T],
    *,
    attribute_name: str,
    axis: int = 0,
) -> Callable[P, T]:
    """Decorator to validate input features."""
    attribute_list = attribute_name.split(".")

    def check_axis_shape(x, in_features: int, axis: int) -> None:
        if in_features is None:
            # lazy initialization
            return x
        if x.shape[axis] != in_features:
            raise ValueError(f"Specified {in_features=}, got {x.shape[axis]=}.")
        return x

    @ft.wraps(func)
    def wrapper(self, array, *a, **k):
        check_axis_shape(array, recursive_getattr(self, attribute_list), axis)
        return func(self, array, *a, **k)

    return wrapper


def lazy_call(
    func: Callable[P, T],
    is_lazy: Callable[..., bool],
    updates: dict[str, Callable[..., Any]],
) -> Callable[P, T]:
    @ft.wraps(func)
    def inner(self, *a, **k):
        if not is_lazy(self):
            return func(self, *a, **k)

        kwargs = dict(vars(self))
        for key, update in updates.items():
            kwargs[key] = update(self, *a, **k)
        getattr(type(self), "__init__")(self, **kwargs)
        return func(self, *a, **k)

    return inner
