import tkinter
import webbrowser
from tkinter import Button, font, Label, Listbox, messagebox, OptionMenu, StringVar, Text, Tk, ttk
from cnf import *
from mods.listing import Listing
from mods.log import Log

class App():

    __current_listing = None # will contain a Listing entity to work on in edit mode
    __SPLIT_STRING = " > "

    def __del__(self):
        self.save_status()

    def __init__(self,
        data_categories: dict,
        data_units: tuple,
        data_categories_custom: dict = {},
        data_units_custom: tuple = ()
    ) -> None:
        self.__log = Log()
        self.__data_categories = data_categories
        self.__data_categories_custom = data_categories_custom
        self.__data_units = data_units
        self.__data_units_custom = data_units_custom
        self.__data = {}
        self.listings = []

        subcategories = 0
        for k in self.__data_categories:
            subcategories += len(self.__data_categories[k])
        self.__log.log("loaded " + str(len(self.__data_categories)) + " product categories with " + str(subcategories) + " sub-categories from data")

        self.__log.log("loaded " + str(len(self.__data_units)) + " measurement units from data")

        subcategories_custom = 0
        for k in self.__data_categories_custom:
            subcategories_custom += len(self.__data_categories_custom[k])
        self.__log.log("loaded " + str(len(self.__data_categories_custom)) + " custom product categories with " + str(subcategories_custom) + " custom sub-categories from custom data")

        self.__log.log("loaded " + str(len(self.__data_units_custom)) + " custom measurement units from custom data")

        self.merge_data() # predefined and custom categories/units in a single list..

        self.load_listings() # populates object's listing list (ordered)

    @classmethod
    def clear_current_listing(cls) -> None:
        cls.__current_listing = None
        Log.write("main app current active listing was reset")

    @classmethod
    def delete_product(cls,
        entry: str
    ) -> bool:
        if cls.__current_listing.delete_item(entry.split(cls.__SPLIT_STRING)):
            Log.write("product '" + entry + "' was removed from listing")
            return True
        Log.write("ERROR removing product '" + entry + "' from listing")
        return False

    def get_categories(self) -> list:
        return list(self.__data['categories'].keys())

    @classmethod
    def get_current_listing(cls) -> object:
        return cls.__current_listing

    def get_subcategories(self,
        category: str = DEFAULT_STRING
    ) -> list:
        return self.__data['categories'][category]

    def get_units(self) -> list: # TBD, returns predefined units to be used in a autocmplete text widget or something similar, ATM not used..
        return self.__data['units']

    def load_listings(self) -> list or bool:
        try:
            self.listings = Listing.load_listings()
        except:
            return False
        return self.listings
 
    def merge_data(self) -> dict: # TBD replace 'default' value with '' or at least 'none'..
        categories = self.__data_categories
        categories[DEFAULT_STRING] = []
        for key, values in self.__data_categories_custom.items():
            if key not in categories:
                categories[key] = []
            for value in values:
                categories[key].append(value)

        sorted_categories = {}
        for key in sorted(categories):
            sorted_categories[key] = [DEFAULT_STRING] + categories[key]
        self.__data['categories'] = sorted_categories

        units = self.__data_units
        for item in self.__data_units_custom:
            units.append(item)
        units.sort()
        self.__data['units'] = units

        return self.__data # sets and returns predefined categories and units from data folder..

    @classmethod
    def product_to_string(cls, # formats product data in a string (used as a listbox entry)
        category: str,
        subcategory: str,
        product: str
    ):
        return category + cls.__SPLIT_STRING + subcategory + cls.__SPLIT_STRING + product

    def save_product(self,
        name: str,
        category: str,
        subcategory: str,
        quantity: float,
        unit: str
    ) -> str or False:
        product = self.__current_listing.update_item(name,
            category,
            subcategory,
            quantity,
            unit
        )
        if product:
            self.__current_listing.save()
            return self.product_to_string(category, subcategory, product.to_string())
        self.__log.log("ERROR creating product entry from attributes data")
        return False

    def save_status(self) -> bool: # called on closing GUI / destroying main class object
        try:
            Listing.save_listings() # saves all currently loaded listings
        except:
            self.__log.log("ERROR saving listings status in main app")
            return False
        return True

    @classmethod
    def set_current_listing(cls,
        data: object
    ) -> bool:
        try:
            cls.__current_listing = data
        except:
            return False
        return True

