# Bitmask

Implementation of a Bitmask class in Python, allowing easy manipulation of EnumFlag values.

## Features

* create bitmasks from any EnumFlag type

* simple "flag in Bitmask" syntax

* bitwise operations, e.g. AND (&), OR (|), XOR (^)

* assignment with operators (+=, -=, &=, etc.)

* convenience functions like Bitmask.add(), or Bitmask.discard()

For development and tinkering:

* included unit tests

* ample documentation and examples in code

## Example usage

```python
from bitmask import Bitmask
from enum import IntFlag

class Desc(IntFlag):
	SMALL = 1
	ROUND = 1 << 1
	FUNKY = 1 << 2
	LARGE = 1 << 3

marble = Bitmask(Desc.SMALL, Desc.ROUND, Desc.FUNKY)

Desc.SMALL in marble
>>> True

Desc.LARGE in marble
>>> False

Bitmask(Desc.SMALL, Desc.ROUND) in marble
>>> True
```
