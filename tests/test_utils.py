from datetime import timedelta, datetime
from datestuff.utils import within_delta


def test_within_delta():
    d1 = datetime(2016, 1, 1, 12, 14, 1, 9)
    d2 = d1.replace(microsecond=15)

    assert within_delta(d1, d2, timedelta(seconds=1))
    assert not within_delta(d1, d2, timedelta(microseconds=1))
