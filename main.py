from tkinter import *
from tkinter import ttk

import pyperclip as ppc
from memory_profiler import profile
import tkinter.font as font
import sqlite3, time
from datetime import datetime

@profile
def main():
    mydb = sqlite3.connect('clipsaver.db')
    cursor = mydb.cursor()
    delay = 50

    def getCurrentTable():
        print(MenuComboBox.get())
        print(cursor.execute("SELECT * FROM tables").fetchall())
        return MenuComboBox.get()

    def getTable(index):
        return MenuListBox.get(0,"end")[index]

    def getClip(ListIndex):
        clip = MainListBox.get(ListIndex, ListIndex)
        return clip[0]

    def copy():
        ppc.copy(getClip(MainListBox.curselection()[0]))

    #
    #       Database Access
    #

    def createList(tableName, tableType):
        cursor.execute("CREATE TABLE IF NOT EXISTS {} (dnt DATETIME NOT NULL, clip VARCHAR(65535))".format(tableName))
        cursor.execute("INSERT INTO tables VALUES (?,?)", (tableName, tableType))
        mydb.commit()

    def tableGen(do=False):
        if do:
            length = cursor.execute("SELECT count(*) FROM tables WHERE type = True").fetchone()[0]
            query = cursor.execute("SELECT tableName FROM tables WHERE type = True")
        else:
            length = cursor.execute("SELECT count(*) FROM tables").fetchone()[0]
            query = cursor.execute("SELECT tableName FROM tables")
        for i in range(length):
            yield query.fetchone()[0]

    def delete():
        clip = getClip(MainListBox.curselection()[0])
        cursor.execute(f"DELETE FROM {getCurrentTable()} WHERE clip=?", (clip,))
        MainListBox.delete(MainListBox.curselection()[0])
        mydb.commit()

    def clear(tableName):
        cursor.execute(f"DELETE FROM {tableName}")
        mydb.commit()
        MainListBox.delete(0, MainListBox.size() + 1)

    def writeClip(clip, tableName):
        dnt = time.strftime("%Y-%m-%d %H:%M:%S")
        numb = cursor.execute(f"SELECT count(*) FROM {tableName}").fetchone()[0]
        if numb >= 50:
            cursor.execute(f"DELETE FROM {tableName} WHERE dnt=?", (
                cursor.execute(f"SELECT dnt FROM {tableName} ORDER BY dnt DESC").fetchone()[0],))
            MainListBox.delete(0, 0)

        cursor.execute(f"INSERT INTO {tableName} VALUES(?,?)", (dnt, clip))
        mydb.commit()

    def getBoard(tableName):
        records = cursor.execute(f"SELECT count(*) FROM {tableName}").fetchone()[0]
        query = cursor.execute(f"SELECT clip FROM {tableName}")
        for i in range(records if records <= 50 else 50):
            yield query.fetchone()[0]  # memory optimization technique

    def moveClip(clip, newTable):
        cursor.execute("DELETE FROM {} WHERE clip=?;".format(getCurrentTable()), (clip,))
        MainListBox.delete(MainListBox.get(0, "end").index(clip))
        cursor.execute("INSERT INTO {} VALUES (?,?)".format(newTable), (time.strftime("%Y-%m-%d %H:%M:%S"), clip))
        mydb.commit()

    #
    #       App Windows
    #

    def moveClipWindow(clip):
        moveWindow = Toplevel(mainWindow)
        moveWindow.title("Move Clip")
        moveWindow.resizable(False, False)
        moveWindow.configure(width=300, height=300)

        tables = [x[0] for x in cursor.execute("SELECT tablename FROM tables").fetchall()]

        mainFrame = Frame(moveWindow, padx=20, pady=20)
        buttonFrame = Frame(mainFrame, padx=10, pady=10)
        heading = Label(mainFrame, text="Clip: " + clip, padx=10, pady=10, font=s)
        text1 = Label(mainFrame, text="Move to:", justify=LEFT, padx=10, pady=10, font=s)
        tableList = ttk.Combobox(mainFrame, values=tables, state="readonly", font=s)
        tableList.current(0)

        buttonMove = Button(buttonFrame, text="Move Clip", command=lambda: moveClip(clip, tableList.get()), padx=10,
                            font=s)
        buttonCancel = Button(buttonFrame, text="Cancel", command=moveWindow.destroy, font=s)

        heading.grid(row=0, column=0)
        text1.grid(row=1, column=0)
        tableList.grid(row=2, column=0)
        buttonMove.grid(row=0, column=0)
        buttonCancel.grid(row=0, column=1)
        buttonFrame.grid(row=3, column=0)
        mainFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

    def newListWindow():
        def submitList():
            name = nameField.get()
            pwd = "selected" in typePass.state()
            udlWindow.destroy()
            createList(name, pwd)
            updateMenu()

        udlWindow = Toplevel(mainWindow)
        udlWindow.title("New List")
        udlWindow.resizable(False, False)
        udlWindow.configure(width=350, height=200)
        mainFrame = Frame(udlWindow, padx=20, pady=20)
        buttonFrame = Frame(mainFrame, padx=10, pady=10)
        udlLabel = Label(mainFrame, text="Create New List", padx=10, pady=10, font=("Arial", 20))
        nameField = Entry(mainFrame, width=30, justify=CENTER, name="name", font=s)
        typePass = ttk.Checkbutton(mainFrame, text="Is this a password List?", variable=IntVar())
        submitButton = Button(buttonFrame, text="Submit", command=submitList, padx=10, font=s)
        cancelButton = Button(buttonFrame, text="Cancel", command=udlWindow.destroy, padx=10, font=s)

        udlLabel.grid(row=0, column=0)
        nameField.grid(row=1, column=0)
        typePass.grid(row=2, column=0)
        submitButton.grid(row=0, column=0)
        cancelButton.grid(row=0, column=1)
        buttonFrame.grid(row=3, column=0)

        mainFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

    #
    #       EXITING THE APP
    #

    def exiting():
        cursor.close()
        mydb.close()
        mainWindow.destroy()

    #
    #       App Algorithms
    #

    def deleteList():
        cursor.execute(f"DROP TABLE {getCurrentTable()}")
        cursor.execute(f"DELETE FROM tables WHERE tableName={getCurrentTable()}")
        mydb.commit()
        updateMenu()

    def init():
        cursor.execute('CREATE TABLE IF NOT EXISTS tables(tableName VARCHAR(50), type INTEGER)')
        if not cursor.execute('SELECT * FROM tables').fetchall():
            createList("List1", False)
        mydb.commit()

        updateMenu()

        changeList(MenuComboBox.get())

    def updateMenu():
        tables = tableGen()
        a = []
        for i in tables:
            a.append(i)
        MenuComboBox['values'] = a
        MenuComboBox.current(0)
        del a, tables

    def updateList(tableName):
        newClip = cursor.execute(f"SELECT clip FROM {tableName} ORDER BY dnt DESC").fetchone()[0]
        MainListBox.insert(MainListBox.size(), newClip)

    def deleteOldPwd():
        tables = tableGen(True)
        for table in tables:
            records = cursor.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
            query = cursor.execute(f"SELECT * FROM {table}")
            delL = ""

            for i in range(records):
                result = query.fetchone()  # fetching rows one at a time instead of calling all the rows into memory
                if "day" in str(datetime.now() - datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")):
                    delL += str(result[0])
            del records, query

            for i in delL:
                cursor.execute(f"DELETE FROM {table} WHERE dnt=?", (str(i),))

            if delL != "":
                mydb.commit()

            del delL

    def changeList(tableName):
        MainListBox.delete(0, END)

        b = getBoard(tableName)
        d = MainListBox.get(0, "end")

        for i in b:
            if i not in d:
                MainListBox.insert(0,i)
        del b, d


    def mainLoop():
        deleteOldPwd()

        current = ppc.paste()

        latest = cursor.execute(f"SELECT clip FROM {getCurrentTable()}").fetchone()
        if latest is None:
            latest=[]

        if current in latest:
            writeClip(current, getCurrentTable())

        if MainListBox.curselection() != ():
            CopyButton.config(state=ACTIVE)
            DeleteButton.config(state=ACTIVE)
            MoveButton.config(state=ACTIVE)
        else:
            CopyButton.config(state=DISABLED)
            DeleteButton.config(state=DISABLED)
            MoveButton.config(state=DISABLED)

        root.after(delay, mainLoop)
    #
    #       Main Window
    #

    mainWindow = Tk()
    mainWindow.resizable(False, False)
    mainWindow.configure(width=1020, height=950)

    mainWindow.title("ClipSaver")
    s = font.Font(family="Arial", size=15)
    headingFont = font.Font(family="Arial", size=25)

    root = Frame(mainWindow)
    frameMenu = Frame(root, pady=10)
    frameMiddle = Frame(root, pady=10)
    frameMove = Frame(frameMiddle, pady=10, padx=10)
    frameActions = Frame(root, pady=10)

    MainLabel = Label(root, text="ClipSaver", font=headingFont)

    MainListBox = Listbox(frameMiddle, height=50, width=100, selectmode="SINGLE")

    MenuListBox = Listbox(frameMove, height=20, width=10, selectmode=SINGLE, font=s)
    MenuComboBox = ttk.Combobox(frameMenu, width=30, height=20)
    MenuComboBox.bind("<<ComboboxSelected>>", lambda e: changeList(MenuComboBox.get()))
    DeleteListButton = Button(frameMove, text="Delete List", command=deleteList, font=s)
    NewButton = Button(frameMove, text=" New List ", command=newListWindow, font=s)
    MoveButton = Button(frameMove, text="Move Clip", command=lambda: moveClipWindow(MainListBox.get(MainListBox.curselection()[0])), font=s, state="disabled")

    CloseButton = Button(frameActions, text="Close ClipSaver", command=exiting, font=s)
    CopyButton = Button(frameActions, text="Copy Selection", command=copy, font=s)
    DeleteButton = Button(frameActions, text="Delete Selection", command=delete, font=s)
    ClearButton = Button(frameActions, text="Clear Clipboard", command=lambda: clear(getCurrentTable()), font=s)

    MenuComboBox.grid(row=0, column=0)

    DeleteListButton.grid(column=0, row=1, pady=10)
    NewButton.grid(column=0, row=2, pady=10)
    MoveButton.grid(column=0, row=3, pady=10)

    CloseButton.grid(column=0, row=0, padx=10)
    CopyButton.grid(column=1, row=0, padx=10)
    DeleteButton.grid(column=2, row=0, padx=10)
    ClearButton.grid(column=3, row=0, padx=10)

    MainLabel.grid(row=0, column=0, pady=10)
    frameMenu.grid(row=1, column=0)
    MainListBox.grid(row=0, column=0)
    frameMove.grid(row=0, column=1)
    frameMiddle.grid(row=2, column=0)
    frameActions.grid(row=3, column=0)

    root.place(relx=0.5, rely=0.5, anchor="center")

    init()
    # listRouter()
    mainLoop()

    mainWindow.mainloop()


if __name__ == "__main__":
    main()

    # 0 -> unclassified
    # 1 -> personal
    # 2 -> work
    # 3 -> passwords
