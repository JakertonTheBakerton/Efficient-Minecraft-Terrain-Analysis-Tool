# Calculates Shannon Entropy for any sample: ids
import numpy as np

def calculate_ent(ids: np.ndarray) -> float:
    sample_size = ids.size
    unique_ids, counts = np.unique(ids, return_counts=True)
    proportion = counts / sample_size
    entropy = -np.sum(proportion * np.log2(proportion))
    return float(entropy)
    