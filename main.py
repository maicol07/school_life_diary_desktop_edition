#####################
#                   #
#    SCHOOL LIFE    #
#       DIARY       #
#                   #
#    PC VERSION     #
#                   #
#####################


### START MAIN ###

## IMPORTAZIONE MODULI ESTERNI ##
import gettext, os, ctypes, locale, PIL.Image, PIL.ImageTk, webbrowser, time
import sqlite3 as sql
global pathset
from tkinter import *
from tkinter.ttk import *
from tkinter import Tk, Toplevel # Serve per impostare lo sfondo bianco nelle finestre
import tkinter.messagebox as tkmb



## IMPOSTAZIONE PERCORSO ##
path = os.path.expanduser(r'~\Documents\School Life Diary')

## INSTALLAZIONE LINGUA ##
global lgcode
if not(os.path.exists(os.path.join(path,"language.txt"))):
    windll = ctypes.windll.kernel32
    lgcode=locale.windows_locale[windll.GetUserDefaultUILanguage()]
    lg = gettext.translation("main", localedir=os.path.join(path,'locale'), languages=[lgcode[0:2]])
else:
    try:
        fl=open(os.path.join(path,"language.txt"),"r")
        lgcode=fl.readline()
        lg = gettext.translation('main', localedir=os.path.join(path,'locale'), languages=[lgcode])
    except Exception as ex:
        try:
            tkmb.showerror(title=_("Lingua non impostata!"),
                                     message=_(r"La lingua impostata non è stata riconosciuta. Per risolvere prova a eliminare il file in Documenti/School Life Diary/language.txt . Se il problema non si risolve, contattare lo sviluppatore. Errore: ")+str(ex))
        except NameError:
            tkmb.showerror(title="Can't install the language!",
                           message=r"Can't recognize the set language. To fix this try to delete the file in Documents/School Life Diary/language.txt . If the problem still occurs, contact the developer. Error: ") + str(
                               ex)

lg.install()


## CREAZIONE DATABASE (PRIMO AVVIO) ##

output_filename = "settings.db"

if not(os.path.exists(path)):
    os.mkdir(path)
if not(os.path.exists(os.path.join(path,output_filename))):
    if os.path.exists(os.path.join(path,"settings.npy")):
        tkmb.showwarning(title=_("Attenzione! Database non presente!"),
                                       message=_("Non hai effettuato la migrazione del database. Il programma si avvierà, ma non saranno visualizzati i tuoi dati fino a che non effettuerai la migrazione."))
        rd=tkmb.askokcancel(title=_("Conferma download strumento migrazione database"),
                                       message=_("Vuoi scaricare lo strumento di migrazione del database?"))
        if rd==True:
            webbrowser.open("https://github.com/maicol07/school_life_diary_pc/releases")
    fs=open(os.path.join(path, output_filename), "w")
    fs.close()
    conn=sql.connect(os.path.join(path, output_filename),isolation_level=None)
    c=conn.cursor()
    c.execute("""CREATE TABLE `settings` ( `setting` TEXT,
                                                   `value` TEXT,
                                                   `descr` TEXT);""")
    c.execute("""INSERT INTO settings (setting,value,descr) VALUES ("ORE_MAX_GIORNATA","5", "{}"); """.format(_("Numero di ore massime per giornate da visualizzare nell'orario")))
    c.execute("""INSERT INTO settings (setting,value,descr) VALUES ("PC_THEME","vista", "{}"); """.format(_("Tema visivo dell'applicazione")))
else:
    conn=sql.connect(os.path.join(path, output_filename),isolation_level=None)
    c=conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='settings';")
    ris=c.fetchall()
    if not(len(ris)==1):
       c.execute("""CREATE TABLE `settings` ( `setting` TEXT,
                                                   `value` TEXT,
                                                   `descr` TEXT);""")
    c.execute("""INSERT INTO settings (setting,value,descr) VALUES ("ORE_MAX_GIORNATA","5", "{}"); """.format(_("Numero di ore massime per giornate da visualizzare nell'orario")))
    c.execute("""INSERT INTO settings (setting,value,descr) VALUES ("PC_THEME","vista", "{}"); """.format(_("Tema visivo dell'applicazione")))

    
## IMPORTAZIONE FILE ESTERNI ##
import settings, subjects, timetable, note, prof


