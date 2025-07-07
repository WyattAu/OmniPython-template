# examples/interactive.py
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, Slider

from mandelbrot_chaos.logistic import logistic_map
from mandelbrot_chaos.mandelbrot import compute_mandelbrot


def plot_bifurcation_interactive():
    r_min, r_max = 3.0, 4.0
    r_steps = 1000
    r_points = np.linspace(r_min, r_max, r_steps)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title("Logistic Map Bifurcation Diagram")
    ax.set_xlabel("Growth Rate (r)")
    ax.set_ylabel("Population")
    ax.set_xlim(r_min, r_max)
    ax.set_ylim(0, 1)

    # Create blank scatter plot
    sc = ax.scatter([], [], s=0.5, color="blue", alpha=0.3)

    # Animator function
    def animate(frame, data):
        # Gradually add more points as frames increase
        index = min(int(frame * 10), r_steps - 1)
        r_arr = r_points[:index]
        x_arr = [d for i, d in enumerate(data[:index])]

        # Update scatter plot data
        r_scatter = []
        x_scatter = []
        for i, pts in enumerate(x_arr):
            if frame > 100 or i % 10 == 0:  # More efficient rendering
                for x in pts:
                    r_scatter.append(r_arr[i])
                    x_scatter.append(x)

        sc.set_offsets(np.column_stack([r_scatter, x_scatter]))
        return (sc,)

    # Generate data outside animation loop
    data = []
    for r in track(r_points, description="Precomputing data..."):
        data.append(logistic_map(r, 0.5))

    anim = FuncAnimation(
        fig, animate, frames=np.arange(0, 150, 2), fargs=(data,), interval=50, blit=True
    )

    plt.close()
    return anim


def mandelbrot_interactive():
    axis = [-2, 1, -1.5, 1.5]
    width, height = 600, 400
    max_iter = 100

    fig, ax = plt.subplots(figsize=(8, 6))

    # Initial Mandelbrot plot
    mandel = compute_mandelbrot(width, height, *axis, max_iter)
    im = ax.imshow(mandel, cmap="viridis", extent=axis, vmin=0, vmax=max_iter)

    ax.set_title("Interactive Mandelbrot Viewer")

    # Add sliders
    sliders = []
    params = [
        ("X min", axis[0], -2.5, 0.5),
        ("X max", axis[1], -0.5, 2.0),
        ("Y min", axis[2], -2.0, -0.5),
        ("Y max", axis[3], 0.5, 2.0),
        ("Max Iter", max_iter, 20, 500),
    ]

    slider_axes = []
    slider_values = {}
    for i, (name, val, vmin, vmax) in enumerate(params):
        ax_slider = plt.axes([0.25, 0.05 + 0.05 * i, 0.65, 0.03])
        slider = Slider(ax_slider, name, vmin, vmax, valinit=val)
        slider_axes.append(ax_slider)
        slider_values[name] = slider

    def update(val):
        axis = [
            slider_values["X min"].val,
            slider_values["X max"].val,
            slider_values["Y min"].val,
            slider_values["Y max"].val,
        ]
        max_iter = int(slider_values["Max Iter"].val)

        mandel = compute_mandelbrot(width, height, *axis, max_iter)
        im.set_data(mandel)
        im.set_extent(axis)
        im.set_clim(0, max_iter)
        fig.canvas.draw_idle()

    for slider in slider_values.values():
        slider.on_changed(update)

    plt.tight_layout()
    plt.show()
