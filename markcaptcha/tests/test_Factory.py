import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import unittest
from lib.Factory import Factory

class TestImageProcessing(unittest.TestCase):

    def test_Factory(self):
        self.assertRaises(Exception, Factory().create, "")


if __name__ == '__main__':
    unittest.main()
