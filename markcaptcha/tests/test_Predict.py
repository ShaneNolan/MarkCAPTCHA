import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import unittest
from pathlib import Path
from lib.Predict import Predict

class TestPredict(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #cls.image_obj = ImageProcessingString().importImage(Path('../markcaptcha/data/captchas/captcha_03/captchas/2a9s.png'))

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
         pass

    def tearDown(self):
        pass

    def test_Predict(self):
        # section_image_obj = ImageProcessingSection()
        # self.assertRaises(Exception, section_image_obj.importImage, "")
        #
        # section_image_obj.importImage(self.image_obj.getImage())
        # self.assertIsNotNone(section_image_obj.getImage())
        # self.assertIsNotNone(section_image_obj.getBeforeImage())
        # self.assertRaises(Exception, section_image_obj.getFilename)
        pass


if __name__ == '__main__':
    unittest.main()
