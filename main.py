from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import os
import threading
import pafy

ventana = Tk()
ventana.geometry("712x490")
ventana.configure(background="LightCyan3")
ventana.title("Youtube Catch")
URLL = StringVar()
directorio_actual = StringVar()
total_size = 0
dif = 0

def dire_actu():
    directorio_actual.set(os.getcwd())

def direc():
    directorio = filedialog.askdirectory()
    if directorio != "":
        os.chdir(directorio)
        directorio_actual.set(os.getcwd())

def verify_url():
    try:
        v = pafy.new(URLL.get())
        print(v.title)
        return v
    except:
        messagebox.showwarning("Something was wrong!", "Video unavailable")
        txtUrl.delete(0, len(URLL.get()))

def get(c, v):
    global total_size
    if c == "vid":
        try:
            s = v.getbest(preftype="mp4")
        except:
            s = v.getbest()
    else:
        try:
            s = v.getbestaudio(preftype="m4a")
        except:
            s = v.getbestaudio()
    total_size = s.get_filesize()
    return s

def estado(s):
    btn_direc.config(state=s)
    btn_download.config(state=s)
    btn_audio.config(state=s)

def mycb(total, recvd, ratio, rate, eta):
    global dif
    percnt = (recvd * 100 / total_size)
    eti_percent.config(text=(int(percnt), "%"))
    prog.step(percnt - dif)
    dif = percnt

def myDownloading(co, vid):
    global dif
    so = get(co, vid)
    try:
        so.download(quiet=True, callback=mycb)
        messagebox.showinfo("Download Finished", "Download successfully")
    except:
        messagebox.showwarning("ERROR", "Error while downloaded")
        prog.step(100)
        txtUrl.delete(0, len(URLL.get()))
    estado('normal')
    eti.place(x=317, y=180)
    eti_percent.config(text = " ")
    dif = 0
    total_size = 0

def myDownload(co):
    vid = verify_url()
    if vid != None:
        eti.place(x=306, y=180)
        estado('disabled')
        t1 = threading.Thread(target=myDownloading, args=(co, vid))
        t1.start()

txtUrl = Entry(ventana, font = ('Arial', 15, 'bold'), textvariable = URLL, width = 30)
txtUrl.place(x = 196, y = 130)
txtDirec = Entry(ventana, font = ('Arial', 8), textvariable = directorio_actual, width = 60)
txtDirec.place(x = 185, y = 455)

btn_direc = Button(ventana, width=20, text='Change directory', bg="grey82", command = direc)
btn_direc.place(x = 287, y = 270)

Label(ventana, width = 12, text = 'Destination', bg = "LightCyan3").place(x = 314, y = 432)
Label(ventana, font = ('Arial', 30, 'bold'), text = 'Youtube Catcher!', fg='snow', bg = 'LightCyan3').place(x = 193, y = 17)

btn_download = Button(ventana, width =  20, text = 'Download Video', bg = "grey82", command = lambda:myDownload("vid"))
btn_download.place(x = 287, y = 310)

btn_audio = Button(ventana, width =  20, text = 'Download Audio', bg = "grey82", command = lambda:myDownload("aud"))
btn_audio.place(x = 287, y = 350)

eti = Label(ventana,width = 14, text = 'Progress', bg = 'LightCyan3')
eti.place(x = 350, y = 180)

eti_percent = Label(ventana,width = 4, bg = 'LightCyan3')
eti.place(x = 392, y = 180)

prog = progressbar  = ttk.Progressbar(ventana)
prog.place(x = 196, y = 200, width = 335)


ventana.mainloop()
