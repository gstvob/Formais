# -*- coding: utf-8 -*-

from Models import RegularGrammar, RegularExpression
import re
#Classe que vai conter as operações realizadas nas gramáticas e nas expressões
#E futuramente nos Autômatos
class GrammarOperations:

    def __init__(self, grammars):
        self.grammars = grammars

    def parse_grammar(self, grammar, name, result, update=False):
        result.clear()
        text = grammar.replace(" ", "")
        regex = re.compile(r'([A-Z][0-9]?->([a-z0-9][A-Z]?|\&)([|][a-z][A-Z]?)*(\n|\Z))*')
        match = regex.match(text)

        if (any(x.name == name for x in self.grammars) or name == "") and not update:
            result.textCursor().insertText("There is already a grammar with that name")
            return False

        try :
            if (match.group() == text):
                return self._validate_grammar(text,name,result)
            else :
                result.textCursor().insertText('fail')
                return False
        except AttributeError:
            result.textCursor().insertText('fail')
            return False

    def _validate_grammar(self, text, name, result):
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

        newRg = RegularGrammar(name, text)
        self.grammars.append(newRg)
        result.textCursor().insertText(text)
        return True

    def updateGrammar(self, editor):
        old_grammar_name = editor.choose_grammar.currentText()
        new_grammar_productions = editor.grammar_update.toPlainText()
        result = editor.result
        new_name = editor.grammar_name.text()
        if new_name != old_grammar_name:
            update = False
        else :
            update = True

        att = self.parse_grammar(new_grammar_productions, new_name, result, update)

        if att:
            old_grammar = next(x for x in editor.grammars if x.name == old_grammar_name)
            editor.grammars.remove(old_grammar)
            editor.update_combobox(new_name)

class ExpressionOperations:
    def __init__(self, expressions):
        self.expressions = expressions

    def parse_expression(self, expression, name, result, update):
        result.clear()
        text = expression.replace(" ", "")
        regex = re.compile(r'[(]?[a-z0-9]+([?+*]?([)][?+*]?)?)([|]?[(]?[a-z0-9]+([?+*]?([)][?+*]?[)]?)?))*')
        match = regex.match(text)

        if (any(x.name == name for x in self.expressions) or name == "") and not update:
            result.textCursor().insertText("There is already a expression with that name")
            return False

        open_count = text.count("(")
        close_count = text.count(")")

        if (open_count != close_count):
            result.textCursor().insertText("The paranthesis are not balanced")
            return False
        try :
            if (match.group() == text):
                if not update :
                    new_expr = RegularExpression(name, text)
                    self.expressions.append(new_expr)
                    result.textCursor().insertText(text)
                    return True
                else:
                    ##descobrir como pegar o regex atual/antigo antes do update
                    if name != regex.name and (any(x.name == name for x in self.expressions) or name==""):
                        result.textCursor().insertText("Error in the name of the expression")
                        return False
                    else:
                        regex.set_name(name)
                        regex.set_expression(expression)
                        result.textCursor().insertText(text)
                        return True
            else :
                result.textCursor().insertText('There is something wrong with your expression')
                return False
        except AttributeError:
            print("que")
            result.textCursor().insertText("There is something wrong with your expression")
            return False
