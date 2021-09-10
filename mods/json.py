import json
from .log import Log

class Json():

    def __init__(self,
        file_path: str
    ) -> None:
        self.__log = Log()
        self.__file = None
        self.__obj = {}
        try:
            self.file_path = file_path
            self.__file = open(file_path, 'r')
            self.__log.log("opened file at path: " + self.file_path)
            self.__obj = json.load(self.__file)
            self.__log.log("json was correctly loaded from " + self.file_path)
            self.__file.close()
        except:
            self.__log.log("WARNING: file " + self.file_path + " could not be loaded")

    def set(self,
        obj: object
    ) -> bool:
        try:
            self.__obj = obj
        except:
            return False
        return True

    def get(self) -> object:
        return self.__obj

    def save(self) -> bool:
        try:
            with open(self.file_path, 'w+') as self.__file: # file pointer closing automatically after exiting 'with' block..
                json.dump(self.__obj, self.__file, indent = 4)
            self.__log.log("json object was dumped in " + self.file_path)
        except:
            self.__log.log("ERROR while dumping json object in " + self.file_path)
            return False
        return True
