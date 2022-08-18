from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import scrolledtext
from datetime import datetime
def convStrToNum(s):
    if s == "\x00":
        return b"\x00"
    sAsBytes = bytes(s, encoding="utf-8")
    sAsNumber = int.from_bytes(sAsBytes, byteorder="little")
    return (sAsNumber - 65).to_bytes(1, byteorder="little")
def convMOD():
    blankString = ""
    openedFile = filedialog.askopenfile(mode='rb+',filetypes=['"Poly Tracker" {.ptm}'])
    modComment = commentObject.get("1.0", "end")
    chnlPan = chnObj.get("1.0", "end")
    
    commentsTable = []
    for line in modComment.split('\n'):
        commentsTable.append(line.ljust(28, "\x00"))
    for i in range(32):
        if len(commentsTable) < 32:
            commentsTable.append(("").ljust(28, "\x00"))
        else:
            break
    openedFile.seek(0)
    openedFile.write(bytes(commentsTable[0], encoding="utf-8"))
    openedFile.seek(608)
    for i in range(1, 32, 1):
        openedFile.seek(48, 1)
        openedFile.write(bytes(commentsTable[i], encoding="utf-8"))
        openedFile.seek(4, 1)
    openedFile.seek(64)
    for i in range(32):
        openedFile.write(convStrToNum())
    openedFile.close()
    messagebox.showinfo(title='Information replaced',message='Information replaced.')
mainWindow = Tk()
frm = Frame(mainWindow, padding=4)
frm.grid()
Label(frm, text='Channel Panning').grid(column=0, row=0, sticky="ne")
chnObj = scrolledtext.ScrolledText(frm, width=28, height=1)
chnObj.grid(column=1, row=0, sticky="w")
Label(frm, text='Sample Names').grid(column=0, row=1, sticky="ne")
commentObject = scrolledtext.ScrolledText(frm, width=28, height=32)
commentObject.grid(column=1, row=1, sticky="w")
frm.option_add('*tearOff', FALSE)
mainWindow.title("PTMInfoEdit")
mainWindow.resizable(FALSE,FALSE)
def about():
    aboutWindow = Toplevel(mainWindow)
    aboutWindow.resizable(FALSE,FALSE)
    Label(aboutWindow, text='PTMInfoEdit, by RocketeerEatingEggs').grid(column=0, row=0, sticky="w")
    Label(aboutWindow, text='7/30-8/2/2022').grid(column=0, row=1, sticky="w")
    Label(aboutWindow, text='Panning:').grid(column=0, row=2, sticky="w")
    Label(aboutWindow, text='ABCDEFGHIJKLMNOP').grid(column=0, row=3, sticky="w")
menubar = Menu(mainWindow)
menu_file = Menu(menubar)
vBlankCheckVal = IntVar()
menu_file.add_command(label='Replace info...', command=convMOD)
menu_file.add_command(label='About and Help...', command=about)
menubar.add_cascade(menu=menu_file, label='Menu')
mainWindow['menu'] = menubar
mainWindow.mainloop()
