# src/mandelbrot_chaos/logistic.py
import numpy as np
import numpy.typing as npt


def logistic_map(
    r: float, x0: float, iterations: int = 50, transient: int = 100
) -> npt.NDArray[np.float64]:
    """Compute logistic map values.

    Args:
        r: Growth rate parameter
        x0: Initial population (0 to 1)
        iterations: Number of values to return
        transient: Number of iterations to skip before recording

    Returns:
        Array of population values after the transient period
    """
    results = np.zeros(iterations)
    x = x0

    # Run transient iterations
    for _ in range(transient):
        x = r * x * (1 - x)

    # Record subsequent iterations
    for i in range(iterations):
        x = r * x * (1 - x)
        results[i] = x

    return results


def bifurcation_data(
    r_min: float = 2.8,
    r_max: float = 4.0,
    r_steps: int = 300,
    samples: int = 100,
    iterations: int = 100,
) -> tuple[npt.NDArray[np.float64], npt.NDArray[npt.NDArray]]:
    """Generate bifurcation diagram data.

    Args:
        r_min: Minimum r value
        r_max: Maximum r value
        r_steps: Number of r values to sample
        samples: Number of random initial conditions per r
        iterations: Number of iterations per initial condition

    Returns:
        Tuple of (r_values, data_points) where data_points[i] contains
        the x-values for each r_values[i]
    """
    r_values = np.linspace(r_min, r_max, r_steps)
    bifurcation = [np.array([]) for _ in r_values]

    for i, r in enumerate(r_values):
        # Use multiple initial conditions
        x0s = np.random.random(samples)
        for x0 in x0s:
            trajectory = logistic_map(r, x0, iterations)
            # Store multiple points for each r
            bifurcation[i] = np.append(bifurcation[i], trajectory)

    return r_values, np.array(bifurcation, dtype=object)
