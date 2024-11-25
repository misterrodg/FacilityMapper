def print_top_level(data):
    return {
        key: (
            "[...]"
            if isinstance(value, list)
            else "{...}" if isinstance(value, dict) else value
        )
        for key, value in data.items()
    }
