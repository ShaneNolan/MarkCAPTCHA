import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import cv2

import unittest
from pathlib import Path
from lib.ImageProcessing import ImageProcessing,ImageProcessingSection, ImageProcessingString

class TestImageProcessing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.IMAGE_FILENAME = "R4ZD.png"
        cls.image_obj = ImageProcessingString().importImage(Path('tests/images/'
            + cls.IMAGE_FILENAME))

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
         pass

    def tearDown(self):
        pass

    def test_InitialiseImageProcessing(self):
        self.assertRaises(Exception, ImageProcessing)

    def test_importImage_ImageProcessingString(self):
        string_image_obj = ImageProcessingString()
        self.assertRaises(Exception, string_image_obj.importImage, "")
        self.assertRaises(Exception, string_image_obj.getImage)

        self.assertIsNotNone(self.image_obj.getImage())
        self.assertEqual(self.image_obj.getFilename(), self.IMAGE_FILENAME)
        self.assertIsNotNone(self.image_obj.getBeforeImage())

    def test_importImage_ImageProcessingSection(self):
        section_image_obj = ImageProcessingSection()
        self.assertRaises(Exception, section_image_obj.importImage, None)

        section_image_obj.importImage(self.image_obj.getImage())
        self.assertIsNotNone(section_image_obj.getImage())
        self.assertIsNotNone(section_image_obj.getBeforeImage())
        pass



if __name__ == '__main__':
    unittest.main()
