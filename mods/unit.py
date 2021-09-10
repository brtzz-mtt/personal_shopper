class Unit(): # support class to Product objects, TBD with future autocomplete for GUI..

    def __init__(self,
        name: str
    ) -> None:
        self.__name = name

    def get_name(self) -> str:
        return self.__name
