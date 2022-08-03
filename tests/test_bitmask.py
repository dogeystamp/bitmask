# Copyright 2022 dogeystamp <dogeystamp@disroot.org>
# See LICENSE file for more details.

from bitmask import Bitmask
from enum import IntFlag
import pytest


class Desc(IntFlag):
    SMALL = 1
    ROUND = 1 << 1
    FUNKY = 1 << 2
    SONAR = 1 << 4


class Colors(IntFlag):
    TEAL = 1
    PINK = 1 << 1
    BLUE = 1 << 2


def test_eq():
    """Test equality checks."""
    # Equality
    assert Bitmask() == Bitmask()
    assert Bitmask(Desc.SMALL) == Bitmask(Desc.SMALL)
    assert Bitmask(Desc.SMALL, Desc.ROUND) == Bitmask(Desc, Desc.SMALL, Desc.ROUND)
    assert Bitmask(Desc.ROUND, Desc.SMALL) == Bitmask(Desc, Desc.SMALL, Desc.ROUND)

    # Inequality
    assert Bitmask(Desc.SMALL) != Bitmask(Desc.SMALL, Desc.ROUND)
    assert Bitmask(Desc.SMALL) != Bitmask(Desc.ROUND)
    assert Bitmask(Desc.SMALL) != Bitmask()
    assert Bitmask(Desc.SMALL) != Desc.SMALL
    assert Bitmask(Desc.SMALL) != Desc.ROUND
    assert Bitmask() != Desc.ROUND

    # Wrong types
    assert Bitmask() != "Hello World!"
    assert Bitmask() != 0
    assert Bitmask() != Bitmask(Colors)


def test_repr():
    """Ensure evaluating __repr__ creates an identical object."""
    mask = Bitmask(Desc.ROUND, Desc.FUNKY)
    assert eval(repr(mask)) == mask

    empty_mask = Bitmask()
    assert eval(repr(empty_mask)) == empty_mask


def test_add():
    """Test Bitmask.add() method."""
    mask = Bitmask(Desc.SMALL, Desc.FUNKY)
    mask.add(Desc.ROUND)
    assert mask == Bitmask(Desc.SMALL, Desc.FUNKY, Desc.ROUND)

    mask = Bitmask()
    mask.add(Desc.ROUND)
    assert mask == Bitmask(Desc.ROUND)
    mask.add(Desc.ROUND)
    assert mask == Bitmask(Desc.ROUND)

    with pytest.raises(TypeError, match=".* Desc .* Bitmask.*"):
        mask.add(1)
    with pytest.raises(TypeError, match=r".* Bitmask .* Desc .* Bitmask.*"):
        mask += 1


def test_add_operator():
    """Test + operator."""
    # Individual flags
    mask = Bitmask(Desc.SMALL, Desc.FUNKY)
    assert mask + Desc.ROUND == Bitmask(Desc.SMALL, Desc.FUNKY, Desc.ROUND)
    assert Desc.ROUND + mask == Bitmask(Desc.SMALL, Desc.FUNKY, Desc.ROUND)
    assert Desc.SMALL + mask == Bitmask(Desc.SMALL, Desc.FUNKY)
    assert Bitmask() + Desc.ROUND == Bitmask(Desc.ROUND)

    # Union of bitmasks
    assert Bitmask(Desc.SMALL) + Bitmask(Desc.FUNKY, Desc.ROUND) == Bitmask(
        Desc, Desc.SMALL, Desc.FUNKY, Desc.ROUND
    )
    assert Bitmask(Desc.FUNKY, Desc.ROUND) + Bitmask(Desc.SMALL) == Bitmask(
        Desc, Desc.SMALL, Desc.FUNKY, Desc.ROUND
    )
    assert Bitmask() + Bitmask() == Bitmask()


def test_add_inline():
    """Test += operator."""
    # Individual flags
    mask = Bitmask()
    mask += Desc.FUNKY
    assert mask == Bitmask(Desc.FUNKY)
    mask += Desc.ROUND
    assert mask == Bitmask(Desc.FUNKY, Desc.ROUND)

    # Bitmasks
    mask = Bitmask()
    mask += Bitmask(Desc.ROUND, Desc.FUNKY)
    assert mask == Bitmask(Desc.FUNKY, Desc.ROUND)


