import anvil
import numpy as np
import time
from terrain_efficiency import aggregate
from terrain_efficiency import visualise
from terrain_efficiency import parser
from terrain_efficiency.cat import block_categories
from terrain_efficiency.metrics import entropy
from terrain_efficiency.metrics import air_ratio as ar
from terrain_efficiency.metrics import roughness as rgh
from terrain_efficiency.metrics.biome_diversity import count_biomes_per_chunk

air = []
solid = []
liquid = []
cave = []
chunk_entropy = []
chunk_avg_height = []
chunk_biome_counts = []
region_roughness = {}
biome_diversity = {}
skipped_unloaded = 0
skipped_empty = 0

excluded_ids = (
    block_categories.AIR_IDS
    | set(block_categories.BLOCK_TO_ID[name] for name in block_categories.WOOD_BLOCKS)
    | set(block_categories.BLOCK_TO_ID[name] for name in block_categories.LEAF_BLOCKS)
    | set(block_categories.BLOCK_TO_ID[name] for name in block_categories.LIQUID_BLOCKS)
)

start_time = time.perf_counter()
regions_to_process = parser.discover_regions()

#Main function
for region_x, region_z, filename in regions_to_process:
    biomes = []
    height = []
    region = anvil.Region.from_file(filename)
    for chunk_x in range(32):
        for chunk_z in range(32):
            offset, length = region.chunk_location(chunk_x, chunk_z)
            if offset == 0 and length == 0:
                skipped_unloaded += 1
                continue
            try:
                chunk = anvil.Chunk.from_region(region, chunk_x, chunk_z)
            except Exception:
                skipped_unloaded += 1
                continue
            block_ids_array = parser.get_chunk_block_ids(chunk)
            if block_ids_array is None:
                skipped_empty += 1
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
            biome_count = count_biomes_per_chunk(chunk)
            chunk_biome_counts.append((global_chunk_x, global_chunk_z, biome_count))
            height_results = rgh.height_sensor(block_ids_array, excluded_ids)
            height.append(height_results)
            chunk_world_y = 383 - height_results - 64
            chunk_avg_height.append(
                (global_chunk_x, global_chunk_z, float(np.mean(chunk_world_y)))
            )
    world_y = [383 - h - 64 for h in height]
    roughness = np.var(world_y)
    region_roughness[(region_x, region_z)] = roughness
    biome_results = entropy.calculate_ent(np.array(biomes))
    biome_diversity[(region_x, region_z)] = biome_results


xs = [x for x, z, v in chunk_entropy]
zs = [z for x, z, v in chunk_entropy]
x_bounds = (min(xs), max(xs))
z_bounds = (min(zs), max(zs))

#Build Grids
chunk_roughness_grid, _, _ = aggregate.build_grid(chunk_avg_height, x_bounds, z_bounds)
solid_grid, _, _ = aggregate.build_grid(solid, x_bounds, z_bounds)
liquid_grid, _, _ = aggregate.build_grid(liquid, x_bounds, z_bounds)
cave_grid, _, _ = aggregate.build_grid(cave, x_bounds, z_bounds)

customdata = np.stack([solid_grid, liquid_grid, cave_grid], axis=-1)

biome_count_grid, _, _ = aggregate.build_grid(chunk_biome_counts, x_bounds, z_bounds)
entropy_grid, x_coords, z_coords = aggregate.build_grid(chunk_entropy, x_bounds, z_bounds)
air_grid, _, _ = aggregate.build_grid(air, x_bounds, z_bounds)
roughness_grid, _, _ = aggregate.expand_region_results_to_chunks(region_roughness, x_bounds, z_bounds)
biome_grid, _, _ = aggregate.expand_region_results_to_chunks(biome_diversity, x_bounds, z_bounds)

#CFG
layer_configs = {
    'Air %': {
        'customdata': customdata,
        'hovertemplate': (
            'Chunk (%{x}, %{y})<br>'
            'Air: %{z:.1f}%<br>'
            'Solid: %{customdata[0]:.1f}%<br>'
            'Liquid (count): %{customdata[1]:.0f}<br>'
            'Cave Air (count): %{customdata[2]:.0f}<extra></extra>'
        )
    },
    'Average Height': {
        'customdata': roughness_grid,
        'hovertemplate': (
            'Chunk (%{x}, %{y})<br>'
            'Avg Height: %{z:.1f}<br>'
            'Region Variance: %{customdata:.1f}<extra></extra>'
        )
    },
    'Biome Count': {
        'customdata': biome_grid,
        'hovertemplate': (
            'Chunk (%{x}, %{y})<br>'
            'Distinct Biomes: %{z}<br>'
            'Region Entropy: %{customdata:.2f}<extra></extra>'
        )
    }
}
#Skipped chunk warning
total_skipped = skipped_unloaded + skipped_empty
if total_skipped > 0:
    print("\n--- WARNING ---")
    print(f"Skipped {total_skipped} chunks that contained no usable data.")
    print(f"  - {skipped_unloaded} chunks were completely unloaded (missing from region file).")
    print(f"  - {skipped_empty} chunks were effectively empty (bedrock only).")
    print("These chunks will appear as blank (NaN) spaces in the heatmap.\n")
else:
    print("\nAll chunks in the selected regions were fully loaded and processed.")

#Render Heatmap
visualise.render_multi_metric_heatmap({
    'Entropy': entropy_grid,
    'Air %': air_grid,
    'Average Height': chunk_roughness_grid,
    'Biome Count': biome_count_grid,
}, x_coords, z_coords, layer_configs=layer_configs)
end_time = time.perf_counter()
elapsed = round(end_time - start_time, 2)
print(elapsed)