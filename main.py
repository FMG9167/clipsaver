from tkinter import *
from tkinter import ttk
import pyperclip as ppc
import tkinter.font as font
import sqlite3
from datetime import datetime

latest=""

def main():
    mydb = sqlite3.connect('clipsaver.db')
    cursor = mydb.cursor()
    delay = 50

    #
    #       Basic Python
    #

    def getCurrentTime():
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def copyClip(clip):
        ppc.copy(clip)

    def getCopiedClip():
        return ppc.paste()

    #
    #       Database Access
    #

    def getClipsGeneratorFromTable(tableName):
        length = cursor.execute("SELECT count(*) FROM {}".format(tableName)).fetchone()[0]
        query = cursor.execute("SELECT clip FROM {}".format(tableName))
        for i in range(length):
            yield query.fetchone()[0]

    def createTable(tableName, tableType=0):
        cursor.execute("CREATE TABLE IF NOT EXISTS {}(dnt DATETIME NOT NULL, clip VARCHAR(65335))".format(tableName))
        if cursor.execute("SELECT * FROM tables WHERE tableName=?",(tableName,)).fetchone() is None:
            cursor.execute("INSERT INTO tables VALUES (?,?)", (tableName,tableType))
        mydb.commit()

    def deleteTable(tableName):
        cursor.execute("DROP TABLE IF EXISTS {}".format(tableName))
        cursor.execute("DELETE FROM tables WHERE tableName=?", (tableName,))
        mydb.commit()

    def getTablesList():
        out=[]
        for i in cursor.execute("SELECT tableName FROM tables").fetchall():
            out.append(i[0])
        return out

    def insertClipToTable(tableName, clip):
        cursor.execute("INSERT INTO {} VALUES (?,?)".format(tableName), (getCurrentTime(), clip))
        mydb.commit()

    def deleteClipFromTable(tableName, clip):
        cursor.execute("DELETE FROM {} WHERE clip=?".format(tableName), (clip,))
        mydb.commit()

    #
    #       App Windows
    #

    def moveClipWindow(clip):
        def submit():
            MainListBox.delete(MainListBox.get(0,END).index(clip))
            deleteClipFromTable(getCurrentTable(), clip)
            insertClipToTable(tableList.get(), clip)
            copyClip(clip)
            global latest
            latest=clip
            moveWindow.destroy()

        moveWindow = Toplevel(mainWindow)
        moveWindow.title("Move Clip")
        moveWindow.resizable(False, False)
        moveWindow.configure(width=300, height=300)

        tables = [x[0] for x in cursor.execute("SELECT tablename FROM tables").fetchall()]
        tables.remove(getCurrentTable())

        mainFrame = Frame(moveWindow, padx=20, pady=20)
        buttonFrame = Frame(mainFrame, padx=10, pady=10)
        heading = Label(mainFrame, text="Clip: " + clip, padx=10, pady=10, font=s)
        text1 = Label(mainFrame, text="Move to:", justify=LEFT, padx=10, pady=10, font=s)
        tableList = ttk.Combobox(mainFrame, values=tables, state="readonly", font=s)
        tableList.current(0)

        buttonMove = Button(buttonFrame, text="Move Clip", command=submit, padx=10,
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
            pwd = 1 if "selected" in typePass.state() else 0
            createTable(name, pwd)
            del name, pwd
            udlWindow.destroy()

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
        mydb.commit()
        cursor.close()
        mydb.close()
        mainWindow.destroy()

    #
    #       App Algorithms
    #

    def getCurrentTable():
        print(MenuComboBox.get())
        return MenuComboBox.get()

    def addClipsToListbox():
        generator = getClipsGeneratorFromTable(getCurrentTable())
        for clip in generator:
            if clip not in MainListBox.get(0, END):
                MainListBox.insert(END, clip)
        del generator

    def updateTableCombobox(do=0):
        if do:
            selectedTable=MenuComboBox.get()
        tables = getTablesList()
        MenuComboBox['values'] = tables
        if do:
            MenuComboBox.set(selectedTable)
        del tables

    def updateButtonStates():
        if not MainListBox.curselection():
            DeleteButton.configure(state=DISABLED)
            CopyButton.configure(state=DISABLED)
            MoveButton.configure(state=DISABLED)
        else:
            DeleteButton.configure(state=NORMAL)
            CopyButton.configure(state=NORMAL)
            MoveButton.configure(state=NORMAL)

        if len(MenuComboBox['values']) == 1:
            DeleteListButton.configure(state=DISABLED)
        else:
            DeleteListButton.configure(state=NORMAL)

    def clearMainListbox(e):
        MainListBox.delete(0, END)

    def copySelectedClip():
        copyClip(MainListBox.get(MainListBox.curselection()[0]))

    def deleteSelectedClip():
        deleteClipFromTable(getCurrentTable(), MainListBox.get(MainListBox.curselection()[0]))
        MainListBox.delete(MainListBox.curselection()[0])

    def clearCurrentTable():
        cursor.execute("DELETE FROM {}".format(getCurrentTable()))
        mydb.commit()
        MainListBox.delete(0, END)

    def deleteCurrentList():
        deleteTable(getCurrentTable())
        updateTableCombobox(1)
        MenuComboBox.set(MenuComboBox['values'][0])

    def checkForOldPasswords():
        for i in cursor.execute("SELECT tableName FROM tables WHERE type=1").fetchall():
            for j in cursor.execute("SELECT dnt FROM {}".format(i[0])).fetchall():
                if "day" in str(datetime.strptime(getCurrentTime(), "%Y-%m-%d %H:%M:%S") - datetime.strptime(j[0],"%Y-%m-%d %H:%M:%S")):
                    cursor.execute("DELETE FROM {} WHERE dnt = ?".format(i[0]), (j[0],))
        mydb.commit()

    def init():
        cursor.execute("CREATE TABLE IF NOT EXISTS tables(tableName VARCHAR(64) NOT NULL, type INT NOT NULL)")
        mydb.commit()
        if cursor.execute("SELECT * FROM tables").fetchone() is None:
            createTable("List1",0)

            MenuComboBox['values'] = ['List1']
            MenuComboBox.set('List1')

        updateTableCombobox()

        MenuComboBox.set(MenuComboBox['values'][0])

        addClipsToListbox()

    def mainLoop():
        updateTableCombobox()

        addClipsToListbox()

        updateButtonStates()

        global latest
        if getCopiedClip() not in MainListBox.get(0, END) and getCopiedClip() != latest:
            insertClipToTable(getCurrentTable(), getCopiedClip())
            latest = getCopiedClip()

        checkForOldPasswords()

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

    MenuComboBox = ttk.Combobox(frameMenu, width=30, height=20, state="readonly")
    MenuComboBox.bind("<<ComboboxSelected>>", clearMainListbox)
    DeleteListButton = Button(frameMove, text="Delete List", command=deleteCurrentList, font=s)
    NewButton = Button(frameMove, text=" New List ", command=newListWindow, font=s)
    MoveButton = Button(frameMove, text="Move Clip", command=lambda: moveClipWindow(MainListBox.get(MainListBox.curselection()[0])), font=s, state="disabled")

    CloseButton = Button(frameActions, text="Close ClipSaver", command=exiting, font=s)
    CopyButton = Button(frameActions, text="Copy Selection", command=copySelectedClip, font=s)
    DeleteButton = Button(frameActions, text="Delete Selection", command=deleteSelectedClip, font=s)
    ClearButton = Button(frameActions, text="Clear Clipboard", command=clearCurrentTable, font=s)

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
    mainLoop()

    mainWindow.mainloop()


if __name__ == "__main__":
    main()

    # 0 -> unclassified
    # 1 -> personal
    # 2 -> work
    # 3 -> passwords
