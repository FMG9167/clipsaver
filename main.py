from tkinter import *
import pyperclip as ppc
from memory_profiler import profile
import tkinter.font as font
import sqlite3, time


@profile
def func():
    mydb = sqlite3.connect('clipsaver.db')
    cursor = mydb.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS unclassified(id INTEGER PRIMARY KEY AUTOINCREMENT, dnt DATETIME NOT NULL, '
        'clip VARCHAR(65535))')
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS personal(id INTEGER PRIMARY KEY AUTOINCREMENT, dnt DATETIME NOT NULL, '
        'clip VARCHAR(65535))')
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS work(id INTEGER PRIMARY KEY AUTOINCREMENT, dnt DATETIME NOT NULL, '
        'clip VARCHAR(65535))')
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS passwords(id INTEGER PRIMARY KEY AUTOINCREMENT, dnt DATETIME NOT NULL, '
        'clip VARCHAR(65535))')
    mydb.commit()

    global latest, menu
    latest=""
    menu=0
    delay=50

    def getTable(num):
        match num:
            case 0:
                table="unclassified"
            case 1:
                table="personal"
            case 2:
                table="work"
            case 3:
                table="passwords"
        return table

    def getClip(id,num):
        print("getClip")
        return cursor.execute("SELECT clip FROM "+getTable(num)+" WHERE id=?;",(id,)).fetchone()[0]

    def writeClip(clip,num):
        print("writeClip")
        dnt = time.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO "+getTable(num)+"(dnt, clip) VALUES(?,?)",(dnt,clip))
        mydb.commit()

    def getBoard(num):
        print("getBoard")
        records = cursor.execute("SELECT count(*) FROM " + getTable(num)).fetchone()[0]
        query = cursor.execute("SELECT clip FROM " + getTable(num))
        for i in range(records if records <=50 else 50):
            yield str(i+1)+ "       " + query.fetchone()[0]

    def clear(num):
        print("clear")
        cursor.execute("DELETE FROM " + getTable(num))
        mydb.commit()

    def copy(num):
        print("copy")
        ppc.copy(getClip(Lb1.curselection()[0],num))

    def saveClip():
        print("saveClip")
        global latest
        current = ppc.paste()
        if current != latest:
            writeClip(current,menu)
            latest=current
        r.after(delay,lambda: saveClip())

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
        r.after(delay,listRouter)

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
        r.after(delay,listRouter)

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
        r.after(delay,listRouter)

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
        r.after(delay,listRouter)

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

    def exiting():
        cursor.close()
        mydb.close()
        r.destroy()

    
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

    B1 = Button(frameActions, text = "Close ClipSaver", command=exiting, font = s)
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
    saveClip()

    r.mainloop()

def test():
    mydb=sqlite3.connect("clipsaver.db")
    c=mydb.cursor()
    c.execute(
        'CREATE TABLE IF NOT EXISTS unclassified(id INTEGER PRIMARY KEY AUTOINCREMENT, dnt DATETIME NOT NULL, '
        'clip VARCHAR(65535))')
    print(c.execute("SELECT * FROM unclassified").fetchall())
    c.execute("INSERT INTO unclassified(dnt, clip) VALUES (?, ?)",(time.strftime('%Y-%m-%d %H:%M:%S'), "dem"))
    mydb.commit()
    print(c.execute("SELECT * FROM unclassified").fetchall())
    c.execute("INSERT INTO unclassified(dnt, clip) VALUES (?, ?)",(time.strftime('%Y-%m-%d %H:%M:%S'), "i see"))
    mydb.commit()
    print(c.execute("SELECT * FROM unclassified").fetchone())


if __name__ == "__main__":
    func()
    # test()
    # 0 -> unclassified
    # 1 -> personal
    # 2 -> work
    # 3 -> passwords