""" estimate time and express in proper format.  """


def get_time(n: int, factor1: float = 1.0, factor2: float = 2.0) -> str:
    """ estimate time and express in proper format.  """

    time1 = n * factor1
    time2 = n * factor2

    unit = "sec."
    if time1 > 86400:
        time1 = time1 / 86400.0
        time2 = time2 / 86400.0
        if time2 > 1.0:
            unit = "days"
        else:
            unit = "day"
    elif time1 > 3600:
        time1 = time1 / 3600.0
        time2 = time2 / 3600.0
        unit = "hr."
    elif time1 > 60:
        time1 = time1 / 60.0
        time2 = time2 / 60.0
        unit = "min."

    if time2 == time1:
        time2 += 1.0

    return f"{time1:.1f}-{time2:.1f} ({unit})"