## FINESTRA INFORMAZIONI ##
def info():
    '''Crea la finestra delle informazioni'''
    wi=Toplevel()
    wi.configure(bg="white")
    wi.title(_("Informazioni")+" - School Life Diary")
    wi.iconbitmap("sld_icon_beta.ico")
    wi.geometry("850x750+250+50")
    f1=Frame(wi)
    f1.pack()
    title=Label(f1,text="School Life Diary", font=("Comic Sans MS",25,"bold italic"))
    title.pack(padx=10,pady=5)
    subtitle=Label(f1, text=_("sviluppato e mantenuto da maicol07"))
    fl=Labelframe(f1,text=_("Link"))
    fl.pack()
    bws=Button(fl, text=_("Sito web"),command=lambda: webbrowser.open("https://apps.maicol07.tk"))
    subtitle.pack(padx=10,pady=2)
    bws.grid(row=0,column=0,padx=10,pady=5)
    bgit=Button(fl, text=_("Pagina del progetto su GitHub"), command=lambda: webbrowser.open("https://github.com/maicol07/school_life_diary_pc"))
    bgit.grid(row=0,column=1,padx=10,pady=5)
    l25=Label(f1, text=_("Alcune icone fatte da Pixel Buddha, Freepik, Roundicons e Smash Icons di www.flaticon.com hanno licenza Creative Commons 3.0"))
    l25.pack(padx=10,pady=5)
    l3=Label(f1,text=_("Traduttori: "))
    l3.pack(padx=10,pady=15)
    traduttori=Label(f1,text="maicol07")
    traduttori.pack(padx=10,pady=10)
    l4=Label(f1,text=_("Vuoi diventare anche tu un traduttore?"))
    bt=Button(f1, text=_("CLICCA QUI!"), command=lambda: webbrowser.open("https://github.com/maicol07/school_life_diary_pc/wiki/Vuoi-diventare-traduttore-di-School-Life-Diary%3F"))
    l4.pack(padx=10,pady=5)
    bt.pack(padx=10)
    cl=Labelframe(wi,text=_("Registro delle modifiche"))
    cl.pack()
    changel=Text(cl,font="Courier 10",width=100,height=25)
    changel.pack()
    clf=open("CHANGELOG_{}.md".format(lgcode.upper()[:2]),"r")
    for r in clf.readlines():
        changel.insert(INSERT, r)
    changel.config(state=DISABLED)

## CREAZIONE FINESTRA MENU PRINCIPALE
global w
w=Tk()
w.withdraw()
w.configure(bg="white")
w.title("School Life Diary")
w.iconbitmap(r"images/sld_icon_beta.ico")
#w.geometry("335x325+200+100")
s=Style()
conn=sql.connect(os.path.join(path, output_filename),isolation_level=None)
c=conn.cursor()
s.theme_use(c.execute("SELECT value FROM settings WHERE setting='PC_THEME'").fetchone())
s.configure("TFrame",background="white")
s.configure("TButton",height=100)
s.configure("TLabel",background="white")
s.configure("TPhotoimage",background="white")
s.configure("TLabelframe",background="white")
s.configure("TLabelframe.Label",background="white")

### Verifica se esistono degli aggiornamenti per il programma ###
v="1"
import feedparser
from subprocess import check_output
feed_name="School Life Diary Releases"
url=r"https://github.com/maicol07/school_life_diary_pc/releases.atom"
feed=feedparser.parse(url)
try:
    post=feed.entries[0]
    title=post.title
    lp=title.split(" ")
    if (lp[0][1:].isdecimal()==True):
        lp[0]=lp[0][1:]
    if (v!=lp[0][1:]):
        agg=tkmb.askyesno(title=_("Nuova versione disponibile!"),
                                       message=_("""È disponibile una nuova versione di School Life Diary.
Ti consigliamo di aggiornare il prima possibile per non perdere le nuove funzionalità, i miglioramenti e le correzioni di problemi.
Vuoi accedere alla pagina da cui scaricare l'aggiornamento alla versione {}?""").format(lp[0][1:]))
        if (agg==True):
            webbrowser.open("https://github.com/maicol07/school_life_diary_pc/releases/")
