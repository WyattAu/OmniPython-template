# src/mandelbrot_chaos/visualization.py
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Colormap
from matplotlib.figure import Figure

from .logistic import bifurcation_data
from .mandelbrot import compute_mandelbrot


def plot_mandelbrot(
    width: int = 800,
    height: int = 600,
    max_iter: int = 100,
    cmap: str = "inferno",
    dpi: int = 100,
) -> Figure:
    """Generate Mandelbrot set visualization."""
    mandel = compute_mandelbrot(width=width, height=height, max_iter=max_iter)

    fig = plt.figure(figsize=(width / 100, height / 100), dpi=dpi)
    ax = fig.add_subplot(111)

    # Color handling with normalization
    norm = mpl.colors.PowerNorm(0.3, vmin=0, vmax=max_iter)
    im = ax.imshow(mandel, cmap=cmap, extent=[-2, 1, -1.5, 1.5], norm=norm)

    ax.set_title("Mandelbrot Set", fontsize=16)
    ax.set_xlabel("Real Axis")
    ax.set_ylabel("Imaginary Axis")

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, label="Iterations to Escape")
    cbar.ax.tick_params(labelsize=8)

    return fig


def plot_bifurcation(
    r_min: float = 2.8,
    r_max: float = 4.0,
    r_steps: int = 1000,
    samples: int = 100,
    iterations: int = 100,
    alpha: float = 0.1,
    s: float = 0.1,
    color: str = "darkblue",
    figsize: tuple[float, float] = (10, 7),
) -> Figure:
    """Generate logistic map bifurcation diagram."""
    r_values, x_points = bifurcation_data(
        r_min=r_min,
        r_max=r_max,
        r_steps=r_steps,
        samples=samples,
        iterations=iterations,
    )

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)

    # Plot each point individually for efficiency
    for i, points in enumerate(x_points):
        r = r_values[i]
        ax.plot(
            np.full_like(points, r), points, ",", color=color, alpha=alpha, markersize=s
        )

    ax.set_title("Logistic Map Bifurcation Diagram", fontsize=16)
    ax.set_xlabel("Growth Rate (r)")
    ax.set_ylabel("Population")
    ax.set_xlim(r_min, r_max)
    ax.set_ylim(0, 1)
    ax.grid(alpha=0.3)

    return fig
