from tkinter import *
import pyperclip as ppc
from memory_profiler import profile
import tkinter.font as font
import sqlite3, time


@profile
def main():
    mydb = sqlite3.connect('clipsaver.db')
    cursor = mydb.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS unclassified(id INTEGER PRIMARY KEY, dnt DATETIME NOT NULL, '
        'clip VARCHAR(65535))')
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS personal(id INTEGER PRIMARY KEY, dnt DATETIME NOT NULL, '
        'clip VARCHAR(65535))')
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS work(id INTEGER PRIMARY KEY, dnt DATETIME NOT NULL, '
        'clip VARCHAR(65535))')
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS passwords(id INTEGER PRIMARY KEY, dnt DATETIME NOT NULL, '
        'clip VARCHAR(65535))')
    mydb.commit()

    global menu, prev, latest
    menu = 0
    prev = 0
    latest = ""
    delay = 50
    ppc.copy(latest)

    def getTable(num):
        match num:
            case 0:
                table = "unclassified"
            case 1:
                table = "personal"
            case 2:
                table = "work"
            case 3:
                table = "passwords"
        return table

    def getClip(id):
        return MainListBox.get(id)

    def writeClip(clip,num):
        dnt = time.strftime("%Y-%m-%d %H:%M:%S")
        numb = cursor.execute("SELECT count(*) FROM " + getTable(num)).fetchone()[0]
        if numb>=50:
            cursor.execute("DELETE FROM " + getTable(num) + " WHERE id = 1")
            cursor.execute("UPDATE " + getTable(num) + " SET id = id - 1")
            numb=49
            MainListBox.delete(0,0)
        cursor.execute("INSERT INTO " + getTable(num) + " VALUES(?,?,?)",(numb+1,dnt,clip))

        mydb.commit()

    def getBoard(num):
        records = cursor.execute("SELECT count(*) FROM " + getTable(num)).fetchone()[0]
        query = cursor.execute("SELECT clip FROM " + getTable(num))
        for i in range(records if records <= 50 else 50):
            yield query.fetchone()[0]

    def updateList(num):
        newClip =  cursor.execute("SELECT clip FROM " + getTable(num) + " ORDER BY dnt DESC").fetchone()[0]
        MainListBox.insert(MainListBox.size(),newClip)

    def clear(num):
        cursor.execute("DELETE FROM " + getTable(num))
        mydb.commit()
        MainListBox.delete(0, MainListBox.size()+1)

    def copy():
        global latest
        latest = getClip(MainListBox.curselection()[0])
        ppc.copy(latest)

    def delete():
        global menu
        clip = getClip(MainListBox.curselection()[0])
        cursor.execute("DELETE FROM " + getTable(menu) + " WHERE clip=?", (clip,))
        MainListBox.delete(MainListBox.curselection()[0])
        mydb.commit()

    def saveClip():
        global menu, latest

        current = ppc.paste()

        if current != latest and (time.strftime("%Y-%m-%d %H:%M:%S"), current) not in cursor.execute("SELECT dnt, clip FROM " + getTable(menu)).fetchall():
            writeClip(current,menu)
            latest = current
            updateList(menu)


        if MainListBox.curselection() !=  ():
            CopyButton.configure(state = "normal")
            DeleteButton.configure(state = "normal")
            updateMoveFrame()
        else:
            CopyButton.configure(state = "disabled")
            DeleteButton.configure(state = "disabled")
            updateMoveFrame(1)

        r.after(delay,saveClip)

    def changeMenu(num):
        global menu
        menu = num

        match menu:
            case 0:
                UnclassifiedMenuButton.configure(state = "disabled")
                PersonalMenuButton.configure(state = "normal")
                WorkMenuButton.configure(state = "normal")
                PasswordsMenuButton.configure(state = "normal")
            case 1:
                UnclassifiedMenuButton.configure(state = "normal")
                PersonalMenuButton.configure(state = "disabled")
                WorkMenuButton.configure(state = "normal")
                PasswordsMenuButton.configure(state = "normal")
            case 2:
                UnclassifiedMenuButton.configure(state = "normal")
                PersonalMenuButton.configure(state = "normal")
                WorkMenuButton.configure(state = "disabled")
                PasswordsMenuButton.configure(state = "normal")
            case 3:
                UnclassifiedMenuButton.configure(state = "normal")
                PersonalMenuButton.configure(state = "normal")
                WorkMenuButton.configure(state = "normal")
                PasswordsMenuButton.configure(state = "disabled")
        listRouter()


    def unclassified():
        b = getBoard(0)
        c = 1
        d = MainListBox.get(0,MainListBox.size()+1)
        for i in b:
            if i not in d:
                MainListBox.insert(c,i)
            c += 1

    def personal():
        b = getBoard(1)
        c = 1
        d = MainListBox.get(0,MainListBox.size()+1)
        for i in b:
            if i not in d:
                MainListBox.insert(c,i)
            c += 1

    def work():
        b = getBoard(2)
        c = 1
        d = MainListBox.get(0,MainListBox.size()+1)
        for i in b:
            if i not in d:
                MainListBox.insert(c,i)
            c += 1

    def passwords():
        b = getBoard(3)
        c = 1
        d = MainListBox.get(0,MainListBox.size()+1)
        for i in b:
            if i not in d:
                MainListBox.insert(c,i)
            c += 1

    def updateMoveFrame(do = 0):
        global menu
        if do == 1:
            UnclassifiedMoveButton.configure(state = "disabled")
            PersonalMoveButton.configure(state = "disabled")
            WorkMoveButton.configure(state = "disabled")
            PasswordsMoveButton.configure(state = "disabled")
            return ""

        match menu:
            case 0:
                UnclassifiedMoveButton.configure(state = "disabled")
                PersonalMoveButton.configure(state = "normal")
                WorkMoveButton.configure(state = "normal")
                PasswordsMoveButton.configure(state = "normal")
            case 1:
                UnclassifiedMoveButton.configure(state = "normal")
                PersonalMoveButton.configure(state = "disabled")
                WorkMoveButton.configure(state = "normal")
                PasswordsMoveButton.configure(state = "normal")
            case 2:
                UnclassifiedMoveButton.configure(state = "normal")
                PersonalMoveButton.configure(state = "normal")
                WorkMoveButton.configure(state = "disabled")
                PasswordsMoveButton.configure(state = "normal")
            case 3:
                UnclassifiedMoveButton.configure(state = "normal")
                PersonalMoveButton.configure(state = "normal")
                WorkMoveButton.configure(state = "normal")
                PasswordsMoveButton.configure(state = "disabled")


    def listRouter():
        global menu, prev

        if prev !=  menu:
            MainListBox.delete(0,MainListBox.size()+1)
            prev = menu

        match menu:
            case 0:
                unclassified()
            case 1:
                personal()
            case 2:
                work()
            case 3:
                passwords()

    def moveTo(num):
        global menu
        clip = getClip(MainListBox.curselection()[0])
        cursor.execute("DELETE FROM " + getTable(menu) + " WHERE clip = ?;",(clip,))
        MainListBox.delete(MainListBox.curselection()[0])
        writeClip(clip,num)


    def exiting():
        cursor.close()
        mydb.close()
        r.destroy()

    
    r = Tk()
    r.title("ClipSaver")
    s = font.Font(family = "Arial", size = 10)
    frameMenu = Frame(r,pady = 10)
    frameMove = Frame(r,pady = 10, padx = 5)
    frameActions = Frame(r,pady = 10)

    MainLabel = Label(r, text = "ClipSaver", font = s)

    UnclassifiedMenuButton = Button(frameMenu, text = "Unclassified", command = lambda: changeMenu(0), font = s, state = "disabled")
    PersonalMenuButton = Button(frameMenu, text = "Personal", command = lambda: changeMenu(1), font = s)
    WorkMenuButton = Button(frameMenu, text = "Work", command = lambda: changeMenu(2), font = s)
    PasswordsMenuButton = Button(frameMenu, text = "Passwords", command = lambda: changeMenu(3), font = s)

    CloseButton = Button(frameActions, text = "Close ClipSaver", command = exiting, font = s)
    CopyButton = Button(frameActions, text = "Copy Selection", command = copy, font = s)
    DeleteButton = Button(frameActions, text = "Delete Selection", command = delete, font = s)
    ClearButton = Button(frameActions, text = "Clear Clipboard", command = lambda: clear(menu), font = s)
    
    MoveHeading = Label(frameMove, text = "Move Clip to:", font = s)

    UnclassifiedMoveButton = Button(frameMove, text = "Unclassified", command = lambda: moveTo(0), font = s, state = "disabled")
    PersonalMoveButton = Button(frameMove, text = "Personal", command = lambda: moveTo(1), font = s, state = "disabled")
    WorkMoveButton = Button(frameMove, text = "Work", command = lambda: moveTo(2), font = s, state = "disabled")
    PasswordsMoveButton = Button(frameMove, text = "Passwords", command = lambda: moveTo(3), font = s, state = "disabled")
    

    MainListBox = Listbox(r, height = 50, width = 100, selectmode = "SINGLE")

    UnclassifiedMenuButton.grid(column = 0, row = 0, padx = 5)
    PersonalMenuButton.grid(column = 1, row = 0, padx = 5)
    WorkMenuButton.grid(column = 2, row = 0, padx = 5)
    PasswordsMenuButton.grid(column = 3, row = 0, padx = 5)

    MoveHeading.grid(column = 0, row = 0, pady = 5)
    UnclassifiedMoveButton.grid(column = 0, row = 1, pady = 5)
    PersonalMoveButton.grid(column = 0, row = 2, pady = 5)
    WorkMoveButton.grid(column = 0, row = 3, pady = 5)
    PasswordsMoveButton.grid(column = 0, row = 4, pady = 5)

    CloseButton.grid(column = 0,row = 0,padx = 10)
    CopyButton.grid(column = 1,row = 0,padx = 10)
    DeleteButton.grid(column = 2,row = 0,padx = 10)
    ClearButton.grid(column = 3,row = 0,padx = 10)

    MainLabel.grid(row = 0,column = 0,pady = 10)
    frameMenu.grid(row = 1,column = 0)
    MainListBox.grid(row = 2,column = 0)
    frameMove.grid(row = 2,column = 1)
    frameActions.grid(row = 3,column = 0)

    listRouter()
    saveClip()

    r.mainloop()


if __name__  ==  "__main__":
    main()

    # 0 -> unclassified
    # 1 -> personal
    # 2 -> work
    # 3 -> passwords