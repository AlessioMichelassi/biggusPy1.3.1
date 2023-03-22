# -*- coding: utf-8 -*-
import json
from collections import OrderedDict

import numpy as np
from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QWidget

from BiggusMain.elements.Nodes.AbstractClass.AbstractNodeDataV1_2 import AbstractNodeData
from BiggusMain.elements.Nodes.AbstractClass.AbstractNodeGraphicV1_2 import AbstractNodeGraphic
from BiggusMain.elements.Plugs.PlugData import PlugData

"""
ITA:
Un nodo è composto da:
- un oggetto che rappresenta il nodo nel grafico
- un oggetto che rappresenta il nodo nel codice
- un'interfaccia che permette di comunicare tra il nodo nel grafico event il nodo nel codice

ENG:
A biggusNode consists of:
- an object that represents the biggusNode in the graphic
- an object that represents the biggusNode in the code
- an interface that allows communication between the biggusNode in the graphic and the biggusNode in the code

                    nodeInterface
                    |            \
                    |             \
            nodeGraphic         nodeData

ITA:
Di per se un nodo non fa niente di particolare, a parte prendere un valore in ingresso
 event restituirlo in uscita.

Il nodo può essere modificato in modo da fare qualcosa di particolare, per esempio
un nodo che somma due numeri, o un nodo che moltiplica due numeri, o un nodo che
fa una media di due numeri, etc etc.

Per farlo si può creare una classe che eredita abstractNodeInterface, event che implementa
il metodo calculateOutput(plugIndex).

Inoltre è possibile cambiare il numero di Input, il numero di output, il colore del nodo,
la dimensione del nodo, etc etc.

ENG:
In itself a biggusNode does nothing special, except take a biggusNode as input
and return it as output.

The biggusNode can be modified to do something special, for example
a biggusNode that adds two numbers, or a biggusNode that multiplies two numbers, or a biggusNode that
does an average of two numbers, etc etc.

To do this you can create a class that inherits abstractNodeInterface, and that implements
the calculateOutput (plugIndex) method.

In addition, it is possible to change the number of Input, the number of output, the color of the biggusNode,
the size of the biggusNode, etc etc.
"""


class JSONSerializable:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    @classmethod
    def fromJSON(cls, json_str):
        return json.loads(json_str, object_hook=lambda d: cls(**d))


