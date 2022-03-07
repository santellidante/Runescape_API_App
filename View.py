# Program Created By: Dante Santelli
# GitHub: github.com/santellidante
# LinkedIn: linkedin.com/in/dantesantelli
# For demonstration purposes only

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pubsub import pub
import os


class View:
    def __init__(self, parent):
        self.parent = parent
        self.tabParent = None
        self.hiScoresTab = None
        self.geItemsTab = None
        self.geItemsFrame = None
        self.geItemsInfoFrame = None
        self.geItemsMemory = None
        self.geItemsMemoryVar = None
        self.entryBox = None
        self.searchButton = None
        self.statusText = None
        self.itemsListBox = None
        self.geItemsTabRightFrame = None
        self.nameLabel = None
        self.iconLabel = None
        self.idLabel = None
        self.priceLabel = None
        self.descLabel = None
        self.radioBtnLabel = None
        self.entryBoxLabel = None
        self.menuBar = None
        self.fileMenu = None
        self.helpMenu = None
        self.loadOrSave = None
        self.fileName = None
        self.saveOrLoad = None
        self.fileResponse = None
        self.idRadioBtn = None
        self.nameRadioBtn = None
        self.radioSelection = None
        self.membersOnlyLabel = None
        self.isTradeableLabel = None
        self.availableOnGeLabel = None
        self.isStackableLabel = None
        self.isNoteableLabel = None
        self.lowAlchLabel = None
        self.highAlchLabel = None
        self.itemWeightLabel = None
        self.isQuestItemLabel = None
        self.releaseDateLabel = None
        self.wikiURLLabel = None
        self.horizontalLeftSeparator = None
        self.verticalLeftSeparator = None
        self.creationYearLabel = None
        self.memoryText = None
        self.loadButton = None
        self.removeButton = None
        self.equipableLabel = None
        self.buyLimitLabel = None
        self.listBoxSelect = None
        self.radioVar = tk.IntVar(self.parent, value=1)
        self.createWidgets()
        self.setupMenuBar()
        self.parent.config(menu=self.menuBar)

    # Main window structural generation
    def createWidgets(self):
        self.geItemsFrame = tk.Frame(self.parent)
        self.geItemsFrame.pack(expand=1, fill='both')
        self.geItemsMemory = []
        self.geItemsMemoryVar = tk.StringVar(value=self.geItemsMemory)

        # Widgets to the LEFT of the separator line
        self.radioBtnLabel = tk.Label(self.geItemsFrame, text="Select a name or ID search:")
        self.radioBtnLabel.place(x=10, y=5)
        self.idRadioBtn = tk.Radiobutton(self.geItemsFrame, text="Name Search", variable=self.radioVar, value=1)
        self.idRadioBtn.place(x=30, y=25)
        self.nameRadioBtn = tk.Radiobutton(self.geItemsFrame, text="ID Search", variable=self.radioVar, value=0)
        self.nameRadioBtn.place(x=40, y=45)
        self.entryBoxLabel = tk.Label(self.geItemsFrame, text="Item Name/ID:")
        self.entryBoxLabel.place(x=17, y=70)
        self.entryBox = tk.Entry(self.geItemsFrame, text="Enter an item ID")
        self.entryBox.place(x=18, y=90)
        self.searchButton = tk.Button(self.geItemsFrame, text="Search", command=self.searchButtonCb)
        self.searchButton.place(x=96, y=109)
        self.statusText = tk.Label(self.geItemsFrame, text="Status: ", wraplength=200, justify='left')
        self.statusText.place(x=15, y=137)
        self.memoryText = tk.Label(self.geItemsFrame, text="Memory: ", wraplength=120, justify='left')
        self.memoryText.place(x=15, y=170)
        self.itemsListBox = tk.Listbox(self.geItemsFrame, height=10, width=21, listvariable=self.geItemsMemoryVar)
        self.itemsListBox.place(x=15, y=190)
        self.loadButton = tk.Button(self.geItemsFrame, text="Load Item", command=self.loadItem)
        self.loadButton.place(x=81, y=385)
        self.removeButton = tk.Button(self.geItemsFrame, text="Remove Item", command=self.removeItem)
        self.removeButton.place(x=64, y=353)

        # Widgets to the RIGHT of the separator line
        self.nameLabel = tk.Label(self.geItemsFrame, text="Name: ", anchor='e', justify="left", font="Arial 16 bold")
        self.nameLabel.place(x=240, y=10)
        self.iconLabel = tk.Label(self.geItemsFrame)
        self.iconLabel.place(x=195, y=15)
        self.idLabel = tk.Label(self.geItemsFrame, text="(ID:)")
        self.idLabel.place(x=240, y=35)
        self.priceLabel = tk.Label(self.geItemsFrame, text="Value: ")
        self.priceLabel.place(x=190, y=70)
        self.descLabel = tk.Label(self.geItemsFrame, text="Description: \n", wraplength=300, justify='left')
        self.descLabel.place(x=190, y=280)
        self.membersOnlyLabel = tk.Label(self.geItemsFrame, text="Members Only: ", wraplength=200, justify='left')
        self.membersOnlyLabel.place(x=350, y=70)
        self.isTradeableLabel = tk.Label(self.geItemsFrame, text="Tradeable: ", wraplength=200, justify='left')
        self.isTradeableLabel.place(x=190, y=130)
        self.availableOnGeLabel = tk.Label(self.geItemsFrame, text="Tradeable On GE: ", wraplength=200, justify='left')
        self.availableOnGeLabel.place(x=350, y=130)
        self.isStackableLabel = tk.Label(self.geItemsFrame, text="Stackable: ", wraplength=200, justify='left')
        self.isStackableLabel.place(x=190, y=160)
        self.isNoteableLabel = tk.Label(self.geItemsFrame, text="Noteable: ", wraplength=200, justify='left')
        self.isNoteableLabel.place(x=350, y=160)
        self.equipableLabel = tk.Label(self.geItemsFrame, text="Equipable: ", wraplength=200, justify='left')
        self.equipableLabel.place(x=190, y=190)
        self.buyLimitLabel = tk.Label(self.geItemsFrame, text="Buy Limit: ", wraplength=200, justify='left')
        self.buyLimitLabel.place(x=350, y=190)
        self.lowAlchLabel = tk.Label(self.geItemsFrame, text="Low Alch Price: ", wraplength=200, justify='left')
        self.lowAlchLabel.place(x=190, y=100)
        self.highAlchLabel = tk.Label(self.geItemsFrame, text="High Alch Price: ", wraplength=200, justify='left')
        self.highAlchLabel.place(x=350, y=100)
        self.itemWeightLabel = tk.Label(self.geItemsFrame, text="Weight (Kg): ", wraplength=200, justify='left')
        self.itemWeightLabel.place(x=350, y=220)
        self.isQuestItemLabel = tk.Label(self.geItemsFrame, text="Quest Item: ", wraplength=200, justify='left')
        self.isQuestItemLabel.place(x=190, y=220)
        self.releaseDateLabel = tk.Label(self.geItemsFrame, text="Release Date: ", wraplength=200, justify='left')
        self.releaseDateLabel.place(x=240, y=250)
        self.wikiURLLabel = tk.Label(self.geItemsFrame, text="OSRS Wiki URL: ", wraplength=300, justify='left')
        self.wikiURLLabel.place(x=190, y=340)

        # Widgets BELOW the bottom separator line
        self.creationYearLabel = tk.Label(self.geItemsFrame, text="Created By: Dante Santelli | GitHub: github.com/"
                                                                  "santellidante | LinkedIn: linkedin.com/in/dantesante"
                                                                  "lli")
        self.creationYearLabel.place(x=2, y=422)


        # Separator setup
        self.horizontalLeftSeparator = ttk.Separator(self.parent, orient='horizontal')
        self.horizontalLeftSeparator.place(x=0, y=160, width=165)
        self.verticalLeftSeparator = ttk.Separator(self.parent, orient='vertical')
        self.verticalLeftSeparator.place(x=165, y=0, height=420)
        self.horizontalBottomSeparator = ttk.Separator(self.parent, orient='horizontal')
        self.horizontalBottomSeparator.place(x=0, y=420, width=700)

    def setupMenuBar(self):
        self.menuBar = tk.Menu(self.parent)
        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        self.helpMenu = tk.Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="New", command=self.newSession)
        self.fileMenu.add_command(label="Load", command=self.loadSession)
        self.fileMenu.add_command(label="Save", command=self.saveSession)
        self.helpMenu.add_command(label="Usage", command=self.usageHelp)
        self.helpMenu.add_command(label="Info", command=self.infoHelp)
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)
        self.menuBar.add_cascade(label="Help", menu=self.helpMenu)

    def searchButtonCb(self):
        print("View: Search button pressed!")
        pub.sendMessage("SearchBtnPressed")

    def newSession(self):
        print("View: New session menu button pressed!")
        self.geItemsMemory = []
        self.geItemsMemoryVar.set(value=self.geItemsMemory)
        pub.sendMessage("ClearButtonPressed")
        return

    def loadSession(self):
        self.saveOrLoad = 1
        self.openFileExplorer(self.saveOrLoad)
        pub.sendMessage("LoadSessionButtonPressed", data=self.fileResponse)

    def saveSession(self):
        self.saveOrLoad = 0
        self.openFileExplorer(self.saveOrLoad)
        pub.sendMessage("SaveSessionButtonPressed", data=self.fileResponse)
        return


    def openFileExplorer(self, saveOrLoad):
        self.fileResponse = ""
        if saveOrLoad == 1:
            self.fileResponse = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a file",
                                                           filetypes=(("Bin Files", "*.bin*"), ("all files", "*.*")))
        else:
            self.fileResponse = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Please select a file")

    def loadItem(self):
        pub.sendMessage("LoadListItem")


    def removeItem(self):
        pub.sendMessage("RemoveListItem")

    def usageHelp(self):
        tk.messagebox.showinfo(title="Usage Help", message="Use the searchbar and radio buttons to search for any item "
                                                           "in OldSchool Runescape, by name or ID! For a complete list "
                                                           "of item names and IDs please visit: \n\n"
                                                           "https://www.osrsbox.com/tools/item-search/ \n\n"
                                                           "Every item searched will appear in the memory box, where yo"
                                                           "u may load and delete items from. Under the 'File' tab on t"
                                                           "he top left, you may utilize the 'Load' and 'Save' function"
                                                           "s!")

    def infoHelp(self):
        tk.messagebox.showinfo(title="Information", message="Coded by: Dante Santelli \n\n"
                                                            "Old School RuneScape (OSRS) content and materials are "
                                                            "trademarks and copyrights of JaGeX or its licensors. All "
                                                            "rights reserved. Dante Santelli is not"
                                                            " associated or affiliated with JaGeX or its licensors.\n\n"
                                                            "The osrsbox-db project is released under the GNU General "
                                                            "Public License version 3 as published by the Free Software"
                                                            " Foundation. "
                                                            "Dante Santelli is not associated or affiliated with the"
                                                            " creators of the osrsbox-api or the osrsbox-db project")
