from __future__ import annotations

import dataclasses
import functools as ft

import jax
import jax.numpy as jnp

# import kernex as kex
import pytreeclass as pytc

from .convolution import DepthwiseConv2D


@pytc.treeclass
class _AvgBlur2D:
    conv1: DepthwiseConv2D = pytc.nondiff_field(repr=False)
    conv2: DepthwiseConv2D = pytc.nondiff_field(repr=False)

    def __init__(self, in_features: int, kernel_size: int | tuple[int, int]):
        """Average blur 2D layer
        Args:
            in_features: number of input channels
            kernel_size: size of the convolving kernel
        """
        if not isinstance(in_features, int) or in_features <= 0:
            raise ValueError(
                f"Expected `in_features` to be a positive integer, got {in_features}"
            )
        if not isinstance(kernel_size, int) or kernel_size <= 0:
            raise ValueError(
                f"Expected `kernel_size` to be a positive integer, got {kernel_size}"
            )

        w = jnp.ones(kernel_size)
        w = w / jnp.sum(w)
        w = w[:, None]
        w = jnp.repeat(w[None, None], in_features, axis=0)

        self.conv1 = DepthwiseConv2D(
            in_features=in_features,
            kernel_size=(kernel_size, 1),
            padding="same",
            bias_init_func=None,
        )

        self.conv2 = DepthwiseConv2D(
            in_features=in_features,
            kernel_size=(1, kernel_size),
            padding="same",
            bias_init_func=None,
        )

        self.conv1 = self.conv1.at["weight"].set(w)
        self.conv2 = self.conv2.at["weight"].set(jnp.moveaxis(w, 2, 3))  # transpose

    def __call__(self, x, **kwargs) -> jnp.ndarray:
        assert x.ndim == 3, "`Input` must be 3D."
        return self.conv2(self.conv1(x))


@pytc.treeclass
class AvgBlur2D(_AvgBlur2D):
    def __init__(self, in_features, kernel_size):
        if in_features is None:
            for field_item in dataclasses.fields(self):
                setattr(self, field_item.name, None)

            self._partial_init = ft.partial(
                super().__init__,
                kernel_size=kernel_size,
            )
        else:
            super().__init__(
                in_features=in_features,
                kernel_size=kernel_size,
            )

    def __call__(self, x, **kwargs):
        if hasattr(self, "_partial_init"):
            self._partial_init(in_features=x.shape[0])
            object.__delattr__(self, "_partial_init")
        return super().__call__(x, **kwargs)


@pytc.treeclass
class _GaussianBlur2D:
    in_features: int = pytc.nondiff_field()
    kernel_size: int = pytc.nondiff_field()
    sigma: float = pytc.nondiff_field()

    conv1: DepthwiseConv2D = pytc.nondiff_field(repr=False)
    conv2: DepthwiseConv2D = pytc.nondiff_field(repr=False)

    def __init__(
        self,
        in_features,
        kernel_size,
        *,
        sigma=1.0,
        # implementation="jax",
    ):
        """Apply Gaussian blur to a channel-first image.

        Args:
            in_features: number of input features
            kernel_size: kernel size
            sigma: sigma. Defaults to 1.
        """
        if not isinstance(in_features, int) or in_features <= 0:
            raise ValueError(
                f"Expected `in_features` to be a positive integer, got {in_features}"
            )
        if not isinstance(kernel_size, int) or kernel_size <= 0:
            raise ValueError(
                f"Expected `kernel_size` to be a positive integer, got {kernel_size}"
            )

        self.in_features = in_features
        self.kernel_size = kernel_size
        self.sigma = sigma

        x = jnp.linspace(-(kernel_size - 1) / 2.0, (kernel_size - 1) / 2.0, kernel_size)
        w = jnp.exp(-0.5 * jnp.square(x) * jax.lax.rsqrt(self.sigma))

        w = w / jnp.sum(w)
        w = w[:, None]

        # if implementation == "jax":
        w = jnp.repeat(w[None, None], in_features, axis=0)
        self.conv1 = DepthwiseConv2D(
            in_features=in_features,
            kernel_size=(kernel_size, 1),
            padding="same",
            bias_init_func=None,
        )

        self.conv2 = DepthwiseConv2D(
            in_features=in_features,
            kernel_size=(1, kernel_size),
            padding="same",
            bias_init_func=None,
        )

        self.conv1 = self.conv1.at["weight"].set(w)
        self.conv2 = self.conv2.at["weight"].set(jnp.moveaxis(w, 2, 3))

        # elif implementation == "kernex":
        #     # usually faster than jax for small kernel sizes
        #     # but slower for large kernel sizes

        #     @jax.vmap  # channel
        #     @kex.kmap(kernel_size=(kernel_size, 1), padding="same")
        #     def conv1(x):
        #         return jnp.sum(x * w)

        #     @jax.vmap
        #     @kex.kmap(kernel_size=(1, kernel_size), padding="same")
        #     def conv2(x):
        #         return jnp.sum(x * w.T)

        #     self._func = lambda x: conv2(conv1(x))

        # else:
        #     raise ValueError(f"Unknown implementation {implementation}")

    def __call__(self, x, **kwargs) -> jnp.ndarray:
        assert x.ndim == 3, "`Input` must be 3D."
        return self.conv1(self.conv2(x))


@pytc.treeclass
class GaussianBlur2D(_GaussianBlur2D):
    def __init__(self, in_features, kernel_size, *, sigma=1.0):
        if in_features is None:
            for field_item in dataclasses.fields(self):
                setattr(self, field_item.name, None)

            self._partial_init = ft.partial(
                super().__init__, kernel_size=kernel_size, sigma=sigma
            )
        else:
            super().__init__(
                in_features=in_features,
                kernel_size=kernel_size,
                sigma=sigma,
            )

    def __call__(self, x, **kwargs):
        if hasattr(self, "_partial_init"):
            self._partial_init(in_features=x.shape[0])
            object.__delattr__(self, "_partial_init")
        return super().__call__(x, **kwargs)
