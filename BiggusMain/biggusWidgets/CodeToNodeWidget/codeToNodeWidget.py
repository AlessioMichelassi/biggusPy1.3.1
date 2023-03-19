import ast

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from scratchONodeV0_9.ArguePy_CodeEditor.editorWidgetTool.tools.codeEditor import pythonCodeEditor


class txtWidget(pythonCodeEditor):
    def __init__(self, parent=None):
        super().__init__(parent)

    def contextMenuEvent(self, event) -> None:
        menu = QMenu(self)
        menu.addSection("getNode! Context Menu")
        _updateFunction = menu.addAction("getNode!")
        menu.addSeparator()
        action = menu.exec(self.mapToGlobal(event.pos()))
        if action == _updateFunction:
            self.parent().createNodeFromCode(self.toPlainText())
            self.parent().canvas.graphicView.selectAllCenterSceneAndDeselect()


class CodeToNodeWidget(QWidget):
    argue: txtWidget
    lastNode = None
    lastIfNode = None
    lastForNode = None
    lastFunctionNode = None
    lastWhileNode = None
    code = None
    functionNodeList = []
    copied_functions = {}
    callNodeList = []
    variableForCallNode = []
    callingIndex = 0
    allNodes = []
    appendPositioningFunction = []

    def __init__(self, canvas, parent=None):
        super().__init__(parent)
        self.canvas = canvas
        self.setGeometry(0, 0, 500, 500)
        self.layout = QVBoxLayout()
        self.argue = txtWidget()
        self.layout.addWidget(self.argue)
        self.setLayout(self.layout)

    def contextMenuEvent(self, event) -> None:
        menu = QMenu(self)
        menu.addSection("getNode! Context Menu")
        _updateFunction = menu.addAction("getNode!")
        menu.addSeparator()
        action = menu.exec(self.mapToGlobal(event.pos()))
        if action == _updateFunction:
            self.createNodeFromCode(self.argue.toPlainText())

    def createNodeFromCode(self, _code: str):
        """
        ITA:
            Questo metodo crea un nodo a partire dal codice passato come parametro grazie alla libreria Ast.
            Ast è una libreria che permette di analizzare il codice python event di creare un AST (Abstract Syntax Tree)
            ovvero un albero sintattico astratto. Questo albero viene poi analizzato per creare i nodi.
            Con parseCode() viene creato l'AST event con nodeSearch() viene analizzato l'AST per creare i nodi.
            una volta che tutti i nodi sono stati creati, vengono posizionati nella scena event quindi vengono creati i collegamenti.
        ENG:
            This method creates a biggusNode from the code passed as a parameter thanks to the Ast library.
            Ast is a library that allows you to analyze the python code and create an AST (Abstract Syntax Tree)
            that is, an abstract syntax tree. This tree is then analyzed to create the nodes.
            With parseCode () the AST is created and with nodeSearch () the AST is analyzed to create the nodes.
            once all the nodes have been created, they are positioned in the scene and then the connections are created.
        :param _code:
        :return:
        """
        self.code = _code
        parsedCode = self.parseCode(_code)
        try:
            self.nodeSearch(parsedCode)
            self.setNodePosition()
            self.createConnections()
            self.searchUnpositionNodes()
        except Exception as e:
            print("debug from createNodeFromCode: ", e)
            return

    @staticmethod
    def parseCode(_code: str):
        # parse the code into an AST
        try:
            return ast.parse(_code)
        except Exception as e:
            print("WARNING: parseCode() failed")
            print("debug from parseCode: ", e)

    def removeCodeAndRestart(self, node):
        code = ast.get_source_segment(self.code, node).strip()
        self.code = self.code.replace(code, "")
        self.createNodeFromCode(self.code)

    def printActualCode(self, node):
        try:
            print(f"actual code: {ast.get_source_segment(self.code, node).strip()}")
        except Exception as e:
            a = e

    def nodeSearch(self, parsedCode: ast.AST):
        function_nodes = []
        for node in ast.walk(parsedCode):
            if isinstance(node, ast.FunctionDef):
                fn = self.createFunctionNode(node)
                function_nodes.append(fn)
                self.removeCodeAndRestart(node)
                break
            elif isinstance(node, ast.For):
                self.createForNode(node)
            elif isinstance(node, ast.If):
                self.createIfNode(node)
            elif isinstance(node, ast.Call):
                try:
                    if isinstance(node.func, ast.Name):
                        print(
                            f"debug: {node.func.id} {node.func.__class__.__name__} {node.func.__dict__} {node.func.__class__.__dict__}")
                        self.createCallNode(node)
                    elif isinstance(node.func, ast.Attribute):
                        self.createCallNode(node)
                except Exception as e:
                    print("*" * 20)
                    print(e)
                    print("*" * 20)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        print(f"target: {target.id} = {node.value} {node.value.__class__.__name__}")
                        variable = self.createVariableNode(target.id, node.value)
                        print(f"variable: {variable} {variable.__class__.__name__}")
            """else:
                name = node.__class__.__name__
                value = node.__dict__
                self.returnUnknownNode(name, value)"""

    def setNodePosition(self):
        pass

    def createConnections(self):
        pass

    def createVariableNode(self, name: str, value):
        """
        ITA:
            Crea un nodo per la variabile in base al tipo di valore assegnato
        ENG:
            Create a biggusNode for the variable based on the type of biggusNode assigned
        :param name:
        :param value:
        :return:
        """
        print(f"\ncreateVariableNode: {name} = {value}")
        node = None

        # ast.Num sono i numeri
        if isinstance(value, ast.Num):
            node = self.returnBiggusPyNode("NumberNode", value.n, name)
        elif isinstance(value, ast.Str):
            node = self.returnBiggusPyNode("StringNode", value.s, name)
        elif isinstance(value, ast.List):
            node = self.returnBiggusPyNodeWithElements("ListNode", value, name)
        elif isinstance(value, ast.Tuple):
            node = self.returnBiggusPyNodeWithElements("TupleNode", value, name)
        elif isinstance(value, ast.Dict):
            node = self.returnBiggusPyNodeDictionary("DictionaryNode", value, name)
        elif isinstance(value, ast.Name):
            node = self.returnBiggusPyNode("VariableNode", value.id, name)
        elif isinstance(value, ast.Attribute):
            print(f"Found attribute {value} but AttributeNode is not implemented yet")
        elif isinstance(value, ast.Call):
            if value.func.id == name:
                node = self.createCallNode(value)
            else:
                node = self.returnBiggusPyNode("VariableNode", value.func.id, name)
                self.variableForCallNode.append(node)
        elif isinstance(value, ast.BinOp):
            node = self.createBinOpNode(value, name)
        else:
            print(f"Non ho trovato il tipo {type(value)}")
        return node

    def searchForOtherTypes(self, value, name):
        # sourcery skip: guard, merge-duplicate-blocks, remove-empty-nested-block, remove-pass-elif, remove-redundant-if
        # ast.UnaryOp sono le operazioni unarie tipo -1
        if isinstance(value, ast.UnaryOp):
            pass
        # ast.BoolOp sono le operazioni booleane tipo 1 == 1 and 2 == 2
        elif isinstance(value, ast.BoolOp):
            pass
        # ast.Compare sono le operazioni di confronto tipo 1 == 1
        elif isinstance(value, ast.Compare):
            pass
        # ast.Subscript sono gli indici tipo lista[0] o dizionario["chiave"]
        elif isinstance(value, ast.Subscript):
            pass
        # ast.Index sono gli indici tipo lista[0] o dizionario["chiave"] event sono usati per creare i nodi
        elif isinstance(value, ast.Index):
            pass
        # ast.Slice sono gli slice tipo lista[0:1] o lista[0:1:2]
        elif isinstance(value, ast.Slice):
            pass

    def returnBiggusPyNode(self, className: str, value, name):
        if value is None:
            node = self.canvas.createNode(className, "")
        else:
            node = self.canvas.createNode(className, value)
            node.changeInputValue(0, value, True)
        if node:
            return self.createNodeOnCanvas(node, name)
        print("WARNING: Node not created")
        return None

    def returnUnknownNode(self, name, value):
        path = "/home/tedk/Desktop/python/pyqt5test/BiggusMain/elements/Nodes/AbstractClass/"
        node = self.canvas.createNodeFromAbsolutePath(path, "UnknownNode")
        self.createNodeOnCanvas(node, name)
        node.changeInputValue(0, value, True)
        return node

    def returnBiggusPyNodeWithElements(self, className: str, value, name):
        """
        ITA:
            nel caso in cui il nodo debba avere degli elementi, come una lista o un dizionario,
            questo metodo viene usato.
        :param className:
        :param value:
        :param name:
        :return:
        """
        elements = [el.value for el in value.elts]
        # elements = [el.n if isinstance(el, ast.Num) else el.biggusNode for el in biggusNode.elts]
        node = self.canvas.createNode(className, elements)
        if node:
            return self.createNodeOnCanvas(node, name)
        else:
            print("WARNING: Node not created")
            return None

    def createNodeOnCanvas(self, node, name):
        node.setName(name)
        self.canvas.addNode(node)
        self.allNodes.append(node)
        if self.lastNode is not None:
            self.updateNodePositionByLastNode(node)
        self.lastNode = node
        return node

    def returnBiggusPyNodeDictionary(self, className: str, value, name):
        """
        ITA:
            nel caso di un dizionario una volta trovati key event biggusNode, poiche sono due liste,
            vengono convertiti in un dizionario.
        ENG:
            in the case of a dictionary once keys and values are found, because they are two lists,
            they are converted into a dictionary.
        :param className:
        :param value:
        :param name:
        :return:
        """
        keys = [el.s for el in value.keys]
        values = [el.n if isinstance(el, ast.Num) else (el.s if isinstance(el, ast.Str) else el.id) for el in
                  value.values]
        dictionary = dict(zip(keys, values))
        node = self.canvas.createNode(className, dictionary)
        if node is not None:
            node.setName(name)
            self.canvas.addNode(node)
            if self.lastNode is not None:
                self.updateNodePositionByLastNode(node)
            self.lastNode = node
            return node
        else:
            print("WARNING: Node not created")
            return None

    def returnCallNode(self, value):
        print(f"Found call {value} but CallNode is not implemented yet")

    # ---------------    BINOP NODE    ----------------

    def createBinOpNode(self, node, name):
        from BiggusMain.biggusWidgets.CodeToNodeWidget.nodifyBinOp import NodifyBinOp
        nodifyBinOp = NodifyBinOp(node, name, self.canvas, self)
        return nodifyBinOp.createBinOpNode(node, name)

    def setOpNodePosition(self, arg1, arg2, opNode, assignmentVariable):
        """
        ITA:
            opNode dovrà essere posizionato in base alle variabili che ha,
            se a = 10 event b = 10 a event b vengono posizionati al momento della creazione
            opNode sarà posizionato come:
                x = max(a.getPos().x(), b.getPos().x())* 1.2
                y = (a.getPos().y(), b.getPos().y()) // 2
        ENG:
            opNode must be positioned based on the variables it has,
            if a = 10 and b = 10 a and b are positioned at the time of creation
            opNode will be positioned as:
                x = max(a.getPos().x(), b.getPos().x())* 1.2
                y = (a.getPos().y(), b.getPos().y()) // 2
        :param assignmentVariable: Ex: a = 10 b = 10 c = a + b assignmentVariable = c
        :param opNode: Ex a = 10 b = 10 c = a + b opNode = mathNode
        :param arg2: variableNode 2 Ex: a = 10 b = 10 c = a + b arg2 = b
        :param arg1: variableNode 1 Ex: a = 10 b = 10 c = a + b initialLocation = a
        :return:
        """
        x0 = arg1.getPos().x()
        x1 = max(arg1.getWidth(), arg2.getWidth()) * 1.2
        x = (x0 + x1) * 2
        y0 = arg1.getPos().y()
        y1 = arg2.getPos().y()
        y = (y0 + y1) // 2
        self.updateNodePosition(opNode, x, y)
        # position the assignment variable on the side of opNode
        x = opNode.getPos().x() + opNode.getWidth() * 2
        y = opNode.getPos().y()
        self.updateNodePosition(assignmentVariable, x, y)

    # ------------------ IF NODE ------------------

    @staticmethod
    def returnIfOperator(left=None, right=None, operator=None, value=None):
        if isinstance(value, ast.Compare):
            if left is None:
                left = value.left
            if right is None:
                right = value.comparators[0]
            if operator is None:
                operator = value.ops[0]

            if isinstance(operator, ast.Eq):
                return "=="
            elif isinstance(operator, ast.NotEq):
                return "!="
            elif isinstance(operator, ast.Gt):
                return ">"
            elif isinstance(operator, ast.Lt):
                return "<"
            elif isinstance(operator, ast.GtE):
                return ">="
            elif isinstance(operator, ast.LtE):
                return "<="
            elif isinstance(operator, ast.In):
                return "inRange"
        return None

    def createIfNode(self, node):
        code = ast.get_source_segment(self.code, node).strip()
        print(f"\ncreate IfNode with code:\n {code}\n")
        operator = self.returnIfOperator(left=node.test.left, right=node.test.comparators[0], value=node.test)
        ifNode = self.returnBiggusPyNode("IfNode", True, "IfNode")
        ifNode.setOperator(operator)
        # scrivendo print(ast.dump(biggusNode)) ottengo: If(test=Compare(left=Name(id='b', ctx=Load()), ops=[Gt()],
        # comparators=[Name(id='a', ctx=Load())]), body=[Expr( biggusNode=Call(func=Name(id='print', ctx=Load()),
        # args=[Constant(biggusNode='b is greater than a')], keywords=[]))], orelse=[])
        leftNode = node.test.left
        arg1 = self.canvas.getNodeByName(leftNode.id)
        # arg2 è un nodo oppure una costante
        if isinstance(node.test.comparators[0], ast.Name):
            arg2 = self.canvas.getNodeByName(node.test.comparators[0].id)
        elif isinstance(node.test.comparators[0], ast.Constant):
            arg2 = self.returnBiggusPyNode("NumberNode", True, "ConstantValue")
            arg2.setInputValue(node.test.comparators[0].value, 0)
        else:
            arg2 = None
        if arg1 is not None:
            self.setIfNodePosition(arg1, arg2, ifNode)
            self.createConnection(arg1, ifNode)
        if arg2 is not None:
            self.createConnection(arg2, ifNode)

        self.createIfBodyNode(node, ifNode)

    def createIfBodyNode(self, node, ifNode):
        body = node.body
        # ora devo creare i nodi per il corpo dell'if, per farlo devo creare un nodo per ogni istruzione

        for statement in body:
            if isinstance(statement, ast.Expr):
                if isinstance(statement.value, ast.Call):
                    if statement.value.func.id == "print":
                        # if find a print statement, create a printNode
                        args = statement.value.args
                        if len(args) > 0 and isinstance(args[0], ast.Constant):
                            printNode = self.returnBiggusPyNode("PrintNode", True, "PrintNode")
                            text = args[0].value
                            if text is not None:
                                stringNode = self.returnBiggusPyNode("StringNode", text, "StringNode")
                                self.setIfBodyNodePosition(stringNode)
                                self.setIfOutNodePosition(printNode)
                                self.createConnection(stringNode, ifNode)
                            else:
                                self.setIfBodyNodePosition(printNode)
                            self.createConnection(ifNode, printNode)

    def setIfNodePosition(self, arg1, arg2, ifNode):
        """
        ITA:
            Funziona in modo simile all'opNodePosition, ma setta la posizione di ifNode
            in self.lastIfNode in modo da posizionare i nodi del body dell'if
        ENG:
            Works in a similar way to opNodePosition, but sets the position of ifNode
            in self.lastIfNode in order to position the nodes of the if body
        :param arg1:
        :param arg2:
        :param ifNode:
        :return:
        """
        x0 = arg1.getPos().x()
        if arg2 is not None:
            x1 = max(arg1.getWidth(), arg2.getWidth()) * 1.2
        else:
            x1 = arg1.getWidth() * 1.2
        x = (x0 + x1) * 2
        y0 = arg1.getPos().y()
        y1 = arg2.getPos().y() if arg2 is not None else y0
        y = (y0 + y1) // 2
        self.updateNodePosition(ifNode, x, y)
        self.lastIfNode = ifNode

    def setIfBodyNodePosition(self, *args):
        lastNode = self.lastIfNode
        x = lastNode.getPos().x() + lastNode.getWidth() * 2
        y = lastNode.getPos().y() - lastNode.getHeight() * 1.2
        for node in args:
            self.updateNodePosition(node, x, y)
            x += node.getWidth() * 2
            y += lastNode.getPos().y() - node.getHeight()
            lastNode = node

    def setIfOutNodePosition(self, node):
        lastNode = self.lastIfNode
        x = lastNode.getPos().x() + lastNode.getWidth() * 2
        y = lastNode.getPos().y() + lastNode.getHeight() * 1.2
        self.updateNodePosition(node, x, y)

    # ------------------ WHILE NODE ------------------

    def createWhileNode(self, node):
        code = ast.get_source_segment(self.code, node).strip()
        print(f"\ncreate WhileNode with code:\n {code}\n")
        whileNode = self.returnBiggusPyNode("WhileNode", True, "WhileNode")
        self.createWhileBodyNode(node, whileNode)
        self.createWhileConditionNode(node, whileNode)

    def createWhileConditionNode(self, node, whileNode):
        condition = node.test
        if isinstance(condition, ast.Compare):
            operator = self.returnIfOperator(left=condition.left, right=condition.comparators[0], value=condition)
            whileNode.setOperator(operator)
            leftNode = condition.left
            arg1 = self.canvas.getNodeByName(leftNode.id)
            arg2 = self.canvas.getNodeByName(condition.comparators[0].id)
            if arg1 is not None and arg2 is not None:
                self.setWhileNodePosition(arg1, arg2, whileNode)
                self.createConnection(arg1, whileNode)
                self.createConnection(arg2, whileNode)

    def createWhileBodyNode(self, node, whileNode):
        body = node.body
        for statement in body:
            if isinstance(statement, ast.Expr):
                if isinstance(statement.value, ast.Call):
                    if statement.value.func.id == "print":
                        args = statement.value.args
                        if len(args) > 0 and isinstance(args[0], ast.Constant):
                            printNode = self.returnBiggusPyNode("PrintNode", True, "PrintNode")
                            text = args[0].value
                            if text is not None:
                                stringNode = self.returnBiggusPyNode("StringNode", text, "StringNode")
                                self.setWhileBodyNodePosition(stringNode)
                                self.setWhileOutNodePosition(printNode)
                                self.createConnection(stringNode, whileNode)
                            else:
                                self.setWhileBodyNodePosition(printNode)
                            self.createConnection(whileNode, printNode)

    def setWhileNodePosition(self, arg1, arg2, whileNode):
        x0 = arg1.getPos().x()
        x1 = max(arg1.getWidth(), arg2.getWidth()) * 1.2
        x = (x0 + x1) * 2
        y0 = arg1.getPos().y()
        y1 = arg2.getPos().y()
        y = (y0 + y1) // 2
        self.updateNodePosition(whileNode, x, y)
        self.lastWhileNode = whileNode

    def setWhileBodyNodePosition(self, *args):
        lastNode = self.lastWhileNode
        x = lastNode.getPos().x() + lastNode.getWidth() * 2
        y = lastNode.getPos().y() - lastNode.getHeight() * 1.2
        for node in args:
            self.updateNodePosition(node, x, y)
            x += node.getWidth() * 2
            y += lastNode.getPos().y() - node.getHeight()
            lastNode = node

    def setWhileOutNodePosition(self, node):
        lastNode = self.lastWhileNode
        x = lastNode.getPos().x() + lastNode.getWidth() * 2
        y = lastNode.getPos().y() + lastNode.getHeight() * 1.2
        self.updateNodePosition(node, x, y)

    # ------------------ FOR NODE ------------------

    def createForNode(self, node):
        code = ast.get_source_segment(self.code, node).strip()
        forNode = self.returnBiggusPyNode("ForNode", [], "ForNode")
        self.createForConditionNode(node, forNode)
        self.createForBody(code, forNode)

    def createForConditionNode(self, node, forNode):
        # condition è un ast.Call ad esempio range(10)
        condition = node.iter
        if isinstance(condition, ast.Name):
            self.checkIterables(condition, forNode)
        if isinstance(condition, ast.Call):
            if condition.func.id == "range":
                self.createRangeNode(condition, forNode)
            elif condition.func.id == "in":
                self.createInNode(condition, forNode)

    def createForBody(self, code, forNode):
        forBody = self.returnBiggusPyNode("StringNode", code, "ForBodyNode")
        self.setForBodyNodePosition(forBody, forNode)
        self.createConnection(forBody, forNode)

    def checkIterables(self, condition, forNode):
        iterable = self.canvas.getNodeByName(condition.id)
        if iterable is not None:
            self.setForNodePosition(iterable, forNode)
            self.createConnection(iterable, forNode)
        else:
            print(f"Debug: iterable {condition.id} is not in canvas")

    def createRangeNode(self, condition, forNode):
        if len(condition.args) == 1:
            if isinstance(condition.args[0], ast.Constant):
                arg1 = self.returnBiggusPyNode("RangeNode", condition.args[0].value, "RangeNode")
                self.createConnection(arg1, forNode)
                return arg1
        elif len(condition.args) == 2:
            if isinstance(condition.args[0], ast.Constant) and isinstance(condition.args[1], ast.Constant):
                arg1 = self.returnBiggusPyNode("RangeNode", condition.args[0].value, "RangeNode")
                arg2 = arg1.setInputValue(1, condition.args[1].value, True)
                self.setForNodePosition(arg1, forNode)
                self.createConnection(arg1, forNode)
                return arg1

    def createInNode(self, condition, forNode):
        if len(condition.args) == 2:
            if isinstance(condition.args[0], ast.Name) and isinstance(condition.args[1], ast.Name):
                arg1 = self.returnBiggusPyNode("InNode", condition.args[0].id, "InNode")
                arg2 = arg1.setInputValue(1, condition.args[1].id, True)
                self.setForNodePosition(arg1, forNode)
                self.createConnection(arg1, forNode)
                return arg1

    def setForNodePosition(self, rangeNode, forNode):
        # il for biggusNode sta alla destra del range biggusNode
        x = self.lastNode.getPos().x() + self.lastNode.getWidth() * 2
        y = self.lastNode.getPos().y()
        rangeNode.setPos(QPointF(x, y))
        self.lastNode = rangeNode
        x = rangeNode.getPos().x() + rangeNode.getWidth() * 3
        y = rangeNode.getPos().y() + (self.lastNode.getHeight())
        forNode.setPos(QPointF(x, y))

    def setForBodyNodePosition(self, bodyNode, forNode):
        # posiziona il body biggusNode alla sinistra del for biggusNode event sotto
        x = forNode.getPos().x() - (forNode.getWidth() + bodyNode.getWidth() * 1.2)
        y = forNode.getPos().y() + (forNode.getHeight() * 1.2)
        self.updateNodePosition(bodyNode, x, y)

    def setForOutNodePosition(self, node):
        lastNode = self.lastForNode
        x = lastNode.getPos().x() + lastNode.getWidth() * 2
        y = lastNode.getPos().y() + lastNode.getHeight() * 1.2
        self.updateNodePosition(node, x, y)

    # ------------------ FUNCTION NODE ------------------

    def createFunctionNode(self, node):
        code = ast.get_source_segment(self.code, node).strip()
        print(f"\ncreate FunctionNode with code:\n {code}\n")
        # deve saltare l'intestazione def...
        functionNode = self.returnBiggusPyNode("FunctionNode", code, "FunctionNode")
        self.functionNodeList.append(functionNode)
        functionNode.setName(node.name)
        self.lastFunctionNode = functionNode
        return functionNode

    def copyFunction(self, function):
        print(function.getName())
        code = function.functionString
        inNum = len(function.inPlugs)
        outNum = len(function.outPlugs)
        functionNode = self.canvas.createNode("FunctionNode", code, inNum, outNum)
        functionNode.setName(function.getName())
        self.canvas.addNode(functionNode)
        return functionNode

    # ------------------ CALL NODE ------------------

    def createCallNode(self, node):
        try:
            code = ast.get_source_segment(self.code, node).strip()
            print(f"\ncreateCallNode: {node.func.id} with code:\n {code}\n")
        except Exception as e:
            a = e
        # cerca se il nodo è già stato creato
        callNode = self.canvas.getNodeByName(node.func.id)

        if callNode is None:
            print("callNode is None")
            callNode = self.returnBiggusPyNode("FunctionNode", node, node.func.id)
            self.canvas.addNode(callNode)
        else:
            print(f"callNode {node.func.id} already exists")
            if callNode.outConnections:
                print(f"callNode {node.func.id} is connected")
                callNode = self.copyFunction(callNode)

        # trovato il nodo, ora devo creare i nodi per gli argomenti
        self.searchForCallNodeArgs(node, callNode)
        return callNode

    def searchForCallNodeArgs(self, node, callNode):
        args = node.args
        constantArgs = []
        for arg in args:
            # se l'argomento è una variabile, devo cercare il nodo corrispondente
            if isinstance(arg, ast.Name):
                argNode = self.canvas.getNodeByName(arg.id)
                if argNode is not None:
                    self.createConnection(argNode, callNode)
                    self.callNodePosition(argNode, callNode)
                else:
                    print(f"argNode {arg.id} is None")
            # se l'argomento è una costante, generalmente è l'argomento della funzione stessa
            elif isinstance(arg, ast.Constant):
                if isinstance(arg.value, str):
                    argNode = self.returnBiggusPyNode("StringNode", arg.value, "StringNode")
                elif isinstance(arg.value, (int, float)):
                    argNode = self.returnBiggusPyNode("NumberNode", arg.value, "NumberNode")
                else:
                    argNode = self.returnBiggusPyNode("VariableNode", arg.value, "VariableNode")
                constantArgs.append(argNode)
                self.createConnection(argNode, callNode)
            elif isinstance(arg, ast.Assign):
                print("arg is Assign")
        if constantArgs:
            self.setConstantArgsPosition(constantArgs, callNode)

    def callNodePosition(self, argNode, callNode):
        x = (argNode.getPos().x() + argNode.getWidth()) * 2
        y = argNode.getPos().y()
        self.updateNodePosition(callNode, x, y)

    def setConstantArgsPosition(self, constantArgs, callNode):
        x = (constantArgs[0].getPos().x() + constantArgs[0].getWidth()) * 2 * (len(constantArgs) - 1)
        y = (constantArgs[0].getPos().y() + constantArgs[-1].getPos().y()) // 2
        callNode.setPos(QPointF(x, y))
        if len(self.variableForCallNode) > self.callingIndex:
            x = callNode.getWidth() * 2
            y = callNode.getPos().y() + (callNode.getHeight() // 3)
            self.variableForCallNode[self.callingIndex].setPos(QPointF(x, y))
            self.createConnection(callNode, self.variableForCallNode[self.callingIndex])
            self.callingIndex += 1

    def checkPositionForFunctionNext(self, left, right, opNode, assignmentVariable):
        x = (left.getPos().x() + right.getPos().x()) * 40
        y = (left.getPos().y() + right.getPos().y()) // 2
        opNode.setPos(QPointF(x, y))
        self.createConnection(left, opNode)
        self.createConnection(right, opNode)
        x = opNode.getPos().x() + opNode.getWidth() * 2
        y = opNode.getPos().y()
        assignmentVariable.setPos(QPointF(x, y))
        self.createConnection(opNode, assignmentVariable)

    # ------------------ NODE POSITIONING ------------------

    def updateNodePosition(self, node, x, y):
        """
        ITA:
            Aggiorna la posizione del nodo nella scena. Quindi va a cercare il nodo
            nel canvas event aggiorna la sua posizione.
        ENG:
            Update the position of the biggusNode in the scene. Then it looks for the biggusNode
            in the canvas and updates its position.
        :param x:
        :param y:
        :param node:
        :return:
        """
        if node is not None:
            self.canvas.updateNodePosition(node, x, y)

    def updateNodePositionByLastNode(self, node):
        """
        ITA:
            Aggiorna la posizione del nodo nella scena rispetto a lastNode. Quando viene
            chiamata questa funzione di solito i nodi vengono posizionati sotto a lastNode.
        ENG:
            Update the position of the biggusNode in the scene with respect to lastNode. When this
            function is called, the nodes are usually positioned under lastNode.
        :param node:
        :return:
        """
        x = self.lastNode.getPos().x()
        y = self.lastNode.getPos().y() + self.lastNode.getHeight() * 2
        self.updateNodePosition(node, x, y)

    def searchUnpositionNodes(self):
        # se un nodo ha una in connection posiziona il nodo a destra
        for connection in self.canvas.connections:
            outNode = connection.outputNode
            inNode = connection.inputNode
            if inNode.nodeInterface.getPos().x() < outNode.nodeInterface.getPos().x():
                x = outNode.nodeInterface.getPos().x() + outNode.nodeInterface.getWidth() * 2
                y = outNode.nodeInterface.getPos().y() + outNode.nodeInterface.getHeight() // 2
                if len(inNode.inPlugs) > 1:
                    # cerca se il nodo ha altre connessioni in entrata
                    for conn in self.canvas.connections:
                        if conn.inputNode == inNode:
                            y += inNode.nodeInterface.getHeight() * 1.5
                self.updateNodePosition(inNode.nodeInterface, x, y)

    # ------------------ NODE CONNECTION ------------------

    def createConnection(self, node1, node2):
        plugIndex = 0
        for plug in node2.inPlugs:
            if plug.inConnection is None:
                break
            plugIndex += 1
        self.canvas.addConnection(node2, plugIndex, node1, 0)
