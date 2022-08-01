# Copyright 2022 dogeystamp <dogeystamp@disroot.org>
# See LICENSE file for more details.

"""Miscellaneous utilities for formatting exceptions, etc."""

def fullname(obj):
    """Get the full class name of an object, including module.

    Returns:
        String with class name, which can be used in an `eval()`.
    """
    return f"{obj.__class__.__qualname__}"
