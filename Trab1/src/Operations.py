# -*- coding: utf-8 -*-

from Models import RegularGrammar, RegularExpression, State, Automaton, Transition
import re

#Classe que contém as operações realizadas em gramáticas.
#O método parse_grammar serve para verificar se dadas as produções entradas
#a gramática é uma gramática válida, e o método validate grammar verifica se
#a existencia de epsilon na gramática ainda à mantém regular.
#o método updateGrammar é utilizado para atualizar uma gramática.
#O método grammar_automaton utiliza o algoritmo visto em aula para passar
#uma gramática regular para um autômato finito.

class GrammarOperations:

    def __init__(self, grammars):
        self.grammars = grammars

    def parse_grammar(self, grammar, name, result, update=False, change_name=True):
        result.clear()
        text = grammar.replace(" ", "")
        regex = re.compile(r'([A-Z][0-9]?->([a-z0-9][A-Z]?|\&)([|][a-z][A-Z]?)*(\n|\Z))*')
        match = regex.match(text)

        if (any(x.name == name for x in self.grammars) or name == "") and change_name:
            result.textCursor().insertText("There is already a grammar with that name/Grammar name cannot be empty")
            return False

        try :
            if (match.group() == text):
                return self._validate_grammar(text,name,result,update)
            else :
                result.textCursor().insertText('There is something wrong with your grammar')
                return False
        except AttributeError:
            result.textCursor().insertText('There is something wrong with your grammar')
            return False

    def _validate_grammar(self, text, name, result, update):
        if "&" in text:
            first_enter = text.find('\n')
            last_epsilon= text.rfind('&')

            if last_epsilon > first_enter and first_enter != -1:
                text = "Gramática não regular"
                result.textCursor().insertText(text)
                return False

            for i in range(len(text)):
                if text[i] == text[0] and i != 0:
                    text = "Gramática não regular"
                    result.textCursor().insertText(text)
                    return False

        if not update:
            newRg = RegularGrammar(name, text)
            self.grammars.append(newRg)
        result.textCursor().insertText(text)
        return True

    def updateGrammar(self, editor):
        old_name = editor.choose_grammar.currentText()
        new_productions = editor.grammar_update.toPlainText()
        result = editor.result
        new_name = editor.grammar_name.text()
        if new_name != old_name and new_name != "":
            change_name = True
        else :
            change_name = False

        att = self.parse_grammar(new_productions, new_name, result, True, change_name)

        if att:
            old_grammar = next(x for x in self.grammars if x.name == old_name)
            old_grammar.set_name(editor.grammar_name.text())
            old_grammar.set_productions(editor.result.toPlainText())
            editor.update_combobox()

    def covert_to_automaton(self, grammar):
        states = [for x in grammar.vn: State(x)]
        alphabet = grammar.vt
        q0 = states[0]
        extra = State("$", True)
        states.append(extra)
        f = all(for x in states if x.acceptance == True)
        print(states)
        print(alphabet)

class ExpressionOperations:
    def __init__(self, expressions):
        self.expressions = expressions

    def parse_expression(self, expression, name, result, update=False, change_name=True):
        result.clear()
        text = expression.replace(" ", "")
        regex = re.compile(r'[(]?[a-z0-9]+([?+*]?([)][?+*]?)?)([|]?[(]?[a-z0-9]+([?+*]?([)][?+*]?[)]?)?))*')
        match = regex.match(text)

        if (any(x.name == name for x in self.expressions) or name == "") and change_name:
            result.textCursor().insertText("There is already a expression with that name/expression name cannot be empty")
            return False

        open_count = text.count("(")
        close_count = text.count(")")

        if (open_count != close_count):
            result.textCursor().insertText("The paranthesis are not balanced")
            return False
        try :
            if (match.group() == text):
                if not update:
                    new_expr = RegularExpression(name, text)
                    self.expressions.append(new_expr)
                result.textCursor().insertText(text)
                return True
            else:
                result.textCursor().insertText("There is something wrong with your expression")
                return False

        except AttributeError:
            result.textCursor().insertText("There is something wrong with your expression")
            return False

    def updateExpression(self, editor):
        oldname = editor.choose_expression.currentText()
        new_name = editor.expression_name.text()
        if new_name != oldname and new_name != "":
            change_name = True
        else:
            change_name = False
        regex = editor.expression_new.text()
        att = self.parse_expression(regex, new_name, editor.result, True, change_name)
        if att :
            old_expression = next(x for x in self.expressions if x.name == oldname)
            old_expression.set_name(editor.expression_name.text())
            old_expression.set_expression(editor.result.toPlainText())
            editor.update_combobox()
