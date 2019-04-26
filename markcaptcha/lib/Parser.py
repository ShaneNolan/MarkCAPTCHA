from abc import ABC, abstractmethod
from collections import OrderedDict
import json, pickle, os


class Parser(ABC):

    def __init__(self):
        if type(self) is Parser:
            raise Exception('Parser is an abstract class and cannot be instantiated.')
        self.parsed_content = None

    def pathExists(self, path):
        '''
        Checks if a given path exists.
        @params:
            path   - Required  : path to file (String)
        '''

        if not os.path.exists(path):
            raise Exception("Path: {} doesn't exist.".format(path))

    @abstractmethod
    def parse(self, path):
        '''
        Parse content based on a path.
        @params:
            path   - Required  : path to file (String)
        '''

        pass

    def getParsedContent(self):
        if self.parsed_content == None:
            raise Exception("No parsed content exists.")
        return self.parsed_content


class JSONParser(Parser):

    def __init__(self):
        super().__init__()
        return

    def parse(self, path):
        super().pathExists(path)

        try:
            self.parsed_content = json.load(open(path), object_pairs_hook=OrderedDict)
        except Exception as ex:
            raise Exception("Unable to parse JSON: {}\nError: {}".format(path, ex))

        return self


    def addValue(self, path, key, value):
        self.parsed_content.update({key : value})

        try:
            with open(path, 'w') as f:
                json.dump(self.parsed_content, f)
            f.close()
        except Exception as ex:
            raise Exception("Unable to update JSON: {}\nError: {}".format(path, ex))


class PickleParser(Parser):

    def __init__(self):
        super().__init__()
        return

    def parse(self, path):
        super().pathExists(path)

        try:
            with open(path, "rb") as f:
                self.parsed_content = pickle.load(f)
            f.close()
        except Exception as ex:
            raise Exception("Unable to parse Pickle: {}\nError: {}".format(path, ex))

        return self

    def save(self, path, content):
        try:
            with open(str(path), "wb") as f:
                pickle.dump(content, f)
            f.close()
        except Exception as ex:
            raise Exception("Unable to save Pickle content: {}\nError: {}".format(path, ex))
