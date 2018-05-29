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
        grammar_form = GrammarForm()
        grammar_form.insert(self.grammars)
        self.setCentralWidget(grammar_form)

    def _create_expression(self):
        expression_form = ExpressionForm()
        expression_form.insert(self.expressions)
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
        grammar_edit = GrammarForm()
        grammar_edit.update(self.grammars)
        self.setCentralWidget(grammar_edit)

    def _edit_expressions(self):
        expression_edit = ExpressionForm()
        expression_edit.update(self.expressions)
        self.setCentralWidget(expression_edit)

    def _convert_grammar_automaton(self):
        conversion = GrammarOperations()
        conversion.choose_for_conversion(self.grammars, self.automata)
        self.setCentralWidget(conversion)

    def _convert_automaton_grammar(self):
        conversion = AutomatonOperations()
        conversion.choose_for_conversion(self.automata, self.grammars)
        self.setCentralWidget(conversion)

    def _grammar_union(self):
        union = GrammarOperations()
        union.choose_for_op(self.grammars, 0)
        self.setCentralWidget(union)
    
    def _grammar_concat(self):
        concat = GrammarOperations()
        concat.choose_for_op(self.grammars, 1)
        self.setCentralWidget(concat)

    def _kleene_star(self):
        kStar = GrammarOperations()
        kStar.choose_for_op(self.grammars, 2)
        self.setCentralWidget(kStar)

    def _check_input(self):
        check_input = AutomatonOperations()
        check_input.automaton_test_input(self.automata)
        self.setCentralWidget(check_input)

    def _enumerate_sentences(self):
        enumerate_sentences = AutomatonOperations()
        enumerate_sentences.enumerate_nsize_inputs(self.automata)
        self.setCentralWidget(enumerate_sentences)

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
        concat_operation = QAction("Concat", self)
        concat_operation.setStatusTip("Concatenation between two grammars")
        concat_operation.triggered.connect(self._grammar_concat)
        kleene_star_op = QAction("Kleene Star", self)
        kleene_star_op.setStatusTip("The kleene star of a grammar")
        kleene_star_op.triggered.connect(self._kleene_star)
        grammar_menu.addAction(union_operation)
        grammar_menu.addAction(concat_operation)
        grammar_menu.addAction(kleene_star_op)

        check_input = QAction("Recognize Input", self)
        check_input.setStatusTip("Check if automaton recognizes given input")
        check_input.triggered.connect(self._check_input)
        enumerate_sentences = QAction("Enumerate Sentences", self)
        enumerate_sentences.setStatusTip("Enumerate the sentences of given size n")
        enumerate_sentences.triggered.connect(self._enumerate_sentences)

        operations_menu.addAction(check_input)
        operations_menu.addAction(enumerate_sentences)
        operations_menu.addMenu(grammar_menu)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    GUI = MainWindow()
    sys.exit(app.exec_())
