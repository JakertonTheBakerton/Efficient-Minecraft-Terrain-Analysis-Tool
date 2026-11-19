import anvil
import numpy as np
from terrain_efficiency.metrics.entropy import calculate_ent
from terrain_efficiency import parser
import time
import csv

def count_biomes_per_chunk(chunk):
    """Counts distinct biomes in a chunk by sampling a 4x4 horizontal grid at 3 depths."""
    unique_biomes = set()
    # x and z offsets for 1.21 4x4x4 biome cells
    offsets = [0, 4, 8, 12] 
    # y-levels: surface, mid-cave, deep (deep dark/dripstone)
    y_levels = [80, 0, -48] 
    
    for y in y_levels:
        for x in offsets:
            for z in offsets:
                biome = chunk.get_biome(x, y, z)
                if biome is not None:
                    unique_biomes.add(biome.id)
                    
    return len(unique_biomes)
    
start_time = time.perf_counter()
biome_list = []
regions_to_process = parser.discover_regions()
for region_x, region_z, filename in regions_to_process: 
    biomes = []
    region = anvil.Region.from_file(filename)
    for local_chunk_x in range(32):
        for local_chunk_z in range(32):
            try:
                chunk = anvil.Chunk.from_region(region, local_chunk_x, local_chunk_z)
            except Exception:
                continue
            biome = chunk.get_biome(0, 64, 0)
            biomes.append(biome.id)
    biome_ent = calculate_ent(np.array(biomes))
    biome_list.append(biome_ent)


end_time = time.perf_counter()
elapsed = end_time - start_time

with open('results/benchmarks.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['basic', 'biome_diversity', elapsed])