def test_or_operator():
    """Test | operator."""
    # Individual flags
    mask = Bitmask(Desc.SMALL, Desc.FUNKY)
    assert mask | Desc.ROUND == Bitmask(Desc.SMALL, Desc.FUNKY, Desc.ROUND)
    assert Desc.ROUND | mask == Bitmask(Desc.SMALL, Desc.FUNKY, Desc.ROUND)
    assert Desc.SMALL | mask == Bitmask(Desc.SMALL, Desc.FUNKY)
    assert Bitmask() | Desc.ROUND == Bitmask(Desc.ROUND)

    # Union of bitmasks
    assert Bitmask(Desc.SMALL) | Bitmask(Desc.FUNKY, Desc.ROUND) == Bitmask(
        Desc, Desc.SMALL, Desc.FUNKY, Desc.ROUND
    )
    assert Bitmask(Desc.FUNKY, Desc.ROUND) | Bitmask(Desc.SMALL) == Bitmask(
        Desc, Desc.SMALL, Desc.FUNKY, Desc.ROUND
    )
    assert Bitmask() | Bitmask() == Bitmask()


def test_or_inline():
    """Test |= operator."""
    # Individual flags
    mask = Bitmask()
    mask |= Desc.FUNKY
    assert mask == Bitmask(Desc.FUNKY)
    mask |= Desc.ROUND
    assert mask == Bitmask(Desc.FUNKY, Desc.ROUND)

    # Bitmasks
    mask = Bitmask()
    mask |= Bitmask(Desc.ROUND, Desc.FUNKY)
    assert mask == Bitmask(Desc.FUNKY, Desc.ROUND)


def test_and_operator():
    """Test & operator."""
    # Individual flags
    mask = Bitmask(Desc.SMALL, Desc.FUNKY)
    assert mask & Desc.SMALL == Bitmask(Desc.SMALL)
    assert Desc.SMALL & mask == Bitmask(Desc.SMALL)
    assert Desc.ROUND & mask == Bitmask()
    assert Bitmask() & Desc.ROUND == Bitmask()

    # AND of bitmasks
    assert Bitmask(Desc.FUNKY, Desc.SONAR) & Bitmask(
        Desc, Desc.FUNKY, Desc.ROUND
    ) == Bitmask(Desc.FUNKY)
    assert Bitmask(Desc.FUNKY, Desc.ROUND) & Bitmask(Desc.SMALL) == Bitmask(Desc)
    assert Bitmask() & Bitmask() == Bitmask()


def test_and_inline():
    """Test &= operator."""
    # Individual flags
    mask = Bitmask(Desc.FUNKY, Desc.SMALL)
    mask &= Desc.FUNKY
    assert mask == Bitmask(Desc.FUNKY)
    mask &= Desc.ROUND
    assert mask == Bitmask()

    # Bitmasks
    mask = Bitmask(Desc.ROUND, Desc.FUNKY)
    mask &= Bitmask(Desc.SMALL)
    assert mask == Bitmask()


def test_remove():
    """Test the `Bitmask.remove()` method."""
    mask = Bitmask(Desc.SMALL, Desc.FUNKY)
    mask.remove(Desc.SMALL)
    assert mask == Bitmask(Desc.FUNKY)
    with pytest.raises(KeyError):
        mask.remove(Desc.SMALL)

    empty_mask = Bitmask()
    with pytest.raises(KeyError):
        empty_mask.remove(Desc.SMALL)


def test_discard():
    """Test the `Bitmask.discard()` method."""
    mask = Bitmask(Desc.SMALL, Desc.FUNKY)
    mask.discard(Desc.SMALL)
    assert mask == Bitmask(Desc.FUNKY)
    mask.discard(Desc.SMALL)
    assert mask == Bitmask(Desc.FUNKY)

    empty_mask = Bitmask()
    empty_mask.discard(Desc.SMALL)
    assert empty_mask == Bitmask()
    with pytest.raises(TypeError, match="can only discard Desc from Bitmask"):
        empty_mask.discard(Bitmask(Desc.SMALL))


def test_subtract():
    """Test - operator."""
    # Individual flag
    assert Bitmask(Desc.SMALL, Desc.FUNKY) - Desc.SMALL == Bitmask(Desc, Desc.FUNKY)
    assert Bitmask(Desc.FUNKY, Desc.SMALL) - Desc.SMALL == Bitmask(Desc, Desc.FUNKY)

    # Two bitmasks
    assert Bitmask(Desc.SMALL, Desc.FUNKY, Desc.ROUND) - Bitmask(
        Desc, Desc.SMALL, Desc.ROUND
    ) == Bitmask(Desc.FUNKY)
    assert (
        Bitmask(Desc.FUNKY, Desc.SMALL) - Bitmask(Desc, Desc.SMALL, Desc.FUNKY)
        == Bitmask()
    )


