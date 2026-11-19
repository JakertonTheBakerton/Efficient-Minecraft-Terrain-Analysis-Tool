import math
import anvil
import numpy as np
from terrain_efficiency.cat import block_categories
from terrain_efficiency import parser
import time
import csv

excluded_ids = (
    block_categories.AIR_IDS
    | set(block_categories.BLOCK_TO_ID[name] for name in block_categories.WOOD_BLOCKS)
    | set(block_categories.BLOCK_TO_ID[name] for name in block_categories.LEAF_BLOCKS)
    | set(block_categories.BLOCK_TO_ID[name] for name in block_categories.LIQUID_BLOCKS)
)

def height_sensor(chunk_array, excluded_ids):
    is_solid = ~np.isin(chunk_array, list(excluded_ids))
    is_solid_topdown = is_solid[::-1]
    surface_indices = np.argmax(is_solid_topdown, axis=0)
    return surface_indices

start_time = time.perf_counter()
chunk_avg_height = []
region_roughness = {}
regions_to_process = parser.discover_regions()

for region_x, region_z, filename in regions_to_process:
    height = [] 
    region = anvil.Region.from_file(filename)
    for chunk_x in range(32):      # -1, 0, 1
        for chunk_z in range(32):
            offset, length = region.chunk_location(chunk_x, chunk_z)
            if offset == 0 and length == 0:
                continue
            try:
                chunk = anvil.Chunk.from_region(region, chunk_x, chunk_z)
            except Exception:
                continue
            chunk_array = parser.get_chunk_block_ids(chunk)
            if chunk_array is None:
                continue
            surface_indices = height_sensor(chunk_array, excluded_ids)
            height.append(surface_indices)
            global_chunk_x = region_x * 32 + chunk_x
            global_chunk_z = region_z * 32 + chunk_z
            chunk_world_y = 383 - surface_indices - 64
            chunk_avg_height.append(
                (global_chunk_x, global_chunk_z, float(np.mean(chunk_world_y)))
            )
    world_y = [383 - h - 64 for h in height]
    roughness = np.var(world_y)
    region_roughness[(region_x, region_z)] = roughness

end_time = time.perf_counter()
elapsed = round(end_time - start_time, 2)
with open('results/benchmarks.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['vectorised', 'per_region_roughness', elapsed])
