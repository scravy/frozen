import random
import string
from collections.abc import Mapping, Hashable, MutableMapping
from copy import copy
from typing import Final

import pytest

from frozen import frozendict


def _random_string() -> str:
    alphabet = string.printable
    return "".join(alphabet[random.randint(0, len(alphabet) - 1)] for _ in range(10))


def _shuffled(xs: list) -> list:
    ixs = [*range(len(xs))]
    random.shuffle(ixs)
    return list(xs[ix] for ix in ixs)


def test_construction() -> None:
    fd: frozendict[str, int] = frozendict(dict(foo=1337, bar=4711))
    assert {*fd.keys()} == {"foo", "bar"}
    assert {*fd.values()} == {1337, 4711}


def test_construction_from_tuples() -> None:
    fd = frozendict((17, "foo"), (19, "bar"))
    assert {*fd.keys()} == {17, 19}
    assert {*fd.values()} == {"foo", "bar"}


def test_instanceof() -> None:
    fd = frozendict(dict(foo=1337, bar=4711))
    assert isinstance(fd, Mapping)
    assert isinstance(fd, Hashable)
    assert not isinstance(fd, MutableMapping)


def test_subclass() -> None:
    assert issubclass(frozendict, Mapping)
    assert issubclass(frozendict, Hashable)
    assert not issubclass(frozendict, MutableMapping)


def test_eq_and_hash() -> None:
    vs1: list[tuple[str, str]] = [
        (_random_string(), _random_string()) for _ in range(10)
    ]
    vs2: list[tuple[str, str]] = [vs1[1], vs1[0], *_shuffled(vs1[2:])]
    fd1: frozendict[str, str] = frozendict(*vs1)
    fd2: frozendict[str, str] = frozendict(*vs2)
    fd3: frozendict[str, str] = frozendict(fd1, fd2, {vs1[0][0]: ""})
    assert fd1 == fd2
    assert fd2 == fd1
    assert not (fd1 != fd2)
    assert not (fd2 != fd1)
    assert fd2 != fd3
    assert fd3 != fd2
    assert fd1 != fd3
    assert fd3 != fd1
    assert not (fd2 == fd3)
    assert not (fd3 == fd2)
    assert not (fd1 == fd3)
    assert not (fd3 == fd1)
    assert hash(fd1) == hash(fd2)
    assert [*fd1.keys()] != [*fd2.keys()]


def test_bool() -> None:
    assert not frozendict()
    assert frozendict(key=1)


def test_equality_and_order() -> None:
    fd1: Mapping[str, int] = frozendict(foo=1337, bar=4711)
    fd2: Mapping[str, int] = frozendict(bar=4711, foo=1337)
    fd3: Mapping[str, int] = frozendict(dict(foo=1337, bar=4711, qux=1828))
    assert fd1 == fd2
    assert [*fd1.keys()] == ["foo", "bar"]
    assert [*fd2.keys()] == ["bar", "foo"]
    assert [*fd3.keys()] == ["foo", "bar", "qux"]


def test_immutability() -> None:
    _INITIAL: int = 11
    fd: frozendict[str, int] = frozendict(foo=_INITIAL)
    # set _hash
    with pytest.raises(AttributeError) as err:
        fd._0 = 389458403  # type: ignore[misc] # pylint: disable=assigning-non-slot,protected-access
    assert err.value.args[0] == "can't set attribute"
    # set _dict
    with pytest.raises(AttributeError) as err:
        fd._1 = {"foo": 19}  # type: ignore[misc] # pylint: disable=assigning-non-slot,protected-access
    assert err.value.args[0] == "can't set attribute"
    # del _hash
    with pytest.raises(AttributeError) as err:
        del fd._0  # pylint: disable=no-member
    assert err.value.args[0] == "can't delete attribute"
    # del _dict
    with pytest.raises(AttributeError) as err:
        del fd._1  # pylint: disable=no-member
    assert err.value.args[0] == "can't delete attribute"
    # change underlying dict
    with pytest.raises(TypeError) as terr:
        fd._1["foo"] = 29  # pylint: disable=no-member,protected-access
    assert (
        terr.value.args[0] == "'mappingproxy' object does not support item assignment"
    )
    # check value
    assert fd["foo"] == _INITIAL


def test_to_dict() -> None:
    fd = frozendict(foo=1337, bar=4711)
    assert {**fd} == {"foo": 1337, "bar": 4711}


def test_getitem() -> None:
    fd: frozendict[str, int] = frozendict(foo=3, bar=7)
    assert fd["foo"] == 3
    assert fd["bar"] == 7
    assert fd.get("foo") == 3
    assert fd.get("bar") == 7
    assert fd.get("foo", 10) == 3
    assert fd.get("bar", 10) == 7
    assert fd.get("foox", 10) == 10
    assert fd.get("barx", 10) == 10
    assert fd.get("foox") is None
    assert fd.get("barx") is None


def test_setitem() -> None:
    fd: frozendict[str, int] = frozendict(foo=3, bar=7)
    with pytest.raises(TypeError) as terr:
        # noinspection PyUnresolvedReferences
        fd["foo"] = 3  # type: ignore[index] # pylint: disable=unsupported-assignment-operation
    assert terr.value.args[0] == "'frozendict' object does not support item assignment"


_ARGS: Final[tuple[frozendict[str, int], ...]] = tuple(
    frozendict(d)
    for d in [
        {},
        {"one": 1},
        {"one": 0},
        {"one": -1},
        {"one": -2},
        {"two": 1},
        {"two": 0},
        {"two": -1},
        {"two": -2},
        {"one": 1, "two": 1},
        {"one": 0, "two": 0},
        {"one": -1, "two": -1},
        {"one": -2, "two": -2},
    ]
)


@pytest.mark.parametrize(
    ["arg"],
    [[v] for v in _ARGS],
)
def test_repr(arg: frozendict) -> None:
    assert eval(repr(arg)) == arg  # pylint: disable=eval-used


@pytest.mark.parametrize(
    ["arg"],
    [[v] for v in _ARGS],
)
def test_str(arg: dict) -> None:
    assert str(arg)


def test_eq() -> None:
    for arg0 in _ARGS:
        assert arg0 != {}
        assert not (arg0 == {})
        for arg1 in _ARGS:
            if arg0 is arg1:
                assert arg0 == arg1
                assert not (arg0 != arg1)
            else:
                assert arg0 != arg1
                assert not (arg0 == arg1)


def test_copy() -> None:
    x = frozendict({"one": 1337})
    assert copy(x) is x


def test_raise() -> None:
    with pytest.raises(TypeError):
        frozendict({"one": {}})


def test_invalid_invocation() -> None:
    with pytest.raises(TypeError):
        frozendict(1)  # type: ignore[arg-type]
    assert frozendict(("foo", 1)) == frozendict({"foo": 1})
    with pytest.raises(TypeError):
        frozendict((1, 2, 3))  # type: ignore[arg-type]
