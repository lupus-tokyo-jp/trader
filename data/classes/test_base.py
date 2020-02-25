import unittest
import base

class TestBase(unittest.TestCase):

    def test_valueNotIncluded(self):
        ret = base.valueNotIncluded([], ValueNotIncludedType.MIN, 0)
        self.assertEqual(0, ret)
    
if __name__ == "__main__":
    unittest.main()
