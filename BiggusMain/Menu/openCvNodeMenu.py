import os
from os.path import exists

from PyQt5.QtWidgets import *


class OpenCvNodeMenu(QMenu):
    """
    ITA:
        Menu che permette di creare un nodo python
    ENG:
        Menu that allows you to create a python biggusNode
    """

    creatorString: str = "Created by BiggusPy"
    availableNodeList: list = []

    def __init__(self, mainMenu, mainWindows, parent=None):
        super().__init__(parent)
        self.mainMenu = mainMenu
        self.biggusPy = mainWindows
        self.setTitle('openCv')
        self.createNodeMenu()

    def createNodeMenu(self):
        """
        ITA:
            Crea il menu dei nodi python
        ENG:
            Create the python nodes menu
        :return:
        """
        self.createNodeList()
        for _node in self.availableNodeList:
            _action = QAction(_node, self)
            _action.triggered.connect(self.makeDoNode(_node))
            self.addAction(_action)

    def createNodeList(self):
        """
        ITA:
            Crea la lista dei nodi python
        ENG:
            Create the list of python nodes
        :return:
        """
        nodeFolderPath = self.biggusPy.returnNodePath("openCv")
        if exists(nodeFolderPath):
            for _file in os.listdir(nodeFolderPath):
                if _file.endswith('.py'):
                    self.availableNodeList.append(_file[:-3])
        else:
            print(f"Path {nodeFolderPath} not found!")

    def updateNodeMenu(self):
        """
        ITA:
            Aggiorna la lista dei nodi python
        ENG:
            Update the list of python nodes
        :return:
        """
        self.clear()
        self.createNodeMenu()

    def doNode(self, nodeName):
        """
        ITA:
            Crea un nodo python
        ENG:
            Create a python biggusNode
        :param nodeName:
        :return:
        """
        print(nodeName)
        self.biggusPy.canvas.addNodeFromMenu(self.biggusPy.nodesFolderPath["openCv"], nodeName)

    def makeDoNode(self, nodeName):
        """
        ITA:
            Crea una funzione che richiama doNode con il nome del nodo specificato come argomento
        ENG:
            Create a function that calls doNode with the specified biggusNode name as an argument
        :param nodeName:
        :return:
        """
        return lambda: self.doNode(nodeName)