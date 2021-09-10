import tkinter
from cnf import *

# CONFIGURATION
root = tkinter.Tk()
root.title(APP_TITLE)
root.minsize(550, 550) # 810..
root.resizable(False, False)
root.rowconfigure(0, weight = 1)
for i in range(1, 11): # TBD check max row and change this accordingly
    root.rowconfigure(i, weight = 2)
root.rowconfigure(11, weight = 1)
root.columnconfigure(0, weight = 1)
root.columnconfigure(1, weight = 1)

# STYLEGUIDE
COLOR_GREY_DARKER = '#555'
COLOR_GREY_DARK = '#777'
COLOR_GREY = '#999'
COLOR_GREY_LIGHT = '#bbb'
COLOR_GREY_LIGHTER = '#ddd'

WIDTH_DEFAULT = 24

PADDING_DEFAULT = 16
PADDING_DEFAULT_HALF = PADDING_DEFAULT / 2
PADDING_DEFAULT_DOUBLE = PADDING_DEFAULT * 2
