#Importazione di Tkinter e librerie utili
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
import os.path #serve per verificare se un file è presente o no
import numpy as np #utility per il salvataggio delle impostazioni in un file .npy

global path
global fn_set
fn_set = "settings.npy"
path = os.path.expanduser(r'~\Documents\School Life Diary')
def salvataggio0():
    try:
        ds["ORE_MAX_GIORNATA"]=int(sv.get())
        np.save(os.path.join(path, fn_set), ds) 
        tkinter.messagebox.showinfo(title="Successo!", message="Parametro modificato con successo!")
        wcv.destroy()
        v0["text"]=ds["ORE_MAX_GIORNATA"]
    except:
        tkinter.messagebox.showerror(title="ERRORE!", message="Si è verificato un errore durante la modifica del parametro. Riprovare o contattare lo sviluppatore!")
def accept_whole_number_only(e=None):
    value = sv.get()
    if int(value) != value:
        sv.set(round(value))
        
def cambiaValore0():
    global wcv
    wcv=Toplevel()
    wcv.title("Cambia valore - Impostazioni - School Life Diary")
    wcv.iconbitmap("sld_icon_beta.ico")
    wcv.geometry("%dx%d+%d+%d" % (400, 200, 600, 250))
    etichetta1=Label(wcv, text="Sceglere il valore da attribuire al parametro:")
    var=IntVar()
    global sv
    sv=Scale(wcv, variable=var, from_=4, to=8, orient=HORIZONTAL, command=accept_whole_number_only)
    lvar=Label(wcv, textvariable=var)
    bt1=Button(wcv,text="SALVA", command=salvataggio0)
    etichetta1.pack(padx=10, pady=10)
    lvar.pack(padx=10, pady=2)
    sv.pack(padx=10, pady=10)
    bt1.pack(padx=10, pady=10)
    wcv.mainloop()
    
def inizializza():
    global ds
    ds=np.load(os.path.join(path, fn_set)).item()
    v0["text"]=ds["ORE_MAX_GIORNATA"]
#Creazione finestra
def creaFinestra():
    s=Style()
    try:
        s.theme_use("vista")
    except:
        s.theme_use()
    ws=Toplevel()
    ws.title("Impostazioni - School Life Diary")
    ws.iconbitmap("sld_icon_beta.ico")
    ws.geometry("%dx%d+%d+%d" % (900, 400, 600, 250))
    fs=Frame(ws)
    fs.pack()
    la1=Label(fs,text="Parametro")
    la2=Label(fs,text="Valore attuale")
    la3=Label(fs,text="Descrizione")
    la4=Label(fs,text="Azioni")
    la1.grid(row=0, column=0, padx=10, pady=10)
    la2.grid(row=0, column=1, padx=10, pady=10)
    la3.grid(row=0, column=2, padx=10, pady=10)
    la4.grid(row=0, column=3, padx=10, pady=10)
    p0=Label(fs,text="ORE_MAX_GIORNATA")
    global v0
    v0=Label(fs,text="5")
    d0=Label(fs,text="Imposta il numero di ore massime per giornate da visualizzare nell'orario")
    a0=Button(fs,text="Cambia", command=cambiaValore0)
    p0.grid(row=1, column=0, padx=10, pady=10)
    v0.grid(row=1, column=1, padx=10, pady=10)
    d0.grid(row=1, column=2, padx=10, pady=10)
    a0.grid(row=1, column=3, padx=10, pady=10)
    inizializza()
    ws.mainloop()
