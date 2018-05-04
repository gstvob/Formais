# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QPushButton,QWidget, QTextEdit, QLineEdit, QLabel, QGridLayout
from Operations import Operations

class GrammarForm(QWidget):

    def __init__(self, grammars):
        super().__init__()
        self.initUI(grammars)

    def initUI(self, grammars):
        ops = Operations(grammars)
        grammar_name = QLineEdit()
        grammar_start = QLabel('G : P = {')
        grammar_end = QLabel('}')
        grammar_edit = QTextEdit()
        save_grammar = QPushButton("Save Grammar")
        result = QTextEdit()
        result.setReadOnly(True)

        result.setMaximumHeight(200)
        grammar_edit.setMaximumHeight(300)
        grammar_name.setPlaceholderText("Name your grammar")
        grid = QGridLayout()

        grid.addWidget(grammar_name, 1, 0)
        grid.addWidget(grammar_start, 2, 0)
        grid.addWidget(grammar_edit, 3, 0)
        grid.addWidget(grammar_end,4, 1)
        grid.addWidget(result,5, 0)
        grid.addWidget(save_grammar,6, 0)

        save_grammar.clicked.connect(lambda: ops.parse_grammar(grammar_edit.toPlainText(), grammar_name.text(), result))

        self.setLayout(grid)
        self.show()