main = App(DATA_CATEGORIES, DATA_UNITS, DATA_CATEGORIES_CUSTOM, DATA_UNITS_CUSTOM)

from gui import *

# FUNCTIONs
def open_web_link(event) -> None:
    webbrowser.open_new(WEB_URL)

def clear_root() -> None:
    for item in root.grid_slaves():
        if int(item.grid_info()["row"]) < 11: # footer (at 11th row) remains
            item.grid_forget()

def back_to_main() -> None:
    clear_root()
    start_grid()

def validate_listing_name(event) -> bool: # button is active only if entry widget contains some string..
    if len(entry_listing_name.get()) != 0:
        button_listing_save['cursor'] = 'hand2'
        button_listing_save['state'] = tkinter.NORMAL
        return True
    button_listing_save['cursor'] = 'X_cursor'
    button_listing_save['state'] = tkinter.DISABLED
    return False

def validate_product_name(event) -> bool: # button is active only if entry widget contains some string..
    if main.get_current_listing() \
    and len(entry_product_name.get()) != 0:
        button_product_save['cursor'] = 'hand2'
        button_product_save['state'] = tkinter.NORMAL
        return True
    button_product_save['cursor'] = 'X_cursor'
    button_product_save['state'] = tkinter.DISABLED
    return False

def listing_new() -> None:
    main.clear_current_listing()
    listing_add()

def listing_add() -> None:
    clear_root()
    entry_listing_name.delete(0, tkinter.END)
    listbox_listing.delete(0, tkinter.END)

    current_listing = main.get_current_listing()
    if current_listing:
        entry_listing_name.insert(0, current_listing.get_name())
        label_header_listing_edit.grid(row = 0, column = 0, columnspan = 2, ipadx = PADDING_DEFAULT, ipady = PADDING_DEFAULT, sticky = 'new')
        label_listing_hash.grid(row = 1, column = 0, columnspan = 2, ipadx = PADDING_DEFAULT, ipady = PADDING_DEFAULT, sticky = 'nsew')
        label_listing_hash_var.set("Listing's hash: " + current_listing.get_hash())
        current_items = current_listing.get_items()
        for i in range(len(current_items)):
            listbox_listing.insert(i, main.product_to_string(current_items[i][0], current_items[i][1], current_items[i][2]))
    else:
        label_header_listing_add.grid(row = 0, column = 0, columnspan = 2, ipadx = PADDING_DEFAULT, ipady = PADDING_DEFAULT, sticky = 'new')
        label_listing_add.grid(row = 1, column = 0, columnspan = 2, ipadx = PADDING_DEFAULT, ipady = PADDING_DEFAULT, sticky = 'nsew')

    # LISTINGs
    label_listing_name.grid(row = 2, column = 0, ipadx = PADDING_DEFAULT, ipady = PADDING_DEFAULT, sticky = 'e')
    entry_listing_name.grid(row = 2, column = 1, padx = PADDING_DEFAULT_HALF, pady = PADDING_DEFAULT_HALF)
    listbox_listing.grid(row = 3, column = 0, columnspan = 2, padx = PADDING_DEFAULT, pady = PADDING_DEFAULT, ipadx = PADDING_DEFAULT_HALF, ipady = PADDING_DEFAULT_HALF, sticky = 'nsew')

    # PRODUCTs
    label_listing_product.grid(row = 4, column = 0, ipadx = PADDING_DEFAULT, ipady = PADDING_DEFAULT, sticky = 'e')
    entry_product_name.grid(row = 4, column = 1, padx = PADDING_DEFAULT_HALF, pady = PADDING_DEFAULT_HALF)
    label_optional_quantity.grid(row = 5, column = 0, padx = PADDING_DEFAULT_HALF, pady = PADDING_DEFAULT_HALF, sticky = 's')
    label_optional_unit.grid(row = 5, column = 1, padx = PADDING_DEFAULT_HALF, pady = PADDING_DEFAULT_HALF, sticky = 's')
    entry_product_quantity.grid(row = 6, column = 0, padx = PADDING_DEFAULT_HALF, pady = PADDING_DEFAULT_HALF, sticky = 'n')
    entry_product_unit.grid(row = 6, column = 1, padx = PADDING_DEFAULT_HALF, pady = PADDING_DEFAULT_HALF, sticky = 'n')

    # CATEGORIEs & SUBCATEGORIESs
    label_optional_category.grid(row = 7, column = 0, padx = PADDING_DEFAULT_HALF, pady = PADDING_DEFAULT_HALF, sticky = 's')
    label_optional_subcategory.grid(row = 7, column = 1, padx = PADDING_DEFAULT_HALF, pady = PADDING_DEFAULT_HALF, sticky = 's')
    options_category.grid(row = 8, column = 0, sticky = 'n')
    options_subcategory.grid(row = 8, column = 1, sticky = 'n')

    button_product_delete.grid(row = 9, column = 0, padx = PADDING_DEFAULT, pady = PADDING_DEFAULT)
    button_product_save.grid(row = 9, column = 1, padx = PADDING_DEFAULT, pady = PADDING_DEFAULT)
    validate_product_name(button_product_save)

    button_back.grid(row = 10, column = 0, padx = PADDING_DEFAULT_HALF, pady = PADDING_DEFAULT_HALF)
    button_listing_save.grid(row = 10, column = 1, padx = PADDING_DEFAULT, pady = PADDING_DEFAULT)
    validate_listing_name(button_listing_save)

