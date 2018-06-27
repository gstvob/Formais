from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QComboBox, QPushButton, QTextEdit, QGridLayout, QLineEdit, QTableWidget, QTableWidgetItem, QInputDialog
from models import *


'''

AUTOR : GUSTAVO BORGES FRANÇA

'''


'''
	Essas classes fazem a "ponte" entre
	a lógica que se encontra nos modelos e a interface visual.
	é por aqui que são feitas as ações que o usuário escolhe
	usando de todos os métodos criados na parte dos modelos.
'''

class ContextFreeOperations(QWidget):

	def __init__(self):
		super().__init__()

	def choose_to_transform(self, grammars):
		grid = QGridLayout(self)
		choose = QComboBox(self)
		for i in grammars:
			if i.has_simple_productions() or not i.is_epsilon_free() or i.has_useless_symbols():
				choose.addItem(i.name)
		grid.addWidget(choose, 0,0)
		choose.activated[str].connect(lambda d: self.transform(choose.currentText(), grammars))
		self.setLayout(grid)
		self.show()

	def transform(self, name, grammars):
		grammar = next(g for g in grammars if g.name == name)
		intermed_g = ContextFreeGrammar("$at", grammar.p_string)
		intermeds = intermed_g.into_proper_grammar()
		original = QTextEdit(self)
		epsilon_free = QTextEdit(self)
		without_simple_prods = QTextEdit(self)
		without_useless_symbols = QTextEdit(self)

		save_epsilon_free = QPushButton(self)
		save_without_simple_prods = QPushButton(self)
		save_without_useless_symbols = QPushButton(self)

		original.setReadOnly(True)
		epsilon_free.setReadOnly(True)
		without_simple_prods.setReadOnly(True)
		without_useless_symbols.setReadOnly(True)

		original.textCursor().insertText(intermed_g.p_string)

		if "e-free" in intermeds:
			epsilon_free.textCursor().insertText(intermeds["e-free"])
		else:
			epsilon_free.textCursor().insertText(intermed_g.p_string)

		if "no-simple" in intermeds:
			without_simple_prods.textCursor().insertText(intermeds["no-simple"])
		else:
			without_simple_prods.textCursor().insertText(intermed_g.p_string)

		if "no-useless" in intermeds:
			without_useless_symbols.textCursor().insertText(intermeds["no-useless"])
		else:
			without_useless_symbols.textCursor().insertText(intermed_g.p_string)


		self.layout().addWidget(original, 1, 0)
		self.layout().addWidget(epsilon_free, 2, 0)
		self.layout().addWidget(without_simple_prods, 3, 0)
		self.layout().addWidget(without_useless_symbols, 4, 0)		
		self.layout().addWidget(save_epsilon_free, 2, 1)
		self.layout().addWidget(save_without_simple_prods, 3, 1)
		self.layout().addWidget(save_without_useless_symbols, 4, 1)		