from keras.models import load_model

import numpy as np
import cv2

class Predict():
    __instance = None

    def __init__(self):
        self.__getInstance()

    def __getInstance(self):
        if Predict.__instance == None:
            self.__instance = self
            self.__prediction = None
            self.__model = None
            self.__labelBinary = None
        else:
            return Predict.__instance

    def initialise(self, model_path, labelBinary, force_initialise = False):
        if (self.__model == None or self.__labelBinary == None) or force_initialise == True:
            if not model_path.is_file():
                raise Exception("No Model exists for: {}".format(str(model_path)))

            self.__model = load_model(str(model_path))

            self.__labelBinary = labelBinary

        return self

    def predict(self, segmented_image, section_image_object, image_size, show = False):
        if segmented_image.successful():
            self.__prediction = ""

            output = segmented_image.getImage().copy()
            for character_cord in segmented_image.getCharacterCords():
                (x, y, w, h) = character_cord

                section_image_object.importImage(segmented_image.getImage()[y - 2:y + h + 2, x - 2:x + w + 2]) \
                    .resize(image_size[0], image_size[1])
                image_section = np.expand_dims(section_image_object.getImage(), axis=2)
                image_section = np.expand_dims(image_section, axis=0)

                predict = self.__model.predict(image_section)
                predicted_character = self.__labelBinary.inverse_transform(predict)[0]

                self.__prediction += predicted_character

                cv2.rectangle(output, (x - 2, y - 2), (x + w + 4, y + h + 4),
                    (255, 255, 255), 1)
                cv2.putText(output, predicted_character, (x + 2, y + 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            if show:
                cv2.imshow("Result", output)
                cv2.waitKey(0)
        else:
            self.__prediction = "FAILED"

        return self

    def getResult(self):
        return self.__prediction
