import cv2
import numpy as np
from pathlib import Path
from PIL import Image
import os, imutils, io, base64
from abc import ABC, abstractmethod


#https://docs.opencv.org/4.0.0/index.html
class ImageProcessing(ABC):

    def __init__(self):
        if type(self) is ImageProcessing:
            raise Exception('ImageProcessing is an abstract class and cannot be instantiated.')
        self._image = None
        self._before_image = None

    @abstractmethod
    def importImage(self, image):
        pass

    '''
        Get Image
            Return the image.
    '''
    def getImage(self):
        if self._image is None:
            raise Exception("No image imported.")
        return self._image

    def getBeforeImage(self):
        if self._before_image is None:
            raise Exception("No image imported to return a before image.")
        return self._before_image

    '''
    Grey
        Greyscale an image.
    '''
    def grey(self):
        if len(self._image.shape) == 3:
            self._image = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)

        return self

    '''
    Erosion
        All pixels near the boundary will be discarded depending upon the size
        of kernel.
    '''
    def erode(self, erode_amount, iterations = 1):
        self._image = cv2.erode(self._image,
            np.ones((int(erode_amount), int(erode_amount)), np.uint8),
            iterations = iterations)

        return self

    '''
    Dilation
        Opposite of Erosion.
    '''
    def dilate(self, dilate_amount, iterations = 1):
        self._image = cv2.dilate(self._image,
            np.ones((int(dilate_amount), int(dilate_amount)), np.uint8),
            iterations = iterations)

        return self

    '''
    Opening
        Opening is erosion followed by dilation.
    '''
    def opening(self, opening_amount):
        self._image = cv2.morphologyEx(self._image, cv2.MORPH_OPEN,
            np.ones((int(opening_amount), int(opening_amount)), np.uint8))

        return self

    '''
    Closing
        Closing is reverse of Opening.
    '''
    def closing(self, closing_amount):
        self._image = cv2.morphologyEx(self._image, cv2.MORPH_CLOSE,
            np.ones((int(closing_amount), int(closing_amount)), np.uint8))

        return self

    '''
    Gradient
        Difference between dilation and erosion.
    '''
    def gradient(self, gradient_amount):
        self._image = cv2.morphologyEx(self._image, cv2.MORPH_GRADIENT,
            np.ones((int(gradient_amount), int(gradient_amount)), np.uint8))

        return self
    '''
    Threshold
        Segmentation method based on the variation of intensity between
        the object pixels and the background pixels.
    '''
    def threshold(self, thresh_value, inverted = False):
        self._image = cv2.threshold(self._image, int(thresh_value), 255,
            cv2.THRESH_BINARY_INV if inverted else cv2.THRESH_BINARY)[1]

        return self

    '''
    Otsu Threshold
        Automatically calculates a threshold value from image histogram.
    '''
    def thresholdOtsu(self):
        self._image = cv2.threshold(self._image, 0, 255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        return self

    '''
    Adaptive Threshold
        Calculate the threshold for a small regions of the image.
        It gives us better results for images with varying illumination.
    '''
    def adaptiveThreshold(self, blocksize, c):
        self._image = cv2.adaptiveThreshold(self._image, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blocksize, c)

        return self

    '''
    Fill Holes
        Fill blank space in an image.
    '''
    def fillHoles(self):
        contours = self.findContours(cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            cv2.drawContours(self._image, [contour], 0, (255, 255, 255), -1)

        return self

    '''
    Line Removal
        Removes lines within an image.
    '''
    def lineRemoval(self, line_width):
        mask = np.zeros_like(self._image)

        lines = cv2.HoughLines(cv2.Canny(self._image, 50, 150, apertureSize = 3),
            	1, (np.pi/180), 0)[0]

        if lines is not None:
            for rho, theta in lines:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho

                pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))

                cv2.line(mask, pt1, pt2, (255, 255, 255), line_width, cv2.LINE_AA)

        self._image = cv2.inpaint(self._image, mask, 1, cv2.INPAINT_TELEA)
        return self

    '''
    Blur
        Gaussian Blur an image.
    '''
    def blur(self, blur_value):
        self._image = cv2.GaussianBlur(self._image, (int(blur_value),
            int(blur_value)), 0)

        return self

    '''
    FindContours
        Finds contours within the image.
        Finding contours is finding white object from black background.
    '''
    def findContours(self, retrieval_mode, approximation_method, image = None):
        return cv2.findContours(self._image if image is None else image, retrieval_mode,
            approximation_method)[0]

    '''
    RemoveContours
        Removes contours based on their area size.
    '''
    def removeContours(self, margin_error):
        contours = self.findContours(cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        areas = [cv2.contourArea(c) for c in contours]
        sorted_areas = sorted(zip(areas, contours), key=lambda x: x[0])

        '''
        contour_margin_error = 0
        for i, (area, contour) in enumerate(sorted_areas):
            if i == round(len(sorted_areas) / 2):
                break
            contour_margin_error += area

        contour_margin_error += np.median([area for area, contours in sorted_areas])
        contour_margin_error = round(contour_margin_error)
        '''

        for area, contour in sorted_areas:
            if area <= margin_error:
                cv2.drawContours(self._image, contour, -1, (0,0,0), 5)

        return self

    '''
    Histogram Equalisation
        Improves the contrast in an image, in order to stretch
        out the intensity range.
    '''
    def histogramEqualisation(self):
        self._image = cv2.equalizeHist(self._image)

        return self

    '''
        Border
            Adds a border to the image.
    '''
    def border(self, height, width, replicate = False, colour = [0,0,0]):
        self._image = cv2.copyMakeBorder(self._image, height, height, width, width,
            cv2.BORDER_REPLICATE if replicate else cv2.BORDER_CONSTANT,
            value=colour)

        return self

    '''
    Resize
        Resizes an image.
    '''
    def resize(self, width, height):
        (h, w) = self._image.shape[:2]

        if w > h:
            self._image = imutils.resize(self._image, width=width)
        else:
            self._image = imutils.resize(self._image, height=height)

        self.border(int((height - h) if height > h else (h - height) / 2.0),
            int((width - w) if width > w else (w - width) / 2.0), False)

        self._image = cv2.resize(self._image, (width, height))

        return self

    '''
    Show
        Display an image.
    '''
    def show(self):
        cv2.imshow("Before Image", self._before_image)
        cv2.imshow("Cleaned image", self._image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return self

    '''
    Save
        Save an image to the specified folder.
    '''
    def save(self, folder, show=False):
        if show:
            self.show()

        save_path = str(folder / self._filename)
        folder.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(save_path, self._image)

        return save_path


class ImageProcessingSection(ImageProcessing):

    def __init__(self):
        super().__init__()
        return

    def importImage(self, image):
        if image is None:
            raise Exception("Invalid image supplied to Image Section.")

        self._image = image
        self._before_image = image

        return self

class ImageProcessingString(ImageProcessing):

    def __init__(self):
        super().__init__()
        return

    def importImage(self, image):
        image_path = str(image)
        if not os.path.exists(image_path):
            raise Exception("Path: {} doesn't exist.".format(image_path))

        self._image = cv2.imread(image_path)
        self._before_image = self._image
        self._filename = image.name

        return self

    '''
        Get Filename
            Return the image filename.
    '''
    def getFilename(self):
        if self._filename is None:
            raise Exception("No filename has been provided.")

        return self._filename


class ImageProcessingBase64(ImageProcessing):

    def __init__(self):
        super().__init__()
        return

    def importImage(self, image):
        image = Image.open(io.BytesIO(base64.b64decode(image)))

        self._image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        self._before_image = self._image

        return self
