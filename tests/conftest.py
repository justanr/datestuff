import datetime


# stub out non-deterministic methods with raising alternatives
@staticmethod
def nondeterminism(*a, **k):
    raise RuntimeError("Relying on non-determinism")

datetime.date = type('RaisingDate', (datetime.date,), {'today': nondeterminism})
datetime.datetime = type('RaisingDateTIme', (datetime.datetime,), {
    'now': nondeterminism,
    'utcnow': nondeterminism,
    'today': nondeterminism
})
