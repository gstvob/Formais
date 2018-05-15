from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QComboBox, QPushButton, QTextEdit, QGridLayout, QLineEdit, QTableWidget, QTableWidgetItem, QInputDialog
from Operations import *
from Forms import *
from Models import Automaton

class GrammarEditor(QWidget):

	def __init__(self, grammars):
		super().__init__()
		self.grammars = grammars
		self.initUI()

	def initUI(self):
		self.grid = QGridLayout()
		self.choose_grammar = QComboBox(self)
		for i in self.grammars:
			self.choose_grammar.addItem(i.name)

		self.grammar_name = QLineEdit()
		self.grammar_update = QTextEdit()
		self.update_grammar = QPushButton("Update Grammar")
		self.result = QTextEdit()

		self.grammar_update.setReadOnly(True)
		self.grammar_name.setReadOnly(True)
		self.result.setReadOnly(True)

		self.grid.addWidget(self.choose_grammar, 0, 0)
		self.grid.addWidget(self.grammar_name, 1, 0)
		self.grid.addWidget(self.grammar_update, 2, 0)
		self.grid.addWidget(self.result, 3, 0)
		self.grid.addWidget(self.update_grammar, 4, 0)
		self.choose_grammar.activated[str].connect(self.updateGrammar)
		self.setLayout(self.grid)
		self.show()

	def updateGrammar(self, grammar_nameOld):

		ops = GrammarOperations(self.grammars)

		self.grammar_name.setReadOnly(False)
		self.grammar_update.setReadOnly(False)

		self.grammar_update.clear()
		self.result.clear()
		self.grammar_name.clear()

		grammar = next(x for x in self.grammars if x.name == grammar_nameOld)

		self.grammar_name.insert(grammar.name)
		self.grammar_update.textCursor().insertText(grammar.p)
		self.result.textCursor().insertText(grammar.p)
		self.update_grammar.clicked.connect(lambda : ops.updateGrammar(self))


	def update_combobox(self):
		index = self.choose_grammar.findText(self.choose_grammar.currentText())
		self.choose_grammar.removeItem(index)
		self.choose_grammar.insertItem(index, self.grammar_name.text())
		self.choose_grammar.setCurrentIndex(index)


class ExpressionEditor(QWidget):

	def __init__(self, expressions):
		super().__init__()
		self.expressions = expressions
		self.initUI()

	def initUI(self):
		self.grid = QGridLayout()
		self.choose_expression = QComboBox(self)

		for i in self.expressions:
			self.choose_expression.addItem(i.name)

		self.expression_name = QLineEdit()
		self.expression_new = QLineEdit()
		self.update_expression = QPushButton("Update Expression")
		self.result = QTextEdit()

		self.expression_name.setPlaceholderText("Update name of expression")
		self.expression_new.setPlaceholderText("Update expression")
		self.expression_new.setReadOnly(True)
		self.expression_name.setReadOnly(True)
		self.result.setReadOnly(True)

		self.grid.addWidget(self.choose_expression, 0, 0)
		self.grid.addWidget(self.expression_name, 1, 0)
		self.grid.addWidget(self.expression_new, 2, 0)
		self.grid.addWidget(self.result, 3, 0)
		self.grid.addWidget(self.update_expression, 4, 0)
		self.choose_expression.activated[str].connect(self.updateExpression)
		self.setLayout(self.grid)
		self.show()

	def updateExpression(self, oldname):
		ops = ExpressionOperations(self.expressions)

		self.expression_name.setReadOnly(False)
		self.expression_new.setReadOnly(False)

		self.expression_new.clear()
		self.result.clear()
		self.expression_name.clear()

		expression = next(x for x in self.expressions if x.name == oldname)

		self.expression_name.insert(expression.name)
		self.expression_new.insert(expression.expression)
		self.result.textCursor().insertText(expression.expression)
		self.update_expression.clicked.connect(lambda : ops.updateExpression(self))

	def update_combobox(self):
		index = self.choose_expression.findText(self.choose_expression.currentText())
		self.choose_expression.removeItem(index)
		self.choose_expression.insertItem(index, self.expression_name.text())
		self.choose_expression.setCurrentIndex(index)


