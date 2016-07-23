from datestuff import DateRange
from datetime import date, datetime, timedelta
import pytest


def test_complains_if_start_not_provided():
    with pytest.raises(TypeError):
        DateRange(start=None, stop=datetime(2016, 1, 1), step=timedelta(days=1))


def test_complains_if_step_not_provided():
    with pytest.raises(TypeError):
        DateRange(start=datetime(2016, 1, 1), stop=None, step=None)


def test_complains_if_step_is_zero():
    with pytest.raises(TypeError):
        DateRange(start=date(2016, 1, 1), step=timedelta(0))


def test_properly_calculates_length():
    dr = DateRange(start=date(2016, 1, 1), stop=date(2016, 1, 6), step=timedelta(days=1))

    assert len(dr) == 5


def test_raises_error_if_infinite_length():
    dr = DateRange(start=date(2016, 1, 1), step=timedelta(days=1))

    with pytest.raises(TypeError):
        len(dr)


@pytest.mark.parametrize('when', [
    date(2016, 1, x) for x in range(1, 31, 2)
])
def test_properly_reports_a_contained_date(when):
    dr = DateRange(start=date(2016, 1, 1), stop=date(2016, 1, 31), step=timedelta(days=2))

    assert when in dr


def test_does_not_contain_end():
    dr = DateRange(date(2016, 1, 1), date(2016, 1, 31), timedelta(days=2))
    assert date(2016, 1, 31) not in dr
    assert date(2016, 1, 31) == dr.stop


@pytest.mark.parametrize('when', [
    datetime(2016, 1, 1, x) for x in range(23)
])
def test_properly_reports_a_contained_datetime(when):
    dr = DateRange(
        start=datetime(2016, 1, 1, 0, 0, 0),
        stop=datetime(2016, 1, 1, 23, 0, 0),
        step=timedelta(minutes=60)
    )

    assert when in dr


def test_reports_contains_a_precise_datetime():
    dr = DateRange(
        start=datetime(2000, 4, 25, 18, 30),
        step=timedelta(minutes=57)
    )

    assert datetime(2000, 4, 29, 7, 3) in dr


@pytest.mark.parametrize('when', [
    datetime(2000, 1, 1, x) for x in range(1, 23)
])
def test_reports_contains_with_negative_step(when):
    dr = DateRange(
        start=datetime(2000, 1, 1, 23),
        stop=datetime(2000, 1, 1),
        step=timedelta(minutes=-60)
    )
    assert when in dr


def test_iterates_properly():
    dr = DateRange(start=date(2016, 1, 1), stop=date(2016, 1, 31), step=timedelta(days=1))

    assert list(dr) == [date(2016, 1, x) for x in range(1, 31)]


def test_reverses_properly():
    dr = DateRange(
        start=datetime(2016, 1, 1),
        stop=datetime(2016, 1, 1, 23),
        step=timedelta(minutes=60)
    )

    assert list(reversed(dr)) == [datetime(2016, 1, 1, x) for x in range(23, 0, -1)]


def test_empty_if_start_is_higher_than_stop_without_negative_step():
    assert [] == list(DateRange(
        start=date(2016, 1, 31),
        stop=date(2016, 1, 1),
        step=timedelta(days=1)
    ))
