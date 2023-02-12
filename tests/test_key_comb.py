import pytest
from src.maze.key_comb import KeyCombination, KeyCombinationException

def test_set_at():
    kc = KeyCombination()
    kc = kc.set_at(0, 1, 2)
    assert kc.comb == 0b111

    kc = kc.set_at(3)
    assert kc.comb == 0b1111

def test_unset_at():
    kc = KeyCombination(0b1111)
    kc = kc.unset_at(0, 1)
    assert kc.comb == 0b1100

    kc = kc.unset_at(2)
    assert kc.comb == 0b1000

def test_is_set_at():
    kc = KeyCombination(0b101)
    assert kc.is_set_at(0) is True
    assert kc.is_set_at(1) is False
    assert kc.is_set_at(2) is True

def test_keys_count():
    kc = KeyCombination(0b101)
    assert kc.keys_count() == 2

    kc = KeyCombination(0b0)
    assert kc.keys_count() == 0

def test_lt():
    kc1 = KeyCombination(0b101)
    kc2 = KeyCombination(0b100)

    assert (kc1 < kc2) is True
    assert (kc2 < kc1) is False

def test_set_exception():
    kc = KeyCombination()
    exception_mmessage = 'Trying to set bit for a key with negative position'
    with pytest.raises(KeyCombinationException, match=exception_mmessage):
        kc = kc.set_at(0, 1, -1)

def test_unset_exception():
    kc = KeyCombination()
    kc.set_at(1,2,3)
    exception_mmessage = 'Trying to unset bit for a key with negative position'
    with pytest.raises(KeyCombinationException, match=exception_mmessage):
        kc = kc.unset_at(2, -1, 1)