def listing_edit():
    listing_add() # mmm.. refactoring needed..

def listing_save() -> None:
    current_listing = main.get_current_listing()
    if current_listing:
        current_listing.set_name(entry_listing_name.get())
        Log.write("saving current listing")
    else:
        current_listing = Listing(entry_listing_name.get())
        main.set_current_listing(current_listing)
        validate_product_name(current_listing)
        Log.write("saving new listing")
    current_listing.save()
    main.load_listings()
    if current_listing.get_items():
        back_to_main()

def listing_save_callback(event) -> None: # called by <Return> binding.. just an experiment
    if validate_listing_name(event):
        listing_save()

def listing_copy(): # copy to clipboard..
    tk = Tk()
    tk.withdraw()
    tk.clipboard_clear()
    tk.clipboard_append(main.get_current_listing().to_string(True))
    tk.update()
    tk.destroy()

def product_save() -> None:
    entry = main.save_product(entry_product_name.get(),
        options_category_selected.get(),
        options_subcategory_selected.get(),
        entry_product_quantity.get(),
        entry_product_unit.get()
    )
    if entry:
        listbox_listing_selection = listbox_listing.curselection()
        index = 0
        if len(listbox_listing_selection):
            index = listbox_listing_selection[0]
        listbox_listing.insert(index, entry)
        button_listing_save['cursor'] = 'X_cursor'
        button_listing_save['state'] = tkinter.DISABLED

def product_delete() -> None:
    listbox_listing_selection = listbox_listing.curselection()
    entry = listbox_listing.get(listbox_listing_selection)
    if len(listbox_listing_selection) \
    and messagebox.askyesno("Deleting product..", "Are you sure?"):
        listbox_listing.delete(listbox_listing_selection)
        main.delete_product(entry)
        button_listing_save['cursor'] = 'X_cursor'
        button_listing_save['state'] = tkinter.DISABLED

