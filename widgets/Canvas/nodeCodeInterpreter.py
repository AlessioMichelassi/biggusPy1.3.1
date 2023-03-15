import ast


class NodeCodeInterpreter:
    currentNode = None
    Nodes = []
    variables = {}

    def __init__(self, biggusPy, canvas):
        self.canvas = canvas
        self.biggusPy = biggusPy

    def parseCommand(self, command):
        print(f"parsing command: {command}")
        parsedCode = ast.parse(command)
        for node in ast.walk(parsedCode):
            if isinstance(node, ast.Call):
                self.handleCall(node)
            elif isinstance(node, ast.Assign):
                self.handleAssign(node)

    def handleAssign(self, node):
        if node.value.func.attr == "createNode":
            node_name = node.targets[0].id
            node_class = node.value.args[0].s
            node_args = node.value.keywords
            node_instance = self.canvas.createNode(node_class,
                                                   **{arg.arg: self.getValue(arg.value) for arg in node_args})
            node_instance.setName(node_name)
            self.variables[node_name] = node_instance
            self.sendToTerminal(f"\n{node_name} = {node_instance.getTitle()}\n")
            return
        self.sendToTerminal("ERROR:", "Invalid command")

    def handleCall(self, node):
        if isinstance(node.func.value, ast.Attribute) and node.func.value.attr == "canvas":
            if node.func.attr == "createNode":
                args = [self.evalNode(arg) for arg in node.args]
                kwargs = {arg.arg: self.evalNode(arg.value) for arg in node.keywords}
                biggusNode = self.canvas.createNode(*args, **kwargs)
                if biggusNode is None:
                    self.sendToTerminal("WARNING:", "Node not found")
                    return
                self.currentNode = biggusNode
            elif node.func.attr == "addNode":
                args = [self.evalNode(arg) for arg in node.args]
                self.canvas.addNode(args[0])
                self.sendToTerminal(f"\n{args[0].getName()} = {args[0].getTitle()}\n")
            elif node.func.attr == "setPos":
                args = [self.evalNode(arg) for arg in node.args]
                biggusNode = self.canvas.getNodeByName(args[0])
                biggusNode.setPosXY(args[1], args[2])
            elif node.func.attr == "addConnection":
                args = [self.evalNode(arg) for arg in node.args]
                self.canvas.addConnection(*args)
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                obj = self.variables.get(node.func.value.id)
                if obj is not None:
                    attr = node.func.attr
                    args = [self.evalNode(arg) for arg in node.args]
                    if hasattr(obj, attr):
                        method = getattr(obj, attr)
                        method(*args)
                    else:
                        self.sendToTerminal("WARNING:", f"Attribute {attr} not found in object {obj}")
                else:
                    self.sendToTerminal("WARNING:", f"Object {node.func.value.id} not found")
        elif isinstance(node.func, ast.Name):
            self.handleName(node.func)

    def evalNode(self, node):
        if isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Name):
            if node.id in self.variables:
                return self.variables[node.id]
        elif isinstance(node, ast.BinOp):
            left = self.evalNode(node.left)
            right = self.evalNode(node.right)
            op = node.op
            if isinstance(op, ast.Add):
                return left + right
            elif isinstance(op, ast.Sub):
                return left - right
            elif isinstance(op, ast.Mult):
                return left * right
            elif isinstance(op, ast.Div):
                return left / right
        elif isinstance(node, ast.Call):
            args = [self.evalNode(arg) for arg in node.args]
            kwargs = {arg.arg: self.evalNode(arg.value) for arg in node.keywords}
            return getattr(self, node.func.id)(*args, **kwargs)

    def handleName(self, node):
        if node.id == "setPos":
            self.currentNode.setPos(*[self.evalNode(arg) for arg in node.args])
        elif node.id == "setName":
            self.currentNode.setName(self.evalNode(node.args[0]))
        elif node.id == "changeInputValue":
            self.currentNode.changeInputValue(*[self.evalNode(arg) for arg in node.args])
        elif node.id == "connect":
            args = [self.evalNode(arg) for arg in node.args]
            self.canvas.setConnections(*args)

    def sendToTerminal(self, *args):
        returnString = f"{' '.join(args)}"
        self.biggusPy.sendToTerminal(returnString)

    def getValue(self, value):
        if isinstance(value, ast.Str):
            return value.s
        elif isinstance(value, ast.Num):
            return value.n
        elif isinstance(value, ast.Name):
            return self.variables[value.id]
        elif isinstance(value, ast.List):
            return [self.getValue(v) for v in value.elts]
        elif isinstance(value, ast.Tuple):
            return tuple(self.getValue(v) for v in value.elts)
        elif isinstance(value, ast.Dict):
            return {self.getValue(k): self.getValue(v) for k, v in zip(value.keys, value.values)}
        elif isinstance(value, ast.Call):
            return self.handleCall(value)
        else:
            return None

    def getVar(self, var):
        return self.variables[var]
