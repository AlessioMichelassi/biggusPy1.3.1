from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication, QCompleter, QPlainTextEdit, QMainWindow
from PyQt5.QtCore import Qt

from scratchNodeV0_9.ArguePy_CodeEditor.editorWidgetTool.tools.codeEditor import pythonCodeEditor

python_keywords = [
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue',
    'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in',
    'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'
]


class PlainTextEditWithCompleter(pythonCodeEditor):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.completer = QCompleter()
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.activated[str].connect(self.insert_completion)

    def keyPressEvent(self, event):
        if self.completer.popup().isVisible():

            if event.key() in (Qt.Key_Enter, Qt.Key_Return):
                self.completer.setCurrentRow(self.completer.currentRow() + 1)
                return
            elif event.key() == Qt.Key_Tab:
                self.insert_completion(self.completer.currentCompletion())
                self.completer.popup().hide()

                return

        super().keyPressEvent(event)

        completion_prefix = self.text_under_cursor()
        if completion_prefix != self.completer.completionPrefix():
            self.update_completer_popup_items(completion_prefix)

        if len(completion_prefix) > 0:
            # Aggiungi questa riga per assicurarti che il popup del completer sia valido
            self.completer.setWidget(self)
            self.completer.complete()
        else:
            self.completer.popup().hide()

    def update_completer_popup_items(self, completion_prefix):
        self.completer.setCompletionPrefix(completion_prefix)
        self.completer.popup().setCurrentIndex(self.completer.completionModel().index(0, 0))

    def text_under_cursor(self):
        text_cursor = self.textCursor()
        text_cursor.select(QTextCursor.WordUnderCursor)
        return text_cursor.selectedText()

    def insert_completion(self, completion):
        text_cursor = self.textCursor()
        extra = len(completion) - len(self.completer.completionPrefix())
        text_cursor.movePosition(QTextCursor.Left)
        text_cursor.movePosition(QTextCursor.EndOfWord)
        text_cursor.insertText(completion[-extra:])
        self.setTextCursor(text_cursor)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor = PlainTextEditWithCompleter(self)
        completer = QCompleter(python_keywords, self.editor)
        self.editor.completer = completer
        self.setCentralWidget(self.editor)

def main():
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()

if __name__ == '__main__':
    main()
