# Efficient Minecraft Terrain Analysis Tool

A performance-focused analysis of Minecraft world generation, built to measure the *structural efficiency* of terrain — how diverse, varied, and "interesting" different parts of a generated world actually are — and to explore how far raw Python can be optimised when processing real binary game data at scale.

The project has two goals, roughly equal in weight:
1. Quantify terrain properties (block-type diversity, air/solid/liquid composition, surface roughness, biome diversity) across a real Minecraft world.
2. Demonstrate a measured, honest optimisation journey — naive Python → vectorised NumPy — with real timing data, not just a claim that "it's faster now."

## Data

- **Minecraft version:** 1.21.1
- **World data:** Overworld only (the `region/` folder — no Nether or End data used)
- **Sample area:** a square 32-chunk radius centred on the world's spawn point, full height range (bedrock, Y=-64, to build limit, Y=319)
- **Format:** raw `.mca` region files, parsed directly rather than through an in-game export

Raw world data is **not included in this repository** (see `.gitignore`) — Minecraft world saves aren't licensed for redistribution, and the files are large enough that GitHub rejects them outright. Only derived, computed results (grids, aggregated metrics) are committed. To regenerate results from scratch, supply your own world save's region files in `data/raw/`.

## Metrics

| Metric | Granularity | What it measures |
|---|---|---|
| Chunk entropy | Per chunk | Shannon entropy (base 2) of block-type distribution across the full chunk column |
| Air / solid / liquid ratio | Per chunk | Percentage breakdown of a chunk's volume by category, plus a cave-air count as a secondary "cave score" |
| Roughness | Per region (with per-chunk colour layer) | Variance of surface height — how much terrain elevation varies |
| Biome diversity | Per region | Shannon entropy of biome distribution across a region's chunks |

**Why the mixed granularity:** entropy and air ratio are computed independently per chunk, since each chunk's full block data is read anyway. Roughness and biome diversity are computed at the region level (32×32 chunks) — chunk-level roughness turned out too data-sparse to be meaningful on its own, and biome diversity requires comparing *many* chunks against each other to produce a real distribution. Both are also displayed with a per-chunk colour layer (average column height for roughness, a multi-point-sampled entropy value for biome) so the heatmap isn't visually flat, while the true region-scale number is preserved as hover-only context.

## Block classification

Every block encountered is mapped to an integer ID and sorted into one of seven categories: `stone`, `wood`, `planks`, `organic`, `leaf`, `ore`, `air`. Liquids and raw ore blocks (which don't naturally generate — they're crafting-only) are catalogued with valid IDs but deliberately left uncategorised. Light-emitting blocks (torches, lanterns, campfires) are excluded from the table entirely, since they're not part of terrain generation.

**A meaningful chunk of the classification work went into confirming which blocks can *actually* generate in the Overworld** — several blocks that seem Overworld-plausible turned out to be Nether-exclusive on inspection: quartz variants (which only generate inside bastion remnants), the entire crimson/warped wood family and Nether-flora (nether wart, weeping/twisting vines — all exclusive to the Nether's crimson/warped forest biomes), and most of the basalt/blackstone family. A few blocks that sound Nether-associated but do genuinely occur in the Overworld were kept: `netherrack` and `crying_obsidian` (both generate as part of ruined portal structures, which spawn in both dimensions), `magma_block` (generates naturally on Overworld ocean floors), and `polished_granite`/`polished_andesite`/`polished_diorite` (confirmed to generate in ocean ruins, igloo basements, and woodland mansions).

## Optimization

The core performance story: reading Minecraft's chunk data block-by-block via the parsing library's `get_block()` interface is extremely slow — each call resolves NBT structure and palette lookups individually. The optimised path instead reads each chunk **section's** raw palette and bit-packed index array directly, converts the whole section to integer IDs in one vectorised NumPy operation, and assembles a full chunk from its ~24 sections in one pass.

### Benchmarks

All final benchmarks were run with the laptop unplugged (power-saving mode) for consistency, since plugged-in vs. unplugged CPU clock speed was found to meaningfully affect timing during development.

| Metric | Basic (naive) | Vectorized | Scope | Speedup |
|---|---|---|---|---|
| Roughness | 989.5s | 64.45s | 9 regions | ~140x* |
| Biome diversity | 17.5s | 13.24s | 9 regions | — |
| Chunk entropy | 1.95s | — | 1 region | — |
| Air ratio | 2.23s | — | 1 region | — |

*Basic roughness was only benchmarked on a single region (989.5s); scaled linearly across all 9 regions, the naive approach would take roughly **2.5 hours**. The vectorised version completes the full 9-region sample in about a minute — the comparison above uses that scaled estimate.

Roughness was consistently the slowest basic-version metric by a wide margin (roughly 450-500x slower than the other three), because it requires scanning down each of a chunk's 256 columns individually rather than a single pass over the whole block array — making it the clear first target for optimisation.

## Notable findings

- **Region (0, -1)** showed dramatically lower roughness (variance ≈ 376) than every other region in the sample — over 40x flatter than the next-lowest region — consistent with a large, uniform ocean floor near spawn.
- **Regions (-1, -2) and (0, -2)** were the most varied by roughness (variance ≈ 17,655 and 15,081 respectively), suggesting genuinely mountainous or cliff-heavy terrain.
- **Whole-column entropy is dominated by bulk terrain composition.** Because entropy is computed across the entire bedrock-to-build-limit column, and any chunk's volume is overwhelmingly air, stone, and deepslate (one sampled chunk was 98.1% just those three block types), entropy values cluster into a fairly narrow band across most chunks regardless of how much genuinely interesting detail (ore veins, caves, biome-specific surface blocks) is present. This is an honest limitation of the metric as scoped, not a bug — smaller-scale features contribute comparatively little to a whole-column entropy score.

## Tech stack

- **Python** — `anvil-parser2` (chunk/region parsing), `numpy` (vectorised computation), `plotly` (interactive heatmap visualisation)
- Custom NBT palette/bit-unpacking logic for direct section-level reads, bypassing the parsing library's slower per-block interface

## Status

Core metrics, block classification, and the basic-vs-vectorised benchmarking are complete for roughness and biome diversity. Chunk entropy and air ratio have working vectorised implementations but are not yet benchmark-logged at full-sample scale. The interactive multi-metric heatmap renders with a working dropdown between metrics; per-chunk colour layers for roughness and biome diversity (replacing the flat per-region blocks) are in progress. Parallelisation across chunks/regions, as a further optimisation stage, has not yet been implemented.
