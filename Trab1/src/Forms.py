# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QPushButton,QWidget, QTextEdit, QLineEdit, QLabel, QGridLayout
from Operations import GrammarOperations, ExpressionOperations

class GrammarForm(QWidget):
    def __init__(self, grammars):
        super().__init__()
        self.initUI(grammars)

    def initUI(self, grammars):
        ops = GrammarOperations(grammars)
        grammar_name = QLineEdit()
        grammar_start = QLabel('G : P = {')
        grammar_end = QLabel('}')
        grammar_edit = QTextEdit()
        save_grammar = QPushButton("Save Grammar")
        result = QTextEdit()
        result.setReadOnly(True)
        result.setPlaceholderText("The results will be shown here.")
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


class ExpressionForm(QWidget):

    def __init__(self, expressions, update=False):
        super().__init__()
        self.initUI(expressions, update)

    def initUI(self, expressions, update):

        ops = ExpressionOperations(expressions)
        expression_name = QLineEdit()
        expression_edit = QLineEdit()
        save_expression = QPushButton("Save Expression")
        result = QTextEdit()
        result.setReadOnly(True)
        result.setPlaceholderText("The results will be shown here.")
        result.setMaximumHeight(200)
        expression_name.setPlaceholderText("Name your expression")
        expression_edit.setPlaceholderText("Valid expression")

        grid = QGridLayout()

        grid.addWidget(expression_name, 1, 0)
        grid.addWidget(expression_edit, 2, 0)
        grid.addWidget(result,3, 0)
        grid.addWidget(save_expression,4, 0)

        save_expression.clicked.connect(lambda: ops.parse_expression(expression_edit.text(), expression_name.text(), result, update))
        self.setLayout(grid)
        self.show()
