from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QComboBox, QPushButton, QTextEdit, QGridLayout, QLineEdit, QTableWidget, QTableWidgetItem, QInputDialog
from Models import *

class GrammarOperations(QWidget):

	def __init__(self):
		super().__init__()

	def choose_for_conversion(self, grammars, automata):
		grid = QGridLayout()
		choose = QComboBox(self)
		for i in grammars:
			choose.addItem(i.name)
		grid.addWidget(choose, 0,0)
		choose.activated[str].connect(lambda d: self.convert(choose.currentText(), automata, grammars))
		self.setLayout(grid)
		self.show()

	def choose_for_op(self, grammars, op):
		grid = QGridLayout()
		choose_grammar1 = QComboBox(self)
		g1 = QTextEdit()
		g1.setReadOnly(True)
		
		if op != 2:
			choose_grammar2 = QComboBox(self)
			g2 = QTextEdit()
			g2.setReadOnly(True)
			for i in grammars:
				choose_grammar2.addItem(i.name)

			choose_grammar2.activated[str].connect(lambda d: self._change_text(choose_grammar2.currentText(), g2, grammars))
			grid.addWidget(choose_grammar2, 0 ,1)
			grid.addWidget(g2, 1, 1)
		
		for i in grammars:
			choose_grammar1.addItem(i.name)
		
		choose_grammar1.activated[str].connect(lambda d: self._change_text(choose_grammar1.currentText(), g1, grammars))
		grid.addWidget(choose_grammar1, 0, 0)
		grid.addWidget(g1, 1, 0)
		#união
		button = None
		if op == 0:
			button = QPushButton("Unir gramáticas")
			button.clicked.connect(lambda d: self.operate(choose_grammar1.currentText(), choose_grammar2.currentText(), grammars, 0))
		elif op ==1 :
			button = QPushButton("Concatenar gramáticas")
			button.clicked.connect(lambda d: self.operate(choose_grammar1.currentText(), choose_grammar2.currentText(), grammars, 1))
		else :
			button = QPushButton("Realizar Fecho")
			button.clicked.connect(lambda d: self.operate(choose_grammar1.currentText(), "", grammars, 2))
		
		grid.addWidget(button,2,0)
		self.setLayout(grid)
		self.show()


	def convert(self, grammar_name, automata, grammars):
		grammar = next(x for x in grammars if x.name == grammar_name)
		regular_grammar = QTextEdit()
		regular_grammar.setReadOnly(True)
		regular_grammar.textCursor().insertText("G:P={\n"+grammar.p+"}")

		convert_ = QPushButton("Converter para autômato")
		convert_.setStatusTip("Converter a gramática para um AFN(ou AFD dependendo da gramática)")
		self.layout().addWidget(regular_grammar, 1,0)
		self.layout().addWidget(convert_, 2, 0)
		convert_.clicked.connect(lambda d: self.apply_conversion(grammar, automata))

	def operate(self,name1,name2, grammars, op):
		result = QTextEdit()
		result.setReadOnly(True)

		grammar1 = next(x for x in grammars if x.name == name1)
		if op != 2:
			grammar2 = next(x for x in grammars if x.name == name2)

		operation_ = None
		save = None
		if op == 0:
			save = QPushButton("Salvar união")
			operation_ = grammar1.union(grammar2)
		elif op == 1:
			save = QPushButton("Salvar concatenação")
			operation_ = grammar1.concatenate(grammar2)
		else:
			save = QPushButton("Salvar Fecho")
			operation_ = grammar1.kleene_star()

		if operation_ != None:
			result.textCursor().insertText(operation_.p)
			save.clicked.connect(lambda d: self.save_grammar(operation_, grammars))
		else :
			result.textCursor().insertText("A intersecção dos não terminais das gramáticas deve ser vazia")
		self.layout().addWidget(result,3,0)
		self.layout().addWidget(save,3,1)

	def apply_conversion(self, grammar, automata):
		automaton = grammar.convert()
		self.build_table(automaton, automata)

	def determinize(self, automaton, automata):
		det = AutomatonOperations() 
		dfa_automaton = det.determinize(automaton)
		self.build_table(dfa_automaton, automata)

	def minimize(self, automaton, automata):
		mini = AutomatonOperations()
		minimal = mini.minimize(automaton)
		self.build_table(minimal, automata)

	def build_table(self, automaton, automata):
		states = automaton.states
		alphabet = automaton.alphabet

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

		self.layout().addWidget(table_representation, 1, 1)

		save_automaton = QPushButton("Salvar Autômato")
		determinize = QPushButton("Determinizar")
		minimize = QPushButton("Minimizar")
		save_automaton.clicked.connect(lambda d: self.save_automata(automata, automaton))
		determinize.clicked.connect(lambda d: self.determinize(automaton, automata))
		minimize.clicked.connect(lambda d: self.minimize(automaton, automata))
		if automaton.non_deterministic:
			self.layout().addWidget(determinize, 2,1)
		else:
			self.layout().addWidget(minimize, 2, 1)
		self.layout().addWidget(save_automaton, 3,1)

	def save_automata(self, automata, automaton):
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
	def save_grammar(self, grammar,grammars):
		saved = False
		while not saved:
			name, ok = QInputDialog().getText(self, "Input Dialog", "Nomeie a gramática")
			if ok:
				if not any(x.name == name for x in grammars) and name != "":
					grammar.set_name(name)
					grammars.append(grammar)
					saved = True
			else:
				break

	def _change_text(self, combobox_text, text_edit, grammars):
		p = next(x.p for x in grammars if combobox_text == x.name)
		text_edit.clear()
		text_edit.textCursor().insertText(p)


