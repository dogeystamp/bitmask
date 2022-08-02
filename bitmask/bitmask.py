# Copyright 2022 dogeystamp <dogeystamp@disroot.org>
# See LICENSE file for more details.

"""Utilities for manipulating bitmasks."""

from bitmask.util import type_name, fullname


class Bitmask:
    """Generic bitmask, which represents multiple Enum values.

    Args:
        AllFlags (Enum): Enum of values with corresponding bitmasks.
        flags: Variable length list of flags to enable.

    Examples:
        Initialise bitmask::

            from bitmask import Bitmask
            from enum import IntFlag

            class Desc(IntFlag):
                BIG = 1
                ROUND = 1 << 1
                FUNKY = 1 << 2

            bmask = Bitmask(Desc, Desc.BIG, Desc.FUNKY)

        Determine if a flag enabled::

            Desc.FUNKY in bmask

        Show all enabled flags::

            for flag in bmask:
                print(flag)

        Enable flag in bitmask::

            bmask.add(Desc.ROUND)

        Remove flag from bitmask::

            bmask.discard(Desc.ROUND)
    """

    def __init__(self, AllFlags, *flags):
        """Init symbol enum and state."""
        self._AllFlags = AllFlags

        self._value = self._AllFlags(0)

        for flag in flags:
            self.add(flag)

    @property
    def AllFlags(self):
        """Enum defining all flags used in the bitmask, and their values."""
        return self._AllFlags

    @property
    def value(self):
        """Integer value for direct access to bitmask state."""
        return self._value

    @value.setter
    def value(self, value):
        if not issubclass(type(value), int):
            raise TypeError("value must be an integer")
        self._value = value

    def __contains__(self, item):
        """Determine if a mask is enabled."""
        if issubclass(type(item), type(self)):
            for flag in item:
                if flag not in self:
                    return False
            else:
                return True
        elif issubclass(type(item), self.AllFlags):
            return bool(self.value & item)
        else:
            raise TypeError(
                f"item must be {type_name(self)} or {type_name(self.AllFlags)}"
            )

    def __iter__(self):
        """Return list of enabled flags."""
        for flag in self.AllFlags:
            if flag in self:
                yield flag

    def __int__(self):
        return int(self.value)

    def __index__(self):
        return int(self)

    def __str__(self):
        return "|".join([flag.name for flag in self]) or "0"

    def __repr__(self):
        enum_name = fullname(self.AllFlags(0))
        args = ", ".join([enum_name] + [f"{enum_name}.{flag.name}" for flag in self])

        return f"{fullname(self)}({args})"

    def __eq__(self, other):
        """Check equality."""
        if not issubclass(type(other), type(self)):
            return False
        elif not issubclass(other.AllFlags, self.AllFlags):
            return False
        else:
            return other.value == self.value

    def _flag_op(self, flag, op):
        """Apply a single flag to the bitmask.

        Args:
            flag (enum value): flag to apply to the bitmask.
            op (function): function that returns new numerical value for the
                bitmask, given the initial value and the flag.
        """
        if not issubclass(type(flag), self.AllFlags):
            raise TypeError(
                f"can only apply {type_name(self.AllFlags)} to {type_name(self)}"
            )
        self.value = op(self.value, flag)

    def __mask_op(self, other, op):
        """Run operations on two bitmasks/bitmask and flag.

        Will run `__flag_op` with each flag in the other bitmask.

        Args:
            other (Bitmask or Enum value): bitmask to run operation with.
            op (function): operation passed to `__flag_op` for applying individual flags.
        """
        new_bitmask = self.__class__(self.AllFlags, *(flag for flag in self))

        if issubclass(type(other), type(self)):
            new_bitmask.value = op(self.value, other.value)
        elif issubclass(type(other), self.AllFlags):
            new_bitmask._flag_op(other, op)
        else:
            raise TypeError(
                f"can only apply {type_name(self)} or {type_name(self.AllFlags)} to {type_name(self)}"
            )

        return new_bitmask

    def add(self, other):
        """Add single flag to the bitmask."""
        self._flag_op(other, lambda a, b: a | b)

    def __add__(self, other):
        """Implement + operator."""
        return self.__mask_op(other, lambda a, b: a | b)

    def __radd__(self, other):
        """Alias the + operator in reverse."""
        return self.__add__(other)

    def __or__(self, other):
        """Implement | operator."""
        return self + other

    def __ror__(self, other):
        """Alias the | operator in reverse."""
        return self.__or__(other)

    def __xor__(self, other):
        """Implement ^ operator."""
        return self.__mask_op(other, lambda a, b: a ^ b)

    def __rxor__(self, other):
        """Alias the ^ operator in reverse."""
        return self.__xor__(other)

    def __and__(self, other):
        """AND bitmasks/flags together."""
        return self.__mask_op(other, lambda a, b: a & b)

    def __rand__(self, other):
        """Alias the & operator in reverse."""
        return self.__and__(other)

    def __sub__(self, other):
        """Subtract by bitmask/flag."""
        return self.__mask_op(other, lambda a, b: a & ~b)

    def discard(self, flag):
        """Remove flag bitmask if present.

        This behaves the same as built-in `set.discard()`.

        Raises:
            TypeError: `flag` is not a single Enum value.
        """
        if not issubclass(type(flag), self._AllFlags):
            raise TypeError(
                f"can only discard {type_name(self._AllFlags)} from {type_name(self)}"
            )

        return self._flag_op(flag, lambda a, b: a & ~b)

    def remove(self, flag):
        """Remove `flag` from the bitmask.

        This behaves the same as built-in `set.remove()`.

        Raises:
            KeyError: flag is not in bitmask.
        """
        if flag not in self:
            raise KeyError(type(flag), self.AllFlags)

        self.discard(flag)
