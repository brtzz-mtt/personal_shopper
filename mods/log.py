import datetime

class Log():

    __file_path = 'debug.log' # it will be created/saved in app's root folder

    def __del__(self):
        self.__file.close()

    def __init__(self) -> None:
        try:
            self.__file = open(self.__file_path, 'a+')
        except ValueError as e: # prevents application's crash if path/file not writable..
            print(e)

    def log(self,
        message: str,
        print_in_cli = True
    ) -> None:
        now = datetime.datetime.now()
        message = now.strftime("%y-%m-%d @ %H:%M:%S") + " | " + message
        self.__file.write(message + "\n")
        if print_in_cli:
            print(message)

    @staticmethod # for other class/static usages..
    def write(message: str,
        print_in_cli = True
    ) -> None:
        log = Log()
        log.log(message, print_in_cli)
