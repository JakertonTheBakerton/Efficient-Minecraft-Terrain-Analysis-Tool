import numpy as np

def build_grid(chunk_results, x_bounds=None, z_bounds=None):
    """chunk_results: list of (chunk_x, chunk_z, value) tuples."""
    xs = [x for x, z, v in chunk_results]
    zs = [z for x, z, v in chunk_results]

    x_min, x_max = x_bounds if x_bounds else (min(xs), max(xs))
    z_min, z_max = z_bounds if z_bounds else (min(zs), max(zs))

    width = x_max - x_min + 1
    height = z_max - z_min + 1
    grid = np.full((height, width), np.nan)

    for x, z, value in chunk_results:
        grid[z - z_min, x - x_min] = value

    x_coords = list(range(x_min, x_max + 1))
    z_coords = list(range(z_min, z_max + 1))
    return grid, x_coords, z_coords

def expand_region_results_to_chunks(region_results, x_bounds, z_bounds):
    """region_results: dict of (region_x, region_z) -> value.
    Returns a per-chunk grid where every chunk shares its region's value."""
    x_min, x_max = x_bounds
    z_min, z_max = z_bounds
    width = x_max - x_min + 1
    height = z_max - z_min + 1
    grid = np.full((height, width), np.nan)

    for chunk_x in range(x_min, x_max + 1):
        for chunk_z in range(z_min, z_max + 1):
            region_x = chunk_x // 32
            region_z = chunk_z // 32
            value = region_results.get((region_x, region_z))
            if value is not None:
                grid[chunk_z - z_min, chunk_x - x_min] = value

    x_coords = list(range(x_min, x_max + 1))
    z_coords = list(range(z_min, z_max + 1))
    return grid, x_coords, z_coords

