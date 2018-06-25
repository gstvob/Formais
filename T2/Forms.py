from PyQt5.QtWidgets import QPushButton,QWidget, QTextEdit,QLineEdit, QLabel, QGridLayout, QComboBox
from models import *

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
		self.grammar_name = QLineEdit(self)
		self.grammar_edit = QTextEdit(self)
		save_grammar = QPushButton("Salvar Gramática")
		self.result = QTextEdit(self)
		self.result.setReadOnly(True)
		self.result.setPlaceholderText("Os resultados aparecerão aqui.")
		self.result.setMaximumHeight(200)
		self.grammar_edit.setMaximumHeight(300)
		self.grammar_name.setPlaceholderText("Dê um nome para sua gramática")
		grid = QGridLayout()

		grid.addWidget(self.grammar_name, 1, 0)
		grid.addWidget(self.grammar_edit, 2, 0)
		grid.addWidget(self.result,3, 0)
		grid.addWidget(save_grammar,4, 0)

		save_grammar.clicked.connect(lambda d: self.build_grammar(grammars))
		self.setLayout(grid)
		self.show()

	def handle_text(self):
		grammar = self.grammar_edit.toPlainText()


	def build_grammar(self, grammars):
		self.result.clear()
		grammar = ContextFreeGrammar(self.grammar_name.text(), self.grammar_edit.toPlainText())
		self.result.textCursor().insertText(self.grammar_edit.toPlainText())
		grammars.append(grammar)
'''
    def build_update(self, index, productions, name, result, grammars):
        result.clear()
        grammar = RegularGrammar(name, productions)
        changed_name = name != grammars[index].name
-
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
'''

'''
def update(self, grammars):

grid = QGridLayout()
self.choose_grammar = QComboBox(self)
for i in grammars:
    self.choose_grammar.addItem(i.name)

grid.addWidget(self.choose_grammar, 0, 0)
self.choose_grammar.activated[str].connect(lambda d: self.edit(self.choose_grammar.currentText(), grammars))

self.setLayout(grid)
self.show()
'''