class AutomatonOperations(QWidget):
	def __init__(self):
		super().__init__()

	def automaton_test_input(self, automata):
		grid = QGridLayout(self)
		choose_automaton = QComboBox(self)
		for i in automata:
			if not i.non_deterministic:
				choose_automaton.addItem(i.name)

		choose_automaton.activated[str].connect(lambda d: self._input(choose_automaton.currentText(), automata))
		grid.addWidget(choose_automaton, 0, 0)
		self.setLayout(grid)
		self.show()


	def automata_for_binary_op(self, automata, op):
		grid = QGridLayout()
		choose_automaton1 = QComboBox(self)
		choose_automaton2 = QComboBox(self)
		for i in automata:
			if not i.non_deterministic:
				choose_automaton1.addItem(i.name)
				choose_automaton2.addItem(i.name)

		choose_automaton1.activated[str].connect(lambda d: self._show_af_table(choose_automaton1.currentText(), automata, 0))
		choose_automaton2.activated[str].connect(lambda d: self._show_af_table(choose_automaton2.currentText(), automata, 1))
		grid.addWidget(choose_automaton1, 0, 0)		
		grid.addWidget(choose_automaton2, 0, 1)
		button = None
		if op == 0:
			button = QPushButton("Unir")
			button.clicked.connect(lambda d: self.operate(choose_automaton1.currentText(), choose_automaton2.currentText(), automata, 0))
		elif op ==1 :
			button = QPushButton("Interseccionar")
			button.clicked.connect(lambda d: self.operate(choose_automaton1.currentText(), choose_automaton2.currentText(), automata, 1))
		else :
			button = QPushButton("Diferença")
			button.clicked.connect(lambda d: self.operate(choose_automaton1.currentText(), choose_automaton2.currentText(), automata, 2))
		
		grid.addWidget(button,2,0)
		self.setLayout(grid)
		self.show()

	def automata_for_unary_op(self, automata, op):
		grid = QGridLayout()
		choose_automaton1 = QComboBox(self)
		for i in automata:
			if not i.non_deterministic:
				choose_automaton1.addItem(i.name)

		choose_automaton1.activated[str].connect(lambda d: self._show_af_table(choose_automaton1.currentText(), automata, 0))
		grid.addWidget(choose_automaton1, 0, 0)		
		button = None
		if op == 3:
			button = QPushButton("Complemento")
			button.clicked.connect(lambda d: self.operate(choose_automaton1.currentText(), "",automata, 3))
		else:
			button = QPushButton("Reverso")
			button.clicked.connect(lambda d: self.operate(choose_automaton1.currentText(), "", automata, 4))
		
		grid.addWidget(button,2,0)
		self.setLayout(grid)
		self.show()

	def _show_af_table(self, a_name, automata, column):
		automaton = next(x for x in automata if a_name == x.name)
		self.build_table(automaton, column=column)

	def operate(self, a_name1, a_name2, automata, op):
		if a_name1!="" and a_name2!="":
			if op == 0:
				automaton1 = next(x for x in automata if x.name == a_name1)
				automaton2 = next(x for x in automata if x.name == a_name2)
				union = automaton1.union(automaton2)
				save_button = QPushButton("Salvar")
				save_button.clicked.connect(lambda d: self.save_automaton(union, automata))
				self.build_table(union, 3, 0)
				self.layout().addWidget(save_button, 3, 1)
		elif a_name1!="":
			if op == 3:
				automaton = next(x for x in automata if x.name == a_name1)
				complement = automaton.complement()
				self.build_table(complement)

	def determinize(self, automaton):
		dfa_automaton = automaton.ndfa_to_dfa()
		return dfa_automaton

	def minimize(self, automaton):
		automaton.remove_dead_states()
		reversed_automaton = automaton.reverse()
		determinize_reverse = reversed_automaton.ndfa_to_dfa()
		determinize_reverse.remove_unreachable_states()
		reverse_determinize_reverse = determinize_reverse.reverse()
		minimal = reverse_determinize_reverse.ndfa_to_dfa()
		minimal.remove_unreachable_states()
		minimal.merge_equal_states()
		return minimal

	def enumerate_nsize_inputs(self, automata):
		grid = QGridLayout(self)
		choose_automaton = QComboBox(self)
		for i in automata:
			if not i.non_deterministic:
				choose_automaton.addItem(i.name)
		choose_automaton.activated[str].connect(lambda d: self._choose_size(choose_automaton.currentText(), automata))
		grid.addWidget(choose_automaton, 0, 0)
		self.setLayout(grid)
		self.show()

	def _choose_size(self, automaton_name, automata):
		automaton = next(x for x in automata if x.name == automaton_name)
		size = QLineEdit(self)
		button = QPushButton("Enumerar entradas")

		self.build_table(automaton)

		button.clicked.connect(lambda d: self._enumerate(size.text(), automaton))

		self.layout().addWidget(size, 2, 0)
		self.layout().addWidget(button,3, 0)

	def _enumerate(self, size, automaton):
		result = QTextEdit()
		result.setReadOnly(True)

		if not size.isdigit():
			result.textCursor().insertText("Entrada não é um digito")
		else:
			entries = automaton.enumerate(size)
			for entry in entries:
				result.textCursor().insertText(entry+"\n")

		self.layout().addWidget(result, 4, 0)

	def _input(self, automaton_name, automata):
		automaton = next(x for x in automata if x.name == automaton_name)
		inp = QLineEdit(self)
		button = QPushButton("Testar entrada")

		self.build_table(automaton)

		button.clicked.connect(lambda d: self._test_input(inp.text(), automaton))

		self.layout().addWidget(inp, 2, 0)
		self.layout().addWidget(button,3, 0)

	def _test_input(self, inp, automaton):
		test = automaton.parse_input(inp)
		result = QLineEdit()
		result.setReadOnly(True)

		if test:
			result.insert("aceitou")
		else:
			result.insert("recusou")


		self.layout().addWidget(result, 3, 1)

	def choose_for_conversion(self, automata, grammars):
		grid = QGridLayout()
		choose = QComboBox(self)
		for i in automata:
			choose.addItem(i.name)
		grid.addWidget(choose, 0,0)
		choose.activated[str].connect(lambda d : self.show_automaton(choose.currentText(), automata, grammars))
		self.setLayout(grid)
		self.show()

	def show_automaton(self, automaton_name, automata, grammars):
		automaton = next(x for x in automata if x.name == automaton_name)
		self.build_table(automaton)
		convert_to_grammar = QPushButton("Converter para gramática")
		convert_to_grammar.setStatusTip("Converter esse autômato em uma gramática regular")
		convert_to_grammar.clicked.connect(lambda d: self.convert(automaton, grammars))
		self.layout().addWidget(convert_to_grammar, 2, 1)

	def save_automaton(self, automaton, automata):
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

	def build_table(self, automaton,row = 1, column=1):
		states = automaton.states
		alphabet = automaton.alphabet
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

		self.layout().addWidget(table_representation, row, column)

	def convert(self, automaton, grammars):
		grammar = automaton.convert()
		self.print_grammar(grammar, grammars)

	def print_grammar(self, grammar, grammars):
		productions = QTextEdit()
		productions.setReadOnly(True)

		productions.textCursor().insertText(grammar.p)
		#possível botão pra salvar a gramática?

		self.layout().addWidget(productions,1,0)