async def is_positive_int(val):
    try:
        int(val)
    except ValueError:
        return False
    else:
        return int(val) > 0
