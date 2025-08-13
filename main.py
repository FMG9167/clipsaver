from tkinter import *
import pyperclip as ppc
from memory_profiler import profile
import tkinter.font as font

@profile
def func():
    filename = "saved.txt"
    try:
        f=open(filename, "r")
        f.close()
    except:
        f=open(filename, "w")
        f.close()

    def getClip(number):
        with open(filename, "r") as f:
            l = f.read().split("\n")
            if number <= len(l):
                return l[number]
            else:
                return "EOF"

    def writeClip(clip):
        with open(filename, "a") as f:
            f.write(clip + "\n")

    def getBoard():
        with open(filename, "r") as f:
            a = f.read().split("\n")[0:-1]
            for i in range(len(a)):
                yield str(i+1)+ "       " + a[i]

    def clear():
        with open(filename, "w") as f:
            f.write()
    
    def copy():
        ppc.copy(getClip(Lb1.curselection()[0]))

    def efunc():
        b= getBoard()
        c=1
        d = Lb1.get(0,Lb1.size()+1)
        for i in b:
            if (c,i) not in d:
                Lb1.insert(c,i)
            c+=1
        if Lb1.get(0,Lb1.size()+1) != tuple():
            Lb1.activate(0)
        r.after(2000,efunc)
    
    r=Tk()
    r.title("ClipSaver")
    s = font.Font(family="Arial", size=25)
    f = Frame(r,pady = 10)

    L1 = Label(r, text = "ClipSaver", font=s)
    B1 = Button(f, text = "Close ClipSaver", command=r.destroy, font = s)
    B2 = Button(f, text = "Copy Selection", command=copy, font = s)
    B3 = Button(f, text = "Clear Clipboard", command=clear, font = s)
    Lb1 = Listbox(r, height=50, width=100, selectmode="SINGLE")
    Lb1.grid(row=1,column=0)


    B1.grid(column=0,row=0,padx=10)
    B2.grid(column=1,row=0,padx=10)
    B3.grid(column=2,row=0,padx=10)

    f.grid(row=2,column=0)
    L1.grid(row=0,column=0,pady = 10)

    efunc()

    r.mainloop()

if __name__ == "__main__":
    func()