def test_subtract_inline():
    """Test -= operator."""
    mask = Bitmask(Desc.SMALL, Desc.FUNKY)
    mask -= Desc.SMALL
    assert mask == Bitmask(Desc.FUNKY)


def test_xor_operator():
    """Test ^ operator."""
    # Individual flags
    mask = Bitmask(Desc.SMALL, Desc.FUNKY)
    assert mask ^ Desc.ROUND == Bitmask(Desc.SMALL, Desc.FUNKY, Desc.ROUND)
    assert Desc.ROUND ^ mask == Bitmask(Desc.SMALL, Desc.FUNKY, Desc.ROUND)
    assert Desc.SMALL ^ mask == Bitmask(Desc.FUNKY)
    assert Bitmask() ^ Desc.ROUND == Bitmask(Desc.ROUND)

    # XOR bitmasks
    assert Bitmask(Desc.SMALL) ^ Bitmask(Desc.FUNKY, Desc.ROUND) == Bitmask(
        Desc, Desc.SMALL, Desc.FUNKY, Desc.ROUND
    )
    assert (
        Bitmask(Desc.FUNKY, Desc.ROUND) ^ Bitmask(Desc, Desc.FUNKY, Desc.ROUND)
        == Bitmask()
    )
    assert Bitmask() ^ Bitmask() == Bitmask()


def test_xor_inline():
    """Test ^= operator."""
    # Individual flags
    mask = Bitmask()
    mask ^= Desc.FUNKY
    assert mask == Bitmask(Desc.FUNKY)
    mask ^= Desc.ROUND
    assert mask == Bitmask(Desc.FUNKY, Desc.ROUND)
    mask ^= Desc.ROUND
    assert mask == Bitmask(Desc.FUNKY)

    # Bitmasks
    mask = Bitmask(Desc.ROUND)
    mask ^= Bitmask(Desc.ROUND, Desc.FUNKY)
    assert mask == Bitmask(Desc.FUNKY)


def test_value():
    """Ensure Bitmask.value lines up with the state."""
    mask = Bitmask(Desc.SMALL, Desc.FUNKY)
    assert mask.value == 5
    mask.add(Desc.ROUND)
    assert mask.value == 7

    assert Bitmask().value == 0

    # Setting values directly
    mask.value = 0
    assert mask == Bitmask()
    mask.value = 1
    assert mask == Bitmask(Desc.SMALL)
    with pytest.raises(TypeError, match="value must be an integer"):
        mask.value = 1j
    with pytest.raises(TypeError, match="value must be an integer"):
        mask.value = 2.5


def test_contains():
    """Test `flag in mask` check."""
    mask = Bitmask(Desc.SMALL, Desc.FUNKY)
    empty_mask = Bitmask()

    # Individual flags
    assert Desc.FUNKY in mask
    assert Desc.SMALL in mask
    assert Desc.ROUND not in mask
    assert Desc.ROUND not in empty_mask

    # Bitmasks
    assert mask in mask
    assert Bitmask(Desc.SMALL, Desc.FUNKY) in mask
    assert Bitmask(Desc.SMALL, Desc.FUNKY, Desc.ROUND) not in mask
    assert Bitmask(Desc.FUNKY) in mask
    with pytest.raises(TypeError, match="item must be Bitmask or Desc"):
        assert 1 in mask


def test_iter():
    """Test iteration."""
    assert [i for i in Bitmask(Desc.SMALL, Desc.FUNKY)] == [
        Desc.SMALL,
        Desc.FUNKY,
    ]


def test_str():
    """Test string conversion."""
    mask = Bitmask(Desc.SMALL, Desc.FUNKY)

    assert str(mask) == "SMALL|FUNKY"
    mask.add(Desc.ROUND)
    assert str(mask) == "SMALL|ROUND|FUNKY"
    assert str(Bitmask(Desc.ROUND)) == "ROUND"
    assert str(Bitmask()) == "0"


def test_int():
    """Test int conversion."""
    mask = Bitmask(Desc.SMALL, Desc.FUNKY)
    assert int(mask) == mask.value
    mask.value = 4
    assert int(mask) == mask.value


def test_hex():
    """Test hexadecimal conversion."""
    assert hex(Bitmask(Desc.SMALL)) == "0x1"
    assert hex(Bitmask()) == "0x0"
    assert hex(Bitmask(Desc.SONAR)) == "0x10"
