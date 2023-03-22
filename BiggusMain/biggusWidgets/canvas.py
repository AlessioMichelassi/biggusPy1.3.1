import importlib
import shutil
from importlib import *
import json
import os
import sys
from collections import OrderedDict
from os.path import exists
from shutil import copytree

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from BiggusMain.biggusWidgets.CodeToNodeWidget.codeToNode import FromCodeToNode
from BiggusMain.biggusWidgets.customFocusWidget import customFocusWidget
from BiggusMain.elements.Connections.Connection import Connection
from BiggusMain.graphicEngine.GraphicSceneOverride import GraphicSceneOverride
from BiggusMain.graphicEngine.graphicViewOverride import GraphicViewOverride

import sys


class Canvas(customFocusWidget):
    mainLayout: QVBoxLayout
    graphicScene: GraphicSceneOverride
    graphicView: GraphicViewOverride
    canvasWidth: int = 64000
    canvasHeight: int = 64000
    clipboard = None
    node_name_list = []

    def __init__(self, biggusPy, parent=None):
        """
        ITA:
        Costruttore della classe Canvas, che rappresenta il canvas su cui verranno disegnati i nodi e le connessioni.
        ENG:
        Canvas class constructor, which represents the canvas on which the nodes and connections will be drawn.
        :param biggusPy:
        :param parent:
        """
        super().__init__(biggusPy, parent)
        self.fileName = "Untitled"
        self.initUI()
        self.nodes = []
        self.nodesTitleList = []
        self.connections = []
        self.clipboard = QApplication.clipboard()
        self.setAcceptDrops(True)

    def __str__(self):
        returnNodes = ""
        for node in self.nodes:
            returnNodes += f"{node}\n"
        return returnNodes

    def initUI(self):
        self.mainLayout = QVBoxLayout()
        self.graphicScene: GraphicSceneOverride = GraphicSceneOverride()
        self.graphicScene.setGraphicSceneSize(self.canvasWidth, self.canvasHeight)
        self.graphicView: GraphicViewOverride = GraphicViewOverride(self, self.graphicScene)
        self.graphicScene.canvas = self
        self.graphicScene.graphicView = self.graphicView
        self.mainLayout.addWidget(self.graphicView, 1, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.mainLayout)

    # ------------------- CONTEXT MENU -------------------

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        contextMenu = QMenu(self)

        actionCenterObject = contextMenu.addAction("Center Object on View")
        contextMenu.addSeparator()
        contextMenu.addSection("Python Nodes")
        _numberNode = contextMenu.addAction("Number Node")
        _stringNode = contextMenu.addAction("String Node")
        contextMenu.addSeparator()
        _nodeToCode = contextMenu.addAction("codeToNode")
        contextMenu.addSeparator()
        action = contextMenu.exec(self.mapToGlobal(event.pos()))

        if action == actionCenterObject:
            self.graphicView.selectAllCenterSceneAndDeselect()
        if action == _numberNode:
            self.addNodeByName("NumberNode")
        elif action == _stringNode:
            self.addNodeByName("StringNode")

        elif action == _nodeToCode:
            fromCodeToNodeWindow = FromCodeToNode(self, self.parent())
            fromCodeToNodeWindow.show()

    # ------------------- KEYBOARD EVENTS -------------------
    def keyPressEvent(self, event: QKeyEvent):
        """
        ITA:
            Il tasto tab da dei problemi in Qt perchè viene usato tanto. Nel canvas si usa per richiamare
            il tool per cercare i nodi. Se il tool è aperto e si preme tab si seleziona il nodo da aggiungere.
        ENG:
            The tab key gives problems in Qt because it is used so much. In the canvas it is used to call
            the tool to search for nodes. If the tool is open and tab is pressed, the node to be added is selected.
        :param event:
        :return:
        """
        if event.key() == Qt.Key.Key_Tab:
            if not self.graphicView.isTabWindowsOpen:
                self.graphicView.openTabWindow()
                return True
        else:
            super().keyPressEvent(event)

    # ------------------- NODES -------------------

    def searchNodePath(self, className):
        """
        ITA:
        Cerca il path del nodo a partire dal nome della classe. Ritorna il path del nodo.
        ENG:
        Search the path of the node from the name of the class. Returns the path of the node.
        :param className:
        :return:
        """
        for key, value in self.biggusPy.nodesFolderPath.items():
            files = os.listdir(value)
            for file in files:
                if className in file:
                    return value

    def createNode(self, className: str, *args, **kwargs):
        """
        ITA:
        Crea un nodo a partire dal nome della classe ad Es: "NumberNode". Il metodo importa il modulo event crea
        un oggetto della classe passata come parametro, quindi ritorna l'interfaccia del nodo. In args event kwargs
        vanno passati i parametri come Value, Name, InputNumber, OutputNumber ecc...

        ENG:
        Create a biggusNode from the name of the class, for example "NumberNode". The method imports the module and
        creates an object of the class passed as a parameter, then it returns the biggusNode interface. In args and
        kwargs you have to pass parameters such as Value, Name, InputNumber, OutputNumber etc...
        :param className:
        :param kwargs: :return:

        """
        absPath = kwargs.get("absPath", None)
        if absPath:
            del kwargs["absPath"]
        path = self.searchNodePath(className)
        modulePath = path.replace("/", ".")
        module = importlib.import_module(f"{modulePath}.{className}")
        nodeClass = getattr(module, className)
        node = nodeClass(*args, **kwargs)
        node.modulePath = modulePath
        node.canvas = self
        node.setFont()
        value = kwargs.get("value", node.startValue)
        if value:
            node.startValue = value
        return node

    def addNodeFromMenu(self, path, className):
        """
        ITA:
            Aggiunge un nodo alla canvas, tramite il menu. Si usa un metodo diverso da addNode perché cambia
            la posizione di inserimento del nodo.
        ENG:
            Add a biggusNode to the canvas, through the menu. A different method is used from addNode because it changes
            the position of the node insertion.
        :param path:
        :param className:
        :return:
        """
        node = self.createNode(className)
        position = self.graphicScene.currentMousePos
        if not position:
            position = self.graphicScene.sceneRect().center()
        if node:
            self.addNode(node)
            node.setPos(position)

    def addNode(self, node):
        """
        ITA:
            Aggiunge un nodo alla canvas. Se il nodo è già presente nella canvas, aggiorna il titolo aumentando l'indice
            del nodo.
        ENG:
            Add a biggusNode to the canvas. If the node is already present in the canvas, update the title by increasing the
            index of the node.
        :param node:
        :return:
        """
        _node = self.updateTitle(node)
        _node.updateTitle()
        self.nodesTitleList.append(_node.getTitle())
        self.nodes.append(_node)
        self.graphicScene.addItem(_node.nodeGraphic)

    def addNodeByName(self, name, value=None):
        node = self.createNode(name, value) if value else self.createNode(name)
        if node:
            self.addNode(node)
            node.setPos(self.graphicScene.currentMousePos)

    def createAndReturnNode(self, name, value=None):
        return self.createNode(name, value) if value else self.createNode(name)

    def updateTitle(self, node):
        """
        This method update the title of the biggusNode if it is present in the canvas
        :param node: biggusNode to update
        :return:
        """
        while node.getTitle() in self.nodesTitleList:
            node.index += 1
        node.updateAll()
        node.canvas = self
        self.nodesTitleList.append(node.getTitle())
        return node

    def addConnection(self, inputNode, inIndex, outputNode, outIndex):
        """
        This method create a connection object in the Canvas and in the scene.
        Is generally called during deserialization
        :param inputNode:
        :param inIndex:
        :param outputNode:
        :param outIndex:
        :return:
        """
        inputNodeData = inputNode.nodeData
        OutputNodeData = outputNode.nodeData

        outputPlug = OutputNodeData.outPlugs[outIndex]
        inputPlug = inputNodeData.inPlugs[inIndex]
        _connection = Connection(OutputNodeData, outputPlug, outputPlug.index, inputNodeData, inputPlug,
                                 inputPlug.index)
        _connection.outputNode.outConnect(_connection)
        _connection.inputNode.inConnect(_connection)
        self.connections.append(_connection)
        self.graphicScene.addItem(_connection)

    def deleteNode(self, node):
        """
        ITA:
            Quando si cancella un nodo, bisogna prima cancellare tutte le connessioni che ha se le ha.
            Poi si rimuove il nodo dalla lista dei nodi e dalla lista dei titoli dei nodi.
            Infine si rimuove il nodo dalla scena.
        ENG:
            When you delete a node, you must first delete all the connections it has if it has them.
            Then you remove the node from the list of nodes and from the list of node titles.
            Finally, you remove the node from the scene.
        :param node:
        :return:
        """
        for connection in self.connections:
            if node.nodeData in [connection.outputNode, connection.inputNode]:
                connection.disconnect()
                if connection in self.graphicScene.items():
                    self.graphicScene.removeItem(connection)

        self.nodesTitleList.remove(node.getTitle())
        self.nodes.remove(node)

    def deleteConnection(self, connection):
        """
        ITA:
            delete a connection from the canvas and from the scene
        ENG:
            delete a connection from the canvas and from the scene
        :param connection:
        :return:
        """
        connection.disconnect()

    def getNodeByTitle(self, title):
        """
        ITA:
            ritorna un nodo a partire dal suo titolo. Se non lo trova ritorna None.
        ENG:
            returns a node from its title. If it does not find it, it returns None.
        :param title:
        :return:
        """
        for node in self.nodes:
            if node.getTitle() == title:
                return node
        print(f"biggusNode title: {title} not found")
        return None

    def cleanTheScene(self):
        """
        ITA:
            Questo metodo serve per pulire la scena. Rimuove tutti i nodi e le connessioni.
        ENG:
            This method is used to clean the scene. Remove all nodes and connections.
        :return:
        """
        items = self.graphicScene.items()
        for item in items:
            if isinstance(item, Connection):
                item.disconnect()
        for item in items:
            if item is not None:
                self.graphicScene.removeItem(item)

        self.nodes = []
        self.connections = []
        self.nodesTitleList = []

    def copyNode(self, nodes):
        """
        ITA:
            Questo metodo serve per copiare un nodo. Lo serializza e lo mette nella clipboard.
        ENG:
            This method is used to copy a node. It serializes it and puts it in the clipboard.
        :param nodes:
        :return:
        """
        nodesList = []
        for node in nodes:
            nodesList.append(node.serialize())
        self.clipboard.setText(json.dumps(nodesList))

    def pasteNode(self):
        """
        ITA:
            Questo metodo serve per incollare un nodo. Prende il testo dalla clipboard e lo deserializza.
            se la deserializzazione va a buon fine, aggiunge il nodo alla scena altrimenti stampa un avviso.
        ENG:
            This method is used to paste a node. It takes the text from the clipboard and deserializes it.
            if the deserialization goes well, it adds the node to the scene otherwise it prints a warning.
        :return:
        """
        try:
            nodes = self.clipboard.text()
            currentPos = self.graphicScene.currentMousePos
            deserializeNodes = json.loads(nodes)
            for node in deserializeNodes:
                self.addSerializedNode(node, currentPos)
        except Exception as e:
            print(e)

    # ------------------ FROM CODE TO NODE ------------------

    def getNodeByName(self, name):
        """
        ITA:
            E' un metodo pericoloso, se due nodi hanno lo stesso nome, ritorna il primo che trova
            però può essere usato quando si sta facendo il codeToNode event si sa che non ci sono
            due nodi con lo stesso nome oppure ci si riferisce sempre alla stessa variabile.
        ENG:
            It is a dangerous method, if two nodes have the same name, it returns the first one it finds
            but it can be used when doing codeToNode and you know that there are not
            two nodes with the same name or you always refer to the same variable.
        :param name:
        :return:
        """
        print(f"getNodeByName: {name}")
        for node in self.nodes:
            if node.nodeData.name == name:
                return node
        return None

    def createNodeFromCodeToNode(self, className, *args, **kwargs):
        """
        This method create a biggusNode from a codeToNode
        :param className: name of the class
        :param args: args of the class
        :param kwargs: kwargs of the class
        :return: biggusNode created
        """
        node = self.createNode(className, *args, **kwargs)
        if node:
            self.addNode(node)
            node.setPos(self.graphicScene.currentMousePos)
        return node

    def updateNodePosition(self, node, x, y):
        """
        ITA:
            Aggiorna la posizione di un nodo. Di solito si usa questo metodo durante il codeToNode.
        ENG:
            Updates the position of a node. This method is usually used during codeToNode.
        :param node:
        :param x:
        :param y:
        :return:
        """
        if node is not None:
            nodeToUpdate = self.getNodeByTitle(node.getTitle())
            nodeToUpdate.setPos(QPointF(x, y))
        else:
            print(f"biggusNode {node} not found")

    # ------------------ SERIALIZATION ------------------

    def serialize(self):
        listOfNodeSerialized = []
        for node in self.nodes:
            listOfNodeSerialized.append(node.serialize())
        dicts = OrderedDict([
            ('name', self.fileName),
            ('sceneWidth', self.canvasWidth),
            ('sceneHeight', self.canvasHeight),
            ('Nodes', listOfNodeSerialized)])
        return json.dumps(dicts, indent=4)

    def deserialize(self, serializedString):
        try:
            self.fileName = serializedString['name']
            self.canvasWidth = serializedString['sceneWidth']
            self.canvasHeight = serializedString['sceneHeight']
            nodes = serializedString['Nodes']
            for node in nodes:
                try:
                    self.addSerializedNode(node)
                except Exception as e:
                    print("WARNING THERE WAS AN ERROR UNPACKING NODES")
                    print(f"node was {node}")
                    print(e)
            for node in nodes:
                try:
                    self.deserializeConnections(node)
                except Exception as e:
                    print("WARNING THERE WAS AN ERROR UNPACKING CONNECTIONS")
                    print(f"node was {node}")
                    print(e)
        except Exception as e:
            print("WARNING THERE WAS AN ERROR IN DESERIALIZATION")
            print("is it a biggus file?")
            print(e)

    def addSerializedNode(self, dictionary, _position=None):
        _className = dictionary["className"]
        _modulePath = dictionary["modulePath"]
        _name = dictionary["name"]
        _title = dictionary["title"]
        _index = dictionary["index"]
        _value = dictionary["startValue"]
        try:
            _menuOperation = dictionary["menuReturnValue"]
        except Exception as e:
            # this is for compatibility with old version
            a = e
            _menuOperation = None
        _pos = dictionary["pos"]
        _inPlugsNumb = dictionary["inPlugsNumb"]
        _outPlugsNumb = dictionary["outPlugsNumb"]
        # se viene specificata la posizione, aumenta la pos corrente
        # del valore specificato
        # è utile quando si fa il paste di un nodo
        if _position:
            pos = QPointF(float(_pos[0] + _position.x()), float(_pos[1] + _position.y()))
        else:
            pos = QPointF(float(_pos[0]), float(_pos[1]))

        node = self.createNode(_className, value=_value, inNum=_inPlugsNumb,outNum=_outPlugsNumb)
        node.setName(_name)
        node.setMenuOperation(_menuOperation)
        self.addNode(node)
        node.setPos(pos)

    def deserializeConnections(self, dictionary):
        connections = dictionary["connections"]
        for connection in connections:

            inputNodeName = connection["inputNodeName"]
            inIndex = int(connection["inputPlug"])
            outputNodeName = connection["outputNodeName"]
            outIndex = int(connection["outputPlug"])

            inputNode = self.getNodeByTitle(inputNodeName)
            outputNode = self.getNodeByTitle(outputNodeName)

            if inputNode and outputNode:
                self.addConnection(inputNode, inIndex, outputNode, outIndex)
