from PyQt5.QtWidgets import QWidget, QComboBox, QPushButton, QTextEdit, QGridLayout, QLineEdit
from Operations import GrammarOperations
from Models import RegularGrammar

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


	def update_combobox(self, updated_name):
		index = self.choose_grammar.findText(self.choose_grammar.currentText())
		self.choose_grammar.removeItem(index)
		self.choose_grammar.insertItem(index, self.grammar_name.text())
		self.choose_grammar.setCurrentIndex(index)
