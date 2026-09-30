#AIR_RATIO.PY
import anvil
import numpy as np
from terrain_efficiency.cat import block_categories
import time
import csv

def air_ratios(ids: np.ndarray):
    quant = ids.size
    air_count: int = 0
    liquid_count: int = 0
    cave_air_count: int = 0
    for y in range(-64, 319):
        for x in range(16):
            for z in range (16):
                block = ids[y, x, z]
                if block == block_categories.CAVE_AIR_ID:
                    cave_air_count = cave_air_count + 1
                if block in block_categories.AIR_IDS:
                    air_count = air_count + 1
                if block in block_categories.LIQUID_IDS:
                    liquid_count = liquid_count + 1
    air_percentage = round((air_count / quant) * 100, 3)
    liquid_percentage = round((liquid_count / quant) * 100, 3)
    solid_percentage = round(100 - air_percentage - liquid_percentage, 3)
    #print(f'The ratio is: Air = {air_percentage}  Solid = {solid_percentage}  Liquid = {liquid_percentage} ({liquid_count} blocks)')
    #print(f'Cave Score: {cave_air_count}')
    return air_percentage, solid_percentage, liquid_percentage, liquid_count, cave_air_count

region = anvil.Region.from_file('data/raw/r.0.0.mca')
chunk = anvil.Chunk.from_region(region, 20, -15)

start_time = time.perf_counter()

ids = []
for y in range(-64, 319):
    layer = []
    for x in range(16):
        row = []
        for z in range(16):
            block = chunk.get_block(x, y, z)
            row.append(block_categories.get_id(block.id))
        layer.append(row)
    ids.append(layer)

results = air_ratios(np.array(ids))

end_time = time.perf_counter()
elapsed = end_time - start_time

#with open('results/benchmarks.csv', 'a', newline='') as f:
#    writer = csv.writer(f)
#    writer.writerow(['basic', 'air_ratio', elapsed])
#air_perc = results[1]
#solid_perc = results[2]
#liquid_perc = results[3]
#liquid_cnt = results[4]

#BIOME_DIVERSITY.PY
import anvil
import numpy as np
from terrain_efficiency.metrics.entropy import calculate_ent
import time
import csv

start_time = time.perf_counter()
biomes = []
for region_x in range(-1, 2):
    for region_z in range(-2, 1):
        filename = f'data/raw/r.{region_x}.{region_z}.mca'
        region = anvil.Region.from_file(filename)
        for local_chunk_x in range(32):
            for local_chunk_z in range(32):
                try:
                    chunk = anvil.Chunk.from_region(region, local_chunk_x, local_chunk_z)
                    biome = chunk.get_biome(0, 64, 0)
                    biomes.append(biome.id)
                except Exception:
                    continue

print(f'Entropy Score: {calculate_ent(np.array(biomes))}')

end_time = time.perf_counter()
elapsed = end_time - start_time

#with open('results/benchmarks.csv', 'a', newline='') as f:
#    writer = csv.writer(f)
#    writer.writerow(['basic', 'biome_diversity', elapsed])

#ENTROPY.PY
# Calculates Shannon Entropy for any sample: ids
import numpy as np

def calculate_ent(ids: np.ndarray) -> float:
    sample_size = ids.size
    unique_ids, counts = np.unique(ids, return_counts=True)
    proportion = counts / sample_size
    entropy = -np.sum(proportion * np.log2(proportion))
    return entropy

#ROUGHNESS.PY
import anvil
import numpy as np
from terrain_efficiency.cat import block_categories
import time
import csv

def per_region_roughness(region):
    height = []
    for chunk_x in range(32):
        for chunk_z in range(32):
            chunk = anvil.Chunk.from_region(region, chunk_x, chunk_z)
            for column_x in range(16):
                for column_z in range(16):
                    block_y = 319
                    block = chunk.get_block(column_x, block_y, column_z)
                    while block.id == 'air' or block.id in block_categories.LIQUID_BLOCKS:
                        block_y = block_y - 1
                        block = chunk.get_block(column_x, block_y, column_z)
                    height.append(block_y)
    return height

start_time = time.perf_counter()
region = anvil.Region.from_file('data/raw/r.0.0.mca')
result = per_region_roughness(region)
end_time = time.perf_counter()

elapsed = end_time - start_time
#print(f"Elapsed time: {elapsed:.3f} seconds")

#with open('results/benchmarks.csv', 'a', newline='') as f:
#    writer = csv.writer(f)
#    writer.writerow(['basic', 'per_region_roughness', elapsed])