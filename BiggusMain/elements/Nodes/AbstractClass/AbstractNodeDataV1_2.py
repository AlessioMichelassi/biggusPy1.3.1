# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class AbstractNodeData:
    className = "newAbstractNode"
    name: str
    index: int = 0
    isDisabled = False
    isNodeCreated: bool = False

    def __init__(self, className: str = None, nodeInterface=None):
        """
        ITA:
            Questa classe rappresenta un nodo generico. Un nodo è un oggetto che può essere collegato ad altri nodi.
            Un nodo può avere dei plug di input e dei plug di output e il numero minimo è uno per ogni tipo.
            La classe viene chiamata da abstractNodeInterface al momento della creazione del nodo e contiene i dati
            del nodo come la classe del nodo "NumberNode" o "StringNode" e il nome che può essere x, y, z, ecc, il
            titolo che viene usato per identificare il nodo nella canvas in modo univoco ed è definito dal nome
            e dall'indice del nodo. L'indice viene incrementato ogni volta che viene creato un nodo con lo stesso titolo.
        ENG:
            This class represents a generic node. A node is an object that can be connected to other nodes.
            A node can have input and output plugs and the minimum number is one for each type.
            The class is called by abstractNodeInterface at the time of creating the node and contains the data
            of the node such as the class of the node "NumberNode" or "StringNode" and the name that can be x, y, z, etc., the
            title that is used to identify the node in the canvas in a unique way and is defined by the name
            and the index of the node. The index is incremented each time a node with the same title is created.
        :param className:
        :param nodeInterface:
        """
        self.name = className
        self.className = className
        self.nodeGraphic = None
        self.nodeInterface = nodeInterface
        self.inPlugs = []
        self.outPlugs = []
        self.outConnections = []
        self.inConnections = None
        self.isNodeCreated = True

    def __str__(self):
        """
        ITA:
            Ritorna una stringa con i dati del nodo. E' utile per il debug.
        ENG:
            Returns a string with the data of the node. It is useful for debugging.
        :return:
        """
        returnPlugs = ""

        for plug in self.inPlugs:
            returnPlugs += f"{plug.getTitle()} = {plug.getValue()} - "
        for plug in self.outPlugs:
            returnPlugs += f"{plug.getTitle()} = {plug.getValue()} -"

        returnConnectionString = ""
        for connection in self.outConnections:
            returnConnectionString += f"{connection} - "
        return f"className: {self.className}\n\tName: {self.name}\n\tTitle: {self.getTitle()}\n\tplugs: {returnPlugs}" \
               f"\n\t{returnConnectionString}"

    def getTitle(self):
        """
        ITA:
            Ritorna il titolo del nodo che è definito dal nome e dall'indice del nodo.
        ENG:
            Returns the title of the node which is defined by the name and the index of the node.
        :return:
        """
        return f"{self.name}_{self.index}"

    def deleteInPlug(self, index):
        """
        ITA:
            Elimina un plug di input.
        ENG:
            Delete an input plug.
        :param index:
        :return:
        """
        try:
            self.inPlugs.pop(index)
        except IndexError:
            print("Warning from AbstractNodeData.deleteInPlug: index out of range")

    def changeValue(self, index=0, value=1, isAResetValue=False):
        """
        ITA:
            Cambia il valore di un plug di input.
            Questa funzione viene chiamata quando un plug di input viene modificato durante
            l'inizializzazione del nodo o quando un plug di output viene ricalcolato.
        ENG:
            Change the biggusNode of an input plug.
            This function is called when an input plug is modified during
            the initialization of the biggusNode or when an output plug is recalculated.
        :param value: a biggusNode like 10 or "hello"
        :param index: plug index
        :param isAResetValue: This biggusNode is used to reset the biggusNode of the plug. Comes handy to set a
                                default biggusNode for a plug when is created or disconnected.
        :return:
        """
        if isAResetValue:
            print(f"Resetting {self.name} plug {index} to {value}")
            self.nodeInterface.startValue = value
        self.inPlugs[index].setValue(value)
        self.calculate()
        if self.outConnections:
            for connection in self.outConnections:
                connection.updateValue()

    def calculate(self):
        """
            For every output plug, calculate the return biggusNode
        :return:
        """
        for i in range(len(self.outPlugs)):
            self.nodeInterface.calculateOutput(i)

    def calculateCode(self):
        """
        Calculate the code of the biggusNode
        :return:
        """
        return self.nodeInterface.getCode()

    def checkInput(self, _type):
        """
        Check if the input is All of correct type
        :param _type:
        :return:
        """
        valueReturn = []
        for plug in self.inPlugs:
            if plug.getValue() is None:
                return False
            if type(plug.getValue()) == _type:
                valueReturn.append(True)
            else:
                valueReturn.append(False)
        return False not in valueReturn

    def outConnect(self, connection):
        """
        ITA:
            Quando viene creata una connessione con l'outPlug del nodo, viene aggiunta la connessione
            alla lista delle connessioni del nodo e viene chiamata la funzione updateValue() per
            aggiornare il valore del plug di output.
        ENG:
            When a connection is created with the outPlug of the biggusNode, the connection is added
            to the list of connections of the biggusNode and the updateValue() function is called to
            update the value of the output plug.
        :param connection:
        :return:
        """
        self.outConnections.append(connection)
        for _connection in self.outConnections:
            _connection.updateValue()

    def inConnect(self, connection):
        """
        ITA:
            Questa è una piccola violazione alla regola delle connessioni possibili solo da out a in.
            Se si cancella un nodo e questo è collegato in input ad un altro nodo, l'unico modo per risalire
            al nodo collegato in input è attraverso la connessione. Quindi quando viene creata una connessione
            con l'inPlug del nodo, siccome è permessa una sola connessione in input, viene eliminata la
            connessione precedente e viene aggiunta la nuova connessione.
        ENG:
            This is a small violation of the rule of connections only from out to in.
            If you delete a biggusNode and it is connected as input to another biggusNode, the only way to get back
            to the biggusNode connected as input is through the connection. So when a connection is created
            with the inPlug of the biggusNode, since only one input connection is allowed, the previous connection is
            deleted and the new connection is added.
        :param connection:
        :return:
        """
        inPlug = connection.inputPlug
        inPlug.inConnection = connection
        self.inConnections = connection

    def disconnect(self, node, nodePlugIndex):
        """
        ITA:
            node è il nodo da cui si vuole disconnettere il plug. Viene chiamata la funzione calculate() per
            aggiornare il valore del plug di output e viene chiamata la funzione resetPlug() per resettare il
            valore del plug di input dell'altro nodo.
        :param node: the biggusNode to disconnect
        :param nodePlugIndex: the index of the plug to disconnect
        :return:
        """
        self.calculate()
        node.inPlugs[nodePlugIndex].resetPlug()
        node.calculate()