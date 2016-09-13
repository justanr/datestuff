=========
datestuff
=========

For when you need some :code:`datetime` helpers but not a complete replacement for the modules.

Why?
====

Frankly, I love the built in :code:`datetime` module. Almost everything I need to do, I can just do with it.

However, a few things tend to creep up datetime and datetime again. Things like:

* Creating a range of dates
* Creating an unfixed date
* Checking if two datetimes are within a certain delta of one another

Here's a short look at what's included.

RelativeDate and RelativeDateTime
=================================

These allow you to create an unfixed :code:`date` or :code:`datetime` instance by providing a :code:`timedelta` offset and/or factory method.

By default, :code:`RelativeDate` uses :code:`date.today` and :code:`RelativeDateTime` uses :code:`datetime.now` as the default factories and both have a default offset of :code:`timedelta(0)`:

.. code-block:: python

        rd = RelativeDate()
        rd.as_date()  # date(2016, 7, 24)

        rdt = RelativeDateTime()
        rd.as_datetime()  # datetime(2016, 7, 24, 12, 29)


However, it is also possible to provide other factories as well:


.. code-block:: python

        import arrow
        rdt = RelativeDateTime(clock=arrow.utcnow)
        rdt.as_datetime() # <Arrow [2016-07-24T17:34:58.970460+00:00]>

And as long as the underlying factory produces a :code:`date` or :code:`datetime` compatible object, everything will *just work*. By compatible, I mean implements the :code:`date` or :code:`datetime` interface.

Additionally, if only a static offset from today or now is desired, you can simply provide the offset argument with a :code:`timedelta` or dateutil :code:`relativedelta`. Note that currently, :code:`timedelta` and :code:`relativedelta` are not interoperable.


.. code-block:: python

        from datetime import timedelta
        rd = RelativeDate(offset=timedelta(days=6))
        rd.as_date()  # date(2016, 7, 30)

:code:`RelativeDate` and :code:`RelativeDateTime` also allow comparing against regular :code:`date` and :code:`datetime` instances with the standard operators (==, !=, >, etc). Making these incredibly useful for quickly defining date boundaries that are defined statically (such as in a serializer or ORM model):

.. code-block:: python

        from datetime import timedelta, date

        rd = RelativeDate(offset=timedelta(days=7))

        assert rd > date.today()  # always true


Adding and subtracting relative instances actually operate on their offsets, rather than underlying :code:`date` or :code:`datetime` values.

.. code-block:: python
 
        from datetime import timedelta

        rd = RelativeDate(offset=timedelta(days=1))

        rd + rd == RelativeDate(offset(timedelta(days=2)))

        rd - rd == RelativeDate()

Some alternate constructors are provided where it makes sense, each allows passing an offset but defaults to :code:`timedelta()`, provided are:

* :code:`RelativeDate.today`: the default constructor
* :code:`RelativeDateTime.now`: the default constructor, allows passing a tzinfo object to the factory
* :code:`RelativeDateTime.utcnow`: factory produces UTC-based datetimes (note: these are NAIVE as it relies on the underlying :code:`datetime.utcnow`)
* :code:`RelativeDateTime.today`: the default constructor, does not allow passing a tzinfo object

For convenience sake there are also truly static constructors:

* :code:`RelativeDate.fromdate`: hoists a regular date into relative context
* :code:`RelativeDateTime.fromdatetime`: hoists a regular datetime into
* :code:`RelativeDateTime.fromdate`: hoists a date into a :code:`RelativeDateTime` context, allows passing a tzinfo object, factory looks like :code:`datetime.combine(the_date, time(tzinfo=tzinfo))`

Any additional static constructors, such as :code:`datetime.strptime`, can be derived from these if truly needed.

.. code-block:: python

        from datetime import date, time, timedelta

        rd = RelativeDate.fromdate(date(2016, 7, 24), offset=timedelta(days=7))
        rd.as_date()  # date(2016, 7, 31), always


Finally, any functionality not implemented directly in the relative instance is proxied to the underlying :code:`date` or :code:`datetime` instance.

DateRange
=========

A range of dates is another tool I find myself needing from time to time, however eager creation can sometimes be very expensive for a large range.

Instead, :code:`DateRange` is modeled after the Python 3 :code:`range` type, which has fast path lookup for membership, lazy iteration, indexing and slicing (slices return new :code:`DateRange` objects)

.. code-block:: python

        from datestuff import DateRange
        from datetime import date, timedelta

        dr = DateRange(start=date(2016, 1, 1), stop=date(2016, 12, 31), step=timedelta(days=7))

        date(2016, 1, 8) in dr  # true

        len(dr)  # 53, yes this is correct

        list(dr)  # [date(2016, 1, 1), date(2016, 1, 8), ...]

        dr[1] == date(2016, 1, 8)   # True
        dr[1:-1:2] == DateRange(date(2016, 1, 8), date(2016, 12, 30), step=timedelta(days=14))  # True

:code:`DateRange` also allows creating an open ended range by simply omitting the stop argument. In this case, the only functionality that will not work is using :code:`len` and negative indexing/slicing (as there is no end)

Currently, :code:`DateRange` does not support :code:`relativedelta` as under the hood it uses :code:`timedelta.total_seconds` for Python 2 and 3 compatiblity. This could be resolved in the future, but is unlikely. :code:`DateRange` is, however, compatible with :code:`date` and :code:`datetime` like objects and other :code:`timedelta` like objects. Interestingly, this would apply to :code:`RelativeDate` and :code:`RelativeDateTime` as well.


utils
=====

Currently, the only util is :code:`within_delta` which is useful for comparing two :code:`date` or :code:`datetime` (or like) instances within a certain delta.

.. code-block:: python

        from datetime import datetime, timedelta
        from datestuff import within_delta

        d1 = datetime.now()
        d2 = datetime.now()

        d1 == d2  # false

        within_delta(d1, d2, timedelta(seconds=1))  # true

If simple boundary checking is needed, this tool is much more light weight than either :code:`DateRange` or :code:`RelativeDate`. Sadly, this is another tool that cannot interoperate with :code:`relativedelta` as it and :code:`timedelta` are unorderable (at least in Python 3).
