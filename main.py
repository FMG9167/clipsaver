from tkinter import *
import pyperclip as ppc
# import json
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
            if number <= len(l)-1 and number > 0:
                return l[number-1]
            else:
                return "EOF"

    def writeClip(clip):
        with open(filename, "a") as f:
            f.write(clip + "\n")

    def getBoard():
        with open(filename, "r") as f:
            a = f.read().split("\n")[0:-1]
            for i in range(len(a)):
                yield str(i+1)+ "\t\t\t" + a[i]
    def clear():
        with open(filename, "w") as f:
            f.write()
    
    def copy():
        ppc.copy(getClip(Lb1.curselection()[0]))

    def efunc():
        with open(filename, "r") as f:
            a = f.read().count("\n")
        b= getBoard()
        c=1
        for i in b:
            Lb1.insert(c, i)
            c+=1
        Lb1.grid(row=1,column=0)
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


    B1.grid(column=0,row=0,padx=10)
    B2.grid(column=1,row=0,padx=10)
    B3.grid(column=2,row=0,padx=10)

    f.grid(row=2,column=0)
    L1.grid(row=0,column=0,pady = 10)

    efunc()

    r.mainloop()

if __name__ == "__main__":
    func()


# root = Tk(baseName = "ClipSaver")
# root.title("ClipSaver")
# S25 = font.Font(family="Arial", size=25)

# L1 = Label(root, text="ClipSaver is working", font=S25)
# B1 = Button(root, text="exit", command=root.destroy, font=S25)
# I1 = Entry(root, font=S25)

# clips=[]


# L1.grid(row=0,column=2, columnspan=100)
# B1.grid(row=0,column=0)
# I1.grid(row=1,column=2,columnspan=100)

# root.mainloop()

