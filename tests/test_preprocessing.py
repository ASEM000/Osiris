import jax.numpy as jnp
import numpy.testing as npt

from serket.nn import HistogramEqualization2D


def test_histogram():
    # tested against skimage.exposure.equalize_hist

    x = jnp.array(
        [
            [
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                82,
                82,
                82,
                82,
                82,
                82,
                82,
                82,
                82,
                82,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                82,
            ],
            [
                82,
                82,
                83,
                83,
                83,
                83,
                83,
                82,
                82,
                82,
                82,
                82,
                82,
                82,
                82,
                82,
                82,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
            ],
            [
                80,
                81,
                83,
                83,
                83,
                83,
                83,
                82,
                82,
                82,
                82,
                82,
                82,
                82,
                82,
                82,
                82,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                82,
            ],
            [
                82,
                82,
                83,
                83,
                83,
                83,
                83,
                82,
                82,
                82,
                82,
                82,
                82,
                82,
                82,
                82,
                82,
                82,
                83,
                82,
                82,
                83,
                82,
                82,
                83,
            ],
            [
                83,
                82,
                83,
                84,
                82,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                82,
                82,
                82,
                82,
                82,
                82,
                82,
                82,
                81,
                82,
                83,
            ],
            [
                83,
                82,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                82,
                82,
                82,
                82,
                82,
                82,
                83,
                85,
                84,
                82,
                83,
            ],
            [
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                82,
                82,
                82,
                82,
                83,
                82,
                83,
                86,
                85,
                82,
                82,
            ],
            [
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                82,
                84,
                86,
                86,
                85,
                84,
                87,
                86,
                84,
            ],
            [
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                84,
                85,
                85,
                85,
                84,
                86,
                86,
                84,
            ],
            [
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                82,
                84,
                86,
                84,
                82,
                82,
                83,
                86,
                86,
                86,
                86,
            ],
            [
                83,
                83,
                83,
                83,
                83,
                83,
                82,
                83,
                83,
                83,
                83,
                83,
                82,
                83,
                83,
                84,
                86,
                84,
                82,
                84,
                84,
                84,
                84,
                84,
                85,
            ],
            [
                83,
                83,
                83,
                82,
                83,
                82,
                82,
                83,
                83,
                83,
                83,
                83,
                81,
                84,
                82,
                83,
                86,
                84,
                82,
                85,
                86,
                82,
                82,
                82,
                84,
            ],
            [
                83,
                83,
                82,
                84,
                85,
                83,
                82,
                83,
                83,
                83,
                83,
                83,
                84,
                85,
                85,
                84,
                83,
                84,
                85,
                86,
                87,
                85,
                83,
                85,
                85,
            ],
            [
                83,
                83,
                82,
                84,
                86,
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                85,
                86,
                86,
                85,
                82,
                84,
                86,
                84,
                85,
                86,
                84,
                86,
                85,
            ],
            [
                83,
                83,
                83,
                83,
                83,
                83,
                82,
                82,
                82,
                82,
                84,
                85,
                85,
                85,
                82,
                83,
                85,
                85,
                86,
                85,
                85,
                85,
                85,
                85,
                85,
            ],
            [
                83,
                83,
                83,
                83,
                83,
                83,
                83,
                82,
                83,
                83,
                84,
                86,
                85,
                85,
                83,
                84,
                86,
                85,
                86,
                86,
                86,
                85,
                85,
                85,
                85,
            ],
            [
                82,
                83,
                82,
                85,
                86,
                86,
                86,
                82,
                83,
                86,
                85,
                85,
                85,
                85,
                86,
                85,
                85,
                85,
                86,
                85,
                86,
                85,
                85,
                85,
                85,
            ],
            [
                84,
                83,
                82,
                84,
                84,
                83,
                83,
                82,
                83,
                86,
                85,
                85,
                85,
                85,
                85,
                86,
                85,
                85,
                86,
                85,
                86,
                85,
                85,
                85,
                85,
            ],
            [
                82,
                82,
                82,
                82,
                82,
                83,
                83,
                82,
                83,
                86,
                85,
                85,
                85,
                85,
                85,
                87,
                85,
                84,
                86,
                85,
                85,
                85,
                85,
                85,
                85,
            ],
            [
                84,
                83,
                82,
                84,
                85,
                84,
                84,
                84,
                85,
                85,
                85,
                85,
                85,
                85,
                86,
                86,
                86,
                85,
                85,
                85,
                85,
                85,
                85,
                85,
                85,
            ],
            [
                86,
                85,
                82,
                85,
                86,
                83,
                83,
                86,
                86,
                85,
                85,
                85,
                85,
                85,
                86,
                86,
                86,
                86,
                85,
                85,
                85,
                85,
                85,
                85,
                85,
            ],
            [
                85,
                85,
                85,
                85,
                86,
                85,
                85,
                86,
                86,
                86,
                86,
                86,
                86,
                86,
                85,
                85,
                85,
                85,
                86,
                86,
                86,
                86,
                84,
                85,
                87,
            ],
            [
                85,
                85,
                85,
                86,
                86,
                86,
                86,
                86,
                86,
                86,
                86,
                86,
                86,
                86,
                85,
                85,
                85,
                86,
                86,
                86,
                86,
                86,
                84,
                85,
                86,
            ],
            [
                86,
                86,
                85,
                86,
                86,
                86,
                86,
                86,
                86,
                86,
                86,
                86,
                86,
                86,
                84,
                85,
                86,
                85,
                86,
                86,
                86,
                85,
                85,
                85,
                85,
            ],
            [
                84,
                85,
                85,
                85,
                85,
                85,
                85,
                85,
                86,
                86,
                86,
                86,
                85,
                86,
                85,
                85,
                85,
                85,
                85,
                86,
                85,
                85,
                85,
                85,
                85,
            ],
        ]
    )

    y = jnp.array(
        [
            [
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                48.552,
            ],
            [
                48.552,
                48.552,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
            ],
            [
                0.408,
                1.632,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                48.552,
            ],
            [
                48.552,
                48.552,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                133.824,
                48.552,
                48.552,
                133.824,
                48.552,
                48.552,
                133.824,
            ],
            [
                133.824,
                48.552,
                133.824,
                151.776,
                48.552,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                1.632,
                48.552,
                133.824,
            ],
            [
                133.824,
                48.552,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                133.824,
                211.344,
                151.776,
                48.552,
                133.824,
            ],
            [
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                48.552,
                48.552,
                48.552,
                48.552,
                133.824,
                48.552,
                133.824,
                253.368,
                211.344,
                48.552,
                48.552,
            ],
            [
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                48.552,
                151.776,
                253.368,
                253.368,
                211.344,
                151.776,
                255.0,
                253.368,
                151.776,
            ],
            [
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                151.776,
                211.344,
                211.344,
                211.344,
                151.776,
                253.368,
                253.368,
                151.776,
            ],
            [
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                48.552,
                151.776,
                253.368,
                151.776,
                48.552,
                48.552,
                133.824,
                253.368,
                253.368,
                253.368,
                253.368,
            ],
            [
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                48.552,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                48.552,
                133.824,
                133.824,
                151.776,
                253.368,
                151.776,
                48.552,
                151.776,
                151.776,
                151.776,
                151.776,
                151.776,
                211.344,
            ],
            [
                133.824,
                133.824,
                133.824,
                48.552,
                133.824,
                48.552,
                48.552,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                1.632,
                151.776,
                48.552,
                133.824,
                253.368,
                151.776,
                48.552,
                211.344,
                253.368,
                48.552,
                48.552,
                48.552,
                151.776,
            ],
            [
                133.824,
                133.824,
                48.552,
                151.776,
                211.344,
                133.824,
                48.552,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                151.776,
                211.344,
                211.344,
                151.776,
                133.824,
                151.776,
                211.344,
                253.368,
                255.0,
                211.344,
                133.824,
                211.344,
                211.344,
            ],
            [
                133.824,
                133.824,
                48.552,
                151.776,
                253.368,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                211.344,
                253.368,
                253.368,
                211.344,
                48.552,
                151.776,
                253.368,
                151.776,
                211.344,
                253.368,
                151.776,
                253.368,
                211.344,
            ],
            [
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                48.552,
                48.552,
                48.552,
                48.552,
                151.776,
                211.344,
                211.344,
                211.344,
                48.552,
                133.824,
                211.344,
                211.344,
                253.368,
                211.344,
                211.344,
                211.344,
                211.344,
                211.344,
                211.344,
            ],
            [
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                133.824,
                48.552,
                133.824,
                133.824,
                151.776,
                253.368,
                211.344,
                211.344,
                133.824,
                151.776,
                253.368,
                211.344,
                253.368,
                253.368,
                253.368,
                211.344,
                211.344,
                211.344,
                211.344,
            ],
            [
                48.552,
                133.824,
                48.552,
                211.344,
                253.368,
                253.368,
                253.368,
                48.552,
                133.824,
                253.368,
                211.344,
                211.344,
                211.344,
                211.344,
                253.368,
                211.344,
                211.344,
                211.344,
                253.368,
                211.344,
                253.368,
                211.344,
                211.344,
                211.344,
                211.344,
            ],
            [
                151.776,
                133.824,
                48.552,
                151.776,
                151.776,
                133.824,
                133.824,
                48.552,
                133.824,
                253.368,
                211.344,
                211.344,
                211.344,
                211.344,
                211.344,
                253.368,
                211.344,
                211.344,
                253.368,
                211.344,
                253.368,
                211.344,
                211.344,
                211.344,
                211.344,
            ],
            [
                48.552,
                48.552,
                48.552,
                48.552,
                48.552,
                133.824,
                133.824,
                48.552,
                133.824,
                253.368,
                211.344,
                211.344,
                211.344,
                211.344,
                211.344,
                255.0,
                211.344,
                151.776,
                253.368,
                211.344,
                211.344,
                211.344,
                211.344,
                211.344,
                211.344,
            ],
            [
                151.776,
                133.824,
                48.552,
                151.776,
                211.344,
                151.776,
                151.776,
                151.776,
                211.344,
                211.344,
                211.344,
                211.344,
                211.344,
                211.344,
                253.368,
                253.368,
                253.368,
                211.344,
                211.344,
                211.344,
                211.344,
                211.344,
                211.344,
                211.344,
                211.344,
            ],
            [
                253.368,
                211.344,
                48.552,
                211.344,
                253.368,
                133.824,
                133.824,
                253.368,
                253.368,
                211.344,
                211.344,
                211.344,
                211.344,
                211.344,
                253.368,
                253.368,
                253.368,
                253.368,
                211.344,
                211.344,
                211.344,
                211.344,
                211.344,
                211.344,
                211.344,
            ],
            [
                211.344,
                211.344,
                211.344,
                211.344,
                253.368,
                211.344,
                211.344,
                253.368,
                253.368,
                253.368,
                253.368,
                253.368,
                253.368,
                253.368,
                211.344,
                211.344,
                211.344,
                211.344,
                253.368,
                253.368,
                253.368,
                253.368,
                151.776,
                211.344,
                255.0,
            ],
            [
                211.344,
                211.344,
                211.344,
                253.368,
                253.368,
                253.368,
                253.368,
                253.368,
                253.368,
                253.368,
                253.368,
                253.368,
                253.368,
                253.368,
                211.344,
                211.344,
                211.344,
                253.368,
                253.368,
                253.368,
                253.368,
                253.368,
                151.776,
                211.344,
                253.368,
            ],
            [
                253.368,
                253.368,
                211.344,
                253.368,
                253.368,
                253.368,
                253.368,
                253.368,
                253.368,
                253.368,
                253.368,
                253.368,
                253.368,
                253.368,
                151.776,
                211.344,
                253.368,
                211.344,
                253.368,
                253.368,
                253.368,
                211.344,
                211.344,
                211.344,
                211.344,
            ],
            [
                151.776,
                211.344,
                211.344,
                211.344,
                211.344,
                211.344,
                211.344,
                211.344,
                253.368,
                253.368,
                253.368,
                253.368,
                211.344,
                253.368,
                211.344,
                211.344,
                211.344,
                211.344,
                211.344,
                253.368,
                211.344,
                211.344,
                211.344,
                211.344,
                211.344,
            ],
        ]
    )

    npt.assert_allclose(y, HistogramEqualization2D()(x[None])[0], atol=1e-3)
