# examples/mandelbrot_cli.py
from typing import Optional

import matplotlib.pyplot as plt
import typer
from rich import print

from mandelbrot_chaos.visualization import plot_mandelbrot

app = typer.Typer(help="Mandelbrot Set Visualization Tool")


@app.command()
def main(
    width: int = typer.Option(800, "--width", "-w", help="Image width"),
    height: int = typer.Option(600, "--height", "-h", help="Image height"),
    max_iter: int = typer.Option(100, "--max-iter", "-i", help="Max iterations"),
    cmap: str = typer.Option("twilight", "--cmap", "-c", help="Color map"),
    output: str | None = typer.Option(None, "--output", "-o", help="Output file"),
    dpi: int = typer.Option(100, "--dpi", "-d", help="Image resolution"),
):
    """
    Generate a visualization of the Mandelbrot set with specified parameters.

    Examples:

    mandelbrot_cli.py --width 800 --height 600 --max-iter 100
    mandelbrot_cli.py -w 1024 -h 768 -i 200 -o mandelbrot.png
    """
    print(
        f"[bold green]Generating Mandelbrot set:[/] "
        f"{width}x{height}px, max_iter={max_iter}"
    )

    fig = plot_mandelbrot(
        width=width, height=height, max_iter=max_iter, cmap=cmap, dpi=dpi
    )

    if output:
        fig.savefig(output, bbox_inches="tight", dpi=dpi)
        print(f"\n[bold green]✓ Saved to {output}[/]")
    else:
        print("\n[bold yellow]Displaying visualization...")
        plt.show()

    plt.close(fig)


if __name__ == "__main__":
    app()
