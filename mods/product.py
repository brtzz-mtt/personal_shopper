#from .category import Category, Subcategory
#from .unit import Unit

class Product():

    def __init__(self,
        name: str,
        category: str,#Category, # TBD
        subcategory: str,#Subcategory, # TBD
        quantity: float = None,
        unit: str = None#unit: Unit = None # TBD
    ) -> None:
        self.__name = name
        self.__category = category#.get_name() # TBD
        self.__subcategory = subcategory#.get_name() # TBD
        self.__quantity = quantity
        self.__unit = unit#self.__unit = unit.get_name() see Unit from .unit, TBD

    def get_category(self) -> str:
        return self.__category

    def get_name(self) -> str:
        return self.__name

    def get_quantity(self) -> float:
        return self.__quantity

    def get_subcategory(self) -> str:
        return self.__subcategory

    def get_unit(self) -> str:
        return self.__unit

    def to_string(self) -> str:
        string_elements = [
            str(self.get_quantity()).strip(),
            self.get_unit().strip(),
            self.get_name().strip()
        ]
        string = " ".join(string_elements)
        return string.strip()
