from PyQt5.QtWidgets import QPushButton,QWidget, QTextEdit,QLineEdit, QLabel, QGridLayout, QComboBox
from Models import *

'''

AUTOR : GUSTAVO BORGES FRANÇA

'''

'''
   Essas classes são as classes visuais que mostram
   os formulários para criação de gramáticas e expressões regulares.
   sem nenhuma operação ou lógica complexa, apenas definições e chamadas. 
'''

class GrammarForm(QWidget):
    def __init__(self):
        super().__init__()

    def insert(self, grammars):
        grammar_name = QLineEdit()
        grammar_start = QLabel('G : P = {')
        grammar_end = QLabel('}')
        grammar_edit = QTextEdit()
        save_grammar = QPushButton("Salvar Gramática")
        result = QTextEdit()
        result.setReadOnly(True)
        result.setPlaceholderText("Os resultados aparecerão aqui.")
        result.setMaximumHeight(200)
        grammar_edit.setMaximumHeight(300)
        grammar_name.setPlaceholderText("Dê um nome para sua gramática")
        grid = QGridLayout()

        grid.addWidget(grammar_name, 1, 0)
        grid.addWidget(grammar_start, 2, 0)
        grid.addWidget(grammar_edit, 3, 0)
        grid.addWidget(grammar_end,4, 1)
        grid.addWidget(result,5, 0)
        grid.addWidget(save_grammar,6, 0)

        save_grammar.clicked.connect(lambda d: self.build_grammar(
                                                grammar_edit.toPlainText(),
                                                grammar_name.text(),
                                                result, grammars))

        self.setLayout(grid)
        self.show()


    def update(self, grammars):

        grid = QGridLayout()
        self.choose_grammar = QComboBox(self)
        for i in grammars:
            self.choose_grammar.addItem(i.name)

        grid.addWidget(self.choose_grammar, 0, 0)
        self.choose_grammar.activated[str].connect(lambda d: self.edit(self.choose_grammar.currentText(), grammars))

        self.setLayout(grid)
        self.show()

    def build_grammar(self, productions, name, result, grammars):
        result.clear()
        grammar = RegularGrammar(name, productions)

        if grammar.validate_grammar(productions) and (name not in [x.name for x in grammars] and name != ""):
            result.textCursor().insertText(productions)
            grammars.append(grammar)
        else:
            result.textCursor().insertText("Existe um erro na sua gramática/existe uma gramática com esse nome/nome de gramática vazio")

    def build_update(self, index, productions, name, result, grammars):
        result.clear()
        grammar = RegularGrammar(name, productions)
        changed_name = name != grammars[index].name

        if grammar.validate_grammar(productions) and (not changed_name or (name not in [x.name for x in grammars])) and name != "":
            result.textCursor().insertText(productions)
            grammars[index] = grammar
            self._update_combobox(grammar)
        else:
            result.textCursor().insertText("Existe um erro na sua atualização de gramática")


    def edit(self, name, grammars):
        grammar_name = QLineEdit()
        grammar_update = QTextEdit()
        update_grammar = QPushButton("Atualizar Gramatica")
        result = QTextEdit()
        print(name)
        print([x.name for x in grammars])
        index = grammars.index(next(x for x in grammars if x.name == name))
        grammar_name.insert(grammars[index].name)
        grammar_update.textCursor().insertText(grammars[index].p)
        result.textCursor().insertText(grammars[index].p)
        update_grammar.clicked.connect(lambda d: self.build_update(index, 
                                                        grammar_update.toPlainText(), 
                                                        grammar_name.text(),
                                                        result,
                                                        grammars))
        self.layout().addWidget(grammar_name, 1, 0)
        self.layout().addWidget(grammar_update, 2, 0)
        self.layout().addWidget(result, 3, 0)
        self.layout().addWidget(update_grammar, 4, 0)

    def _update_combobox(self, new_grammar):
        index = self.choose_grammar.findText(self.choose_grammar.currentText())
        self.choose_grammar.removeItem(index)
        self.choose_grammar.insertItem(index, new_grammar.name)
        self.choose_grammar.setCurrentIndex(index)

class ExpressionForm(QWidget):

    def __init__(self):
        super().__init__()

    def insert(self, expressions):

        expression_name = QLineEdit()
        expression_edit = QLineEdit()
        save_expression = QPushButton("Salvar Expressão")
        result = QTextEdit()
        result.setReadOnly(True)
        result.setPlaceholderText("Os resultados aparecerão aqui")
        result.setMaximumHeight(200)
        expression_name.setPlaceholderText("Dê um nome para sua expressão")
        expression_edit.setPlaceholderText("Expressão Válida")

        grid = QGridLayout()

        grid.addWidget(expression_name, 1, 0)
        grid.addWidget(expression_edit, 2, 0)
        grid.addWidget(result,3, 0)
        grid.addWidget(save_expression,4, 0)

        save_expression.clicked.connect(lambda d: self.build_expression(
                                                        expression_edit.text(),
                                                        expression_name.text(),
                                                        result, expressions))
        self.setLayout(grid)
        self.show()


    def update(self, expressions):

        grid = QGridLayout()
        self.choose_expression = QComboBox(self)
        for i in expressions:
            self.choose_expression.addItem(i.name)

        grid.addWidget(self.choose_expression, 0, 0)
        self.choose_expression.activated[str].connect(lambda d: self.edit(self.choose_expression.currentText(), expressions))

        self.setLayout(grid)
        self.show()

    def build_expression(self, expression, name, result, expressions):
        result.clear()
        regexp = RegularExpression(name, expression)

        if regexp.validate_expression(expression) and (name not in [x.name for x in expressions] and name!=""):
            expressions.append(regexp)
            result.textCursor().insertText(expression)
        else:
            result.textCursor().insertText("Algo de errado na sua expressão/nome de expressão existente/nome vazio")


    def build_update(self, index, expression, name, result, expressions):
        result.clear()
        regexp = RegularExpression(name,expression)
        changed_name = name != expressions[index].name

        if regexp.validate_expression(expression) and (not changed_name or (name not in [x.name for x in expressions])) and name != "":
            result.textCursor().insertText(expression)
            expressions[index] = regexp
            self._update_combobox(regexp)
        else:
            result.textCursor().insertText("Existe um erro na sua atualização de expressão")


    def edit(self, name, expressions):
        expression_name = QLineEdit()
        expression_update = QTextEdit()
        update_expression = QPushButton("Atualizar Expressão")
        result = QTextEdit()
        index = expressions.index(next(x for x in expressions if x.name == name))
        expression_name.insert(expressions[index].name)
        expression_update.textCursor().insertText(expressions[index].expression)
        result.textCursor().insertText(expressions[index].expression)
        update_expression.clicked.connect(lambda d: self.build_update(index, 
                                                        expression_update.toPlainText(), 
                                                        expression_name.text(),
                                                        result,
                                                        grammars))
        self.layout().addWidget(expression_name, 1, 0)
        self.layout().addWidget(expression_update, 2, 0)
        self.layout().addWidget(result, 3, 0)
        self.layout().addWidget(update_expression, 4, 0)

    def _update_combobox(self, new_regex):
        index = self.choose_grammar.findText(self.choose_grammar.currentText())
        self.choose_grammar.removeItem(index)
        self.choose_grammar.insertItem(index, new_regex.name)
        self.choose_grammar.setCurrentIndex(index)



