import unittest

import os
import sys
import pprint
import pathlib

sys.path.append('../')

import classes.base

class TestBase(unittest.TestCase):

    def test_valueNotIncluded(self):
#        ret = base.valueNotIncluded([], ValueNotIncludedType.MIN, 0)
        ret = 1
        self.assertEqual(0, ret)
    
if __name__ == "__main__":
    pprint.pprint(sys.path)
    print(os.getcwd())
#    unittest.main()