class ConversionEditor(QWidget):

	def __init__(self, op, grammars, automata):
		super().__init__()
		self.grammars = grammars
		self.automata = automata
		if op == 1:
			self.grammar_automaton()
		else :
			self.automaton_grammar()

	#Fazer um combobox que permite eu escolher a gramática que eu quero Converter
	def _view(self, list):
		self.grid = QGridLayout()
		self.choose = QComboBox(self)
		for i in list:
			self.choose.addItem(i.name)
		self.grid.addWidget(self.choose, 0,0)
		self.setLayout(self.grid)
		self.show()

	def grammar_automaton(self):
		self._view(self.grammars)
		self.choose.disconnect()
		self.choose.activated[str].connect(self.show_grammar)

	def automaton_grammar(self):
		self._view(self.automata)
		self.choose.disconnect()
		self.choose.activated[str].connect(self.show_automaton)


	def show_grammar(self, grammar_name):
		grammar = next(x for x in self.grammars if x.name == grammar_name)
		ops = GrammarOperations(self.grammars)
		regular_grammar = QTextEdit()
		regular_grammar.setReadOnly(True)
		regular_grammar.textCursor().insertText("G:P={\n"+grammar.p+"}")

		convert = QPushButton("Convert to automaton")
		convert.setStatusTip("Convert the current grammar to a NDFA(or dfa directly depending on the grammar)")
		self.grid.addWidget(regular_grammar, 1,0)
		self.grid.addWidget(convert, 2, 0)
		convert.clicked.connect(lambda d: ops.convert_to_automaton(grammar, self))

	def show_automaton(self, automaton_name):
		automaton = next(x for x in self.automata if x.name == automaton_name)
		ops = AutomatonOperations(self.automata)
		self.build_table(automaton.states, automaton.alphabet, True)
		convert_to_grammar = QPushButton("Convert to grammar")
		convert_to_grammar.setStatusTip("Convert this automaton to a regular grammar")
		convert_to_grammar.clicked.connect(lambda d: ops.convert_to_grammar(automaton, self))
		self.grid.addWidget(convert_to_grammar, 2, 1)

	#colocar a opção de minimizar o automato-
	#depois de determinizar o autômato eu mostro o minimizar, se clicar
	#quando minimizar o automato ele substitui.
	def build_table(self, states, alphabet, alter=False):
		ops = AutomatonOperations(self.automata)

		table_representation = QTableWidget()
		table_representation.setColumnCount(len(alphabet))
		table_representation.setRowCount(len(states))
		states_labels = []
		
		for x in states:
			label = ""
			if x.acceptance:
				label+= "*"
			if x == states[0]:
				label += "->"
			label += x.label
			states_labels.append(label)

		table_representation.setVerticalHeaderLabels(states_labels)
		table_representation.setHorizontalHeaderLabels(alphabet)
		i = 0
		for state in states:
			header = table_representation.verticalHeaderItem(i)
			for j in range(len(alphabet)):
				symbol = table_representation.horizontalHeaderItem(j)
				transition = [x.target for x in state.transitions if x.symbol == symbol.text()]
				target_states = ""
				for tst in transition:
					target_states+=tst.label+" "
				newItem = QTableWidgetItem(target_states)
				newItem.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled )
				table_representation.setItem(i, j, newItem)
			i+=1

		self.grid.addWidget(table_representation, 1, 1)
		
		if not alter:
			save_automaton = QPushButton("Save Automaton")
			determinize = QPushButton("Determinize")
			at = Automaton("$at", states, alphabet)
			save_automaton.clicked.connect(lambda d: self.save_automata(states, alphabet))
			determinize.clicked.connect(lambda d: ops.ndfa_to_dfa(at, self))
			if at.non_deterministic:
				self.grid.addWidget(determinize, 2,1)
			self.grid.addWidget(save_automaton, 3,1)

	def print_productions(self, prod):
		productions = QTextEdit()
		productions.setReadOnly(True)
		productions.textCursor().insertText(prod)
		self.grid.addWidget(productions, 1,0)

	def save_automata(self, states, alphabet):
		saved = False

		while not saved:			
			name, ok = QInputDialog().getText(self,"Input Dialog", "Enter a name for this automaton")
			if ok:
				if not any(x.name == name for x in self.automata) and name != "":			
					automaton = Automaton(str(name), states, alphabet)
					self.automata.append(automaton)
					print(automaton.non_deterministic)
					saved = True
			else:
				break


