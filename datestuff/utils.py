def within_delta(dt1, dt2, delta):
    """
    Useful for comparing two datetimes that may a negilible difference
    to be considered equal.
    """
    difference = dt1 - dt2
    return -delta <= difference <= delta
