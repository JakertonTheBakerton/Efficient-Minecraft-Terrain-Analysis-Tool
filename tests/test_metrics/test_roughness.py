import math
import anvil
import numpy as np
from terrain_efficiency.cat import block_categories
import time
import csv

def unpack_indices(long_value, bits_per_index, indices_per_long):
    mask = (1 << bits_per_index) - 1
    indices = []
    for i in range(indices_per_long):
        index = (long_value >> (i * bits_per_index)) & mask
        indices.append(index)
    return indices


def get_section_block_ids(chunk, section_y):
    section = chunk.get_section(section_y)
    if section is None:
        return np.full((16, 16, 16), block_categories.AIR_ID, dtype=int)

    block_states = section['block_states']
    palette = block_states['palette']

    # Convert this section's palette to your own int IDs, once — not per block.
    palette_names = [str(entry['Name']).replace('minecraft:', '') for entry in palette]
    palette_to_your_id = np.array(
        [block_categories.get_id(name) for name in palette_names]
    )

    if 'data' not in block_states.keys():
        # Uniform section — every block is palette[0].
        your_id = palette_to_your_id[0]
        return np.full((16, 16, 16), your_id, dtype=int)

    data = block_states['data']
    bits_per_index = max(4, math.ceil(math.log2(len(palette))))
    indices_per_long = 64 // bits_per_index

    palette_indices = []
    for long_value in data:
        palette_indices.extend(unpack_indices(long_value, bits_per_index, indices_per_long))
    palette_indices = np.array(palette_indices[:4096])  # trim any padding overflow

    # Map every palette index to your int ID in one vectorized step.
    your_ids_flat = palette_to_your_id[palette_indices]

    return your_ids_flat.reshape((16, 16, 16))
excluded_ids = (
    block_categories.AIR_IDS
    | set(block_categories.BLOCK_TO_ID[name] for name in block_categories.WOOD_BLOCKS)
    | set(block_categories.BLOCK_TO_ID[name] for name in block_categories.LEAF_BLOCKS)
    | set(block_categories.BLOCK_TO_ID[name] for name in block_categories.LIQUID_BLOCKS)
)
start_time = time.perf_counter()
region_roughness = {}
for region_x in range(-1, 2):      # -1, 0, 1
    for region_z in range(-2, 1):  # -2, -1, 0
        height = []
        filename = f"data/raw/r.{region_x}.{region_z}.mca"
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
                
                sections = []
                for y_section in range(-4, 20):
                    section_array = get_section_block_ids(chunk, y_section)
                    sections.append(section_array)
                chunk_array = np.concatenate(sections, axis=0)
                is_solid = ~np.isin(chunk_array, list(excluded_ids))
                is_solid_topdown = is_solid[::-1]
                surface_indices = np.argmax(is_solid_topdown, axis=0)
                height.append(surface_indices)
        world_y = [383 - h - 64 for h in height]
        roughness = np.var(world_y)
        region_roughness[(region_x, region_z)] = roughness

end_time = time.perf_counter()
elapsed = end_time - start_time
for coords in sorted(region_roughness.keys()):
    print(f"Region {coords} variance: {region_roughness[coords]}")
print(f'Time elapsed: {elapsed}')
with open('results/benchmarks.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['vectorized', 'per_region_roughness', elapsed])