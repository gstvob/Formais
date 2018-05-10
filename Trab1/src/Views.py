from PyQt5.QtWidgets import QWidget, QPushButton, QTextEdit, QComboBox, QGridLayout


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
