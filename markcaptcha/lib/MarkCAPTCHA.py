from lib.Factory import Factory
from pathlib import Path

import sys, io, base64

class MarkCAPTCHA():

    '''
        Facade Design Pattern
    '''

    '''
        Constant Variables for a CAPTCHA json file.
    '''
    __CONFIG_FOLDER = "folder"
    __CONFIG_FUNCTIONS = "functions"
    __CONFIG_PREVIEW = "preview"
    __CONFIG_CAPTCHA_LENGTH = "captcha_length"
    __CONFIG_THRESHOLD = "threshold"
    __CONFIG_MODEL_FILENAME = "model_filename"
    __CONFIG_LABEL_FILENAME = "label_filename"

    '''
        ... for paths.
    '''
    __PATH_CAPTCHAS = "data/captchas/"
    __PATH_MODELS = "data/models/"
    __PATH_CHARACTERS = "characters/"
    __PATH_CONFIG_CAPTCHA = "data/configs/captchas/"
    __PATH_CONFIG_MODEL = "data/configs/models/"
    __PATH_CLEANED_FOLDER = "cleaned/"

    '''
        ... for filenames.
    '''
    __FILENAME_MODEL_JSON = "model.json"

    '''
        ... for a MODEL json file.
    '''
    __MODEL_IMAGE_SIZE = "image_size"
    __MODEL_HIDDEN_LAYERS = "hidden_layers"
    __MODEL_ITERATIONS = "iterations"
    __MODEL_TESTING_RATIO = "testing_ratio"
    __MODEL_POOL_SIZE = "pool_size"
    __MODEL_STRIDE = "stride"
    __MODEL_PREVIEW = "preview"

    def __init__(self):
        self.__image_configs = {}
        self.__model_config = None
        self.__image_filename = None
        self.__predictors = {}
        return

    def __preSegmentImage(self, image_object):
        if image_object is None:
            raise Exception("Null image object supplied to function _preSegmentImage.")

        return image_object.grey().threshold(0).border(4, 4).fillHoles()


    def importConfigs(self):
        path = Path(MarkCAPTCHA.__PATH_CONFIG_CAPTCHA)
        for config in path.glob('*.json'):
            self.__image_configs[config.name] = Factory().create(Factory.CLASS_JSONPARSER) \
                                                .parse(str(config))

        if len(self.__image_configs) == 0:
            raise Exception("No configurations found: {}".format(path))

        self.__model_config = Factory().create(Factory.CLASS_JSONPARSER) \
                .parse(MarkCAPTCHA.__PATH_CONFIG_MODEL +
                    MarkCAPTCHA.__FILENAME_MODEL_JSON)

        return self

    def processImages(self, config_filename):
        print("{}:".format(config_filename))
        config = self.__image_configs[config_filename]
        captcha_config = config.getParsedContent()

        captcha_images = list(Path(MarkCAPTCHA.__PATH_CAPTCHAS +
            captcha_config[MarkCAPTCHA.__CONFIG_FOLDER]).glob("*.png"))
        total_captcha_images = len(captcha_images)

        if total_captcha_images <= 0:
            raise Exception("No CAPTCHA images exist in {}".format(captcha_config[MarkCAPTCHA.__CONFIG_FOLDER]))

        counter = 1
        outliers = Factory().create(Factory.CLASS_OUTLIERS)
        for captcha in captcha_images:

            self.printProgress(counter, total_captcha_images,
                "Image Processing:", bar_length=25)

            cleaned_image = Factory().create(Factory.CLASS_IMAGEPROCESSING_STRING) \
                .importImage(Path(captcha))

            cleaned_image = self.__classFunctionsFromJSON(config.getParsedContent()[MarkCAPTCHA.__CONFIG_FUNCTIONS], cleaned_image)

            captcha_saved_path = cleaned_image.save(Path(MarkCAPTCHA.__PATH_CAPTCHAS +
                captcha_config[MarkCAPTCHA.__CONFIG_FOLDER] + MarkCAPTCHA.__PATH_CLEANED_FOLDER),
                captcha_config[MarkCAPTCHA.__CONFIG_PREVIEW])
            counter += 1

            outliers.addImageObject(self.__preSegmentImage(Factory().create(
                Factory.CLASS_IMAGEPROCESSING_STRING) \
                    .importImage(Path(captcha_saved_path))))

        print("Finding Outliers . . .")
        outliers.doOutliers(captcha_config[MarkCAPTCHA.__CONFIG_CAPTCHA_LENGTH][1])

        config.addValue(str(Path(MarkCAPTCHA.__PATH_CONFIG_CAPTCHA + config_filename)),
            MarkCAPTCHA.__CONFIG_THRESHOLD, outliers.getMinOutlier())

        number_of_images = outliers.getSumImageObjects()
        for counter in range(number_of_images):
            self.printProgress(counter + 1, number_of_images,
                "Segmenting:", bar_length=25)

            Factory().create(Factory.CLASS_SEGMENT) \
                .segment(outliers.getImageObject(), captcha_config[MarkCAPTCHA.__CONFIG_CAPTCHA_LENGTH],
                    outliers.getMinOutlier()) \
                .saveCharacters(Path(MarkCAPTCHA.__PATH_CAPTCHAS +
                    captcha_config[MarkCAPTCHA.__CONFIG_FOLDER] +
                    MarkCAPTCHA.__PATH_CHARACTERS))
        return self

    def buildModel(self, config_filename):
        model_config = self.__model_config.getParsedContent()
        model = Factory().create(Factory.CLASS_MODEL) \
            .initialise(model_config[MarkCAPTCHA.__MODEL_IMAGE_SIZE],
                model_config[MarkCAPTCHA.__MODEL_HIDDEN_LAYERS],
                model_config[MarkCAPTCHA.__MODEL_ITERATIONS],
                model_config[MarkCAPTCHA.__MODEL_TESTING_RATIO],
                model_config[MarkCAPTCHA.__MODEL_POOL_SIZE],
                model_config[MarkCAPTCHA.__MODEL_STRIDE])

        self.__checkForConfig(config_filename)
        config = self.__image_configs[config_filename]
        captcha_config = config.getParsedContent()

        model.train(Factory().create(Factory.CLASS_IMAGEPROCESSING_STRING),
            Path((MarkCAPTCHA.__PATH_CAPTCHAS + captcha_config[MarkCAPTCHA.__CONFIG_FOLDER]
                + MarkCAPTCHA.__PATH_CHARACTERS))) \
            .build(Factory().create(Factory.CLASS_PICKLEPARSER),
                MarkCAPTCHA.__PATH_MODELS + captcha_config[MarkCAPTCHA.__CONFIG_LABEL_FILENAME],
                MarkCAPTCHA.__PATH_MODELS + captcha_config[MarkCAPTCHA.__CONFIG_MODEL_FILENAME],
                model_config[MarkCAPTCHA.__MODEL_PREVIEW])

        return self

    def predict(self, config_filename, image, show = False):
        self.__checkForConfig(config_filename)
        captcha_config = self.__image_configs[config_filename]

        if '.' in image:
            cleaned_image = Factory().create(Factory.CLASS_IMAGEPROCESSING_STRING) \
                .importImage(Path(image))
            self.__image_filename = cleaned_image.getFilename()
        else:
            cleaned_image = Factory().create(Factory.CLASS_IMAGEPROCESSING_BASE64) \
                .importImage(image)

        cleaned_image = self.__classFunctionsFromJSON(captcha_config.getParsedContent()[MarkCAPTCHA.__CONFIG_FUNCTIONS], cleaned_image)

        pre_segmented_image = self.__preSegmentImage(cleaned_image)

        captcha_config = captcha_config.getParsedContent()
        segmented_captcha = Factory().create(Factory.CLASS_SEGMENT) \
            .segment(pre_segmented_image,
                captcha_config[MarkCAPTCHA.__CONFIG_CAPTCHA_LENGTH],
                captcha_config[MarkCAPTCHA.__CONFIG_THRESHOLD])

        #.get(x, y) not working.
        if config_filename not in self.__predictors:
            self.__predictors[config_filename] = Factory().create(Factory.CLASS_PREDICT) \
            .initialise(Path(MarkCAPTCHA.__PATH_MODELS + captcha_config[MarkCAPTCHA.__CONFIG_MODEL_FILENAME]),
                Factory().create(Factory.CLASS_PICKLEPARSER) \
            .parse(MarkCAPTCHA.__PATH_MODELS + captcha_config[MarkCAPTCHA.__CONFIG_LABEL_FILENAME]) \
            .getParsedContent())

        return self.__predictors[config_filename].predict(segmented_captcha,
                    Factory().create(Factory.CLASS_IMAGEPROCESSING_SECTION),
                    self.__model_config.getParsedContent()[MarkCAPTCHA.__MODEL_IMAGE_SIZE],
                    show) \
                .getResult()

    def getImageFilename(self):
        return self.__image_filename

    def __checkForConfig(self, config_name):
        '''
            key in dict is the second fastest look up, outperformed by try except.
        '''
        if config_name not in self.__image_configs:
            raise Exception("Invalid configuration name: {}".format(config_name))

        return True

    def __classFunctionsFromJSON(self, config, image_object):
        '''
        Process a image based on its JSON functions.
        @params:
            config        - Required  : JSON functions key configuration.  (Dictionary)
            image_object  - Required  : ImageProcessing Object (ImageProcessing)
        '''
        for function in config:
            for function_name, function_value in function.items():
                try:
                    getattr(image_object, function_name.split("_", 1)[0])(*function_value)
                except Exception as ex:
                    raise Exception("Invalid image processing function provided: {}:{}\nError: {}" \
                        .format(function_name, function_value, ex))

        return image_object

    #Credit: https://gist.github.com/aubricus/f91fb55dc6ba5557fbab06119420dd6a
    def printProgress(self, iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
        '''
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            bar_length  - Optional  : character length of bar (Int)
        '''

        str_format = "{0:." + str(decimals) + "f}"
        percents = str_format.format(100 * (iteration / float(total)))
        filled_length = int(round(bar_length * iteration / float(total)))
        bar = '█' * filled_length + '-' * (bar_length - filled_length)

        sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

        if iteration == total:
            sys.stdout.write('\n')
        sys.stdout.flush()
