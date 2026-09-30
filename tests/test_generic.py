import anvil
import numpy as np
from terrain_efficiency import aggregate
from terrain_efficiency import visualise
from terrain_efficiency import parser
from terrain_efficiency.cat import block_categories
from terrain_efficiency.metrics import entropy
from terrain_efficiency.metrics import air_ratio as ar
from terrain_efficiency.metrics import roughness as rgh

air = []
solid = []
liquid = []
cave = []
chunk_entropy = []
region_roughness = {}
biome_diversity = {}

excluded_ids = (
    block_categories.AIR_IDS
    | set(block_categories.BLOCK_TO_ID[name] for name in block_categories.WOOD_BLOCKS)
    | set(block_categories.BLOCK_TO_ID[name] for name in block_categories.LEAF_BLOCKS)
    | set(block_categories.BLOCK_TO_ID[name] for name in block_categories.LIQUID_BLOCKS)
)

for region_x in range(-1, 2):      # -1, 0, 1
    for region_z in range(-2, 1):  # -2, -1, 0
        biomes = []
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
                block_ids_array = parser.get_chunk_block_ids(chunk)
                if block_ids_array is None:
                    continue
                global_chunk_x = region_x * 32 + chunk_x
                global_chunk_z = region_z * 32 + chunk_z
                air_results = ar.air_ratios(block_ids_array)
                air.append((global_chunk_x, global_chunk_z, air_results[0]))
                solid.append((global_chunk_x, global_chunk_z, air_results[1]))
                liquid.append((global_chunk_x, global_chunk_z, air_results[3]))
                cave.append((global_chunk_x, global_chunk_z, air_results[4]))
                chunk_entropy_results = entropy.calculate_ent(block_ids_array)
                chunk_entropy.append((global_chunk_x, global_chunk_z, chunk_entropy_results))
                biome = chunk.get_biome(0, 64, 0)
                biomes.append(biome.id)
                height_results = rgh.height_sensor(block_ids_array, excluded_ids)
                height.append(height_results)
        world_y = [383 - h - 64 for h in height]
        roughness = np.var(world_y)
        region_roughness[(region_x, region_z)] = roughness
        biome_results = entropy.calculate_ent(np.array(biomes))
        biome_diversity[(region_x, region_z)] = biome_results


xs = [x for x, z, v in chunk_entropy]
zs = [z for x, z, v in chunk_entropy]
x_bounds = (min(xs), max(xs))
z_bounds = (min(zs), max(zs))

solid_grid, _, _ = aggregate.build_grid(solid, x_bounds, z_bounds)
liquid_grid, _, _ = aggregate.build_grid(liquid, x_bounds, z_bounds)
cave_grid, _, _ = aggregate.build_grid(cave, x_bounds, z_bounds)

# Combine them into one customdata array — this happens ONCE, here
customdata = np.stack([solid_grid, liquid_grid, cave_grid], axis=-1)

entropy_grid, x_coords, z_coords = aggregate.build_grid(chunk_entropy, x_bounds, z_bounds)
air_grid, _, _ = aggregate.build_grid(air, x_bounds, z_bounds)
roughness_grid, _, _ = aggregate.expand_region_results_to_chunks(region_roughness, x_bounds, z_bounds)
biome_grid, _, _ = aggregate.expand_region_results_to_chunks(biome_diversity, x_bounds, z_bounds)

visualise.render_multi_metric_heatmap({
    'Entropy': entropy_grid,
    'Air %': air_grid,
    'Roughness': roughness_grid,
    'Biome Diversity': biome_grid,
}, x_coords, z_coords, customdata=customdata, customdata_metric='Air %')