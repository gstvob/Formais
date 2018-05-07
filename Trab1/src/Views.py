from PyQt5.QtWidgets import QWidget, QPushButton, QTextEdit, QComboBox, QGridLayout

class GrammarView(QWidget):

	def __init__(self, grammarList):
		super().__init__()
		self.grammarList = grammarList
		self.initUI()

	def initUI(self):

		self.grid = QGridLayout()
		self.choose_grammar = QComboBox()
		self.view_grammar = QTextEdit()
		self.view_grammar.setReadOnly(True)
		for i in self.grammarList:
			self.choose_grammar.addItem(i.name)
		self.choose_grammar.activated[str].connect(self._grammar)
		self.grid.addWidget(self.choose_grammar,0,0)
		self.grid.addWidget(self.view_grammar,1,0)
		self.setLayout(self.grid)
		self.show()

	def _grammar(self, name):
		self.view_grammar.clear()
		grammar = next(x for x in self.grammarList if x.name == name)
		self.view_grammar.textCursor().insertText(grammar.p)
