# -*- coding: utf-8 -*-

import sys
import os
import psutil
from PyQt5.QtWidgets import (QTextEdit, QApplication, QMainWindow, QWidget, QAction, qApp)
from Forms import GrammarForm
from Views import GrammarView
from Editors import GrammarEditor

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initGUI()

    def initGUI(self):
        self.grammars = []
        self.statusBar()
        menubar = self.menuBar()
        new_menu = menubar.addMenu("&New")
        list_menu = menubar.addMenu("&List")
        edit_menu = menubar.addMenu("&Edit")

        self.set_newMenu(new_menu)
        self.set_listMenu(list_menu)
        self.set_editMenu(edit_menu)
        self.setGeometry(300, 300, 640, 480)
        self.setWindowTitle('Aplicação para manipulação de caralhos')
        self.show()


    def create_grammar(self):
        grammar_form = GrammarForm(self.grammars)
        self.setCentralWidget(grammar_form)

    def view_grammars(self):
        grammar_view = GrammarView(self.grammars)
        self.setCentralWidget(grammar_view)

    def edit_grammars(self):
        grammar_edit = GrammarEditor(self.grammars)
        self.setCentralWidget(grammar_edit)

    def set_newMenu(self, new_menu):

        new_regularG = QAction("&Regular Grammar", self)
        new_regularG.setStatusTip("New regular grammar")
        new_regularG.triggered.connect(self.create_grammar)
        new_regularE = QAction("&Regular Expression", self)
        new_regularE.setStatusTip("New regular expression")

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
        list_regularG.triggered.connect(self.view_grammars)

        #operações para listar expressões regulares.
        list_menu.addAction(list_regularG)

    def set_editMenu(self, edit_menu):
        edit_regularG = QAction("&Edit regular grammar", self)
        edit_regularG.setStatusTip("Edit a regular grammar")
        edit_regularG.triggered.connect(self.edit_grammars)

        edit_menu.addAction(edit_regularG)

if __name__ == "__main__":

    process = psutil.Process(os.getpid())
    print(process)
    app = QApplication(sys.argv)
    GUI = MainWindow()
    sys.exit(app.exec_())
