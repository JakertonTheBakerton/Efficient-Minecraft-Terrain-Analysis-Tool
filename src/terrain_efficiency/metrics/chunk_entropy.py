import anvil
import numpy as np
from terrain_efficiency.cat import block_categories
from terrain_efficiency.metrics.entropy import calculate_ent
from terrain_efficiency import parser
import time
import csv

start_time = time.perf_counter()
entropy = []
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
                result = calculate_ent(block_ids_array)
                global_chunk_x = region_x * 32 + chunk_x
                global_chunk_z = region_z * 32 + chunk_z
                entropy.append(global_chunk_x, global_chunk_z, result)

end_time = time.perf_counter()
elapsed = end_time - start_time
#print(elapsed)
#with open('results/benchmarks.csv', 'a', newline='') as f:
#    writer = csv.writer(f)
#    writer.writerow(['vectorised', 'chunk_entropy', elapsed])

