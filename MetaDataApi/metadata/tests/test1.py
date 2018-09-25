import unittest
import inc_dec


class Test_TestIncrementDecrement(unittest.TestCase):
    def test_increment(self):
        self.assertEquals(inc_dec.increment(3), 4)

    def test_decrement(self):
        self.assertEquals(inc_dec.decrement(3), 4)


if __name__ == '__main__':
    unittest.main()
