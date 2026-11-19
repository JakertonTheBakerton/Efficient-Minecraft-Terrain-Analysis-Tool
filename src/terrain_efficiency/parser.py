import math
import numpy as np
from terrain_efficiency.cat import block_categories


def discover_regions(data_dir="data/raw", max_regions=32):
    """Finds .mca files, parses coordinates, enforces the limit, and checks rectangularity."""
    files = glob.glob(f"{data_dir}/r.*.*.mca")
    regions = []
    for f in files:
        m = re.search(r"r\.(-?\d+)\.(-?\d+)\.mca", os.path.basename(f))
        if m:
            regions.append((int(m.group(1)), int(m.group(2)), f))
    regions.sort()
    
    if not regions:
        raise ValueError(f"No region files found in {data_dir}")
    
    if len(regions) > max_regions:
        raise ValueError(f"Found {len(regions)} regions, max is {max_regions}")
    
    # --- NEW: Rectangular grid check ---
    unique_rx = sorted(set(rx for rx, rz, f in regions))
    unique_rz = sorted(set(rz for rx, rz, f in regions))
    expected_count = len(unique_rx) * len(unique_rz)
    
    if len(regions) != expected_count:
        existing = set((rx, rz) for rx, rz, f in regions)
        missing = [
            (rx, rz) 
            for rx in unique_rx 
            for rz in unique_rz 
            if (rx, rz) not in existing
        ]
        raise ValueError(
            f"Region files do not form a complete rectangle.\n"
            f"Found {len(regions)} regions covering X={unique_rx} and Z={unique_rz} "
            f"(a solid rectangle would need {expected_count}).\n"
            f"Missing regions: {missing}\n"
            f"Please add the missing .mca files or remove regions to form a rectangle."
        )
    
    return regions

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

