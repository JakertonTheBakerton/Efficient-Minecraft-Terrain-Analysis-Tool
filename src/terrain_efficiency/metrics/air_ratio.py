import anvil
import numpy as np
from terrain_efficiency.cat import block_categories
from terrain_efficiency import parser
import time
import csv

def air_ratios(ids):
    quant = ids.size

    air_count = int(np.count_nonzero(np.isin(ids, list(block_categories.AIR_IDS))))
    liquid_count = int(np.count_nonzero(np.isin(ids, list(block_categories.LIQUID_IDS))))
    cave_air_count = int(np.count_nonzero(ids == block_categories.CAVE_AIR_ID))

    air_percentage = float(round((air_count / quant) * 100, 3))
    liquid_percentage = float(round((liquid_count / quant) * 100, 3))
    solid_percentage = float(round(100 - air_percentage - liquid_percentage, 3))
    #print(f'The ratio is: Air = {air_percentage}  Solid = {solid_percentage}  Liquid = {liquid_percentage} ({liquid_count} blocks)')
    #print(f'Cave Score: {cave_air_count}')
    return air_percentage, solid_percentage, liquid_percentage, liquid_count, cave_air_count


start_time = time.perf_counter()
air_ratio = []
for region_x in range(-1, 2):      # -1, 0, 1
    for region_z in range(-2, 1):  # -2, -1, 0
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
                block_ids_array = parser.get_chunk_block_ids(chunk)
                if block_ids_array is None:
                    continue
                results = air_ratios(block_ids_array)
                global_chunk_x = region_x * 32 + chunk_x
                global_chunk_z = region_z * 32 + chunk_z
                air_ratio.append((global_chunk_x, global_chunk_z, results))



end_time = time.perf_counter()
elapsed = end_time - start_time
#print(air_ratio)
#print(elapsed)
#with open('results/benchmarks.csv', 'a', newline='') as f:
    #writer = csv.writer(f)
    #writer.writerow(['vectorised', 'air_ratio', elapsed])

