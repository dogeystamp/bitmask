from bitmask import Bitmask
from enum import IntFlag
import unittest

class Desc(IntFlag):
    SMALL = 1
    ROUND = 1 << 1
    FUNKY = 1 << 2
    SONAR = 1 << 4

class TestBitmask(unittest.TestCase):
    def test_eq(self):
        """Test equality checks."""
        self.assertEqual(
            Bitmask(Desc),
            Bitmask(Desc)
        )
        self.assertEqual(
            Bitmask(Desc, Desc.SMALL),
            Bitmask(Desc, Desc.SMALL)
        )
        self.assertEqual(
            Bitmask(Desc, Desc.SMALL, Desc.ROUND),
            Bitmask(Desc, Desc.SMALL, Desc.ROUND)
        )
        self.assertEqual(
            Bitmask(Desc, Desc.ROUND, Desc.SMALL),
            Bitmask(Desc, Desc.SMALL, Desc.ROUND)
        )
        self.assertNotEqual(
            Bitmask(Desc, Desc.SMALL),
            Bitmask(Desc, Desc.SMALL, Desc.ROUND)
        )
        self.assertNotEqual(
            Bitmask(Desc, Desc.SMALL),
            Bitmask(Desc, Desc.ROUND)
        )
        self.assertNotEqual(
            Bitmask(Desc, Desc.SMALL),
            Bitmask(Desc)
        )
        self.assertNotEqual(
            Bitmask(Desc, Desc.SMALL),
            Desc.SMALL
        )
        self.assertNotEqual(
            Bitmask(Desc, Desc.SMALL),
            Desc.ROUND
        )
        self.assertNotEqual(
            Bitmask(Desc),
            Desc.ROUND
        )

    def test_repr(self):
        """Ensure evaluating __repr__ creates an identical object."""
        mask = Bitmask(Desc, Desc.ROUND, Desc.FUNKY)
        self.assertEqual(
            eval(repr(mask)),
            mask
        )
        empty_mask = Bitmask(Desc)
        self.assertEqual(
            eval(repr(empty_mask)),
            empty_mask
        )

    def test_add(self):
        """Test Bitmask.add() method."""
        mask = Bitmask(Desc, Desc.SMALL, Desc.FUNKY)
        mask.add(Desc.ROUND)
        self.assertEqual(
            mask,
            Bitmask(Desc, Desc.SMALL, Desc.FUNKY, Desc.ROUND)
        )

        mask = Bitmask(Desc)
        mask.add(Desc.ROUND)
        self.assertEqual(
            mask,
            Bitmask(Desc, Desc.ROUND)
        )
        mask.add(Desc.ROUND)
        self.assertEqual(
            mask,
            Bitmask(Desc, Desc.ROUND)
        )

    def test_add_operator(self):
        """Test + operator."""
        # Individual flags
        mask = Bitmask(Desc, Desc.SMALL, Desc.FUNKY)
        self.assertEqual(
            mask + Desc.ROUND,
            Bitmask(Desc, Desc.SMALL, Desc.FUNKY, Desc.ROUND)
        )
        self.assertEqual(
            Desc.ROUND + mask,
            Bitmask(Desc, Desc.SMALL, Desc.FUNKY, Desc.ROUND)
        )
        self.assertEqual(
            Desc.SMALL + mask,
            Bitmask(Desc, Desc.SMALL, Desc.FUNKY)
        )
        self.assertEqual(
            Bitmask(Desc) + Desc.ROUND,
            Bitmask(Desc, Desc.ROUND)
        )

        # Union of bitmasks
        self.assertEqual(
            Bitmask(Desc, Desc.SMALL) + Bitmask(Desc, Desc.FUNKY, Desc.ROUND),
            Bitmask(Desc, Desc.SMALL, Desc.FUNKY, Desc.ROUND)
        )
        self.assertEqual(
            Bitmask(Desc, Desc.FUNKY, Desc.ROUND) + Bitmask(Desc, Desc.SMALL),
            Bitmask(Desc, Desc.SMALL, Desc.FUNKY, Desc.ROUND)
        )
        self.assertEqual(
            Bitmask(Desc) + Bitmask(Desc),
            Bitmask(Desc),
        )

    def test_add_inline(self):
        """Test += operator."""
        # Individual flags
        mask = Bitmask(Desc)
        mask += Desc.FUNKY
        self.assertEqual(
            mask,
            Bitmask(Desc, Desc.FUNKY)
        )
        mask += Desc.ROUND
        self.assertEqual(
            mask,
            Bitmask(Desc, Desc.FUNKY, Desc.ROUND)
        )
            
    def test_remove(self):
        """Test the `Bitmask.remove()` method."""
        mask = Bitmask(Desc, Desc.SMALL, Desc.FUNKY)
        mask.remove(Desc.SMALL)
        self.assertEqual(
            mask,
            Bitmask(Desc, Desc.FUNKY)
        )
        with self.assertRaises(KeyError):
            mask.remove(Desc.SMALL)

        empty_mask = Bitmask(Desc)
        with self.assertRaises(KeyError):
            empty_mask.remove(Desc.SMALL)
    
    def test_discard(self):
        """Test the `Bitmask.discard()` method."""
        mask = Bitmask(Desc, Desc.SMALL, Desc.FUNKY)
        mask.discard(Desc.SMALL)
        self.assertEqual(
            mask,
            Bitmask(Desc, Desc.FUNKY)
        )
        mask.discard(Desc.SMALL)
        self.assertEqual(
            mask,
            Bitmask(Desc, Desc.FUNKY)
        )

        empty_mask = Bitmask(Desc)
        empty_mask.discard(Desc.SMALL)
        self.assertEqual(
            empty_mask,
            Bitmask(Desc)
        )
        with self.assertRaises(TypeError):
            empty_mask.discard(Bitmask(Desc, Desc.SMALL))

    def test_subtract(self):
        """Test - operator."""
        # Individual flag
        self.assertEqual(
            Bitmask(Desc, Desc.SMALL, Desc.FUNKY) - Desc.SMALL,
            Bitmask(Desc, Desc.FUNKY)
        )
        self.assertEqual(
            Bitmask(Desc, Desc.FUNKY, Desc.SMALL) - Desc.SMALL,
            Bitmask(Desc, Desc.FUNKY)
        )

        # Two bitmasks
        self.assertEqual(
            Bitmask(Desc, Desc.SMALL, Desc.FUNKY, Desc.ROUND)
            - Bitmask(Desc, Desc.SMALL, Desc.ROUND),
            Bitmask(Desc, Desc.FUNKY)
        )
        self.assertEqual(
            Bitmask(Desc, Desc.FUNKY, Desc.SMALL)
            - Bitmask(Desc, Desc.SMALL, Desc.FUNKY),
            Bitmask(Desc)
        )

    def test_subtract_inline(self):
        """Test -= operator."""
        mask = Bitmask(Desc, Desc.SMALL, Desc.FUNKY)
        mask -= Desc.SMALL
        self.assertEqual(
            mask,
            Bitmask(Desc, Desc.FUNKY)
        )

    def test_value(self):
        """Ensure Bitmask.value lines up with the state."""
        mask = Bitmask(Desc, Desc.SMALL, Desc.FUNKY)
        self.assertEqual(mask.value, 5)
        mask.add(Desc.ROUND)
        self.assertEqual(mask.value, 7)

        self.assertEqual(Bitmask(Desc).value, 0)

        # Setting values directly
        mask.value = 0
        self.assertEqual(
            mask,
            Bitmask(Desc)
        )
        mask.value = 1
        self.assertEqual(
            mask,
            Bitmask(Desc, Desc.SMALL)
        )
        with self.assertRaises(TypeError):
            mask.value = 1j
        with self.assertRaises(TypeError):
            mask.value = 2.5

    def test_contains(self):
        """Test `flag in mask` check."""
        mask = Bitmask(Desc, Desc.SMALL, Desc.FUNKY)
        empty_mask = Bitmask(Desc)

        self.assertIn(Desc.FUNKY, mask)
        self.assertIn(Desc.SMALL, mask)
        self.assertNotIn(Desc.ROUND, mask)
        self.assertNotIn(Desc.ROUND, empty_mask)
        with self.assertRaises(TypeError):
            mask in mask

    def test_iter(self):
        """Test iteration."""
        self.assertEqual(
            [i for i in Bitmask(Desc, Desc.SMALL, Desc.FUNKY)],
            [Desc.SMALL, Desc.FUNKY]
        )

    def test_str(self):
        """Test string conversion."""
        mask = Bitmask(Desc, Desc.SMALL, Desc.FUNKY)

        self.assertEqual(
            str(mask),
            "SMALL|FUNKY"
        )
        mask.add(Desc.ROUND)
        self.assertEqual(
            str(mask),
            "SMALL|ROUND|FUNKY"
        )
        self.assertEqual(
            str(Bitmask(Desc, Desc.ROUND)),
            "ROUND"
        )
        self.assertEqual(
            str(Bitmask(Desc)),
            "0"
        )

    def test_int(self):
        """Test int conversion."""
        mask = Bitmask(Desc, Desc.SMALL, Desc.FUNKY)
        self.assertEqual(
            int(mask),
            mask.value
        )
        mask.value = 4
        self.assertEqual(
            int(mask),
            mask.value
        )

    def test_hex(self):
        """Test hexadecimal conversion."""
        self.assertEqual(
            hex(Bitmask(Desc, Desc.SMALL)),
            "0x1"
        )
        self.assertEqual(
            hex(Bitmask(Desc)),
            "0x0"
        )
        self.assertEqual(
            hex(Bitmask(Desc, Desc.SONAR)),
            "0x10"
        )

if __name__ == '__main__':
    unittest.main()
