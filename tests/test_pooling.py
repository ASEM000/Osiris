from __future__ import annotations

import jax.numpy as jnp
import numpy.testing as npt

from serket.nn.pooling import (
    AvgPool1D,
    AvgPool2D,
    AvgPool3D,
    MaxPool1D,
    MaxPool2D,
    MaxPool3D,
)


def test_MaxPool1D():

    layer = MaxPool1D(kernel_size=2, padding="SAME", strides=1)
    x = jnp.arange(1, 11).reshape(1, 10).astype(jnp.float32)
    npt.assert_allclose(layer(x), jnp.array([[2, 3, 4, 5, 6, 7, 8, 9, 10, 10]]))

    layer = MaxPool1D(kernel_size=2, padding="SAME", strides=2)
    npt.assert_allclose(layer(x), jnp.array([[2, 4, 6, 8, 10]]))

    layer = MaxPool1D(kernel_size=2, padding="VALID", strides=1)
    npt.assert_allclose(layer(x), jnp.array([[2, 3, 4, 5, 6, 7, 8, 9, 10]]))

    layer = MaxPool1D(kernel_size=2, padding="VALID", strides=2)
    npt.assert_allclose(layer(x), jnp.array([[2, 4, 6, 8, 10]]))


def test_MaxPool2D():

    layer = MaxPool2D(kernel_size=2, padding="SAME", strides=1)
    x = jnp.arange(1, 10).reshape(1, 3, 3).astype(jnp.float32)
    npt.assert_allclose(layer(x), jnp.array([[[5, 6, 6], [8, 9, 9], [8, 9, 9]]]))


def test_MaxPool3D():
    layer = MaxPool3D(kernel_size=(1, 2, 2), padding="SAME", strides=1)
    x = jnp.arange(1, 10).reshape(1, 1, 3, 3).astype(jnp.float32)
    npt.assert_allclose(layer(x), jnp.array([[[[5, 6, 6], [8, 9, 9], [8, 9, 9]]]]))


def test_AvgPool1D():
    layer = AvgPool1D(kernel_size=2, padding="SAME", strides=1)
    x = jnp.arange(1, 11).reshape(1, 10).astype(jnp.float32)
    npt.assert_allclose(
        layer(x), jnp.array([[1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 5]])
    )


def test_AvgPool2D():
    layer = AvgPool2D(kernel_size=2, padding="SAME", strides=1)
    x = jnp.arange(1, 10).reshape(1, 3, 3).astype(jnp.float32)
    npt.assert_allclose(
        layer(x), jnp.array([[[3, 4, 2.25], [6, 7, 3.75], [3.75, 4.25, 2.25]]])
    )


def test_AvgPool3D():
    layer = AvgPool3D(kernel_size=(1, 2, 2), padding="SAME", strides=1)
    x = jnp.arange(1, 10).reshape(1, 1, 3, 3).astype(jnp.float32)
    npt.assert_allclose(
        layer(x), jnp.array([[[[3, 4, 2.25], [6, 7, 3.75], [3.75, 4.25, 2.25]]]])
    )