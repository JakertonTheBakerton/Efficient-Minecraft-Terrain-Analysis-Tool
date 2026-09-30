import anvil
import numpy as np
from terrain_efficiency.cat import block_categories
from terrain_efficiency import parser
import time
import csv

def air_ratios(ids):
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
region = anvil.Region.from_file('data/raw/r.1.0.mca')
chunk = anvil.Chunk.from_region(region, 11, 17)
x = parser.get_chunk_block_ids(chunk)
if x is None:
    print("Chunk is effectively empty")
else:
    unique, counts = np.unique(x, return_counts=True)
    for u, c in sorted(zip(unique, counts), key=lambda pair: -pair[1]):
        print(block_categories.ID_TO_BLOCK[u], c)
print(air_ratios(x))