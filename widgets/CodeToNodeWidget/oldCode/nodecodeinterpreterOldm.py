import ast


class NodeCodeInterpreter:
    currentBiggusNode = None
    biggusNodes = []

    def __init__(self, biggusPy, canvas):
        self.canvas = canvas
        self.biggusPy = biggusPy

    def parseCommand(self, command):
        print(f"parsing command: {command}")
        parsedCode = ast.parse(command)
        for node in ast.walk(parsedCode):

            if isinstance(node, ast.Call):
                print(f"Debug from ast.call: biggusNode.func: {node.func}")
                self.handleCall(node)
            elif isinstance(node, ast.Assign):
                self.handleAssign(node)

    def handleAssign(self, astNode):
        """
        ITA:
            Handle Assign avviene quando ad esempio trova a = createNode("NumberNode", value=5)
        :param astNode:
        :return:
        """
        if astNode.value.func.id == "createNode":
            biggusNode = self.createNode(astNode.value)
            variable = astNode.targets[0].id
            var = {variable: biggusNode}


    def handleCall(self, node):
        if isinstance(node.func, ast.Attribute):
            print(f"Debug from ast.attribute: biggusNode.func: {node.func}")
            self.handleAttribute(node.func)
        elif isinstance(node.func, ast.Name):
            print(f"Debug from ast.name: biggusNode.func: {node.func}")
            self.handleName(node)

    def handleAttribute(self, node):
        pass

    def handleName(self, node):
        if node.func.id == "createNode":
            self.createNode(node)
        elif node.func.id == "addNode":
            self.addNode(node)
        elif node.func.id == "setPos":
            self.setPos(self.currentBiggusNode, node.args[0].n, node.args[1].n)
        elif node.func.id == "setConnections":
            self.setConnections(self.currentBiggusNode, node.args[0].n, node.args[1].s, node.args[2].n)

    def createNode(self, astNode):
        """
        ITA:
            Se nel terminale viene scritto: createNode("NumberNode")
            allora viene creato un nodo NumberNode e viene salvato in self.currentBiggusNode
            il nodo può essere inizializzato con un valore di default oppure con un nome
            e con un valore di partenza.
        ENG:
            If in the terminal is written: createNode("NumberNode")
            then a NumberNode is created and saved in self.currentBiggusNode
            the node can be initialized with a default value or with a name
            and with a starting value.
        :param astNode: ast.Call
        :return:
        """
        nodeClass = astNode.args[0].s
        nodeName = None
        nodeValue = astNode.keywords[0].value.n if astNode.keywords else None
        biggusNode = self.canvas.createNode(nodeClass)
        if biggusNode is None:
            self.sendToTerminal("WARNING:", "Node not found")
            return
        if nodeName:
            biggusNode.setName(nodeName)
        if nodeValue:
            biggusNode.changeInputValue(0, nodeValue)
        self.currentBiggusNode = biggusNode
        return biggusNode

    def addNode(self, node):
        """
        ITA:
            Se nel terminale viene scritto: addNode() senza parametri
            allora viene aggiunto al canvas l'ultimo nodo creato
            Se invece viene scritto: addNode("NumberNode_0")
            allora viene aggiunto al canvas il nodo NumberNode_0
        ENG:
            If in the terminal is written: addNode() without parameters
            then the last created biggusNode is added to the canvas
            If instead it is written: addNode("NumberNode_0")
            then the NumberNode_0 biggusNode is added to the canvas
        :param node:
        :return:
        """
        # questo non funziona perchè c'è confusione fra nodi ast e nodi biggus
        if isinstance(node.args[0], ast.Str):
            node = self.canvas.getNodeByName(node.args[0].s)
        elif isinstance(node.args[0], ast.Name):
            node = self.canvas.getNodeByName(node.args[0].id)
        elif isinstance(node.args[0], ast.Attribute):
            node = self.canvas.getNodeByName(node.args[0].attr)
        elif isinstance(node, 'AbstractNodeInterface'):
            pass
        if node is None:
            if self.currentBiggusNode is not None:
                self.biggusNodes.append(self.currentBiggusNode)
                self.currentBiggusNode = None
        else:
            self.biggusNodes.append(node)
            self.canvas.addNode(node)
            self.currentBiggusNode = None

    def setPos(self, node, x, y):
        node.setPos(x, y)

    def setConnections(self, node1, index1=0, node2=None, index2=0):
        """
        ITA:
            nel canvas per creare la connessione si usa:
            addConnection(self, inputNode, inIndex, outputNode, outIndex):
            Se nel terminale viene scritto: setConnections("NumberNode_0", "NumberNode_1")
            si da per scontato che la connessione avvenga fra l'out principale del primo nodo
            e il primo in libero del secondo nodo.
            Se invece viene scritto: setConnections("NumberNode_0", 1, "NumberNode_1", 2)
            allora viene creata una connessione tra i due nodi con gli indici specificati
        ENG:
            in the canvas to create the connection you use:
            addConnection(self, inputNode, inIndex, outputNode, outIndex):
            If in the terminal it is written: setConnections("NumberNode_0", "NumberNode_1")
            it is assumed that the connection takes place between the main out of the first biggusNode
            and the first free in of the second biggusNode.
            If instead it is written: setConnections("NumberNode_0", 1, "NumberNode_1", 2)
            then a connection between the two nodes with the specified indices is created

        :param node1:
        :param index1: out index of node1
        :param node2:
        :param index2: in index of node2 or if 0 the first free in
        :return:
        """
        if node2 is None:
            self.sendToTerminal("WARNING:", "Missing node2")
            return
        if index2 == 0:
            index2 = node2.getFirstFreeInPlug()
            if index2 == -1:
                self.sendToTerminal("WARNING:", "No free in plug, index will be set to 0")
                index2 = 0
        self.canvas.setConnections(node1, index1, node2, index2)

    def help(self):
        helpString = ""
        return helpString

    def sendToTerminal(self, *args):
        returnString = f"{' '.join(args)}"
        self.biggusPy.sendToTerminal(returnString)
