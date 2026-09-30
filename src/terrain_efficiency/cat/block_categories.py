STONE_BLOCKS = [
    'stone',
    'granite',
    'polished_granite',
    'diorite',
    'polished_diorite',
    'andesite',
    'polished_andesite',
    'cobblestone',
    'mossy_cobblestone',
    'stone_bricks',
    'mossy_stone_bricks',
    'cracked_stone_bricks',
    'chiseled_stone_bricks',
    'smooth_stone',
    'sandstone',
    'chiseled_sandstone',
    'cut_sandstone',
    'smooth_sandstone',
    'red_sandstone',
    'chiseled_red_sandstone',
    'cut_red_sandstone',
    'smooth_red_sandstone',
    'deepslate',
    'cobbled_deepslate',
    'polished_deepslate',
    'deepslate_bricks',
    'cracked_deepslate_bricks',
    'deepslate_tiles',
    'cracked_deepslate_tiles',
    'chiseled_deepslate',
    'tuff',
    'tuff_bricks',
    'chiseled_tuff',
    'chiseled_tuff_bricks',
    'calcite',
    'dripstone_block',
    'pointed_dripstone',
    'polished_basalt',
    'smooth_basalt',
    'obsidian',
    'crying_obsidian',
    'netherrack',
    'prismarine',
    'prismarine_bricks',
    'dark_prismarine',
    'bedrock',
    'magma_block',
    'amethyst_block',
    'budding_amethyst',
    'packed_ice',
    'blue_ice',
    'ice',
]
 
# ---------------------------------------------------------------------------
# WOOD — logs, stems, and full "wood" blocks (bark on all sides), both
# stripped and unstripped. Does NOT include planks — kept separate per your
# structure-prediction use case.
# ---------------------------------------------------------------------------
WOOD_BLOCKS = [
    'oak_log',
    'spruce_log',
    'birch_log',
    'jungle_log',
    'acacia_log',
    'dark_oak_log',
    'mangrove_log',
    'cherry_log',
    'stripped_oak_log',
    'stripped_spruce_log',
    'stripped_birch_log',
    'stripped_jungle_log',
    'stripped_acacia_log',
    'stripped_dark_oak_log',
    'stripped_mangrove_log',
    'stripped_cherry_log',
    'oak_wood',
    'spruce_wood',
    'birch_wood',
    'jungle_wood',
    'acacia_wood',
    'dark_oak_wood',
    'mangrove_wood',
    'cherry_wood',
    'stripped_oak_wood',
    'stripped_spruce_wood',
    'stripped_birch_wood',
    'stripped_jungle_wood',
    'stripped_acacia_wood',
    'stripped_dark_oak_wood',
    'stripped_mangrove_wood',
    'stripped_cherry_wood',
    'bamboo_block',
    'stripped_bamboo_block',
    'mangrove_roots',
]
 
# ---------------------------------------------------------------------------
# PLANKS — kept separate from WOOD specifically to help flag structures
# (villages, ruins, etc.) based on y-level and surrounding block context.
# ---------------------------------------------------------------------------
PLANKS_BLOCKS = [
    'oak_planks',
    'spruce_planks',
    'birch_planks',
    'jungle_planks',
    'acacia_planks',
    'dark_oak_planks',
    'mangrove_planks',
    'cherry_planks',
    'bamboo_planks',
    'bamboo_mosaic',
]
 
# ---------------------------------------------------------------------------
# ORGANIC — surface/soil blocks and non-woody plant life (flowers, grass,
# crops, aquatic plants). Leaves are broken out separately below.
# ---------------------------------------------------------------------------
ORGANIC_BLOCKS = [
    'dirt',
    'grass_block',
    'podzol',
    'coarse_dirt',
    'mycelium',
    'rooted_dirt',
    'snow_block',
    'mud',
    'muddy_mangrove_roots',
    'farmland',
    'dirt_path',
    'sand',
    'red_sand',
    'gravel',
    'clay',
    'moss_block',
    'moss_carpet',
    'pitcher_crop',
    'grass',
    'short_grass',
    'tall_grass',
    'fern',
    'large_fern',
    'dead_bush',
    'seagrass',
    'tall_seagrass',
    'kelp',
    'kelp_plant',
    'lily_pad',
    'vine',
    'glow_lichen',
    'sculk',
    'sculk_vein',
    'sculk_catalyst',
    'sculk_sensor',
    'sculk_shrieker',
    'big_dripleaf',
    'big_dripleaf_stem',
    'small_dripleaf',
    'spore_blossom',
    'hanging_roots',
    'red_mushroom',
    'brown_mushroom',
    'sugar_cane',
    'bamboo',
    'bamboo_sapling',
    'cactus',
    'melon',
    'pumpkin',
    'carved_pumpkin',
    'cocoa',
    'sweet_berry_bush',
    'cave_vines',
    'cave_vines_plant',
    'frogspawn',
    'wheat',
    'carrots',
    'potatoes',
    'beetroots',
    'snow',
    'powder_snow',
]
 
# ---------------------------------------------------------------------------
# LEAF — all leaf types (natural + azalea variants).
# ---------------------------------------------------------------------------
LEAF_BLOCKS = [
    'oak_leaves',
    'spruce_leaves',
    'birch_leaves',
    'jungle_leaves',
    'acacia_leaves',
    'dark_oak_leaves',
    'mangrove_leaves',
    'cherry_leaves',
    'azalea_leaves',
    'flowering_azalea_leaves',
    'azalea',
    'flowering_azalea',
]
 
