@staticmethod
def createNodeOther(path, className: str, *args, **kwargs):
    # sourcery skip: use-named-expression
    """
    ITA:
        Crea un nodo a partire dal nome della classe ad Es: "NumberNode".
        Il metodo importa il modulo event crea un oggetto della classe passata come parametro,
        quindi ritorna l'interfaccia del nodo. In args event kwargs vanno passati i parametri
        come Value, Name, InputNumber, OutputNumber ecc...
    ENG:
        Create a biggusNode from the name of the class, for example "NumberNode".
        The method imports the module and creates an object of the class passed as a parameter,
        then it returns the biggusNode interface. In args and kwargs you have to pass the parameters
        as Value, Name, InputNumber, OutputNumber etc ...
    :param path:
    :param className: class name of the biggusNode
    :param args:  biggusNode, name, inputNumber, outputNumber etc...
    :param kwargs:  biggusNode, name, inputNumber, outputNumber etc...
    :return:
    """
    module = None
    nodeClass = None
    try:
        module = importlib.import_module(f"{path}.{className}")
    except Exception as e:
        print(f"module not found: {className} not found {e}")
    try:
        if module:
            nodeClass = getattr(module, className)
    except Exception as e:
        print(f"Error in nodeClass: {className} {e}")
        return None
    try:
        if nodeClass:
            node = nodeClass(*args, **kwargs)
            value = kwargs.get("biggusNode", node.startValue)
            if value:
                node.startValue = value
            return node
    except Exception as e:
        print(f"Error in createNode: {className} {e}")
        return None


@staticmethod
def createNodeFromDeserialize(className, modulePath, *args, **kwargs):
    """
    ITA:
        Quando si carica un progetto, per deserializzare un nodo si chiama questo metodo.
        Il metodo importa il modulo event crea un oggetto della classe passata come parametro,
        quindi ritorna l'interfaccia del nodo. In args event kwargs vanno passati i parametri
        come Value, Name, InputNumber, OutputNumber ecc...
    ENG:
        When a project is loaded, to deserialize a node this method is called.
        The method imports the module and creates an object of the class passed as a parameter,
        then it returns the biggusNode interface. In args and kwargs you have to pass the parameters
        as Value, Name, InputNumber, OutputNumber etc ...
    :param className:
    :param modulePath:
    :param args:
    :param kwargs:
    :return:
    """
    module = None
    nodeClass = None
    try:
        module = importlib.import_module(f"{modulePath}.{className}")
    except Exception as e:
        try:
            # this is for compatibility with older versions
            module = importlib.import_module(f"BiggusMain.{modulePath}.{className}")
        except Exception as e:
            print(f"module not found: {className} -- {e}")
            return None
    try:
        if module:
            nodeClass = getattr(module, className)
    except Exception as e:
        print(f"Error in nodeClass: {className} -- {e}")
        return None
    try:
        if nodeClass:
            node = nodeClass(*args, **kwargs)
            node.modulePath = modulePath
            return node
    except Exception as e:
        print(f"Error in createNode: {className} {e}")
        return None


def findModuleWinNT(self, path, className):
    if getattr(sys, 'frozen', False):
        # Se siamo in un eseguibile PyInstaller, cambiamo il percorso di ricerca dei moduli
        # per far sì che punti alla cartella temporanea creata da PyInstaller
        nodes_folder = sys._MEIPASS
        print(f"nodes_folder: {nodes_folder} compiled version")
        moduleFolder = os.path.join(nodes_folder, "biggusFolder")
        print(f"folder to copy: {moduleFolder}")
        if not exists(moduleFolder):
            print("folder not exists")
            srcDir = os.path.join(os.getcwd(), "biggusFolder")
            shutil.copytree(srcDir, moduleFolder)
            if not exists(path):
                print("ERROR: moduleFolder not found")
                raise Exception("ERROR: moduleFolder not found")
    nodes_folder = os.path.abspath(path)
    nodes_folder = nodes_folder.replace("/", "\\")
    char = "\\"
    relativePath = os.path.relpath(nodes_folder, os.getcwd())
    modulePath = f"{relativePath.replace(char, '.').replace('C:.', '')}"
    moduleName = f"{modulePath}.{className}"
    try:
        module = importlib.import_module(moduleName)
        print(f"Module {module} found")
        return module, modulePath
    except Exception as e:
        print(f"WARNING FROM createNodeFromAbsolutePath:")
        print(f"module not found:\nclassName:\n\t{className}\npath:\n\t{nodes_folder}\n"
              f"module path\n\t{modulePath}\nmodule name:\n\t{moduleName}\n{e}")
        return None, None


def findModuleLinuxAndMac(self, path, className):
    nodes_folder = os.path.abspath(path)
    relative_path = os.path.relpath(nodes_folder, os.getcwd())
    modulePath = f"{relative_path.replace('/', '.')}"
    moduleName = f"{modulePath}.{className}"
    module = None
    try:
        module = importlib.import_module(moduleName)
        return module, modulePath
    except Exception as e:
        print(f"WARNING FROM createNodeFromAbsolutePath:")
        print(f"module not found:\nclassName:\n\t{className}\npath:\n\t{nodes_folder}\n"
              f"module path\n\t{modulePath}\nmodule name:\n\t{moduleName}\n{e}")
        return None, None


def createNodeFromAbsolutePath(self, path, className: str, *args, **kwargs):
    # sourcery skip: use-named-expression
    """
    ITA:
        Crea un nodo a partire dal nome della classe ad Es: "NumberNode".
        Il metodo importa il modulo event crea un oggetto della classe passata come parametro,
        quindi ritorna l'interfaccia del nodo. In args event kwargs vanno passati i parametri
        come Value, Name, InputNumber, OutputNumber ecc...
    ENG:
        Create a biggusNode from the name of the class, for example "NumberNode".
        The method imports the module and creates an object of the class passed as a parameter,
        then it returns the biggusNode interface. In args and kwargs you have to pass the parameters
        as Value, Name, InputNumber, OutputNumber etc ...
    :param path:
    :param className: class name of the biggusNode
    :param args:  biggusNode, name, inputNumber, outputNumber etc...
    :param kwargs:  biggusNode, name, inputNumber, outputNumber etc...
    :return:
    """
    nodes_folder = os.path.abspath(path)
    # this is for compatibility with windows
    # linux directory: biggusFolder/imgs/icon/biggusIcon
    # windows directory: biggusFolder\imgs\icon\biggusIcon
    # mac directory: biggusFolder/imgs/icon/biggusIcon
    module = None
    modulePath = None
    if os.name == "nt":
        module, modulePath = self.findModuleWinNT(path, className)
    elif os.name == "posix":
        module, modulePath = self.findModuleLinuxAndMac(path, className)
    if module is None:
        print("module is None")
        return None
    nodeClass = None
    try:
        if module:
            nodeClass = getattr(module, className)
    except Exception as e:
        print(f"Error in nodeClass: {className} {e}")
        return None
    try:
        if nodeClass:
            node = nodeClass(*args, **kwargs)
            node.modulePath = modulePath
            value = kwargs.get("biggusNode", node.startValue)
            if value:
                node.startValue = value
            return node
    except Exception as e:
        print(f"Error in createNode: {className} {e}")
        return None