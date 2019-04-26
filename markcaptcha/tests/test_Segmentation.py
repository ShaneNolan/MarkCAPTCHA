import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import unittest
from pathlib import Path
from lib.Segmentation import Outliers, Segment

class TestSegmentation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #cls.image_obj = ImageProcessingString().importImage(Path('../markcaptcha/data/captchas/captcha_03/captchas/1a5d.png'))

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
         pass

    def tearDown(self):
        pass

    def test_(self):
        pass


if __name__ == '__main__':
    unittest.main()