def start_grid() -> None:
    label_logo.grid(row = 0, column = 0, columnspan = 2, ipadx = PADDING_DEFAULT, ipady = PADDING_DEFAULT, sticky = 'new') # header (only on main screen)
    if len(main.listings):
        create_tabs(main.listings)
        if not main.get_current_listing():
            main.set_current_listing(main.listings[0])
        else:
            #notebook.select(main.listings.index(main.get_current_listing())) not working because of object different pointers..
            notebook.select(next((i for i, item in enumerate(main.listings) if item.get_hash() == main.get_current_listing().get_hash()), -1))
        button_listing_delete.grid(row = 9, column = 0, padx = PADDING_DEFAULT, pady = PADDING_DEFAULT)
        button_listing_edit.grid(row = 9, column = 1, padx = PADDING_DEFAULT, pady = PADDING_DEFAULT)
        button_listing_copy.grid(row = 10, column = 0, padx = PADDING_DEFAULT, pady = PADDING_DEFAULT)
        button_listing_new.grid(row = 10, column = 1, padx = PADDING_DEFAULT, pady = PADDING_DEFAULT)
    else:
        label_start.grid(row = 1, column = 0, columnspan = 2, ipadx = PADDING_DEFAULT, ipady = PADDING_DEFAULT, sticky = 'nsew')
        button_start.grid(row = 10, column = 0, columnspan = 2, padx = PADDING_DEFAULT, pady = PADDING_DEFAULT, ipadx = PADDING_DEFAULT, ipady = PADDING_DEFAULT, sticky = 'nsew') # actions

# TABs & LISTBOXes (all logic together, for convenience..)
notebook = ttk.Notebook(root)

def tab_select_callback(event):
    main.set_current_listing(main.listings[notebook.index('current')])

def create_tabs(listings = []) -> None:
    for tab in notebook.winfo_children():
        tab.destroy()
    for listing in listings: # creates and populates a tab (frame) for every loaded listing
        tab = ttk.Frame(notebook)
        tab_text = Text(tab,
            padx = PADDING_DEFAULT_HALF,
            pady = PADDING_DEFAULT_HALF
        )
        tab_text.pack(expand = True)
        tab_text.insert(tkinter.INSERT, listing.to_string())
        tab_text['state'] = tkinter.DISABLED # in order to avoid direct modifications (maybe a future feature..)
        notebook.add(tab,
            text = listing.get_name()
        )
    notebook.grid(row = 1, column = 0, rowspan = 8, columnspan = 2, sticky = "nsew")
    notebook.bind('<<NotebookTabChanged>>', tab_select_callback) # sets current listing accordingly..

def listbox_listing_select(event) -> bool: # button is active only if a listbox widget entry is actually selected..
    if event.widget.curselection():
        button_product_delete['cursor'] = 'hand2'
        button_product_delete['state'] = tkinter.NORMAL
        return True
    button_product_delete['cursor'] = 'X_cursor'
    button_product_delete['state'] = tkinter.DISABLED
    return False

listbox_listing = Listbox(root,
    selectmode = tkinter.SINGLE
)

listbox_listing.bind('<<ListboxSelect>>', listbox_listing_select)

# IMAGEs, icons are from https://www.flaticon.com/search?author_id=1&style_id=153&type=standard&word=web
image_logo = tkinter.PhotoImage(file = IMGS_PATH + 'logo.png')
image_logo_small = image_logo.subsample(2)

image_icon_github = tkinter.PhotoImage(file = IMGS_PATH + 'icon_github_inv.png')
image_icon_github_small = image_icon_github.subsample(16)
image_icon_github_smaller = image_icon_github.subsample(24)

image_icon_yes = tkinter.PhotoImage(file = IMGS_PATH + 'icon_yes.png')
image_icon_yes_small = image_icon_yes.subsample(16)
image_icon_yes_smaller = image_icon_yes.subsample(24)

image_icon_no = tkinter.PhotoImage(file = IMGS_PATH + 'icon_no.png')
image_icon_no_small = image_icon_no.subsample(16)
image_icon_no_smaller = image_icon_no.subsample(24)

image_icon_back = tkinter.PhotoImage(file = IMGS_PATH + 'icon_back.png')
image_icon_back_small = image_icon_back.subsample(16)
image_icon_back_smaller = image_icon_back.subsample(24)

