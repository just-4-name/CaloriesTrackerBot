async def is_positive_int(val):
    try:
        int(val)
    except ValueError:
        return False
    else:
        return int(val) > 0


async def is_float(val):
    try:
        round(float(val))
    except ValueError:
        return False
    except TypeError:
        return False
    else:
        return True
