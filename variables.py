import os.path
import tkinter.messagebox as tkmb
from tkinter.filedialog import *
from tkinter.ttk import Entry, Frame, Button

from PIL import Image, ImageTk
from ttkthemes.themed_style import *


def style_init():
    """
    Inizializzazione delle variabili globali
    :return:
    """
    global s
    s = ThemedStyle()
    s.configure("TFrame", background="white")
    s.configure("TButton", height=100)
    s.configure("TLabel", background="white")
    s.configure("TPhotoimage", background="white")
    s.configure("TLabelframe", background="white")
    s.configure("TLabelframe.Label", background="white")
    s.configure("TScale", background="white")
    s.configure("TCheckbutton", background="white")
    s.configure('.', font=('Arial', 10, "normal roman"))


def path_init():
    global path
    if not (os.path.exists("path.txt")):
        w = Tk()
        w.title("Select data path")
        w.iconbitmap(r"images/school_life_diary.ico")
        Label(w, text="Select the path where the data folder will be created. If you would like to use the default one,"
                      "then click OK.").pack()
        f = Frame(w)
        f.pack()
        var = StringVar()
        var.set(os.path.expanduser(r'~\Documents'))
        e = Entry(f, textvariable=var, width=45)
        i_folder = Image.open(r"icons\folder.png")
        f_image = ImageTk.PhotoImage(i_folder)
        b = Button(f, image=f_image, compound="left", command=lambda: var.set(askdirectory()))
        e.grid(row=0, column=0)
        b.grid(row=0, column=1, padx=5)
        b_ok = Button(w, text="OK", command=lambda: w.destroy())
        b_ok.pack()
        w.mainloop()
        path = var.get()
        txt = open("path.txt", "w")
        txt.write(path)
        txt.close()
        txt = open("path.txt", "r")
        path = txt.read() + "\School Life Diary"
        txt.close()
    else:
        txt = open("path.txt", "r")
        path = txt.read()
        if not (os.path.exists(path)):
            try:
                os.makedirs(path)
            except FileNotFoundError:
                tkmb.showerror(title="Can't find path",
                               message="We couldn't find the path of the app data files.\nTo fix this please type in "
                                       "the file path.txt (if it doesn't exists create it) inside the installation "
                                       "folder the path to your documents folder. To find it right click on documents "
                                       "folder in explorer and then go to path tab. Copy the path and paste inside it "
                                       "the file.")
        txt.close()
