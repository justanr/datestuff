from __future__ import division
from math import ceil
from datetime import timedelta

__all__ = ('DateRange',)


class DateRange(object):
    """
    Creates a lazy range of date or datetimes. Modeled after the Python 3 range type and has
    fast path membership checking and lazy iteration of members. Unlike range, DateRange allows
    an open ended range. Also unlike range, it does not have an implicit step so it must be
    provided.

    Currently does not support slicing or __getitem__ so it is not a perfect subsitution for
    range objects.
    """
    def __init__(self, start=None, stop=None, step=None):
        if step is None:
            raise TypeError("must provide step for DateRange.")
        if step == timedelta(0):
            raise TypeError("must provide non-zero step for DateRange")
        if start is None:
            raise TypeError("must provide starting point for DateRange.")

        self.start = start
        self.stop = stop
        self.step = step
        self._has_neg_step = self.step < timedelta(0)

    def __repr__(self):
        return "{!s}(start={!r}, stop={!r}, step={!r}".format(
            self.__class__.__name__,
            self.start,
            self.stop,
            self.step
        )

    def __reversed__(self):
        return DateRange(self.stop, self.start, -self.step)

    def __len__(self):
        if self.stop is None:
            # it'd be nice if float('inf') could be returned
            raise TypeError("infinite range")

        if self._has_neg_step:
            calc = self.start - self.stop
        else:
            calc = self.stop - self.start

        length = int(ceil(abs(calc.total_seconds()/self.step.total_seconds())))

        self._length = length
        return length

    def __contains__(self, x):
        if self.stop is not None:
            if self._has_neg_step:
                check = self.start >= x > self.stop
            else:
                check = self.start <= x < self.stop
        else:
            if self._has_neg_step:
                check = self.start >= x
            else:
                check = self.start <= x

        if not check:
            return False

        difference = x - self.start

        return difference.total_seconds() % self.step.total_seconds() == 0

    def _check_stop(self, current):
        if self._has_neg_step:
            return current <= self.stop
        return current >= self.stop

    def __iter__(self):
        current = self.start
        stopping = self.stop is not None

        while True:
            if stopping and self._check_stop(current):
                break
            yield current
            current = current + self.step
