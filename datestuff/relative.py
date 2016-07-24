from datetime import date, timedelta
from ._comparable import ComparableMixin

try:
    from datetutil.relativedelta import relativedelta
except ImportError:
    relativedelta = timedelta


class RelativeDate(ComparableMixin):
    def __init__(self, offset=timedelta(), clock=date.today):
        self._offset = offset
        self._clock = clock

    @property
    def _now(self):
        return self._clock() + self._offset

    @property
    def offset(self):
        return self._offset

    def _compare(self, other, operator):
        if isinstance(other, RelativeDate):
            return operator(self.offset, other.offset)
        return operator(self._now, other)

    def __add__(self, other):
        if isinstance(other, RelativeDate):
            new_offset = self.offset + other.offset
            return self.__class__(new_offset, self._clock)
        elif isinstance(other, (timedelta, relativedelta)):
            return self.__class__(self.offset + other, self._clock)
        return self._now + other

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, (timedelta, relativedelta)):
            return self.__class__(self.offset - other, self._clock)
        elif isinstance(other, RelativeDate):
            new_offset = self.offset - other.offset
            return self.__class__(new_offset, self._clock)
        return self._now - other

    __rsub__ = __sub__

    def __getattr__(self, attr):
        return getattr(self._now, attr)

    def __format__(self, pattern):
        return format(self._now, pattern)

    def __str__(self):
        return str(self._now)

    def __bool__(self):
        return bool(self._now)

    __nonzero__ = __bool__

    def __repr__(self):
        return "<{} offset={!r} clock={!r}>".format(
            self.__class__.__name__,
            self.offset,
            self._clock
        )
