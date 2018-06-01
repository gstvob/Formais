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

    def _language_union(self, op):
        if not op:
            #União definida pela gramática.
            return False
        else:
            union = AutomatonOperations()
            union.automata_for_binary_op(self.automata, 0)
            self.setCentralWidget(union)

    def _language_complement(self, op):
        if not op :
            #complemento definido pela gramática
            return False
        else:
            complement = AutomatonOperations()
            complement.automata_for_unary_op(self.automata, 3)
            self.setCentralWidget(complement)

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
        grammar_menu = QMenu("&Gramática", self)
        union_operation = QAction("União", self)
        union_operation.setStatusTip("União entre duas gramáticas regulares")
        union_operation.triggered.connect(self._grammar_union)
        concat_operation = QAction("Concatenar", self)
        concat_operation.setStatusTip("Concatenação entre duas gramáticas")
        concat_operation.triggered.connect(self._grammar_concat)
        kleene_star_op = QAction("Kleene Star", self)
        kleene_star_op.setStatusTip("Operação estrela em uma gramática regular")
        kleene_star_op.triggered.connect(self._kleene_star)
        grammar_menu.addAction(union_operation)
        grammar_menu.addAction(concat_operation)
        grammar_menu.addAction(kleene_star_op)

        language_menu = QMenu("&Linguagem Regular", self)
        language_union = QMenu("&União", self)
        language_complement = QMenu("&Complemento", self)
        language_intersection = QMenu("&Intersecção", self)
        language_diff = QMenu("&Diferença", self)
        language_reverse = QMenu("&Reverso", self)
        language_menu.addMenu(language_union)
        language_menu.addMenu(language_complement)
        language_menu.addMenu(language_intersection)
        language_menu.addMenu(language_diff)
        language_menu.addMenu(language_reverse)

        union_lr_defined_grammar = QAction("Por gramática",self)
        union_lr_by_af = QAction("Por autômato", self)
        union_lr_defined_grammar.triggered.connect(lambda d: self._language_union(0))
        union_lr_by_af.triggered.connect(lambda d: self._language_union(1))

        complement_lr_defined_grammar = QAction("Por gramática", self)
        complement_lr_by_af = QAction("Por autômato", self)
        complement_lr_defined_grammar.triggered.connect(lambda d: self._language_complement(0))
        complement_lr_by_af.triggered.connect(lambda d: self._language_complement(1))

        intersection_lr_defined_grammar = QAction("Por gramática", self)
        intersection_lr_by_af = QAction("Por autômato", self)

        diff_lr_defined_grammar = QAction("Por gramática", self)
        diff_lr_by_af = QAction("Por autômato", self)

        reverse_lr_defined_grammar = QAction("Por gramática",self)
        reverse_lr_by_af = QAction("Por autômato",self)

        language_union.addAction(union_lr_defined_grammar)
        language_union.addAction(union_lr_by_af)
        language_complement.addAction(complement_lr_defined_grammar)
        language_complement.addAction(complement_lr_by_af)
        language_intersection.addAction(intersection_lr_defined_grammar)
        language_intersection.addAction(intersection_lr_by_af)
        language_diff.addAction(diff_lr_defined_grammar)
        language_diff.addAction(diff_lr_by_af)
        language_reverse.addAction(reverse_lr_defined_grammar)
        language_reverse.addAction(reverse_lr_by_af)

        check_input = QAction("Reconhecer entrada", self)
        check_input.setStatusTip("Checa se uma entrada é aceita pelo autômato")
        check_input.triggered.connect(self._check_input)
        enumerate_sentences = QAction("Enumerar Sentenças", self)
        enumerate_sentences.setStatusTip("Enumera as sentenças de um dado tamanho n")
        enumerate_sentences.triggered.connect(self._enumerate_sentences)

        operations_menu.addAction(check_input)
        operations_menu.addAction(enumerate_sentences)
        operations_menu.addMenu(grammar_menu)
        operations_menu.addMenu(language_menu)
if __name__ == "__main__":

    app = QApplication(sys.argv)
    GUI = MainWindow()
    sys.exit(app.exec_())
