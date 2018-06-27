import sys
from PyQt5.QtWidgets import (QTextEdit, QApplication, QMainWindow, QWidget, QAction, qApp, QMenu)
from Forms import *
from Views import *
from operations import *

'''

AUTOR : GUSTAVO BORGES FRANÇA


'''


'''
    Essa classe apenas faz a parte da interface visual
    ela inicializa varios componentes como menus e etc.
    e mostra na telas as opções para o usuário utilizando
    a biblioteca PyQt5
'''

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.initGUI()

	def initGUI(self):
		self.grammars = []
		self.statusBar()

		menubar = self.menuBar()
		new_menu = menubar.addMenu("&Novo")
		list_menu = menubar.addMenu("&Listar")
		operation_menu = menubar.addMenu("&Operações")

		self.set_newMenu(new_menu)
		self.set_listMenu(list_menu)
		self.set_operations_menu(operation_menu)
		self.setGeometry(300, 300, 560, 320)
		self.setWindowTitle("Aplicação para manipulação GLCs")
		self.show()

	def _create_grammar(self):
		grammar_form = GrammarForm()
		grammar_form.insert(self.grammars)
		self.setCentralWidget(grammar_form)

	def _view_grammars(self):
		grammar_view = View(self.grammars)
		self.setCentralWidget(grammar_view)

	def _into_proper(self):
		to_proper = ContextFreeOperations()
		to_proper.choose_to_transform(self.grammars)
		self.setCentralWidget(to_proper)

	def set_newMenu(self, new_menu):

		new_regularG = QAction("&Gramática Livre de Contexto", self)
		new_regularG.setStatusTip("Nova gramática livre de contexto")
		new_regularG.triggered.connect(self._create_grammar)
		exitAct = QAction('&Sair', self)
		exitAct.setShortcut('Ctrl+Q')
		exitAct.setStatusTip('fechar aplicação')
		exitAct.triggered.connect(qApp.quit)
		new_menu.addAction(new_regularG)
		new_menu.addAction(exitAct)

	def set_listMenu(self, list_menu):
		list_regularG = QAction("&Listar gramáticas", self)
		list_regularG.setStatusTip("Ver todas as gramáticas salvas")
		list_regularG.triggered.connect(self._view_grammars)
		list_menu.addAction(list_regularG)

	def set_operations_menu(self,operations_menu):
		into_proper = QAction("Transformar em GLC propria", self)
		into_proper.setStatusTip("Transformar GLC em propria")
		into_proper.triggered.connect(self._into_proper)
		operations_menu.addAction(into_proper)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    GUI = MainWindow()
    sys.exit(app.exec_())