image_icon_listing_add = tkinter.PhotoImage(file = IMGS_PATH + 'icon_listing_add.png')
image_icon_listing_add_small = image_icon_listing_add.subsample(16)
image_icon_listing_add_smaller = image_icon_listing_add.subsample(24)

image_icon_listing_edit = tkinter.PhotoImage(file = IMGS_PATH + 'icon_listing_edit.png')
image_icon_listing_edit_small = image_icon_listing_edit.subsample(16)
image_icon_listing_edit_smaller = image_icon_listing_edit.subsample(24)

image_icon_listing_copy = tkinter.PhotoImage(file = IMGS_PATH + 'icon_listing_copy.png')
image_icon_listing_copy_small = image_icon_listing_copy.subsample(16)
image_icon_listing_copy_smaller = image_icon_listing_copy.subsample(24)

image_icon_save = tkinter.PhotoImage(file = IMGS_PATH + 'icon_save.png')
image_icon_save_small = image_icon_save.subsample(16)
image_icon_save_smaller = image_icon_save.subsample(24)

image_icon_delete = tkinter.PhotoImage(file = IMGS_PATH + 'icon_delete.png')
image_icon_delete_small = image_icon_delete.subsample(16)
image_icon_delete_smaller = image_icon_delete.subsample(24)

# FONTs
font_header = font.Font(size = 24)
font_button = font.Font(size = 16, weight = 'bold')
font_footer = font.Font(size = 14)

# LABELs
label_logo = Label(root,
    image = image_logo_small,
    background = COLOR_GREY_LIGHT
)

label_start = Label(root,
    text = "Hallo!\n\n..it seems you don't have any shopping list yet.\n\nLet's start with a fresh one!"
)

label_header_listing_add = Label(root,
    text = " Create new listing",
    font = font_header,
    justify = tkinter.LEFT,
    image = image_icon_listing_add_small,
    compound = tkinter.LEFT,
    background = COLOR_GREY_LIGHTER
)

label_header_listing_edit = Label(root,
    text = " Edit listing",
    font = font_header,
    justify = tkinter.LEFT,
    image = image_icon_listing_edit_small,
    compound = tkinter.LEFT,
    background = COLOR_GREY_LIGHTER
)

label_listing_add = Label(root,
    text = "Please enter a name for your new listing, e.g.:\n'My Wishes', 'Supermarket' or 'xMas presents'.."
)

label_listing_hash_var = StringVar(root, '')
label_listing_hash = Label(root,
    textvariable = label_listing_hash_var
)

label_listing_name = Label(root,
    text = "Listing name:"
)

label_listing_product = Label(root,
    text = "Add/edit product:"
)

label_optional_quantity = Label(root,
    text = "Quantity (optional):"
)

label_optional_unit = Label(root,
    text = "Unit (optional):"
)

label_optional_category = Label(root,
    text = "Category (optional):"
)

label_optional_subcategory = Label(root,
    text = "Subcategory (optional):"
)

label_copyright = Label(root,
    text = COPYRIGHT + " ", # beacause of the image..
    font = font_footer,
    fg = COLOR_GREY_DARKER,
    background = COLOR_GREY_DARK,
    cursor = 'hand2',
    image = image_icon_github_smaller,
    compound = tkinter.RIGHT
)

# ENTRIEs
entry_listing_name = tkinter.Entry(root,
    width = WIDTH_DEFAULT,
    borderwidth = PADDING_DEFAULT_HALF,
    relief = tkinter.FLAT
)

entry_product_name = tkinter.Entry(root,
    width = WIDTH_DEFAULT,
    borderwidth = PADDING_DEFAULT_HALF,
    relief = tkinter.FLAT
)

entry_product_quantity = tkinter.Entry(root,
    width = WIDTH_DEFAULT,
    borderwidth = PADDING_DEFAULT_HALF,
    relief = tkinter.FLAT
)

entry_product_unit = tkinter.Entry(root, # TBD add autocomplete
    width = WIDTH_DEFAULT,
    borderwidth = PADDING_DEFAULT_HALF,
    relief = tkinter.FLAT
)

