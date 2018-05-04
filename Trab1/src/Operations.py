# -*- coding: utf-8 -*-

from Models import RegularGrammar

#Classe que vai conter as operações realizadas nas gramáticas e nas expressões
#E futuramente nos Autômatos
class Operations:

    def __init__(self, grammars):
        self.grammars = grammars

    def parse_grammar(self, grammar, name, result):
        error = False
        finishable = False
        result.clear()
        text = grammar.replace(" ", "")
        for i in range(len(text)):
            try :
                if i == 0:
                    if not(text[i].isupper()) or text[i+1] != "-":
                        error = True
                        break
                elif text[i] == "-":
                    finishable = False
                    if text[i+1] != ">":
                        error = True
                        break
                elif text[i] == ">":
                    finishable = False
                    if text[i+1] != "&" and not(text[i+1].islower()) and not(text[i+1].isdigit()):
                        error = True
                        break
                elif text[i] == "\n":
                    finishable = True
                    if not(text[i+1].isupper()):
                        finishable = False
                        error = True
                        break
                elif text[i] == "|":
                    finishable = False
                    if not(text[i+1].islower()) and not(text[i+1].isdigit()) and text[i+1] != "&":
                        error = True
                        break
                elif text[i].islower() or text[i].isdigit():
                    finishable = True
                    if text[i+1] != "|" and not(text[i+1].isupper()) and text[i+1] != "\n":
                        finishable = False
                        error = True
                        break
                elif text[i].isupper():
                    finishable = True
                    if text[i-1] == "\n":
                        finishable = False
                        if text[i+1] != "-":
                            error = True
                            break
                    elif text[i+1] != "\n" and text[i+1] != "|":
                        finishable = False
                        error = True
                        break
                elif text[i] == "&":
                    finishable = True
                    if text[i+1] != "|" and text[i+1] != "\n":
                        finishable = False
                        error = True
                        break
            except IndexError:
                if finishable :
                    return self.validate_grammar(text,name,result)
                else:
                    result.textCursor().insertText('fail')
                    return False

        if finishable :
            return self.validate_grammar(text,name,result)
        elif error :
            result.textCursor().insertText('fail')
            return False

    def validate_grammar(self, text, name, result):
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
        att = self.parse_grammar(new_grammar_productions, new_name, result)

        if att:
            old_grammar = next(x for x in editor.grammars if x.name == old_grammar_name)
            editor.grammars.remove(old_grammar)
        editor.update_combobox(new_name)