class AbstractNodeInterface:
    colorTrain = []
    toolWidget: QWidget = None
    isDisabled = False
    contextMenu = None
    # Quando il nodo viene salvato, viene salvato anche il valore del menu a tendina
    # in modo da ripristinare lo stato del nodo quando viene caricato
    menuReturnValue = None
    startValue = 0
    isEditable = False
    canvas = None
    mainWidget = None
    _isNodeCreated = False
    hasAToolWidget = False
    # this variable is used to set the biggusNode of the plug to check the compatibility
    valueType = int
    modulePath = "elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2"
    logo = r"Release/biggusFolder/imgs/logos/pythonLogo.png"

    def __init__(self, value=None, inNum=1, outNum=1, canvas=None, parent=None):
        """
        ITA:
            Questa è la classe base per tutti i nodi. Tutti i nodi devono ereditare questa classe.
            AbstractNodeInterface è una classe che fa da ponte fra la parte grafica e la parte dati. I metodi
            che sono definiti in questa classe sono quelli che vengono chiamati dalle altri altre due classi.
        ENG:
            This is the base class for all nodes. All nodes must inherit this class.
            AbstractNodeInterface is a class that acts as a bridge between the graphic part and the data part.
            All methods that are defined in this class are the ones that are called by the other two classes.
        :param value:
        :param inNum:
        :param outNum:
        :param parent:
        """
        self.canvas = canvas
        self.nodeData = AbstractNodeData("AbstractNodeInterface", self)



    @property
    def className(self):
        return self.nodeData.className

    def setName(self, name):
        self.nodeData.name = name
        self.nodeGraphic.updateTitle(name)

    def getName(self):
        return self.nodeData.name

    def setClassName(self, className):
        self.nodeData.className = className
        self.nodeGraphic.updateTitle(className)

    @property
    def index(self):
        return self.nodeData.index

    @index.setter
    def index(self, index):
        self.nodeData.index = index

    def getFont(self, fontType):
        return self.canvas.biggusPy.configFontAndColors[fontType]

    # ------- NODE GRAPHICS METHODS -------

    def getTitle(self):
        return self.nodeData.getTitle()

    def setPos(self, pos):
        self.nodeGraphic.setPos(pos)

    def setPosXY(self, x, y):
        point = QPointF(x, y)
        self.nodeGraphic.setPos(point)

    def getPos(self):
        return self.nodeGraphic.pos()

    def getWidth(self):
        return self.nodeGraphic.width

    def getHeight(self):
        return self.nodeGraphic.height

    def createGraphicClass(self, canvas):
        self.canvas = canvas
        self.nodeGraphic = AbstractNodeGraphic(self)
        self.contextMenu = self.nodeGraphic.contextMenu
        self.createPlug(inNum, outNum)
        self.nodeGraphic.createTitle()
        self.nodeGraphic.createTxtValue()
        pngFile = self.logo
        self.nodeGraphic.setLogo(pngFile)
        if self.colorTrain:
            self.setColorTrain(self.colorTrain)

    def updateTitle(self):
        title = self.nodeData.getTitle()
        self.nodeGraphic.updateTitle(title)
        self.nodeGraphic.updateTitlePosition()

    def setGraphicTitleText(self, title):
        """
        ITA:
            Questo metodo viene chiamato quando il titolo del nodo viene modificato
            dall'utente. Il titolo viene modificato sia nella parte dati che nella parte grafica.
        ENG:
            This method is called when the title of the node is modified by the user.
            The title is modified both in the data part and in the graphic part.
        :param title:
        :return:
        """
        self.nodeData.name = title
        self.canvas.updateTitle(self)
        self.updateTitle()

    def updateTxtTitleFromGraphics(self, title):
        self.nodeData.name = title
        self.nodeData.index = 0
        if self.isEditable:
            self.mainWidget.changeNodeTitle(title)
        if not self.canvas:
            return self.title
        if not self.canvas.getNodeByTitle(self.title):
            self.canvas.nodesTitleList.append(title)
            self.nodeData.index = 0
            return self.title
        node = self.canvas.updateTitle(self)
        return node.getTitle

    def setColorTrain(self, colorTrain):
        self.nodeGraphic.setColorTrain(colorTrain)

    def getColorTrain(self):
        return self.nodeGraphic.getColorTrain()

    def setDisabled(self, isDisabled):
        self.isDisabled = isDisabled

    def getDisabled(self):
        return self.isDisabled

    def setLogo(self, logo):
        self.nodeGraphic.setLogo(logo)

    def changeSize(self, width, height):
        self.nodeGraphic.changeSize(width, height)

    def updateAll(self):
        self.nodeGraphic.updateTitlePosition()
        self.nodeGraphic.updateTxtValuePosition()
        self.nodeGraphic.updatePlugsPos()
        self.nodeGraphic.updateLogoPosition()

    # ------- UPDATE NODE DATA IN NODE GRAPHIC -------

    def updateInPlugValueFromGraphics(self, value):
        """
        ITA:
            Se si connette un nodo ad un altro nodo, questo metodo viene chiamato per aggiornare il valore
            del nodo che viene connesso. Alcuni nodi sono incompatibili fra loro. Una stringa ad esempio non
            sempre può essere convertita in un intero. Per non far crashare il programma, questo metodo
            controlla il tipo di dato che viene passato e lo converte nel tipo di dato che il nodo accetta.
        ENG:
            If you connect a node to another node, this method is called to update the value of the node that
            is connected.
            Some nodes are incompatible with each other. A string for example is not always convertible to an integer.
            To not crash the program, this method checks the type of data that is passed and converts it into
            the type of data that the node accepts.
        :param value:
        :return:
        """
        if self.nodeData.inPlugs[0].valueType == int:
            try:
                value = int(value)
                self.changeInputValue(0, value)
            except ValueError:
                print("ValueError: the biggusNode is not an integer")
        elif self.nodeData.inPlugs[0].valueType == float:
            try:
                value = float(value)
                self.changeInputValue(0, value)
            except ValueError:
                print("ValueError: the biggusNode is not a float")
        else:
            self.changeInputValue(0, value)
        self.nodeGraphic.updateTxtValuePosition()

    # ------- CONNECTION METHODS -------

    @property
    def inConnections(self):
        return self.nodeData.inConnections

    @property
    def outConnections(self):
        return self.nodeData.outConnections

    def disconnect(self, node, index):
        self.nodeData.disconnect(node, index)

    # ------- THIS FUNCTION IS FOR DATA NODES

    def getOutputValue(self, plugIndex):
        return self.nodeData.outPlugs[plugIndex].getValue()

    def getInputValue(self, plugIndex):
        return self.nodeData.inPlugs[plugIndex].getValue()

    def calculateOutput(self, plugIndex):
        """
        Override this function to calculate the output of the node
        :param plugIndex:
        :return:
        """
        raise NotImplementedError

    def getCode(self):
        """
        ITA:
            Questa funzione viene chiamata quando si vuole ottenere il codice del nodo.
            event viene creata direttamente dal nodo.
        ENG:
            This function is called when you want to get the code of the biggusNode.
            and it is created directly by the biggusNode.
        :return:
        """
        print("getCode() not implemented")
        return None

    def getCodeFromInput(self, index):
        """
        ITA:
            Questa funzione viene chiamata quando si vuole ottenere il codice del nodo. Quando si connettono
            due nodi, il nodo in input concatena il suo codice a quello che gli viene passato.
        ENG:
            This function is called when you want to get the code of the biggusNode. When two nodes are connected,
            the input biggusNode concatenates its code to the one that is passed to it.
        :param index:
        :return:
        """
        try:
            if not self.inPlugs[index].inConnection:
                return self.getTitle(), self.inPlugs[index].getCode()
            inPlugNodeName = self.inPlugs[index].inConnection.outputNode.getTitle()
            return inPlugNodeName, self.inPlugs[index].inConnection.outputNode.nodeInterface.getCode()
        except Exception as e:
            return None, None

    # ------- THIS FUNCTION IS FOR PLUGS -------

    def changeInputValue(self, plugIndex, value, isAResetValue=False):
        """
        ITA:
            Cambia il valore di un plug di input.
            Questa funzione viene chiamata quando un plug di input viene modificato durante
            l'inizializzazione del nodo o quando un plug di output viene ricalcolato.
        ENG:
            Change the biggusNode of an input plug.
            This function is called when an input plug is modified during
            the initialization of the biggusNode or when an output plug is recalculated.
        :param isAResetValue: if True, the biggusNode is a reset biggusNode, comes handy when you want disconnect the biggusNode
        :param plugIndex:
        :param value:
        :return:
        """
        self.nodeData.changeValue(plugIndex, value, isAResetValue)
        self.nodeData.calculate()
        if self.outConnections:
            for connection in self.outConnections:
                connection.updateValue()
        self.updateAll()

    @property
    def inPlugs(self):
        return self.nodeData.inPlugs

    @property
    def outPlugs(self):
        return self.nodeData.outPlugs

    def getFirstFreeInPlug(self):
        """
        ITA:
            Ritorna il primo plug di input libero.
        ENG:
            Returns the first free input plug.
        :return:
        """
        for plug in self.inPlugs:
            if not plug.inConnection:
                return plug
        return None

    def createPlug(self, inNumber, outNumber):
        """
        Create the input and output plugs
        :param inNumber: how many input plugs
        :param outNumber: how many output plugs
        :return:
        """
        for x in range(inNumber):
            plug = PlugData("In", x)
            self.nodeData.inPlugs.append(plug)
            gPlug = plug.createPlugGraphic(self.nodeGraphic)
            self.nodeGraphic.inPlugs.append(gPlug)
        for y in range(outNumber):
            plug = PlugData("Out", y)
            self.nodeData.outPlugs.append(plug)
            gPlug = plug.createPlugGraphic(self.nodeGraphic)
            self.nodeGraphic.outPlugs.append(gPlug)
        self.nodeGraphic.updatePlugsPos()

    def setPlugInTitle(self, plugIndex, name):
        """
        ITA:
            Cambia il nome di un plug di input. E' utile quando un plug può avere in ingresso solo un tipo di dato,
            come nel caso di if, while, for, ecc.
        ENG:
            Change the name of an input plug. It is useful when a plug can only have one type of data as input,
            like in the case of if, while, for, etc.
        :param plugIndex:
        :param name:
        :return:
        """
        self.nodeData.inPlugs[plugIndex].setName(name)

    def getPlugInTitle(self, plugIndex):
        return self.nodeData.inPlugs[plugIndex].name

    def setPlugOutTitle(self, plugIndex, name):
        """
        ITA:
            Cambia il nome di un plug di output. E' utile quando ci sono più out e si vuole distinguere il loro
            significato.
        ENG:
            Change the name of an output plug. It is useful when there are more out and you want to distinguish their
            meaning.
        :param plugIndex:
        :param name:
        :return:
        """
        self.nodeData.outPlugs[plugIndex].setName(name)

    def getPlugOutTitle(self, plugIndex):
        return self.nodeData.outPlugs[plugIndex].name

    def addInPlug(self, name=None):
        """
        ITA:
            Ogni nodo viene creato con un numero di plug di default. Alcuni nodi durante la loro vita possono
            richiedere un numero di plug maggiori. Questa funzione aggiunge un plug di input.
        ENG:
            Each biggusNode is created with a default number of plugs. Some biggusNodes during their life can
            require a larger number of plugs. This function adds an input plug.
        :param name:
        :return:
        """
        plug = PlugData("In", len(self.nodeData.inPlugs))
        self.nodeData.inPlugs.append(plug)
        gPlug = plug.createPlugGraphic(self.nodeGraphic)
        if name:
            plug.setName(name)
        self.nodeGraphic.inPlugs.append(gPlug)
        self.nodeGraphic.updatePlugsPos()

    def addInPlugs(self, number, nameList=None):
        """
        ITA:
            Funziona in modo simile a addInPlug, ma aggiunge più plug di input.
        ENG:
            Works in a similar way to addInPlug, but adds more input plugs.
        :param number:
        :param nameList:
        :return:
        """
        for x in range(number):
            plug = PlugData("In", x)
            self.nodeData.inPlugs.append(plug)
            gPlug = plug.createPlugGraphic(self.nodeGraphic)
            if nameList:
                plug.setName(nameList[x])
            self.nodeGraphic.inPlugs.append(gPlug)
        self.nodeGraphic.updatePlugsPos()

    def addOutPlug(self, plug):
        self.nodeData.outPlugs.append(plug)

    def deleteInPlug(self):
        """
        ITA:
            Elimina l'ultimo plug di input. This is for preventing index out of range error
        ENG:
            Delete the last input plug
        :param index:
        :return:
        """
        index = len(self.nodeData.inPlugs) - 1
        if index > 0:
            try:
                if self.nodeData.inPlugs[index].inConnection:
                    connection = self.nodeData.inPlugs[index].inConnection
                    self.canvas.deleteConnection(connection)
                self.canvas.graphicScene.removeItem(self.inPlugs[-1].plugGraphic)
                self.nodeData.deleteInPlug(-1)
                self.nodeGraphic.deleteInPlug(-1)
                self.nodeGraphic.updatePlugsPos()
            except Exception as e:
                print(f"Debug: index was {index} class AbstractNodeInterface, function deleteInPlug, error: {e}")

    def deleteOutPlug(self, index):
        if len(self.nodeData.outPlugs) > 1:
            self.nodeData.outPlugs.pop(index)

    def removeAllUnnecessaryPlugs(self):
        """
        ITA:
            Quando si crea ad esempio un nodo stringa, di default ha 1 plugIn. Se si trasforma il nodo in un replace,
            ha bisogno di 3 inPlug. Per evitare errori, questo metodo elimina tutti i plug che non abbiano indice 0.
        ENG:
            When you create a string node for example, it has a default plugIn. If you turn the node into a replace,
            it needs 3 inPlug. To avoid errors, this method deletes all plugs that do not have index 0.
        :return:
        """
        for _ in range(1, len(self.inPlugs)):
            self.deleteInPlug()
        self.updateAll()

    # ###############################################
    #
    #               CONTEXT MENU
    #

    def showContextMenu(self, position):
        """
        ITA:
            Mostra il menu contestuale del nodo. Questo è il metodo a cui si fa l'override
            per personalizzare il menu contestuale.
        ENG:
            Shows the context menu of the node. This is the method to which you do the override
            to customize the context menu.
        :param position:
        :return:
        """
        pass

    def setMenuOperation(self, operation):
        """
        ITA:
            Quando si salva un nodo, viene salvato anche il valore del menu contestuale in modo che
            alla riapertura del progetto si possa ripristinare lo stato del menu al valore corretto.
        ENG:
            When you save a node, the value of the context menu is also saved so that
            when the project is reopened, the menu state can be restored to the correct value.
        :param operation:
        :return:
        """
        self.menuReturnValue = operation
        # in operation viene salvata la action che ha generato il menu
        # in questo modo si può sapere quale azione è stata scelta
        # event quindi eseguire l'azione corretta
        action = None
        if self.contextMenu is None:
            print("Debug from AbstractNodeInterface: contextMenu is None")
            raise Exception("contextMenu is None")
        for act in self.contextMenu.actions():
            if act.text() == operation:
                action = act
                self.nodeGraphic.contextMenu.setDefaultAction(action)
                return
            print(f"{operation} - Azione non trovata")

    def showToolWidget(self):
        """
        ITA:
            Ogni nodo può avere un widget per regolare i parametri. Questo metodo mostra il widget.
        ENG:
            Each node can have a widget to adjust the parameters. This method shows the widget.
        :return:
        """
        if self.hasAToolWidget:
            self.toolWidget.show()

    # ---------------------- SERIALIZATION  --------------------------------

    def serialize(self):
        connections = []
        for connection in self.nodeData.outConnections:
            connections.append(connection.serialize())

        startValue = self.nodeData.inPlugs[0].getValue()
        if isinstance(startValue, np.ndarray):
            startValue = startValue.tolist()
        elif startValue is not JSONSerializable:
            startValue = str(startValue)
        dicts = OrderedDict([
            ('className', self.className),
            ('modulePath', self.modulePath),
            ('name', self.getName()),
            ('title', self.nodeData.getTitle()),
            ('index', self.index),
            ('startValue', startValue),
            ('menuReturnValue', self.menuReturnValue),
            ('pos', (int(self.nodeGraphic.pos().x()), int(self.nodeGraphic.pos().y()))),
            ('inPlugsNumb', len(self.inPlugs)),
            ('outPlugsNumb', len(self.outPlugs)),
            ('connections', connections)
        ])
        return dicts
