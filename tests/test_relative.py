from datestuff import RelativeDate
from datetime import timedelta, date, datetime
from dateutil.relativedelta import relativedelta
import operator
import pytest


YESTERDAY = date.today() - timedelta(days=1)
TOMORROW = date.today() + timedelta(days=1)


class TestRelativeDate(object):
    def test_relative_at_interaction(self):
        offset = timedelta(days=4)
        subject = RelativeDate(offset=offset)

        assert subject == (date.today() + offset)

    def test_relative_dates_compare_offsets(self):
        off_by_one = RelativeDate(timedelta(days=1))

        assert off_by_one == off_by_one
        assert off_by_one != RelativeDate(timedelta(0))

    def test_adding_two_relative_dates_adds_offsets(self):
        off_by_one = RelativeDate(offset=timedelta(days=1))
        off_by_two = RelativeDate(offset=timedelta(days=2))

        assert off_by_one + off_by_two == RelativeDate(timedelta(days=3))

    def test_adding_timedelta_adds_to_offset(self):
        off_by_one = RelativeDate(timedelta(days=1))

        off_by_three = RelativeDate(timedelta(days=3))
        assert off_by_one + timedelta(days=2) == off_by_three
        assert timedelta(days=2) + off_by_one == off_by_three

    @pytest.mark.parametrize('target,op', [
        (YESTERDAY, operator.gt),
        (YESTERDAY, operator.ge),
        (RelativeDate(timedelta(days=-1)), operator.gt),
        (RelativeDate(timedelta(days=-1)), operator.ge),
        (TOMORROW, operator.le),
        (TOMORROW, operator.lt),
        (RelativeDate(timedelta(days=1)), operator.le),
        (RelativeDate(timedelta(days=1)), operator.lt),
        (RelativeDate(timedelta(days=2)), operator.ne)
    ])
    def test_relative_date_rich_comparisons(self, target, op):
        subject = RelativeDate(clock=date.today)

        assert op(subject, target)

    def test_subtracting_timedelta_from_relative_date_changes_offset(self):
        subject = RelativeDate(offset=timedelta(days=1))

        assert subject - timedelta(days=1) == RelativeDate()
        assert timedelta(days=1) - subject == RelativeDate()

    def test_subtracting_relative_date_from_relative_data_changes_offset(self):
        off_by_one = RelativeDate(timedelta(days=1))

        assert off_by_one - off_by_one == RelativeDate()

    def test_subtracting_date_from_relative_date_gives_timedelta(self):
        off_by_one = RelativeDate(offset=timedelta(days=1))

        assert off_by_one - date.today() == timedelta(days=1)
        assert date.today() - off_by_one == timedelta(days=1)

    def test_proxy_formatting_call_to_underlying_date(self):
        pattern = "{0:%Y-%m-%d}"

        assert pattern.format(RelativeDate()) == pattern.format(date.today())

    def test_textual_representations(self):
        target = date(2016, 3, 8)
        subject = RelativeDate(clock=lambda: target)

        assert str(subject) == str(target)

    def test_proxy_boolness(self):
        assert bool(RelativeDate()) == bool(date.today())

    def test_proxy_attr_access_to_underlying_date(self):
        subject = RelativeDate(clock=lambda: date(2016, 3, 8))
        target = date(2016, 3, 8)

        assert subject.year == target.year
        assert subject.day == target.day
        assert subject.month == target.month

    def test_fromordinal(self):
        rd = RelativeDate.fromordinal(730920, offset=timedelta(days=5))

        assert rd == date.fromordinal(730925)

    def test_today(self):
        rd = RelativeDate.today(offset=timedelta(days=5))

        assert rd == date.today() + timedelta(days=5)


class TestRelativeDeltaInterop(object):
    def test_relative_delta_with_relative_date(self):
        rd = RelativeDate(clock=lambda: datetime(2000, 1, 1), offset=relativedelta(years=16))

        assert rd == datetime(2016, 1, 1)

    def test_add_relative_delta_instances(self):
        rd = RelativeDate(clock=lambda: date(2016, 1, 1), offset=relativedelta(days=1))

        assert rd + rd == RelativeDate(offset=relativedelta(days=2))

    def test_sub_relative_delta_instances(self):
        rd = RelativeDate(clock=lambda: date(2016, 1, 1), offset=relativedelta(days=1))

        assert rd - rd == RelativeDate(offset=relativedelta())
