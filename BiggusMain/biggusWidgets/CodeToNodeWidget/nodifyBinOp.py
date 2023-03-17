"""
   ITA:
       Per BinOp si intende un nodo che ha un operatore binario, come ad esempio
       l'addizione, la sottrazione, la moltiplicazione, la divisione, ecc...
       In questo caso se la variabile assegnata è fra due Numeri, allora viene
       creato un nodo di tipo MathNode, se fra due stringhe viene creato un
       nodo di tipo StringNode, se fra due liste viene creato un nodo di tipo
       ListNode, se fra due tuple viene creato un nodo di tipo TupleNode, se
       fra due set viene creato un nodo di tipo SetNode, se fra due dizionari
       viene creato un nodo di tipo DictNode, se fra due variabili viene creato
       un nodo di tipo VariableNode.
   ENG:
       For BinOp it means a biggusNode that has a binary operator, such as
       addition, subtraction, multiplication, division, etc ...
       In this case if the assigned variable is between two Numbers, then it is
       created a MathNode type biggusNode, if between two strings a StringNode type biggusNode is created,
       if between two lists a ListNode type biggusNode is created, if between two tuples a TupleNode
       type biggusNode is created, if between two sets a SetNode type biggusNode is created, if between two
       dictionaries a DictNode type biggusNode is created, if between two variables a VariableNode
       type biggusNode is created.
   """
import ast


