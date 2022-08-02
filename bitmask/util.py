# Copyright 2022 dogeystamp <dogeystamp@disroot.org>
# See LICENSE file for more details.

"""Miscellaneous utilities for formatting exceptions, etc."""

import enum


def fullname(obj):
    """Get the full class name of an object, including module.

    Returns:
        String with class name, which can be used in an `eval()`.
    """
    return f"{obj.__class__.__qualname__}"


def type_name(obj):
    """Get the short type of an object.

    Returns:
        String with human-readable type of the object.

    Example:

        import bitmask.util as util
        util.type_name(1)
        >>> int
    """
    if issubclass(type(obj), enum.EnumMeta):
        return obj.__name__
    else:
        return obj.__class__.__name__
