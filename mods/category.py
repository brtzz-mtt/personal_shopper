class Category():

    def __init__(self,
        name: str
    ) -> None:
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def save(self) -> bool:
        pass

class Subcategory(Category):

    def __init__(self,
        name: str,
        parent: str
    ) -> None:
        super().__init__(name)
        self.__parent = parent

    def get_parent(self) -> str:
        return self.__parent

    def save(self) -> bool:
        pass
