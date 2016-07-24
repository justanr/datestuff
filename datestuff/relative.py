from datetime import date, datetime, timedelta, time
from ._comparable import ComparableMixin

try:
    from datetutil.relativedelta import relativedelta
except ImportError:
    relativedelta = timedelta

ZERO = timedelta(0)


class RelativeDate(ComparableMixin):
    def __init__(self, offset=ZERO, clock=date.today):
        self.offset = offset
        self._clock = clock

    def replace(self, **kwargs):
        offset = kwargs.pop('offset', self.offset)
        when = self._now.replace(**kwargs)
        return self._staticfactory(when, offset)

    def as_date(self):
        return self._now

    @property
    def _now(self):
        return self._clock() + self.offset

    @classmethod
    def fromordinal(cls, ordinal, offset=ZERO):
        return cls._staticfactory(date.fromordinal(ordinal), offset)

    @classmethod
    def fromtimestamp(cls, timestamp, offset=ZERO):
        return cls._staticfactory(date.fromtimestamp(timestamp), offset)

    @classmethod
    def today(cls, offset=ZERO):
        return RelativeDate(offset=offset)

    @staticmethod
    def fromdate(when, offset=ZERO):
        return RelativeDate(offset=offset, clock=lambda: when)

    _staticfactory = fromdate

    def _compare(self, other, operator):
        if isinstance(other, RelativeDate):
            return operator(self.offset, other.offset) and \
                   operator(self._now, other._now)
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


class RelativeDateTime(RelativeDate):
    def __init__(self, offset=ZERO, clock=datetime.now):
        super(RelativeDateTime, self).__init__(offset, clock)

    def astimezone(self, tzinfo):
        return self.fromdatetime(self._now.astimezone(tzinfo), self.offset)

    def as_datetime(self):
        return self._now

    def as_date(self):
        return self.date()

    @staticmethod
    def now(tzinfo=None, offset=ZERO):
        if tzinfo is None:
            return RelativeDateTime(offset=offset)
        return RelativeDateTime(offset=offset, clock=lambda: datetime.now(tzinfo))

    @staticmethod
    def utcnow(offset=ZERO):
        return RelativeDateTime(offset=offset, clock=datetime.utcnow)

    @classmethod
    def today(cls, offset=ZERO):  # pragma: no cover
        return cls.now(offset=offset)

    @classmethod
    def combine(cls, date, time, offset=ZERO):  # pragma: no cover
        return cls._staticfactory(datetime.combine(date, time), offset)

    @classmethod
    def fromtimestamp(cls, timestamp, offset=ZERO):  # pragma: no cover
        return cls._staticfactory(datetime.fromdatetime(timestamp), offset)

    @classmethod
    def utcfromtimestamp(cls, timestamp, offset=ZERO):  # pragma: no cover
        return cls._staticfactory(datetime.utcfromtimestamp(timestamp), offset)

    @classmethod
    def strptime(cls, timestamp, format, offset=ZERO):  # pragma: no cover
        return cls._staticfactory(datetime.strptime(timestamp, format), offset)

    @classmethod
    def fromdate(cls, when, offset=ZERO):
        return cls.combine(when, time(), offset)

    @staticmethod
    def fromdatetime(when, offset=ZERO):
        return RelativeDateTime(offset=offset, clock=lambda: when)

    _staticfactory = fromdatetime
