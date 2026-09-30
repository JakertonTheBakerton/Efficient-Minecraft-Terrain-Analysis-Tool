import math
import numpy as np
from terrain_efficiency.cat import block_categories


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

    # Map every palette index to an int ID in one vectorized step.
    your_ids_flat = palette_to_your_id[palette_indices]

    return your_ids_flat.reshape((16, 16, 16))


def get_chunk_block_ids(chunk):
    sections = []
    for y_section in range(-4, 20):
        section_array = get_section_block_ids(chunk, y_section)
        sections.append(section_array)
    chunk_array = np.concatenate(sections, axis=0)
    solid_count = np.count_nonzero(chunk_array != block_categories.AIR_ID)
    if solid_count <= 257:  # nothing but the bottom bedrock layer
        return None
    return chunk_array

