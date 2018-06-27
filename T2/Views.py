from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QPushButton, QTextEdit, QComboBox, QGridLayout, QTableWidget, QTableWidgetItem, QLabel
from models import *
'''

AUTOR : GUSTAVO BORGES FRANÇA.

'''

'''
	Mais classes para suporte a interface gráfica.
	Aqui criam-se as visualizações das gramáticas, expressões e autômatos salvos.
'''

class View(QWidget):

	def __init__(self, grammars):
		super().__init__()
		self.grammars = grammars
		self.initUI()

	def initUI(self):
		self.grid = QGridLayout(self)
		self.choose = QComboBox(self)
		self.view = QTextEdit(self)
		self.view.setReadOnly(True)
		for i in self.grammars:
			self.choose.addItem(i.name)
		self.choose.activated[str].connect(self._view)
		self.grid.addWidget(self.choose,0,0)
		self.grid.addWidget(self.view,1,0)
		self.setLayout(self.grid)
		self.show()

	def _view(self, name):
		self.view.clear()
		grammar = next(x for x in self.grammars if x.name == name)
		self.view.textCursor().insertText(grammar.p_string)
		font = QtGui.QFont()
		font.setBold(True)
		states = QLabel(self)
		states.setFont(font)
		rep_g = grammar
		text1 = rep_g.finiteness()
		if rep_g.is_epsilon_free():
			text2 = "Epsilon Livre"
		else:
			text2 = "Não epsilon Livre"
		
		if rep_g.has_simple_productions():
			text3 = "Tem produções simples"
		else:
			text3 = "Não tem produções simples"

		if rep_g.has_useless_symbols():
			text4 = "Tem simbolos inúteis"
		else:
			text4 = "Não tem simbolos inúteis" 

		lfm_recursion = rep_g.has_leftmost_recursion()

		states.setText(text1+"\n"+text2+"\n"+text3+"\n"+text4)
		self.grid.addWidget(states, 1, 1)