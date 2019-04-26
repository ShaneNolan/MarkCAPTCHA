import glob
import pickle
import numpy as np
import os
from pathlib import Path

from keras.models import Sequential
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Flatten, Dense
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt


class Model():
    __instance = None

    def __init__(self):
        self.__getInstance()

    def __getInstance(self):
        if Model.__instance == None:
            self.__instance = self
        else:
            return Model.__instance

    def initialise(self, image_size, hidden_layers, iterations,
    testing_ratio, pool_size, stride):
        self.__image_size = image_size
        self.__hidden_layers = hidden_layers
        self.__iterations = iterations
        self.__testing_ratio = testing_ratio
        self.__pool_size = pool_size
        self.__stride = stride

        return self

    def train(self, image_object, images_path):
        self.__data = []
        self.__labels = []

        if not images_path.exists():
            raise Exception("Path does not exist: {}".format(str(images_path)))

        for character_folder in images_path.iterdir():
            for character in character_folder.glob("*.png"):
                try:
                    image_object.importImage(Path(character)) \
                        .resize(self.__image_size[0], self.__image_size[1])\
                        .grey()

                    self.__data.append(np.expand_dims(image_object.getImage(), axis=2))
                    self.__labels.append(str(character.parents[0]).split(os.path.sep)[-1])
                except Exception as ex:
                    print(ex)
                    continue
        return self

    def build(self, labelBinaryObject, labelBinary_path, model_path, show = False):
        (x_train, x_test, y_train, y_test) = train_test_split(np.array(self.__data, dtype="float") / 255.0,
            np.array(self.__labels), test_size=self.__testing_ratio, random_state=0)

        labelbinary = LabelBinarizer().fit(y_train)
        y_train = labelbinary.transform(y_train)
        y_test = labelbinary.transform(y_test)

        labelBinaryObject.save(labelBinary_path, labelbinary)

        model = Sequential()

        model.add(Conv2D(32, (3, 3), padding="same", input_shape=(self.__image_size[0],
            self.__image_size[1], 1), activation="relu"))
        model.add(MaxPooling2D(pool_size=(self.__pool_size[0], self.__pool_size[1]),
            strides=(self.__stride[0], self.__stride[0])))

        #Dropout?

        model.add(Conv2D(64, (3, 3), padding="same", activation="relu"))
        model.add(MaxPooling2D(pool_size=(self.__pool_size[0], self.__pool_size[1]),
            strides=(self.__stride[0], self.__stride[0])))

        model.add(Flatten())

        model.add(Dense(self.__hidden_layers, activation="relu"))

        model.add(Dense(len(set(self.__labels)), activation="softmax"))

        model.compile(loss="categorical_crossentropy", optimizer="adam",
            metrics=["accuracy"])

        history = model.fit(x_train, y_train, validation_data=(x_test, y_test),
            batch_size=6, epochs=self.__iterations)

        if show:
            plt.plot(history.history['acc'], label="Accuracy")
            plt.plot(history.history['loss'], label="Loss")
            plt.title('Model Training Metrics')
            plt.ylabel('Metrics')
            plt.xlabel('Epochs')
            plt.legend(loc='upper left')
            plt.show()

        model.save(str(Path(model_path)))

        return self