class ExtraOperations(QWidget):
	
	def __init__(self, grammars):
		super().__init__()
		self.grammars = grammars

	def binaryOp(self, step=0, chosen1=""):
		if (step == 0):
			self.grid = QGridLayout()
			choose_grammar1 = QComboBox(self)
			self.g1 = QTextEdit()
			self.g1.setReadOnly(True)
			for i in self.grammars:
				choose_grammar1.addItem(i.name)
			choose_grammar1.activated[str].connect(lambda d: self.binaryOp(1, choose_grammar1.currentText()))
			self.grid.addWidget(choose_grammar1, 0, 0)
			self.grid.addWidget(self.g1, 1, 0)
			self.setLayout(self.grid)
			self.show()
		else:
			choose_grammar2 = QComboBox(self)
			self.g2 = QTextEdit()
			self.g2.setReadOnly(True)
			self.g1.clear()
			chosen1_prod = next(x.p for x in self.grammars if x.name == chosen1)
			self.g1.textCursor().insertText(chosen1_prod)
			for i in self.grammars:
				if i.name != chosen1:
					choose_grammar2.addItem(i.name)
			choose_grammar2.activated[str].connect(lambda d: self.operate(chosen1, choose_grammar2.currentText()))
			self.grid.addWidget(choose_grammar2, 0, 1)
			self.grid.addWidget(self.g2, 1, 1)

	def grammar_union(self):
		self.operation = "Union"
		self.binaryOp()

	def grammar_concat(self):
		self.operation = "Concat"
		self.binaryOp()


	def kleene_star(self):
		self.grid = QGridLayout()
		choose_grammar = QComboBox(self)
		self.g1 = QTextEdit()
		self.g1.setReadOnly(True)
		for i in self.grammars:
			choose_grammar.addItem(i.name)
		choose_grammar.activated[str].connect(self.operate_kleene)
		self.grid.addWidget(choose_grammar, 0, 0)
		self.grid.addWidget(self.g1, 1, 0)
		self.setLayout(self.grid)
		self.show()


	def operate_kleene(self, grammar):
		self.g1.clear()
		op = GrammarOperations(self.grammars)
		rg = next(x for x in self.grammars if x.name == grammar)
		self.g1.textCursor().insertText(rg.p)
		operate = QPushButton("Perform a Kleene Star operation")
		operate.setStatusTip("Perform a kleene star operation in a grammar")

		operate.clicked.connect(lambda d: op.kleene_star(rg, self))

		self.grid.addWidget(operate, 2, 0)

	def operate(self, grammar1, grammar2):
		self.g2.clear()
		op = GrammarOperations(self.grammars)
		rg1 = next(x for x in self.grammars if x.name == grammar1)
		rg2 = next(x for x in self.grammars if x.name == grammar2)
		self.g2.textCursor().insertText(rg2.p)
		operate = QPushButton("Perform "+self.operation)
		operate.setStatusTip("Perform a "+self.operation+" operation between two grammars")


		if (self.operation == "Union"):
			operate.clicked.connect(lambda d: op.grammar_union(rg1, rg2, self))
		else :
			operate.clicked.connect(lambda d: op.grammar_concat(rg1, rg2, self))
		self.grid.addWidget(operate, 2, 0)

	def show(self, grammar):
		result = QTextEdit()
		result.setReadOnly(True)
		result.textCursor().insertText(grammar)

		self.grid.addWidget(result, 3, 1)