# OPTIONs BEWARE, some magic ahead..
def update_options_subcategory(*args):
    options_subcategory_selected.set('')
    options_subcategory['menu'].delete(0, tkinter.END)
    subcategories = main.get_subcategories(options_category_selected.get())
    for item in subcategories:
        options_subcategory['menu'].add_command(label = item, command = tkinter._setit(options_subcategory_selected, item)) # needed after "reset" of widget..
    options_subcategory_selected.set(subcategories[0])

options_category_selected = StringVar(root, DEFAULT_STRING)
options_category = OptionMenu(root, options_category_selected, *main.get_categories())
options_category_selected.trace("w", update_options_subcategory) # traces changing (writing) of tkinter StringVar entity..

options_subcategory_selected = StringVar(root, DEFAULT_STRING)
options_subcategory = OptionMenu(root, options_subcategory_selected, *main.get_subcategories(options_category_selected.get()))

# BUTTONs, see https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html too..
button_start = Button(root,
    text = "BEGIN",
    font = font_button,
    cursor = 'hand2',
    image = image_icon_yes_smaller,
    compound = tkinter.RIGHT,
    command = listing_add
)

button_back = Button(root,
    text = "BACK",
    font = font_button,
    cursor = 'hand2',
    image = image_icon_back_smaller,
    compound = tkinter.RIGHT,
    command = back_to_main
)

button_listing_new = Button(root,
    text = "NEW listing",
    font = font_button,
    cursor = 'hand2',
    image = image_icon_listing_add_smaller,
    compound = tkinter.RIGHT,
    command = listing_new
)

button_listing_delete = Button(root,
    text = "DELETE",
    font = font_button,
    cursor = 'X_cursor',
    image = image_icon_delete_smaller,
    compound = tkinter.RIGHT,
    #command = listing_delete, TBD
    state = tkinter.DISABLED
)

button_listing_edit = Button(root,
    text = "EDIT listing",
    font = font_button,
    cursor = 'hand2',
    image = image_icon_listing_edit_smaller,
    compound = tkinter.RIGHT,
    command = listing_edit
)

button_listing_save = Button(root,
    text = "SAVE listing",
    font = font_button,
    cursor = 'X_cursor',
    image = image_icon_save_smaller,
    compound = tkinter.RIGHT,
    command = listing_save,
    state = tkinter.DISABLED
)

button_listing_copy = Button(root,
    text = "COPY to clipboard",
    font = font_button,
    cursor = 'hand2',
    image = image_icon_listing_copy_smaller,
    compound = tkinter.RIGHT,
    command = listing_copy
)

button_product_delete = Button(root,
    text = "DELETE selected",
    font = font_button,
    cursor = 'X_cursor',
    image = image_icon_delete_smaller,
    compound = tkinter.RIGHT,
    command = product_delete,
    state = tkinter.DISABLED
)

button_product_save = Button(root,
    text = "SAVE product",
    font = font_button,
    cursor = 'X_cursor',
    image = image_icon_save_smaller,
    compound = tkinter.RIGHT,
    command = product_save,
    state = tkinter.DISABLED
)

# BINDINGs
label_copyright.bind('<Button-1>', open_web_link) # just for fun..
entry_listing_name.bind('<Any-KeyRelease>', validate_listing_name)
entry_listing_name.bind('<Return>', listing_save_callback)
entry_product_name.bind('<Any-KeyRelease>', validate_product_name)

# PACKING
start_grid() # real main packing logic, only row 11 (the footer, see next line..) remains constant across whole application flow
label_copyright.grid(row = 11, column = 0, columnspan = 2, ipadx = PADDING_DEFAULT_HALF, ipady = PADDING_DEFAULT_HALF, sticky = 'sew') # footer

# PROTOCOLs
def wm_delete_window():
    if messagebox.askokcancel("Exiting..", "..are you sure?"):
        main.save_status()
        root.destroy()

root.protocol("WM_DELETE_WINDOW", wm_delete_window)

root.mainloop()
