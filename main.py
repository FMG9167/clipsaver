from tkinter import *
import pyperclip as ppc
from memory_profiler import profile
import tkinter.font as font

@profile
def func():
    global latest, menu
    latest=""
    menu=0

    try:
        z = open("unclassified.txt","x")
        z.close()
    except FileExistsError:
        pass
    try:
        z = open("personal.txt","x")
        z.close()
    except FileExistsError:
        pass
    try:
        z = open("work.txt","x")
        z.close()
    except FileExistsError:
        pass
    try:
        z = open("passwords.txt","x")
        z.close()
    except FileExistsError:
        pass

    def getFilename(num):
        match num:
            case 0:
                filename="unclassified.txt"
            case 1:
                filename="personal.txt"
            case 2:
                filename="work.txt"
            case 3:
                filename="passwords.txt"
        return filename

    def getClip(number,num):
        with open(getFilename(num), "r") as f:
            l = f.read().split("\n")
            if number <= len(l):
                return l[number]
            else:
                return "EOF"

    def writeClip(clip,num):
        with open(getFilename(num), "a") as f:
            f.write(clip + "\n")

    def getBoard(num):
        with open(getFilename(num), "r") as f:
            a = f.read().split("\n")[0:-1]
            for i in range(len(a)):
                yield str(i+1)+ "       " + a[i]

    def clear(num):
        with open(getFilename(num), "w") as f:
            f.write("")
    
    def copy(num):
        ppc.copy(getClip(Lb1.curselection()[0],num))

    def saveClip(num):
        global latest
        current = ppc.paste()
        if current != latest:
            writeClip(current,num)
            latest=current
        r.after(50,lambda: writeClip(current,num))

    def changeMenu(num):
        global menu
        menu=num

    def unclassified():
        b=getBoard(0)
        c=1
        d=Lb1.curselection()
        Lb1.delete(0, Lb1.size()+1)
        for i in b:
            Lb1.insert(c,i)
            c+=1
        if d != ():
            Lb1.activate(d[0])
        r.after(50,listRouter)

    def personal():
        b=getBoard(1)
        c=1
        d=Lb1.curselection()
        Lb1.delete(0, Lb1.size()+1)
        for i in b:
            Lb1.insert(c,i)
            c+=1
        if d != ():
            Lb1.activate(d[0])
        r.after(1000,listRouter)

    def work():
        b=getBoard(2)
        c=1
        d=Lb1.curselection()
        Lb1.delete(0, Lb1.size()+1)
        for i in b:
            Lb1.insert(c,i)
            c+=1
        if d != ():
            Lb1.activate(d[0])
        r.after(1000,listRouter)

    def passwords():
        b=getBoard(3)
        c=1
        d=Lb1.curselection()
        Lb1.delete(0, Lb1.size()+1)
        for i in b:
            Lb1.insert(c,i)
            c+=1
        if d != ():
            Lb1.activate(d[0])
        r.after(1000,listRouter)

    def listRouter():
        global menu
        match menu:
            case 0:
                unclassified()
            case 1:
                personal()
            case 2:
                work()
            case 3:
                passwords()

    
    r=Tk()
    r.title("ClipSaver")
    s = font.Font(family="Arial", size=25)
    frameMenu = Frame(r,pady = 10)
    frameActions = Frame(r,pady = 10)

    L1 = Label(r, text = "ClipSaver", font=s)

    B4 = Button(frameMenu, text = "Unclassified", command=lambda: changeMenu(0), font = s)
    B5 = Button(frameMenu, text = "Personal", command=lambda: changeMenu(1), font = s)
    B6 = Button(frameMenu, text = "Work", command=lambda: changeMenu(2), font = s)
    B7 = Button(frameMenu, text = "Passwords", command=lambda: changeMenu(3), font = s)

    B1 = Button(frameActions, text = "Close ClipSaver", command=r.destroy, font = s)
    B2 = Button(frameActions, text = "Copy Selection", command=lambda: copy(menu), font = s)
    B3 = Button(frameActions, text = "Clear Clipboard", command=lambda: clear(menu), font = s)

    Lb1 = Listbox(r, height=50, width=100, selectmode="SINGLE")


    B4.grid(column=0, row=0, padx=5)
    B5.grid(column=1, row=0, padx=5)
    B6.grid(column=2, row=0, padx=5)
    B7.grid(column=3, row=0, padx=5)

    B1.grid(column=0,row=0,padx=10)
    B2.grid(column=1,row=0,padx=10)
    B3.grid(column=2,row=0,padx=10)

    L1.grid(row=0,column=0,pady = 10)
    frameMenu.grid(row=1,column=0)
    Lb1.grid(row=5,column=0)
    frameActions.grid(row=10,column=0)

    listRouter()
    saveClip(menu)

    r.mainloop()

if __name__ == "__main__":
    func()

    # 0 -> unclassified
    # 1 -> personal
    # 2 -> work
    # 3 -> passwords