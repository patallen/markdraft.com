import time
import math


def timestamp(dt):
    stamp = time.mktime((
        dt.year, dt.month, dt.day, dt.hour,
        dt.minute, dt.second, -1, -1, -1)
    ) + dt.microsecond / 1e6
    return int(math.floor(stamp))
