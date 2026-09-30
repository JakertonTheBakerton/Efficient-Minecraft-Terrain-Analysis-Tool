import anvil
import numpy as np
from terrain_efficiency.metrics.entropy import calculate_ent
import time
import csv

start_time = time.perf_counter()
biome_list = []
for region_x in range(-1, 2):
    for region_z in range(-2, 1):
        biomes = []
        filename = f'data/raw/r.{region_x}.{region_z}.mca'
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
print(biome_list)
print(elapsed)

#with open('results/benchmarks.csv', 'a', newline='') as f:
#    writer = csv.writer(f)
#    writer.writerow(['basic', 'biome_diversity', elapsed])