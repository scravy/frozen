from collections import namedtuple
from collections.abc import Mapping, Iterator
from types import MappingProxyType
from typing import Self, TypeVar

K = TypeVar("K")
V = TypeVar("V", covariant=True)


_frozendict_core = namedtuple("_frozendict_core", ("_0", "_1"), rename=True)


class frozendict(_frozendict_core, Mapping[K, V]):
    """Like frozenset, a frozendict.  Keys and values must be hashable (like in frozenset)."""

    def __new__(cls, *args: tuple[K, V] | Mapping[K, V], **kwargs: V):
        _dict: dict[K, V] = dict()
        for arg in args:
            if isinstance(arg, Mapping):
                for k, v in arg.items():
                    _dict[k] = v
            elif isinstance(arg, tuple):
                if len(arg) == 2:
                    k, v = arg
                    _dict[k] = v
                else:
                    raise TypeError("invalid tuple, expecting tuple of length=2")
            else:
                raise TypeError("invalid invocation")
        for k, v in kwargs.items():  # type: ignore[assignment]
            _dict[k] = v
        _hash = 0
        for k in frozenset(_dict.keys()):
            _hash ^= hash((k, _dict[k]))
        # noinspection PyArgumentList
        return _frozendict_core.__new__(cls, _hash, MappingProxyType(_dict))

    def __init__(self, *_args: tuple[K, V] | Mapping[K, V], **_kwargs: V):
        super().__init__()

    def __getitem__(self, key: K) -> V:  # type: ignore[override]
        return self._1[key]

    def __iter__(self) -> Iterator[K]:
        return iter(self._1)

    def __len__(self) -> int:
        return len(self._1)

    def __hash__(self) -> int:
        return self._0

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        if hash(self) != hash(other):
            return False
        # noinspection PyProtectedMember
        if self._1 != other._1:
            return False
        return True

    def __ne__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return True
        if hash(self) != hash(other):
            return True
        # noinspection PyProtectedMember
        if self._1 != other._1:
            return True
        return False

    def __str__(self) -> str:
        return str(self._1)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._1})"

    def __copy__(self) -> Self:
        return self
