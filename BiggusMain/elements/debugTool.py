class debugTool:

    isOnDebug = False

    def __init__(self, className):
        self.className = className

    def setDebugMode(self, isOnDebug):
        self.isOnDebug = isOnDebug

    def dPrint(self, operation, *args):
        if self.isOnDebug:
            print("*" * 50)
            print(f"Debug from class {self.className}: {operation}")
            print(*args)
