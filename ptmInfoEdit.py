from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import scrolledtext
from datetime import datetime
panStuff = {
    "0":0,"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,
    "8":8,"9":9,"A":10,"B":11,"C":12,"D":13,"E":14,"F":15,
    }
def convPanToNum(s):
    if not s in panStuff:
        return 7
    return panStuff[s].to_bytes(1, byteorder="little")
def convMOD():
    blankString = ""
    openedFile = filedialog.askopenfile(mode='rb+',filetypes=['"Poly Tracker" {.ptm}'])
    modName = nameObject.get("1.0", "end")
    modIns = int(insVal.get())
    modComment = commentObject.get("1.0", "end")
    modFN = fnObject.get("1.0", "end")
    chnlPan = chnObj.get("1.0", "end").strip("\n").ljust(32, "0")
    commentsTable = []
    for line in modComment.split('\n'):
        commentsTable.append(line.ljust(28, "\x00"))
    fnTable = []
    for line in modFN.split('\n'):
        fnTable.append(line.ljust(12, "\x00"))
    openedFile.seek(0)
    openedFile.write(bytes(modName, encoding="utf-8"))
    openedFile.seek(34)
    openedFile.write(modIns.to_bytes(2, byteorder="little"))
    openedFile.seek(608)
    for i in range(0, len(commentsTable) - 1, 1):
        openedFile.seek(48, 1)
        openedFile.write(bytes(commentsTable[i], encoding="utf-8"))
        openedFile.seek(4, 1)
    openedFile.seek(608)
    for i in range(0, len(fnTable) - 1, 1):
        openedFile.seek(1, 1)
        openedFile.write(bytes(fnTable[i], encoding="utf-8"))
        openedFile.seek(67, 1)
    openedFile.seek(64)
    for i in range(32):
        openedFile.write(convPanToNum(chnlPan[i]))
    openedFile.close()
    messagebox.showinfo(title='Information replaced',message='Information replaced.')
mainWindow = Tk()
frm = Frame(mainWindow, padding=4)
frm.grid()
Label(frm, text='Channel Panning').grid(column=0, row=0, sticky="ne")
chnObj = Text(frm, width=32, height=1)
chnObj.grid(column=1, row=0, sticky="w")
Label(frm, text='Instruments').grid(column=0, row=1, sticky="ne")
insVal = StringVar(value="31")
insObject = Spinbox(frm, from_=1.0, to=31.0)
insObject.set(31)
insObject.grid(column=1, row=1, sticky="w")
Label(frm, text='Song Name').grid(column=0, row=2, sticky="ne")
nameObject = scrolledtext.ScrolledText(frm, width=28, height=1)
nameObject.grid(column=1, row=2, sticky="w")
Label(frm, text='Sample Info').grid(column=0, row=3, sticky="ne")
commentObject = scrolledtext.ScrolledText(frm, width=28, height=16)
commentObject.grid(column=1, row=3, sticky="w")
fnObject = scrolledtext.ScrolledText(frm, width=12, height=16)
fnObject.grid(column=2, row=3, sticky="w")
frm.option_add('*tearOff', FALSE)
mainWindow.title("PTMInfoEdit")
mainWindow.resizable(FALSE,FALSE)
def about():
    aboutWindow = Toplevel(mainWindow)
    aboutWindow.resizable(FALSE,FALSE)
    Label(aboutWindow,text='PTMInfoEdit, by RocketeerEatingEggs').grid(column=0,row=0,sticky="w")
    Label(aboutWindow, text='8/17-8/23/2022').grid(column=0, row=1, sticky="w")
    Label(aboutWindow, text='To blank sample text, add a blank line.').grid(column=0, row=1, sticky="w")
menubar = Menu(mainWindow)
menu_file = Menu(menubar)
vBlankCheckVal = IntVar()
menu_file.add_command(label='Replace info...', command=convMOD)
menu_file.add_command(label='About and Help...', command=about)
menubar.add_cascade(menu=menu_file, label='Menu')
mainWindow['menu'] = menubar
mainWindow.mainloop()
