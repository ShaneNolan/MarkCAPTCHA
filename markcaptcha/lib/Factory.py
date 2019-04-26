from lib.ImageProcessing import ImageProcessingSection, ImageProcessingString, ImageProcessingBase64
from lib.Segmentation import Segment, Outliers
from lib.Model import Model
from lib.Predict import Predict
from lib.Parser import JSONParser, PickleParser


class Factory():

    CLASS_IMAGEPROCESSING_SECTION = "imageprocessingsection"
    CLASS_IMAGEPROCESSING_STRING = "imageprocessingstring"
    CLASS_IMAGEPROCESSING_BASE64 = "imageprocessingbase64"
    CLASS_SEGMENT = "segment"
    CLASS_OUTLIERS = "outliers"
    CLASS_MODEL = "model"
    CLASS_PREDICT = "predict"
    CLASS_JSONPARSER = "jsonparser"
    CLASS_PICKLEPARSER = "pickleparser"

    __CLASSES = {
        CLASS_IMAGEPROCESSING_SECTION : ImageProcessingSection,
        CLASS_IMAGEPROCESSING_STRING : ImageProcessingString,
        CLASS_IMAGEPROCESSING_BASE64 : ImageProcessingBase64,
        CLASS_SEGMENT : Segment,
        CLASS_OUTLIERS: Outliers,
        CLASS_MODEL : Model,
        CLASS_PREDICT : Predict,
        CLASS_JSONPARSER : JSONParser,
        CLASS_PICKLEPARSER : PickleParser,
    }

    def __init__(self):
        return

    def create(self, classname):
        if classname not in Factory.__CLASSES:
            raise Exception("Invalid Factory Class supplied: {}.".format(classname))

        return Factory.__CLASSES[classname]()
