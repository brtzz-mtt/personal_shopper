import os
from cnf import SAVE_PATH
from .json import Json
from .log import Log
from .utility import generate_md5_hash
#from .category import Category, Subcategory
from .product import Product
#from .unit import Unit

class Listing():

    __loaded_listings = []

    def __init__(self,
        name: str,
        hash: str = ''
    ) -> None:
        self.__log = Log()
        self.__hash = (generate_md5_hash(), hash)[hash != '']
        self.__name = name
        self.__obj = {'name': name, 'items': {}}

    def delete_item(self, # from internal data object
        path: list
    ) -> bool:
        self.__obj['items'][path[0]][path[1]].remove(path[2])
        if not len(self.__obj['items'][path[0]][path[1]]):
            del self.__obj['items'][path[0]][path[1]]
            if not len(self.__obj['items'][path[0]]):
                del self.__obj['items'][path[0]]
        return self.save()

    def get_hash(self) -> str:
        return self.__hash

    def get_items(self) -> list:
        items = []
        for category, subcategories in self.__obj['items'].items():
            for subcategory, products in subcategories.items():
                for product in products:
                    items.append([category, subcategory, product])
        return items

    def get_name(self) -> str:
        return self.__name

    def load(self) -> dict:
        self.__obj = Json(SAVE_PATH + self.__hash + '.json').get()
        self.__name = self.__obj['name']
        return self

    @classmethod
    def load_listings(cls) -> list:
        cls.__loaded_listings = []
        files = [file for file in os.listdir(SAVE_PATH) if os.path.isfile(os.path.join(SAVE_PATH, file))]
        for file in files:
            obj = Json(SAVE_PATH + file).get()
            listing = Listing(obj['name'], file[0:-5])
            listing.__obj = obj
            cls.__loaded_listings.append(listing)
        if len(cls.__loaded_listings):
            Log.write("loaded " + str(len(cls.__loaded_listings)) + " listing(s) from save location")
        return sorted(cls.__loaded_listings, key = lambda x: x.__name) # this sorts listings list by their 'name' attributes..

    def save(self) -> bool:
        json = Json(SAVE_PATH + self.__hash + '.json')
        if json.set(self.__obj):
            json.save()
            return True
        return False

    @classmethod
    def save_listings(cls) -> bool:
        for item in cls.__loaded_listings:
            item.save()

    def set_name(self,
        name: str
    ) -> bool:
        try:
            self.__name = name
            self.__obj.update({'name': name})
        except:
            return False
        return True

    def to_string(self,
        add_title: bool = False,
        show_categories = True, # additional flag in order to make list more compact..
        show_subcategories = True # additional flag in order to make list more compact..
    ) -> str:
        output = ('', self.get_name().upper() + ":\n")[add_title]
        for category, subcategories in self.__obj['items'].items():
            if show_categories:
                output += category + "\n"
            for subcategory, products in subcategories.items():
                if show_subcategories:
                    output += "- " + subcategory + "\n"
                for product in products:
                    if show_subcategories:
                        output += "  "
                    output += "- " + product + "\n"
        return output

    def update_item(self,
        name: str,
        category: str,
        subcategory: str,
        quantity: float,
        unit: str
    ) -> Product or None:
        item = Product(name,
            category,
            subcategory,
            quantity,
            unit
        )
        item_string = item.to_string()

        if category in self.__obj['items'].keys():
            if subcategory in self.__obj['items'][category].keys():
                if item_string in self.__obj['items'][category][subcategory]: # checking for duplicates..
                    return False
            else:
                self.__obj['items'][category].update({subcategory: []})
                self.__obj['items'][category] = dict(sorted(self.__obj['items'][category].items())) # sorts items's category per subcategory name before update..
        else:
            self.__obj['items'].update({category: {}})
            self.__obj['items'][category].update({subcategory: []})
            self.__obj['items'] = dict(sorted(self.__obj['items'].items())) # sorts items per category name before update..
        self.__obj['items'][category][subcategory].append(item_string)
        self.__obj['items'][category][subcategory].sort()

        self.__log.log("item '" + item_string + "' added under category '" + category + "', subcategory '" + subcategory + "'")
        
        return item
