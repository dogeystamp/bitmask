from bitmask import Bitmask
from enum import IntFlag
import unittest

class Desc(IntFlag):
    SMALL = 1
    ROUND = 1 << 1
    FUNKY = 1 << 2

class TestBitmask(unittest.TestCase):
    def setUp(self):
        """Initialize `Bitmask` instances for testing."""
        self.bmask = Bitmask(Desc, Desc.SMALL, Desc.FUNKY)
        self.bmask2 = Bitmask(Desc, Desc.ROUND)
        self.bmask3 = Bitmask(Desc, Desc.ROUND)
        self.bmask_empty = Bitmask(Desc)

    def test_eq(self):
        """Test equality."""
        self.assertEqual(self.bmask2, self.bmask3)
        self.assertNotEqual(self.bmask, self.bmask3)
        self.assertNotEqual(self.bmask, self.bmask_empty)
        self.assertNotEqual(self.bmask, Desc.SMALL)
        self.assertNotEqual(self.bmask, Desc.ROUND)
        self.assertNotEqual(self.bmask_empty, Desc.ROUND)

    def test_repr(self):
        """Test __repr__."""
        self.assertEqual(eval(repr(self.bmask)), self.bmask)
        self.assertEqual(eval(repr(self.bmask_empty)), self.bmask_empty)

    def test_add(self):
        """Test the `Bitmask.add()` method."""
        self.bmask.add(Desc.ROUND)
        self.assertEqual(
            self.bmask,
            Bitmask(Desc, Desc.SMALL, Desc.FUNKY, Desc.ROUND)
        )

        self.bmask_empty.add(Desc.ROUND)
        self.bmask_empty.add(Desc.ROUND)
        self.assertEqual(
            self.bmask_empty,
            Bitmask(Desc, Desc.ROUND)
        )

    def test_add_operator(self):
        """Test the + operator."""
        self.assertEqual(
            self.bmask + Desc.ROUND,
            Bitmask(Desc, Desc.SMALL, Desc.FUNKY, Desc.ROUND)
        )
        self.assertEqual(
            self.bmask_empty + Desc.ROUND,
            Bitmask(Desc, Desc.ROUND)
        )
        # Test `__radd__`.
        self.assertEqual(
            Desc.ROUND + self.bmask,
            Bitmask(Desc, Desc.SMALL, Desc.FUNKY, Desc.ROUND)
        )
        # Test combining bitmasks
        self.assertEqual(
            self.bmask + self.bmask2 + self.bmask3,
            Bitmask(Desc, Desc.SMALL, Desc.FUNKY, Desc.ROUND)
        )

    def test_remove(self):
        """Test the `Bitmask.remove()` method."""
        self.bmask.remove(Desc.SMALL)
        self.assertEqual(
            self.bmask,
            Bitmask(Desc, Desc.FUNKY)
        )
        with self.assertRaises(KeyError):
            self.bmask.remove(Desc.SMALL)
        with self.assertRaises(KeyError):
            self.bmask_empty.remove(Desc.SMALL)
    
    def test_discard(self):
        """Test the `Bitmask.discard()` method."""
        self.bmask.discard(Desc.SMALL)
        self.assertEqual(
            self.bmask,
            Bitmask(Desc, Desc.FUNKY)
        )
        self.bmask.discard(Desc.SMALL)
        self.assertEqual(
            self.bmask,
            Bitmask(Desc, Desc.FUNKY)
        )
        self.bmask_empty.discard(Desc.SMALL)
        self.assertEqual(
            self.bmask_empty,
            Bitmask(Desc)
        )

    def test_value(self):
        """Ensure Bitmask.value lines up with the state."""
        self.assertEqual(self.bmask.value, 5)
        self.bmask.add(Desc.ROUND)
        self.assertEqual(self.bmask.value, 7)

        self.assertEqual(self.bmask_empty.value, 0)

        # Setting values directly
        self.bmask.value = 0
        self.assertEqual(
            self.bmask,
            Bitmask(Desc)
        )
        self.bmask.value = 1
        self.assertEqual(
            self.bmask,
            Bitmask(Desc, Desc.SMALL)
        )
        with self.assertRaises(TypeError):
            self.bmask.value = 1j
        with self.assertRaises(TypeError):
            self.bmask.value = 2.5
        with self.assertRaises(TypeError):
            self.bmask.value = -1

    def test_contains(self):
        """Test `flag in mask` check."""
        self.assertIn(Desc.FUNKY, self.bmask)
        self.assertIn(Desc.SMALL, self.bmask)
        self.assertNotIn(Desc.ROUND, self.bmask)
        self.assertNotIn(Desc.ROUND, self.bmask_empty)
        with self.assertRaises(TypeError):
            self.bmask in self.bmask

    def test_iter(self):
        """Test iteration."""
        self.assertEqual(
            [i for i in self.bmask],
            [Desc.SMALL, Desc.FUNKY]
        )

    def test_str(self):
        """Test string conversion."""
        self.assertEqual(
            str(self.bmask),
            "SMALL|FUNKY"
        )
        self.bmask.add(Desc.ROUND)
        self.assertEqual(
            str(self.bmask),
            "SMALL|ROUND|FUNKY"
        )

        self.assertEqual(
            str(self.bmask_empty),
            "0"
        )
        self.bmask_empty.add(Desc.ROUND)
        self.assertEqual(
            str(self.bmask_empty),
            "ROUND"
        )

    def test_int(self):
        """Test int conversion."""
        self.assertEqual(
            int(self.bmask),
            self.bmask.value
        )
        self.bmask.value = 4
        self.assertEqual(
            int(self.bmask),
            self.bmask.value
        )

if __name__ == '__main__':
    unittest.main()
