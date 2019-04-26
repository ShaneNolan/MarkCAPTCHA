import cv2
from pathlib import Path
import numpy as np

class Segmentation():

    def __init__(self):
        if type(self) is Segmentation:
            raise Exception('Segmentation is an abstract class and cannot be instantiated.')
        self._image = None

    def getImage(self):
        if self._image.getImage().all() == None:
            raise Exception("Segmented image needs to be initialised.")

        return self._image.getImage()

    def pixelCount(self, contour):
        if self._image.getImage() is None:
            raise Exception("No image specified for pixel count.")

        (x, y, w, h) = cv2.boundingRect(contour)
        return cv2.countNonZero(self._image.getImage()[y:y + h, x:x + w])

    def getLargestContours(self, amount):
        contours = self._image.findContours(cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        largest_contours = sorted(contours, key=lambda x: self.pixelCount(x),
            reverse=True)[:amount]

        return [cv2.boundingRect(contour) for contour in largest_contours]


class Outliers(Segmentation):
    THRESHOLD = 3

    def __init__(self):
        self.__outliers = []
        self.__image_objects = []

    def addImageObject(self, image):
        self.__image_objects.append(image)
        return self

    def setOutliers(self, outlier):
        self.__outliers = [outlier]

    def doOutliers(self, captcha_length):
        if len(self.__image_objects) == 0:
            raise Exception("No image objects supplied for outliers.")

        aspect_ratios = []

        for image_object in self.__image_objects:
            self._image = image_object
            image_contours = super().getLargestContours(captcha_length)

            for cords in image_contours:
                (x, y, w, h) = cords

                aspect_ratios.append(w/h)

        self.__outliers = self.calculateZScore(aspect_ratios, Outliers.THRESHOLD)

        return self

    def calculateZScore(self, data, threshold):
        '''
        Discover outliers in a list.
        @params:
            data        - Required  : aspect ratios (List[Int])
            threshold   - Required  : standard deviations (Int)
        '''

        data = np.array(data)
        return [value for value in data if np.abs((value - np.mean(data)) / np.std(data)) > threshold]

    def getOutliers(self):
        if self.__outliers == None:
            raise Exception("No outlier data supplied.")

        return self.__outliers

    def getMinOutlier(self):
        if len(self.__outliers) == 0:
            self.__outliers = [1.5]

        return round(min(self.__outliers), 2)

    def getImageObjects(self):
        return self.__image_objects

    def getSumImageObjects(self):
        return len(self.__image_objects)

    def getImageObject(self):
        if not self.__image_objects:
            raise Exception("No image objects in Outliers.")

        return self.__image_objects.pop()


class Segment(Segmentation):
    __CHARACTER_COUNTER = {}

    def __init__(self):
        super().__init__()
        self.__character_cords = False
        return

    def getCharacterCords(self):
        return self.__character_cords

    def segment(self, image_object, captcha_length, variance):
        self._image = image_object

        largest_contours_cords = super().getLargestContours(captcha_length[1])

        character_cords = []
        contour_counter = 0
        for cords in largest_contours_cords:
            if len(character_cords) == captcha_length[1]:
                break

            (x, y, w, h) = cords

            if w / h > variance:
                half_width = int(w / 2)
                character_cords.append((x, y, half_width, h))
                character_cords.append((x + half_width, y, half_width, h))
            else:
                character_cords.append((x, y, w, h))

        count_character_cords = len(character_cords)
        if count_character_cords >= captcha_length[0] and count_character_cords <= captcha_length[1]:
            self.__character_cords = sorted(character_cords, key=lambda x: x[0])

        return self

    def successful(self):
        return self.__character_cords != False

    def saveCharacters(self, save_path):
        if self.successful():
            for character_cord, character in zip(self.__character_cords,
                self._image.getFilename()[:len(self.__character_cords)]):
                (x, y, w, h) = character_cord

                new_save_path = save_path / character
                new_save_path.mkdir(parents=True, exist_ok=True)

                current_count = Segment.__CHARACTER_COUNTER.get(character, 1)
                cv2.imwrite(str(new_save_path / "{}.png".format(str(current_count))),
                    self._image.getImage()[y - 2:y + h + 2, x - 2:x + w + 2])
                Segment.__CHARACTER_COUNTER[character] = current_count + 1