class NodifyBinOp:
    def __init__(self, node, name, canvas, parent):
        self.node = node
        self.name = name
        self.parent = parent
        self.canvas = canvas
        self.code = parent.code

    @staticmethod
    def returnOperator(value):
        """
        ITA:
            Questo metodo ritorna l'operatore binario.
        ENG:
            This method returns the binary operator.
        :param value:
        :return:
        """
        if isinstance(value, ast.Add):
            return "+"
        elif isinstance(value, ast.Sub):
            return "-"
        elif isinstance(value, ast.Mult):
            return "*"
        elif isinstance(value, ast.Div):
            return "/"
        elif isinstance(value, ast.FloorDiv):
            return "//"
        elif isinstance(value, ast.Mod):
            return "%"
        elif isinstance(value, ast.Pow):
            return "**"
        elif isinstance(value, ast.LShift):
            return "<<"
        elif isinstance(value, ast.RShift):
            return ">>"
        elif isinstance(value, ast.BitOr):
            return "|"
        elif isinstance(value, ast.BitXor):
            return "^"
        elif isinstance(value, ast.BitAnd):
            return "&"
        elif isinstance(value, ast.MatMult):
            return "@"
        else:
            return None

    def createBinOpNode(self, node, name):
        """
        ITA:
            Questo metodo viene chiamato quando viene trovato un nodo di tipo BinOp,
            ovvero una somma o una sottrazione o una moltiplicazione o una divisione.
            Generalmente quando si passa un codice è nella forma a = 10 b = 20 c = a + b
            quindi nel caso in cui a e b sono già state create, viene controllato il tipo
            di variabile. se a = "Hello" e b = "World" in python il risultato è "HelloWorld"
            ma in biggus py per farlo serve un nodo di tipo StringNode, quindi viene creato
            un nodo di tipo StringNode.
        ENG:
            This method is called when a BinOp type biggusNode is found.
            Depending on the type of variable that is assigned, a different type biggusNode is created.
            For example if a = "Hello" and b = "World" in python the result is "HelloWorld"
            but in biggus py to do it a StringNode type biggusNode is needed, so a StringNode type biggusNode is created.
        :param node:
        :param name:
        :return:
        """
        code = ast.get_source_segment(self.code, node).strip()
        print(f"\ncreate BinNode with code:\n {code}\n")
        assignmentVariable = self.parent.returnBiggusPyNode("VariableNode", node, name)
        operator = self.returnOperator(node.op)
        if assignmentVariable is None:
            print("WARNING: assignmentVariable is None")
            return None
        if operator is None:
            print("WARNING: operator is None")
            return None
        opNode = None
        left = node.left
        if left is not None:
            leftVariable = self.canvas.getNodeByName(left.id)
            right = node.right
            if leftVariable is None:
                opNode = self.searchWhichNodeToCreate(left, right, operator, node, name)
                print(f"opNode: {str(opNode)}")
                self.checkIfLeftAndRightVariablesExist(left, right, opNode, assignmentVariable, name)
                return opNode
            else:
                rightVariable = self.canvas.getNodeByName(right.id)
                if rightVariable is not None:
                    opNode = self.parent.returnBiggusPyNode("MathNode", node, name)
                    self.parent.checkPositionForFunctionNext(leftVariable, rightVariable, opNode, assignmentVariable)
                    return opNode

    def returnType(self, value):
        """
        ITA:
            Questo metodo ritorna il tipo di variabile.
        ENG:
            This method returns the type of variable.
        :param value:
        :return:
        """
        if isinstance(value, ast.Num):
            return "Number"
        elif isinstance(value, ast.Str):
            return "String"
        elif isinstance(value, ast.List):
            return "List"
        elif isinstance(value, ast.Tuple):
            return "Tuple"
        elif isinstance(value, ast.Set):
            return "Set"
        elif isinstance(value, ast.Dict):
            return "Dict"
        elif isinstance(value, ast.Name):
            return "Variable"
        else:
            return None

    def searchWhichNodeToCreate(self, left, right, operator, value, name):
        leftType = self.returnType(left)
        rightType = self.returnType(right)
        print(f"leftType: {leftType}")
        # Crea l'op biggusNode dopo aver controllato se left e right esistono
        # se esistono e il className di left è NumberNode crea il mathNode
        # altrimenti crea una string etc etc... altrimenti crea un variableNode
        # e ritorna un opNode che adesso andrà creato nella lista dei nodi!
        arg1 = self.canvas.getNodeByName(left.id)
        opNode = None
        if arg1 is not None:
            if arg1.className == "NumberNode":
                opNode = self.parent.returnBiggusPyNode("MathNode", value, name)
                opNode.operator = operator
            elif arg1.className == "StringNode":
                opNode = self.parent.returnBiggusPyNode("StringNode", value, name)
                opNode.operator = operator
            elif arg1.className == "ListNode":
                opNode = self.parent.returnBiggusPyNode("ListNode", value, name)
                opNode.operator = operator
            elif arg1.className == "TupleNode":
                opNode = self.parent.returnBiggusPyNode("TupleNode", value, name)
                opNode.operator = operator
            elif arg1.className == "SetNode":
                opNode = self.parent.returnBiggusPyNode("SetNode", value, name)
                opNode.operator = operator
            elif arg1.className == "DictNode":
                opNode = self.parent.returnBiggusPyNode("DictNode", value, name)
                opNode.operator = operator
            elif arg1.className == "VariableNode":
                opNode = self.parent.returnBiggusPyNode("VariableNode", value, name)
                opNode.operator = operator
            else:
                print("WARNING: leftType not found")
                opNode = None
            return opNode
        return opNode

    def checkIfLeftAndRightVariablesExist(self, left, right, opNode, assignmentVariable, name):
        arg1 = self.canvas.getNodeByName(left.id)
        arg2 = self.canvas.getNodeByName(right.id)
        if arg1 is None or arg2 is None:
            print("WARNING: One of the variables does not exist")
            return
        if opNode is None:
            print("OpNode not created")
        elif assignmentVariable is not None:
            self.parent.setOpNodePosition(arg1, arg2, opNode, assignmentVariable)
            self.parent.createConnection(arg1, opNode)
            self.parent.createConnection(arg2, opNode)
            self.parent.createConnection(opNode, assignmentVariable)
        else:
            print("Assignment variable not created")
