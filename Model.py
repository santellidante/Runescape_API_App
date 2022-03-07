# Program Created By: Dante Santelli
# GitHub: github.com/santellidante
# LinkedIn: linkedin.com/in/dantesantelli
# For demonstration purposes only

import requests
import json
from pubsub import pub
from PIL import Image, ImageTk
import pickle
import os


class Model:
    def __init__(self):
        self.itemList = []
        self.itemID = None
        self.itemTemp = None
        self.fileName = None
        self.file = None
        self.passData = None
        self.saveDictionaryFile = None
        self.passNameList = None
        self.itemName = None
        self.itemNameFile = None
        self.idResult = None
        self.itemIconLoad = None
        self.itemIconRender = None
        self.equipable = None
        self.buyLimit = None
        self.returnData = None

    def createItemFromID(self, itemID):
        self.itemID = itemID
        try:
            self.itemTemp = self.OSRSItem(self.itemID)
            self.loadItemImage(self.itemID)
        except:
            print("Model: Error finding item!")
        if self.itemTemp:
            self.itemList.insert(0, self.itemTemp)
            pub.sendMessage("OSRSItemCreated", data=self.itemList[0])
            print("Model:", self.itemTemp.name, "Created!")
            pub.sendMessage("PrintStatus", data="Item Found!")
        else:
            print("Model: Could not create item!")
            pub.sendMessage("PrintStatus", data="Item Not Found!")

    def createItemFromName(self, itemName):
        self.itemName = itemName
        self.idResult = 0
        self.file = open("resources/itemsearch/OSRSItemNames.json", "r")
        self.itemNameFile = json.load(self.file)
        self.idResult = self.itemNameFile[self.itemName]
        try:
            self.itemTemp = self.OSRSItem(self.idResult)
            self.loadItemImage(self.idResult)
        except:
            print("Model: Error creating", self.itemName, "!")

        if self.itemTemp:
            self.itemList.insert(0, self.itemTemp)
            pub.sendMessage("OSRSItemCreated", data=self.itemList[0])
            print("Model:", self.itemTemp.name, "Created!")
            pub.sendMessage("PrintStatus", data="Item Found!")
        else:
            print("Model: Could not create item!")

    def loadItemImage(self, itemID):
        self.itemID = itemID
        try:
            self.itemIconLoad = Image.open("resources/images/" + str(self.itemID) + ".png")
            self.itemIconRender = ImageTk.PhotoImage(self.itemIconLoad)
        except:
            print("Model: Error loading image for item", self.itemID)

    # Clear button pressed
    def clrSession(self):
        self.itemList = []
        print("Model: Item list cleared!")

    # Load menu button pressed
    def loadSession(self, fileName):
        self.fileName = fileName
        os.path.split(self.fileName)
        self.passNameList = []
        if self.itemList:
            self.clrSession()
        else:
            print("Model: Retrieving", self.fileName + "...")
        with open(os.path.basename(self.fileName), 'rb') as self.saveDictionaryFile:
            self.passData = pickle.load(self.saveDictionaryFile)
            self.itemList = self.passData
        for i in range(len(self.passData)-1):
            self.passNameList.append(self.passData[i].name)
        return self.passNameList

    # Save menu button pressed
    def saveSession(self, data):
        self.fileName = data
        if self.itemList:
            with open(str(self.fileName), 'wb+') as self.saveDictionaryFile:
                pickle.dump(self.itemList, self.saveDictionaryFile)
        else:
            print("Model: Error saving session! Empty item list!")

    def loadListItem(self, index):
        self.returnData = self.itemList[index]
        self.loadItemImage(self.returnData.id)
        print("Model: Item information retrieved")
        return self.returnData

    def removeListItem(self, index):
        self.itemList.pop(index)
        print("Model: Item removed")

        # Class for item instancing
    class OSRSItem:
        def __init__(self, itemID):
            r = requests.get("https://www.osrsbox.com/osrsbox-db/items-json/" + str(itemID) + ".json")
            if r.status_code == 200:
                print("Controller: Request for item", itemID, "sent")
                data = json.loads(r.text)
                try:
                    self.name = data['name']
                    print("Model:", self.name, "found!")
                    self.price = data['cost']
                    self.description = data['examine']
                    self.id = data['id']
                    self.membersOnly = data['members']
                    self.isTradeable = data['tradeable']
                    self.availableOnGE = data['tradeable_on_ge']
                    self.isStackable = data['stackable']
                    self.isNoteable = data['noteable']
                    self.lowAlch = data['lowalch']
                    self.highAlch = data['highalch']
                    self.itemWeight = data['weight']
                    self.equipable = data['equipable']
                    self.buyLimit = data['buy_limit']
                    self.isQuestItem = data['quest_item']
                    self.releaseDate = data['release_date']
                    self.wikiURL = data['wiki_url']
                except:
                    print("Model: Error creating item!")
                    pub.sendMessage("PrintStatus", data="Item Not Found!")
            else:
                print("Model: Error with item request!")
                pub.sendMessage("PrintStatus", data="Item Not Found!")
