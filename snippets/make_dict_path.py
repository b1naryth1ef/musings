def create_path(obj, parts, value):
    """
    Creates a full path based on a dictionary, a list of recursive keys, and a final value
    """
    if len(parts) == 1:
        obj[parts[0]] = value
        return obj
    else:
        key, parts = parts[0], parts[1:]
        obj[key] = create_path({} if not key in obj else obj[key], parts, value)
        return obj

