from tkinter import *
from tkinter import messagebox
from winreg import *

TITLE = "Alto's editor"
RESOLUTION = "200x50"
PATH = r"Software\Team Alto\The Alto Collection"


def get_coins():
    key = OpenKey(HKEY_CURRENT_USER, PATH)
    for i in range(0, QueryInfoKey(key)[1]):
        entry = EnumValue(key, i)
        if re.search("Save.StatProfile.coinsAd", entry[0]):
            return entry


COINS = get_coins()[1]
REG_PATH = get_coins()[0]


def set_coins(value):
    try:
        key = OpenKey(HKEY_CURRENT_USER, PATH, 0, KEY_ALL_ACCESS)
        SetValueEx(key, REG_PATH, 0, REG_DWORD, int(value))
        CloseKey(key)
    except PermissionError:
        messagebox.showinfo('Access denied', 'Please, run the program as admin!')


class MainWindow:
    root = Tk()
    #root.iconbitmap("icon.ico")
    root.title(TITLE)
    root.geometry(RESOLUTION)
    root.resizable(False, False)


class Frame(MainWindow):
    frame = Frame(MainWindow.root)
    frame.grid(column=0, row=0, sticky=(N, W, E, S))

    coinsLabel = Label(frame, text="Coins: ")
    coinsLabel.grid(column=1, row=1)

    coins = StringVar(frame, COINS)
    coinsEntry = Entry(frame, width=12, justify=CENTER, textvariable=coins)
    coinsEntry.grid(column=2, row=1, sticky=(W, E))
    coinsEntry.update_idletasks()
    submit = Button(frame, text="Change!", command=lambda: set_coins(Frame.coins.get()))
    submit.grid(column=3, row=1)

    # Create padding to all elements
    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)


MainWindow.root.mainloop()
