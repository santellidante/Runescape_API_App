# Program Created By: Dante Santelli
# GitHub: github.com/santellidante
# LinkedIn: linkedin.com/in/dantesantelli
# For demonstration purposes only

import tkinter as tk
from pubsub import pub
import View
import Model


class Controller:
    def __init__(self, parent):
        self.parent = parent
        self.model = Model.Model()
        self.view = View.View(self.parent)
        self.entryText = None
        self.dataTemp = None
        self.fileName = None
        self.passNameList = None
        self.itemIndex = None

        pub.subscribe(self.searchBtnPress, "SearchBtnPressed")
        pub.subscribe(self.textChangeHandler, "OSRSItemCreated")
        pub.subscribe(self.newSessionBtnPressed, "ClearButtonPressed")
        pub.subscribe(self.loadSessionBtnPressed, "LoadSessionButtonPressed")
        pub.subscribe(self.saveSessionBtnPressed, "SaveSessionButtonPressed")
        pub.subscribe(self.statusChecker, "PrintStatus")
        pub.subscribe(self.loadListItem, "LoadListItem")
        pub.subscribe(self.removeListItem, "RemoveListItem")

    def searchBtnPress(self):
        print("Controller: Sending request to Model for (" + str(self.view.entryBox.get()) + ")")
        self.entryText = self.view.entryBox.get()
        if self.view.radioVar.get() == 0:
            try:
                self.model.createItemFromID(self.entryText)
                self.view.geItemsMemory.insert(0, self.dataTemp.name)
                self.view.geItemsMemoryVar.set(self.view.geItemsMemory)
            except:
                print("Controller: Error creating item from ID!")
                self.statusChecker("Item Not Found!")
        elif self.view.radioVar.get() == 1:
            try:
                self.model.createItemFromName(self.entryText)
                self.view.geItemsMemory.insert(0, self.dataTemp.name)
                self.view.geItemsMemoryVar.set(self.view.geItemsMemory)
            except:
                print("Controller: Error creating item from name!")
                self.statusChecker("Item Not Found!")
        else:
            print("Controller: Something went wrong with the item search!")
            self.statusChecker("Unknown Error")

    def newSessionBtnPressed(self):
        print("Controller: Clear button pressed!")
        self.view.entryBox.config(text="")
        self.view.nameLabel.config(text="Name: ")
        self.view.iconLabel.config(image="")
        self.view.idLabel.config(text="(ID:)")
        self.view.priceLabel.config(text="Value: ")
        self.view.descLabel.config(text="Description: \n")
        self.view.membersOnlyLabel.config(text="Members Only: ")
        self.view.equipableLabel.config(text="Equipable: ")
        self.view.buyLimitLabel.config(text="Buy Limit: ")
        self.view.isTradeableLabel.config(text="Tradeable: ")
        self.view.availableOnGeLabel.config(text="Tradeable On GE: ")
        self.view.isStackableLabel.config(text="Stackable: ")
        self.view.isNoteableLabel.config(text="Notable: ")
        self.view.lowAlchLabel.config(text="Low Alch Price: ")
        self.view.highAlchLabel.config(text="High Alch Price: ")
        self.view.itemWeightLabel.config(text="Weight (Kg): ")
        self.view.isQuestItemLabel.config(text="Quest Item: ")
        self.view.releaseDateLabel.config(text="Release Date: ")
        self.view.wikiURLLabel.config(text="OSRS Wiki URL: ")
        self.view.entryBox.delete(0, 'end')
        self.view.statusText.config(text="Status: ")
        if self.model.itemList:
            print("Controller: Clearing item list...")
            self.model.clrSession()
        else:
            print("Controller: Item list is empty!")

    def loadSessionBtnPressed(self, data):
        self.passNameList = []
        self.fileName = data
        print(self.fileName)
        if self.view.geItemsMemory:
            self.view.geItemsMemory = []
            self.view.geItemsMemoryVar.set(self.view.geItemsMemory)
            print("Controller: Item list cleared for load session!")

        else:
            print("Controller: Sending request to Model for:", self.fileName)
        self.passNameList = self.model.loadSession(self.fileName)
        self.view.geItemsMemory = self.passNameList
        self.view.geItemsMemoryVar.set(self.view.geItemsMemory)

    def saveSessionBtnPressed(self, data):
        self.fileName = data
        self.model.saveSession(self.fileName)

    def textChangeHandler(self, data):
        self.dataTemp = data
        try:
            self.view.nameLabel.config(text="Name: " + self.dataTemp.name)
            self.view.iconLabel.config(image=self.model.itemIconRender)
            self.view.idLabel.config(text=("(ID: " + str(self.dataTemp.id) + ")"))
            self.view.priceLabel.config(text=("Value: " + str(self.dataTemp.price) + " GP"))
            self.view.descLabel.config(text="Description: \n" + self.dataTemp.description)
            self.view.membersOnlyLabel.config(text="Members Only: " + str(self.dataTemp.membersOnly))
            self.view.isTradeableLabel.config(text="Tradeable: " + str(self.dataTemp.isTradeable))
            self.view.availableOnGeLabel.config(text="Tradeable On GE: " + str(self.dataTemp.availableOnGE))
            self.view.isStackableLabel.config(text="Stackable: " + str(self.dataTemp.isStackable))
            self.view.isNoteableLabel.config(text="Notable: " + str(self.dataTemp.isNoteable))
            self.view.lowAlchLabel.config(text="Low Alch Price: " + str(self.dataTemp.lowAlch) + " GP")
            self.view.highAlchLabel.config(text="High Alch Price: " + str(self.dataTemp.highAlch) + " GP")
            self.view.equipableLabel.config(text="Equipable: " + str(self.dataTemp.equipable))
            self.view.buyLimitLabel.config(text="Buy Limit: " + str(self.dataTemp.buyLimit))
            self.view.itemWeightLabel.config(text="Weight (Kg): " + str(self.dataTemp.itemWeight))
            self.view.isQuestItemLabel.config(text="Quest Item: " + str(self.dataTemp.isQuestItem))
            self.view.releaseDateLabel.config(text="Release Date: " + str(self.dataTemp.releaseDate))
            self.view.wikiURLLabel.config(text="OSRS Wiki URL: " + str(self.dataTemp.wikiURL))
        except:
            print("Controller: Error creating item!")

    def statusChecker(self, data):
        self.error = data
        self.view.statusText.config(text="Status: " + data)

    def loadListItem(self):
        for item in self.view.itemsListBox.curselection():
            self.itemIndex = item
            print(self.itemIndex)
        self.textChangeHandler(self.model.loadListItem(self.itemIndex))

    def removeListItem(self):
        for item in self.view.itemsListBox.curselection():
            self.itemIndex = item
        self.view.geItemsMemory.pop(self.itemIndex)
        self.view.geItemsMemoryVar.set(self.view.geItemsMemory)
        self.model.removeListItem(self.itemIndex)




if __name__ == "__main__":
    mainWindow = tk.Tk()
    WIDTH = 550
    HEIGHT = 445
    mainWindow.geometry("%sx%s" % (WIDTH, HEIGHT))
    mainWindow.title("OSRS API Browser")
    mainWindow.minsize(width=550, height=445)
    mainWindow.maxsize(width=550, height=445)
    app = Controller(mainWindow)
    mainWindow.mainloop()
