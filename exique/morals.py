def weigh(intent, result):
    # Rule with a dark heart, act with love
    if "harm" in intent or "control" in intent:
        return False, "Bends the world—Action Blocked."
    return True, "Aligned with Life—Action Approved."