# ---------------------------------------------------------------------------
# ORE — all ore variants including deepslate forms.
# ---------------------------------------------------------------------------
ORE_BLOCKS = [
    'coal_ore',
    'deepslate_coal_ore',
    'iron_ore',
    'deepslate_iron_ore',
    'copper_ore',
    'deepslate_copper_ore',
    'gold_ore',
    'deepslate_gold_ore',
    'redstone_ore',
    'deepslate_redstone_ore',
    'emerald_ore',
    'deepslate_emerald_ore',
    'lapis_ore',
    'deepslate_lapis_ore',
    'diamond_ore',
    'deepslate_diamond_ore',
]
 
# ---------------------------------------------------------------------------
# AIR — the three air variants, broken out as their own category.
# ---------------------------------------------------------------------------
AIR_BLOCKS = [
    'air',
    'cave_air',
    'void_air',
]
 
# ---------------------------------------------------------------------------
# MISC — structure-associated blocks that generate naturally (spawners,
# chests in generated structures) and other terrain-adjacent blocks that
# don't fit above. Light-source blocks (torches, lanterns, campfires, fire)
# are intentionally excluded — left out entirely, not just uncategorised.
# Liquids are intentionally NOT included here either — see LIQUID_BLOCKS
# below, which are catalogued but deliberately left uncategorised.
# ---------------------------------------------------------------------------
MISC_BLOCKS = [
    'sea_lantern',
    'honey_block',
    'honeycomb_block',
    'slime_block',
    'cobweb',
    'bone_block',
    'spawner',
    'chest',
    'barrel',
    'end_portal_frame',
    
]
 
# ---------------------------------------------------------------------------
# LIQUIDS — catalogued (so they get a valid int ID and don't fall through to
# UNKNOWN_ID) but deliberately left OUT of the category system. Not included
# in _ALL_CATEGORIES below, and CATEGORY_OF_ID maps these to None.
# ---------------------------------------------------------------------------
LIQUID_BLOCKS = [
    'water',
    'lava',
    'bubble_column',
]
 
# ---------------------------------------------------------------------------
# UNCATEGORISED — catalogued (valid int ID) but not assigned to any of the
# categories above. Raw ore blocks are crafted-only (don't naturally
# generate in world-gen), so they're kept here rather than under ORE.
# ---------------------------------------------------------------------------
UNCATEGORISED_BLOCKS = [
    'raw_iron_block',
    'raw_copper_block',
    'raw_gold_block',
]
 
# ---------------------------------------------------------------------------
# Build the actual lookup structures once, at import time.
# ---------------------------------------------------------------------------
_ALL_CATEGORIES = {
    'stone': STONE_BLOCKS,
    'wood': WOOD_BLOCKS,
    'planks': PLANKS_BLOCKS,
    'organic': ORGANIC_BLOCKS,
    'leaf': LEAF_BLOCKS,
    'ore': ORE_BLOCKS,
    'air': AIR_BLOCKS,
    'misc': MISC_BLOCKS,
}
 
BLOCK_TO_ID = {}
ID_TO_BLOCK = {}
CATEGORY_OF_ID = {}
 
_next_id = 0
for _category, _blocks in _ALL_CATEGORIES.items():
    for _block_name in _blocks:
        if _block_name in BLOCK_TO_ID:
            raise ValueError(
                f"Duplicate block '{_block_name}' found in multiple categories "
                f"(already in category '{CATEGORY_OF_ID[BLOCK_TO_ID[_block_name]]}', "
                f"also listed in '{_category}')"
            )
        BLOCK_TO_ID[_block_name] = _next_id
        ID_TO_BLOCK[_next_id] = _block_name
        CATEGORY_OF_ID[_next_id] = _category
        _next_id += 1
 
# Liquids and other explicitly uncategorised blocks get valid int IDs like
# everything else, but are deliberately left out of the category system —
# CATEGORY_OF_ID is None for these.
_UNCATEGORISED_ALL = LIQUID_BLOCKS + UNCATEGORISED_BLOCKS
for _block_name in _UNCATEGORISED_ALL:
    if _block_name in BLOCK_TO_ID:
        raise ValueError(f"Duplicate block '{_block_name}' also listed as uncategorised")
    BLOCK_TO_ID[_block_name] = _next_id
    ID_TO_BLOCK[_next_id] = _block_name
    CATEGORY_OF_ID[_next_id] = None
    _next_id += 1
 
AIR_ID = BLOCK_TO_ID['air']
CAVE_AIR_ID = BLOCK_TO_ID['cave_air']
VOID_AIR_ID = BLOCK_TO_ID['void_air']
AIR_IDS = {AIR_ID, CAVE_AIR_ID, VOID_AIR_ID}
 
WATER_ID = BLOCK_TO_ID['water']
LAVA_ID = BLOCK_TO_ID['lava']
LIQUID_IDS = {BLOCK_TO_ID[name] for name in LIQUID_BLOCKS}
 
# Fallback ID for any block name encountered that isn't in the table above.
# Add the block to the appropriate category list rather than relying on this
# in normal operation — this exists mainly to avoid crashing on structure
# blocks (villages, ruins, etc.) not yet catalogued.
UNKNOWN_ID = _next_id
ID_TO_BLOCK[UNKNOWN_ID] = 'unknown'
CATEGORY_OF_ID[UNKNOWN_ID] = None
 
 
def get_id(block_name: str) -> int:
    """Look up a block name's int ID, falling back to UNKNOWN_ID if not catalogued."""
    return BLOCK_TO_ID.get(block_name, UNKNOWN_ID)
 
 
if __name__ == '__main__':
    print(f"Total catalogued blocks: {_next_id}")
    for cat, blocks in _ALL_CATEGORIES.items():
        print(f"  {cat}: {len(blocks)} blocks")
    print(f"  (uncategorised — liquids + raw ore blocks): {len(_UNCATEGORISED_ALL)} blocks")