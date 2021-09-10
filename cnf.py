import os
from mods.json import Json

# CONSTANTs
DEFAULT_STRING = 'DEFAULT' # used internally, all other 'constants' names should be self-explaining

BASE_PATH = os.path.dirname(__file__) + '/'
DATA_PATH = BASE_PATH + 'data/'
IMGS_PATH = BASE_PATH + 'imgs/'
SAVE_PATH = BASE_PATH + 'save/'
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

DATA_CATEGORIES = Json(DATA_PATH + 'categories.json').get()
DATA_CATEGORIES_CUSTOM = Json(DATA_PATH + 'categories_custom.json').get()
DATA_UNITS = Json(DATA_PATH + 'units.json').get()
DATA_UNITS_CUSTOM = Json(DATA_PATH + 'units_custom.json').get()

with open(BASE_PATH + 'README.md') as readme_file:
    APP_TITLE = "Personal Shopper v" + readme_file.readline().strip()
    for line in readme_file:
        pass
    COPYRIGHT = line

WEB_URL = 'https://github.com/brtzz-mtt/brtzz-mtt.github.io' # TBD create and update a dedicated repository
