"""
    datestuff._comparable
    ~~~~~~~~~~~~~~~~~~~~~
    Object Mixin to use as a more powerful version of functools.total_ordering
    :copyright: 2016, Alec Reiter
    :license: MIT, see LICENSE for more details
"""
from abc import ABCMeta, abstractmethod
import operator


__all__ = ['ComparableMixin']


# Don't do this at home kids
def compare(self, other, operator):
    return self._compare(other, operator)


@abstractmethod
def _compare(self, other, operator):
    pass


COMPARES = {
    '__{}__'.format(c): lambda s, o, op=getattr(operator, c): s._compare(o, op)
    for c in ['ge', 'gt', 'le', 'lt', 'eq', 'ne']
}
COMPARES['_compare'] = _compare

ComparableMixin = ABCMeta('ComparableMixin', (object,), COMPARES)

del COMPARES
