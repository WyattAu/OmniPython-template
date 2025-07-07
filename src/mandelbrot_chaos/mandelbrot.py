# src/mandelbrot_chaos/mandelbrot.py
import numpy as np
from numba import jit


@jit(nopython=True)
def mandelbrot(c: complex, max_iter: int = 100) -> int:
    z = 0j
    for i in range(max_iter):
        z = z * z + c
        if abs(z) > 2:
            return i
    return max_iter


@jit(nopython=True, parallel=True)
def compute_mandelbrot(
    width: int,
    height: int,
    xmin: float = -2.0,
    xmax: float = 1.0,
    ymin: float = -1.5,
    ymax: float = 1.5,
    max_iter: int = 100,
) -> np.ndarray:
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)

    result = np.zeros((height, width), dtype=np.int64)

    for i in range(height):
        for j in range(width):
            result[i, j] = mandelbrot(complex(x[j], y[i]), max_iter)

    return result


def mandelbrot_data(**kwargs) -> np.ndarray:
    return compute_mandelbrot(**kwargs)
