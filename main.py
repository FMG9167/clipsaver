from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox

import pyperclip as ppc
from memory_profiler import profile
import tkinter.font as font
import sqlite3, time
from datetime import datetime

menu = 0
prev = 0
latest = 0

@profile
def main():
    mydb = sqlite3.connect('clipsaver.db')
    cursor = mydb.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS tables(tableName VARCHAR(50), type INTEGER)')
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS unclassified(dnt DATETIME NOT NULL, '
        'clip VARCHAR(65535))')
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS personal(dnt DATETIME NOT NULL, '
        'clip VARCHAR(65535))')
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS work(dnt DATETIME NOT NULL, '
        'clip VARCHAR(65535))')
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS passwords(dnt DATETIME NOT NULL, '
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
                return "unclassified"
            case 1:
                return "personal"
            case 2:
                return "work"
            case 3:
                return "passwords"
        return None

    def getCurrentTable():
        return getTable(0)

    def getClip(ListIndex):
        clip = MainListBox.get(ListIndex, ListIndex)
        return clip[0]

    def writeClip(clip,num):
        dnt = time.strftime("%Y-%m-%d %H:%M:%S")
        numb = cursor.execute("SELECT count(*) FROM {}".format(getTable(num))).fetchone()[0]
        if numb>=50:
            cursor.execute("DELETE FROM {} WHERE dnt=?".format(getTable(num)),(cursor.execute("SELECT dnt FROM {} ORDER BY dnt DESC".format(getTable(num))).fetchone()[0],))
            MainListBox.delete(0,0)

        cursor.execute("INSERT INTO {} VALUES(?,?)".format(getTable(num)),(dnt,clip))
        mydb.commit()

    def getBoard(num):
        records = cursor.execute("SELECT count(*) FROM {}".format(getTable(num))).fetchone()[0]
        query = cursor.execute("SELECT clip FROM {}".format(getTable(num)))
        for i in range(records if records <= 50 else 50):
            yield query.fetchone()[0]   # memory optimization technique

    def updateList(num):
        newClip =  cursor.execute("SELECT clip FROM {} ORDER BY dnt DESC".format(getTable(num))).fetchone()[0]
        MainListBox.insert(MainListBox.size(),newClip)

    def clear(num):
        cursor.execute("DELETE FROM {}".format(getTable(num)))
        mydb.commit()
        MainListBox.delete(0, MainListBox.size()+1)

    def copy():
        global latest
        latest = getClip(MainListBox.curselection()[0])
        ppc.copy(latest)

    def delete():
        global menu
        clip = getClip(MainListBox.curselection()[0])
        cursor.execute("DELETE FROM {} WHERE clip=?".format(getCurrentTable()), (clip,))
        MainListBox.delete(MainListBox.curselection()[0])
        mydb.commit()

    def deleteOldPwd():
        records = cursor.execute("SELECT count(*) FROM passwords").fetchone()[0]
        query = cursor.execute("SELECT * FROM passwords")
        delL = ""

        for i in range(records):
            result = query.fetchone()    # fetching rows one at a time instead of calling all the rows into memory
            if "day" in str(datetime.now() - datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")):
                delL+=str(result[0])

        for i in delL:
            cursor.execute("DELETE FROM passwords WHERE dnt=?", (str(i),))

        if delL != "":
            mydb.commit()

    def mainLoop():
        global menu, latest
        current = ppc.paste()

        if current != latest and (time.strftime("%Y-%m-%d %H:%M:%S"), current) not in cursor.execute("SELECT dnt, clip FROM {}".format(getCurrentTable())).fetchall():
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
        deleteOldPwd()
        root.after(delay,mainLoop)

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

    def changeList(num):
        b = getBoard(num)
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
            MoveButton.configure(state = "disabled")
            return ""

        MoveButton.configure(state = "normal")
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
        return None


    def createList(tableName, tableType):
        cursor.execute("CREATE TABLE IF NOT EXISTS {} (dnt DATETIME NOT NULL, clip VARCHAR(65535))".format(tableName))
        cursor.execute("INSERT INTO tables VALUES (?,?)", (tableName,tableType))

    def newList():
        def submitList():
            name = nameField.get()
            pwd = "selected" in typePass.state()
            udlWindow.destroy()
            createList(name, pwd)

        udlWindow = Toplevel(mainWindow)
        udlWindow.title("New List")
        udlWindow.resizable(False, False)
        udlWindow.configure(width=350, height=200)
        mainFrame = Frame(udlWindow, padx=20, pady=20)
        buttonFrame= Frame(mainFrame, padx=10, pady=10)
        udlLabel = Label(mainFrame, text = "Create New List", padx=10, pady=10, font=("Arial", 20))
        nameField = Entry(mainFrame, width = 30, justify = CENTER, name = "name", font=s)
        typePass = ttk.Checkbutton(mainFrame, text = "Is this a password List?", variable=IntVar())
        submitButton = Button(buttonFrame, text = "Submit", command = submitList, padx = 10, font=s)
        cancelButton = Button(buttonFrame, text = "Cancel", command = udlWindow.destroy, padx = 10, font=s)

        udlLabel.grid(row = 0, column = 0)
        nameField.grid(row = 1, column = 0)
        typePass.grid(row = 2, column = 0)
        submitButton.grid(row = 0, column = 0)
        cancelButton.grid(row = 0, column = 1)
        buttonFrame.grid(row = 3, column = 0)

        mainFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

    def listRouter():
        global menu, prev

        if prev !=  menu:
            MainListBox.delete(0,MainListBox.size()+1)
            prev = menu

        changeList(menu)

    def moveTo(num):
        global menu

        clip = getClip(MainListBox.curselection()[0])
        cursor.execute("DELETE FROM {} WHERE clip = ?;".format(getCurrentTable()),(clip,))
        writeClip(clip,num)


    def moveClip(clip, newTable):
        cursor.execute("DELETE FROM {} WHERE clip=?;".format(getCurrentTable()),(clip,))
        MainListBox.delete(MainListBox.get(0,"end").index(clip))
        cursor.execute("INSERT INTO {} VALUES (?,?)".format(newTable),(time.strftime("%Y-%m-%d %H:%M:%S"),clip))
        mydb.commit()

    def moveClipWindow(clip):
        moveWindow = Toplevel(mainWindow)
        moveWindow.title("Move Clip")
        moveWindow.resizable(False, False)
        moveWindow.configure(width=300, height=300)

        tables = [x[0] for x in cursor.execute("SELECT tablename FROM tables").fetchall()]

        mainFrame = Frame(moveWindow, padx=20, pady=20)
        buttonFrame = Frame(mainFrame, padx=10, pady=10)
        heading = Label(mainFrame, text = "Clip: "+clip, padx=10, pady=10, font=s)
        text1 = Label(mainFrame, text = "Move to:", justify=LEFT, padx=10, pady=10, font=s)
        tableList = ttk.Combobox(mainFrame, values=tables, state="readonly", font=s)
        tableList.current(0)

        buttonMove = Button(buttonFrame, text = "Move Clip", command = lambda: moveClip(clip, tableList.get()), padx = 10, font=s)
        buttonCancel = Button(buttonFrame, text = "Cancel", command = moveWindow.destroy, font=s)

        heading.grid(row = 0, column = 0)
        text1.grid(row = 1, column = 0)
        tableList.grid(row = 2, column = 0)
        buttonMove.grid(row = 0, column = 0)
        buttonCancel.grid(row = 0, column = 1)
        buttonFrame.grid(row = 3, column = 0)
        mainFrame.place(relx=0.5, rely=0.5, anchor=CENTER)


    def exiting():
        cursor.close()
        mydb.close()
        mainWindow.destroy()

    mainWindow = Tk()
    mainWindow.resizable(False, False)
    mainWindow.configure(width = 1020, height = 950)

    mainWindow.title("ClipSaver")
    s = font.Font(family = "Arial", size = 15)
    headingFont = font.Font(family = "Arial", size = 25)

    root = Frame(mainWindow)
    frameMenu = Frame(root,pady = 10)
    frameMiddle = Frame(root,pady = 10)
    frameMove = Frame(frameMiddle,pady = 10, padx = 10)
    frameActions = Frame(root,pady = 10)

    MainLabel = Label(root, text = "ClipSaver", font = headingFont)




    UnclassifiedMenuButton = Button(frameMenu, text = "Unclassified", command = lambda: changeMenu(0), font = s, state = "disabled")
    PersonalMenuButton = Button(frameMenu, text = "Personal", command = lambda: changeMenu(1), font = s)
    WorkMenuButton = Button(frameMenu, text = "Work", command = lambda: changeMenu(2), font = s)
    PasswordsMenuButton = Button(frameMenu, text = "Passwords", command = lambda: changeMenu(3), font = s)

    MenuListBox = Listbox(frameMenu, height = 50, width = 50, selectmode = SINGLE, font = s)




    MainListBox = Listbox(frameMiddle, height = 50, width = 100, selectmode = "SINGLE")




    MoveHeading = Label(frameMove, text = "Move Clip to:", font = s)
    UnclassifiedMoveButton = Button(frameMove, text = "Unclassified", command = lambda: moveTo(0), font = s, state = "disabled")
    PersonalMoveButton = Button(frameMove, text = "Personal", command = lambda: moveTo(1), font = s, state = "disabled")
    WorkMoveButton = Button(frameMove, text = "Work", command = lambda: moveTo(2), font = s, state = "disabled")
    PasswordsMoveButton = Button(frameMove, text = "Passwords", command = lambda: moveTo(3), font = s, state = "disabled")


    MoveButton = Button(frameMove, text = "Move Clip", command = lambda: moveClipWindow(MainListBox.get(MainListBox.curselection()[0])), font = s, state = "disabled")



    CloseButton = Button(frameActions, text = "Close ClipSaver", command = exiting, font = s)
    CopyButton = Button(frameActions, text = "Copy Selection", command = copy, font = s)
    DeleteButton = Button(frameActions, text = "Delete Selection", command = delete, font = s)
    ClearButton = Button(frameActions, text = "Clear Clipboard", command = lambda: clear(menu), font = s)
    NewButton = Button(frameActions, text = "New List", command = newList, font = s)

    UnclassifiedMenuButton.grid(column = 0, row = 0, padx = 5)
    PersonalMenuButton.grid(column = 1, row = 0, padx = 5)
    WorkMenuButton.grid(column = 2, row = 0, padx = 5)
    PasswordsMenuButton.grid(column = 3, row = 0, padx = 5)

    MoveHeading.grid(column = 0, row = 0, pady = 5)
    UnclassifiedMoveButton.grid(column = 0, row = 1, pady = 5)
    PersonalMoveButton.grid(column = 0, row = 2, pady = 5)
    WorkMoveButton.grid(column = 0, row = 3, pady = 5)
    PasswordsMoveButton.grid(column = 0, row = 4, pady = 5)
    MoveButton.grid(column = 0, row = 5, pady = 5)

    CloseButton.grid(column = 0,row = 0,padx = 10)
    CopyButton.grid(column = 1,row = 0,padx = 10)
    DeleteButton.grid(column = 2,row = 0,padx = 10)
    ClearButton.grid(column = 3,row = 0,padx = 10)
    NewButton.grid(column = 4,row = 0,padx = 10)

    MainLabel.grid(row = 0,column = 0,pady = 10)
    frameMenu.grid(row = 1,column = 0)
    MainListBox.grid(row = 0,column = 0)
    frameMove.grid(row = 0,column = 1)
    frameMiddle.grid(row = 2,column = 0)
    frameActions.grid(row = 3,column = 0)

    root.place(relx = 0.5, rely = 0.5, anchor = "center")

    listRouter()
    mainLoop()

    mainWindow.mainloop()


if __name__  ==  "__main__":
    main()

    # 0 -> unclassified
    # 1 -> personal
    # 2 -> work
    # 3 -> passwords