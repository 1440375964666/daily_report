def calculate_threshold(series):
    """Calculate the midpoint of the rebased series range."""
    sorted_series = series.sort_values(ascending=True)
    min_val = sorted_series.min()
    max_val = sorted_series.max()
    mean_val = (min_val + max_val) / 2
    return min_val, max_val, mean_val

def percentage_position(latest_zscore, min_val, max_val):
    """Calculate percentage position of latest_zscore relative to rebased"""
    per_pos = (latest_zscore - min_val) / (max_val - min_val) * 100
    return per_pos