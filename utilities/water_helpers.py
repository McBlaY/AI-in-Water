"""Dummy helper functions for notebook examples."""


def summarize_flow(flow_values):
    """Return a simple summary for a list of flow values."""
    import statistics

    return {
        "count": len(flow_values),
        "mean": round(statistics.mean(flow_values), 3),
        "min": min(flow_values),
        "max": max(flow_values),
    }


def classify_quality(ph_value):
    """Return a dummy water-quality label."""
    if ph_value < 6.5:
        return "acidic"
    if ph_value > 8.5:
        return "alkaline"
    return "balanced"


def estimate_demand(population, per_capita_use):
    """Return a simple demand estimate in liters/day."""
    return population * per_capita_use
