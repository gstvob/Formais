# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QTextEdit, QApplication, QMainWindow, QWidget, QAction, qApp, QMenu)
from Forms import *
from Views import *
from Editors import *

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initGUI()

    def initGUI(self):
        self.grammars = []
        self.expressions = []
        self.automata = []
        self.statusBar()

        menubar = self.menuBar()
        new_menu = menubar.addMenu("&New")
        list_menu = menubar.addMenu("&List")
        edit_menu = menubar.addMenu("&Edit")
        conversion_menu = menubar.addMenu("&Convert")
        operation_menu = menubar.addMenu("&Operations")

        self.set_newMenu(new_menu)
        self.set_listMenu(list_menu)
        self.set_editMenu(edit_menu)
        self.set_conversion_menu(conversion_menu)
        self.set_operations_menu(operation_menu)
        self.setGeometry(300, 300, 560, 320)
        self.setWindowTitle('Aplicação para manipulação de ER, AF, E GR')
        self.show()

    def _create_grammar(self):
        grammar_form = GrammarForm(self.grammars)
        self.setCentralWidget(grammar_form)

    def _create_expression(self):
        expression_form = ExpressionForm(self.expressions)
        self.setCentralWidget(expression_form)

    def _view_grammars(self):
        grammar_view = GrammarView(self.grammars)
        self.setCentralWidget(grammar_view)

    def _view_expressions(self):
        expression_view = ExpressionView(self.expressions)
        self.setCentralWidget(expression_view)

    def _view_automata(self):
        automata_view = AutomatonView(self.automata)
        self.setCentralWidget(automata_view)

    def _edit_grammars(self):
        grammar_edit = GrammarEditor(self.grammars)
        self.setCentralWidget(grammar_edit)

    def _edit_expressions(self):
        expression_edit = ExpressionEditor(self.expressions)
        self.setCentralWidget(expression_edit)

    def _convert_grammar_automaton(self):
        conversion = ConversionEditor(1, self.grammars, self.automata)
        self.setCentralWidget(conversion)

    def _convert_automaton_grammar(self):
        conversion = ConversionEditor(2, self.grammars, self.automata)
        self.setCentralWidget(conversion)

    def _grammar_union(self):
        union = ExtraOperations(self.grammars)
        union.grammar_union()
        self.setCentralWidget(union)

    def set_newMenu(self, new_menu):

        new_regularG = QAction("&Regular Grammar", self)
        new_regularG.setStatusTip("New regular grammar")
        new_regularG.triggered.connect(self._create_grammar)
        new_regularE = QAction("&Regular Expression", self)
        new_regularE.setStatusTip("New regular expression")
        new_regularE.triggered.connect(self._create_expression)

        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        new_menu.addAction(new_regularG)
        new_menu.addAction(new_regularE)
        new_menu.addAction(exitAct)

    def set_listMenu(self, list_menu):
        list_regularG = QAction("&List regular grammars", self)
        list_regularG.setStatusTip("View all saved regular grammars")
        list_regularG.triggered.connect(self._view_grammars)

        list_regularE = QAction("&List regular expressions", self)
        list_regularE.setStatusTip("View all saved regular expressions")
        list_regularE.triggered.connect(self._view_expressions)

        list_automata = QAction("&List Automata", self)
        list_automata.setStatusTip("View all saved automata")
        list_automata.triggered.connect(self._view_automata)
        #operações para listar expressões regulares.
        list_menu.addAction(list_regularG)
        list_menu.addAction(list_regularE)
        list_menu.addAction(list_automata)
        
    def set_editMenu(self, edit_menu):
        edit_regularG = QAction("&Edit regular grammar", self)
        edit_regularG.setStatusTip("Edit a regular grammar")
        edit_regularG.triggered.connect(self._edit_grammars)

        edit_regularE = QAction("&Edit regular expression", self)
        edit_regularE.setStatusTip("Edit a regular expression")
        edit_regularE.triggered.connect(self._edit_expressions)

        edit_menu.addAction(edit_regularG)
        edit_menu.addAction(edit_regularE)

    def set_conversion_menu(self, conversion_menu):
        grammar_automaton = QAction("&Convert grammar to automaton", self)
        grammar_automaton.setStatusTip("Convert a regular grammar to automaton")
        grammar_automaton.triggered.connect(self._convert_grammar_automaton)

        automaton_grammar = QAction("&Convert automaton to grammar", self)
        automaton_grammar.setStatusTip("Convert a finite automaton to a regular grammar")
        automaton_grammar.triggered.connect(self._convert_automaton_grammar)

        conversion_menu.addAction(grammar_automaton)
        conversion_menu.addAction(automaton_grammar)

    def set_operations_menu(self, operations_menu):
        grammar_menu = QMenu("&Grammar", self)
        union_operation = QAction("Union", self)
        union_operation.setStatusTip("Union between two grammars")
        union_operation.triggered.connect(self._grammar_union)
        grammar_menu.addAction(union_operation)

        operations_menu.addMenu(grammar_menu)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    GUI = MainWindow()
    sys.exit(app.exec_())
