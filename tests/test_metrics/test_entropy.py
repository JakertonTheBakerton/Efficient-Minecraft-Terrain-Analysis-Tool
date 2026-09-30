import anvil
import numpy as np
from terrain_efficiency.cat import block_categories
from terrain_efficiency.metrics.entropy import calculate_ent
import time
import csv

region = anvil.Region.from_file('data/raw/r.0.0.mca')
chunk = anvil.Chunk.from_region(region, 7, -2)



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

block_ids_array = np.array(ids)
result = calculate_ent(block_ids_array)
end_time = time.perf_counter()
elapsed = end_time - start_time
#with open('results/benchmarks.csv', 'a', newline='') as f:
#    writer = csv.writer(f)
#    writer.writerow(['basic', 'chunk_entropy', elapsed])
print(f"Entropy for chunk: {result}")

