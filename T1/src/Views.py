from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QTextEdit, QComboBox, QGridLayout, QTableWidget, QTableWidgetItem
from Editors import *

'''

AUTOR : GUSTAVO BORGES FRANÇA.

'''

'''
	Mais classes para suporte a interface gráfica.
	Aqui criam-se as visualizações das gramáticas, expressões e autômatos salvos.
'''

class View(QWidget):

	def __init__(self, list):
		super().__init__()
		self.list = list
		self.initUI(self)

	def initUI(self, list):
		self.grid = QGridLayout()
		self.choose = QComboBox()
		self.view = QTextEdit()
		self.view.setReadOnly(True)
		for i in self.list:
			self.choose.addItem(i.name)
		self.choose.activated[str].connect(self._view)
		self.grid.addWidget(self.choose,0,0)
		self.grid.addWidget(self.view,1,0)
		self.setLayout(self.grid)
		self.show()

	def _view(self, name):
		self.view.clear()
		object = next(x for x in self.list if x.name == name)
		try:
			self.view.textCursor().insertText(object.p)
		except AttributeError:
			self.view.textCursor().insertText(object.expression)

class GrammarView(View):

	def __init__(self, grammarList):
		super().__init__(grammarList)

class ExpressionView(View):

	def __init__(self, expressionList):
		super().__init__(expressionList)

class AutomatonView(View):

	def __init__(self, automata):
		super().__init__(automata)

	def _view(self, name="", automaton=None):
		if automaton==None:
			automaton = next(x for x in self.list if x.name == name)
		table_representation = QTableWidget()
		table_representation.setColumnCount(len(automaton.alphabet))
		table_representation.setRowCount(len(automaton.states))
		states_labels = []

		for x in automaton.states:
			label = ""
			if x.acceptance:
				label+= "*"
			if x == automaton.states[0]:
				label += "->"
			label += x.label
			states_labels.append(label)

		table_representation.setVerticalHeaderLabels(states_labels)
		table_representation.setHorizontalHeaderLabels(automaton.alphabet)
		i = 0
		for state in automaton.states:
			header = table_representation.verticalHeaderItem(i)
			for j in range(len(automaton.alphabet)):
				symbol = table_representation.horizontalHeaderItem(j)
				transition = [x.target for x in state.transitions if x.symbol == symbol.text()]
				target_states = ""
				for tst in transition:
					target_states+=tst.label+" "
				newItem = QTableWidgetItem(target_states)
				newItem.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
				table_representation.setItem(i, j, newItem)
			i+=1
		self.grid.addWidget(table_representation, 1, 0)
		
		save_automaton = QPushButton("Salvar Autômato")
		determinize = QPushButton("Determinizar")
		minimize = QPushButton("Minimizar")
		save_automaton.clicked.connect(lambda d: self.save_automaton(self.list, automaton))
		determinize.clicked.connect(lambda d: self.determinize(self.list, automaton))
		minimize.clicked.connect(lambda d: self.minimize(self.list, automaton))
		if automaton.non_deterministic:
			self.grid.addWidget(determinize, 2,0)
		else:
			self.grid.addWidget(minimize, 2, 0)
		self.grid.addWidget(save_automaton, 3,0)


	def determinize(self, automata, automaton):
		automatonOperations = AutomatonOperations()
		det = automatonOperations.determinize(automaton)
		self._view(automaton=det)
	def minimize(self, automata, automaton):
		automatonOperations = AutomatonOperations()
		mini = automatonOperations.minimize(automaton)
		self._view(automaton=mini)
	def save_automaton(self, automata, automaton):
		saved = False
		while not saved:			
			name, ok = QInputDialog().getText(self,"Input Dialog", "Nomeie este autômato")
			if ok:
				if not any(x.name == name for x in automata) and name != "":			
					automaton.set_name(name)
					automata.append(automaton)
					saved = True
			else:
				break

			if saved==True:
				self.update_combobox(automata)
	def update_combobox(self, automata):
		self.choose = QComboBox(self)
		for i in automata:
			self.choose.addItem(i.name)
		self.choose.activated[str].connect(self._view)
		self.grid.addWidget(self.choose,0,0)