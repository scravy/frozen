import datetime
import decimal
import enum
import uuid
from collections.abc import Set, Sequence, Mapping
from typing import Final

from ._frozendict import frozendict

_IMMUTABLE_TYPES: Final[tuple[type, ...]] = (
    bool,
    int,
    float,
    complex,
    str,
    bytes,
    uuid.UUID,
    decimal.Decimal,
    enum.Enum,
    datetime.date,
    datetime.datetime,
    datetime.time,
    datetime.timedelta,
)


def deepfreeze(vs):
    if vs is None:
        return None
    if isinstance(vs, _IMMUTABLE_TYPES):
        return vs
    if isinstance(vs, bytearray):
        return bytes(vs)
    if isinstance(vs, Set):
        return frozenset(deepfreeze(v) for v in vs)
    if isinstance(vs, Sequence):
        return tuple(deepfreeze(v) for v in vs)
    if isinstance(vs, Mapping):
        return frozendict({k: deepfreeze(v) for k, v in vs.items()})
    raise TypeError(f"can't deepfreeze {type(vs).__name__}")
