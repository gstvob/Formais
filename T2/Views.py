from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QPushButton, QTextEdit, QComboBox, QGridLayout, QTableWidget, QTableWidgetItem, QLabel
from models import *
'''

AUTOR : GUSTAVO BORGES FRANÇA.

'''

'''
	Mais classes para suporte a interface gráfica.
	Aqui criam-se as visualizações das gramáticas.
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
		self.states = QTextEdit(self)
		self.states.setFont(font)
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

		if rep_g.is_factored():
			text5 = "Está fatorada"
		else:
			text5 = "Não está fatorada"

		rep_g.set_firsts()
		rep_g.set_follows()
		rep_g.set_first_nt()
		text6 = ""
		text7 = ""
		text8 = ""
		for i in rep_g.vn:
			text6 += str(i)+" firsts = "
			text6 += "".join(str(i.first))+"\n"
		for i in rep_g.vn:
			text7 += str(i)+" follows = "
			text7 += "".join(str(i.follow))+"\n"
		for i in rep_g.vn:
			text8 += str(i)+" first_nt = "
			text8 += "".join(str(i.first_nt))+"\n"

		if rep_g.has_leftmost_recursion():
			text9 = "Tem recursão a esquerda"
		else:
			text9 = "Não tem recursão a esquerda"
		self.states.clear()
		self.states.textCursor().insertText(text1+"\n"+text2+"\n"+text3+"\n"+text4+"\n"+text5+"\n"+text6+"\n"+text7+"\n"+text8+"\n"+text9)
		self.grid.addWidget(self.states, 1, 1)