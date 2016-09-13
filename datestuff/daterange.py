from __future__ import division
from math import ceil
from datetime import timedelta

__all__ = ('DateRange',)


class DateRange(object):
    """
    Creates a lazy range of date or datetimes. Modeled after the Python 3 range type and has
    fast path membership checking, lazy iteration, indexing and slicing. Unlike range, DateRange
    allows an open ended range. Also unlike range, it does not have an implicit step so it must be
    provided.
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
        if self.stop:
            return DateRange(self.stop, self.start, -self.step)

        raise ValueError("Cannot reverse infinite range")

    def __len__(self):
        if self.stop is None:
            # it'd be nice if float('inf') could be returned
            raise TypeError("infinite range")

        if self._has_neg_step:
            calc = self.start - self.stop
        else:
            calc = self.stop - self.start

        return int(ceil(abs(calc.total_seconds() / self.step.total_seconds())))

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

    def __eq__(self, other):
        if isinstance(other, DateRange):
            return (
                self.start == other.start and
                self.stop == other.stop and
                self.step == other.step
            )
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, DateRange):
            return not self == other
        return NotImplemented

    def __getitem__(self, idx_or_slice):
        if isinstance(idx_or_slice, int):
            return self._getidx(idx_or_slice)
        elif isinstance(idx_or_slice, slice):
            return self._getslice(idx_or_slice)

        raise TypeError("DateRange indices must be integers or slices, not {}".format(idx_or_slice.__class__))  # noqa

    def _getidx(self, idx):
        if not self.stop and 0 > idx:
            raise IndexError("Cannot negative index infinite range")

        if self.stop and abs(idx) > len(self) - 1:
            raise IndexError("DateRange index out of range")

        if idx == 0:
            return self.start
        elif 0 > idx:
            idx += len(self)

        return self.start + (self.step * idx)

    def _getslice(self, slice):
        s = slice.start, slice.stop, slice.step

        if s == (None, None, None) or s == (None, None, 1):
            return DateRange(
                start=self.start,
                stop=self.stop,
                step=self.step
            )

        start, stop, step = s

        # seems redundant but we're converting None -> 0
        start = start or 0
        stop = stop or 0

        # use 1 here because of multiplication
        step = step or 1

        if not self.stop and (0 > start or 0 > stop):
            raise IndexError("Cannot negative index infinite range")

        new_step = self.step * step

        if not start:
            new_start = self.start
        else:
            new_start = self[start]

        if not stop:
            new_stop = self.stop
        else:
            new_stop = self[stop]

        return DateRange(
            start=new_start,
            stop=new_stop,
            step=new_step
        )
