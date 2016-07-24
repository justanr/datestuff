from datetime import date, datetime, timedelta, time
from ._comparable import ComparableMixin

try:
    from dateutil.relativedelta import relativedelta
except ImportError:  # pragma: no cover
    relativedelta = timedelta

ZERO = timedelta(0)


class RelativeDate(ComparableMixin):
    """
    An unfixed date that is comparable to regular date and datetime objects.
    """
    def __init__(self, offset=ZERO, clock=date.today):
        self.offset = offset
        self._clock = clock

    def replace(self, **kwargs):
        """
        Creates a static instance of RelativeDate, but allows to also change the offset.
        """
        offset = kwargs.pop('offset', self.offset)
        when = self._now.replace(**kwargs)
        return self._staticfactory(when, offset)

    def as_date(self):
        "Return the underlying date instance"
        return self._now

    @property
    def _now(self):
        return self._clock() + self.offset

    @classmethod
    def fromordinal(cls, ordinal, offset=ZERO):
        "Create a static RelativeDate from an ordinal"
        return cls._staticfactory(date.fromordinal(ordinal), offset)

    @classmethod
    def fromtimestamp(cls, timestamp, offset=ZERO):
        "Create a static RelativeDate from a timestamp"
        return cls._staticfactory(date.fromtimestamp(timestamp), offset)

    @classmethod
    def today(cls, offset=ZERO):
        "Create a static RelativeDate from date.today"
        return cls._staticfactory(date.today(), offset=offset)

    @staticmethod
    def fromdate(when, offset=ZERO):
        "Create a static RelativeDate from an arbitrary date instance"
        return RelativeDate(offset=offset, clock=lambda: when)

    _staticfactory = fromdate

    def _compare(self, other, operator):
        if isinstance(other, RelativeDate):
            return operator(self.offset, other.offset) and \
                   operator(self._now, other._now)
        return operator(self._now, other)

    def __add__(self, other):
        """
        Either:
            * add two relative offsets to one another
            * add a timedelta to the relative offset

        These return a new RelativeDate instance with the appropriate changes made. If neither
        are possible, then it adds the other object to the underlying date and returns that result
        """
        if isinstance(other, RelativeDate):
            new_offset = self.offset + other.offset
            return self.__class__(new_offset, self._clock)
        elif isinstance(other, (timedelta, relativedelta)):
            return self.__class__(self.offset + other, self._clock)
        return self._now + other

    __radd__ = __add__

    def __sub__(self, other):
        """
        Either:
            * subtract two relative offsets from each other
            * subtract a timedelta from the relative offset

        These return a new RelativeDate instance with the appropriate changes made. If neither
        are possible, then it subtracts the other object from the underlying date and returns that
        result.
        """
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
    """
    Unfixed datetime instance. Essentially the same as RelativeDate but with some changes
    to make it an appropriate replacement for a datetime object.
    """
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
