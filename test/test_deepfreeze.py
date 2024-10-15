import pytest

from frozen import deepfreeze, frozendict


def test_deepfreeze():
    assert deepfreeze({"one": [1, 2, 3]}) == frozendict({"one": tuple([1, 2, 3])})
    assert deepfreeze({"one": {1, 2, 3}}) == frozendict({"one": frozenset({1, 2, 3})})
    assert deepfreeze({"one": (1, 2, 3)}) == frozendict({"one": tuple([1, 2, 3])})
    assert deepfreeze(
        {
            "one": (1, 2, 3),
            "two": [1, None, {11: 17}],
        }
    ) == frozendict(
        {
            "one": tuple([1, 2, 3]),
            "two": tuple([1, None, frozendict({11: 17})]),
        }
    )
    assert deepfreeze(bytearray("123", encoding="utf8")) == bytes(
        "123", encoding="utf8"
    )

    with pytest.raises(TypeError):
        deepfreeze(lambda x: x)