except IndexError:
    tkmb.showwarning(title=_("Nessuna connessione ad internet"),
                                   message=_("Non è disponibile nessuna connessione ad internet per la ricerca degli aggiornamenti. La ricerca verrà ritentata la prossima volta che sarà riaperto il programma."))

mb=Menu(w)
w.config(menu=mb)
fm=Menu(mb,tearoff=0)
om=Menu(mb,tearoff=0)
hm=Menu(mb,tearoff=0)
iexit = PIL.Image.open(r"icons\exit.png")
pexit = PIL.ImageTk.PhotoImage(iexit)
isettings = PIL.Image.open("icons\settings.png")
psettings = PIL.ImageTk.PhotoImage(isettings)
ilanguage = PIL.Image.open("icons\language.png")
planguage = PIL.ImageTk.PhotoImage(ilanguage)
iguida = PIL.Image.open("icons\help.png")
pguida = PIL.ImageTk.PhotoImage(iguida)
iinfo = PIL.Image.open("icons\info.png")
pinfo = PIL.ImageTk.PhotoImage(iinfo)
mb.add_cascade(label=_("File"),menu=fm)
fm.add_command(label=_("Esci"), image=pexit,
               compound="left",command=w.destroy)
mb.add_cascade(label=_("Opzioni"),menu=om)
om.add_command(label=_("Impostazioni"), image=psettings,
               compound="left", command=settings.creaFinestra)
om.add_command(label=_("Cambia lingua"), image=planguage,
               compound="left", command=settings.cambiaLingua)
mb.add_cascade(label=_("Aiuto"), menu=hm)
hm.add_command(label=_("Guida"), image=pguida,
               compound="left",
               command= lambda: webbrowser.open("https://github.com/maicol07/school_life_diary_pc/wiki"))
hm.add_command(label=_("Informazioni"), image=pinfo,
               compound="left",command=info)
f=Frame(w)
logo=PhotoImage(file=r"images/school_life_diary_splash.png")
title=Label(f,image=logo)
f.pack()
title.pack(padx=10,pady=10)
f2=Frame(w)
f2.pack()
itime = PIL.Image.open(r"icons\timetable.png")
ptime = PIL.ImageTk.PhotoImage(itime)
imaterie = PIL.Image.open(r"icons\subjects.png")
pmaterie = PIL.ImageTk.PhotoImage(imaterie)
iprof = PIL.Image.open(r"icons\educator.png")
pprof = PIL.ImageTk.PhotoImage(iprof)
ivoti = PIL.Image.open(r"icons\medal.png")
pvoti = PIL.ImageTk.PhotoImage(ivoti)
inote = PIL.Image.open(r"icons\notes.png")
pnote = PIL.ImageTk.PhotoImage(inote)
iagenda = PIL.Image.open(r"icons\agenda.png")
pagenda = PIL.ImageTk.PhotoImage(iagenda)
bo=Button(f2,text=_("ORARIO"), #background="#FF6C6C",
          style="TButton",
          image=ptime,
          compound="left",
          command=timetable.creaFinestra)
bm=Button(f2,text=_("MATERIE"), #background="#FFBD45",
          image=pmaterie,
          compound="left",
          command=subjects.creaFinestra)
bp=Button(f2,text=_("PROFESSORI"), #background="#7DFB7D",
          image=pprof,
          compound="left", command=prof.creaFinestra)
bv=Button(f2,text=_("VOTI"), #background="#ADD8E6",
          image=pvoti,
          compound="left", command=lambda: webbrowser.open('https://apps.maicol07.tk/app/sld/voti/'))
ban=Button(f2,text=_("ANNOTAZIONI"), #background="#C389C3",
          image=pnote,
          compound="left", command=note.creaFinestra)
bag=Button(f2,text=_("AGENDA"), #background="#7DFB7D",
          image=pagenda,
          compound="left", command=lambda: webbrowser.open('https://calendar.google.com'))
bo.grid(row=0, column=0,padx=5)
bm.grid(row=0, column=1,padx=5)
bp.grid(row=0, column=2,padx=5)
bv.grid(row=0, column=3,padx=5)
ban.grid(row=0, column=4,padx=5)
bag.grid(row=0, column=5,padx=5)
w.deiconify()
w.mainloop()
c.close()
conn.close()
if "rFile" in globals():
    os.remove(rFile)
