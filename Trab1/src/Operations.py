# -*- coding: utf-8 -*-

from Models import *
import re
import random
import string
#Classe que contém as operações realizadas em gramáticas.
#O método parse_grammar serve para verificar se dadas as produções entradas
#a gramática é uma gramática válida, e o método validate grammar verifica se
#a existencia de epsilon na gramática ainda à mantém regular.
#o método updateGrammar é utilizado para atualizar uma gramática.
#O método grammar_automaton utiliza o algoritmo visto em aula para passar
#uma gramática regular para um autômato finito.

class AutomatonOperations:
    
    def __init__(self, automata):
        self.automata = automata

    def convert_to_grammar(self, automaton, editor):
        vn = [x.label for x in automaton.states]
        vt = automaton.alphabet
        productions = ""
        if automaton.states[0].acceptance:
            productions += vn[0]+"->&|"
        else:
            productions += vn[0]+"->"

        empty_labels = [x.label for x in automaton.states if not any(y for y in x.transitions if y.target.label != "-")]
        for i in vn:
            transitions = next(x.transitions for x in automaton.states if x.label == i)
            non_empty = [y for y in transitions if y.target.label != "-"]
            if non_empty:
                if i != vn[0]:
                    productions += i+"->"
                for j in transitions:
                    if j.target.label != "-":
                        if j.target.label not in empty_labels:
                            productions += j.symbol+j.target.label+"|"
                        if j.target.acceptance:
                            productions += j.symbol+"|"
                productions = productions[:-1] + "\n"

        editor.print_productions(productions)

    def ndfa_to_dfa(self, automaton, editor):
        NDstates = automaton.states
        Dstates = []
        Dstates.append(State(NDstates[0].label, NDstates[0].acceptance))
        for j in automaton.alphabet:
            tx = [x for x in NDstates[0].transitions if x.symbol == j]
            label = "["
            acceptance = False
            for k in tx:
                if k.target.acceptance:
                    acceptance = True
                if k.target.label != "-":
                    label += k.target.label+","

            if label == "[":
                label = "-"
                new_state = State(label, acceptance)
            else :
                label = label[1:-1]
                label = "".join(sorted(label))
                label = "["+label+"]"
                new_state = State(label, acceptance)
                Dstates.append(new_state)
            Dstates[0].add_transition(Transition(new_state, j))

        for d in Dstates:
            state = d.label
            if d != Dstates[0]:
                state = state[1:-1].split(",")
                for i in automaton.alphabet:
                    tx = []
                    label = "["
                    acceptance = False
                    for k in state:
                        nd = next(x for x in NDstates if x.label == k)
                        tx += [x for x in nd.transitions if x.symbol == i]
                    for l in tx:
                        if l.target.acceptance:
                            acceptance = True
                        if l.target.label != "-":
                            label += l.target.label+","
                    if label == "[":
                        label = "-"
                        new_state = State(label, acceptance)
                        d.add_transition(Transition(new_state, i))
                    else :
                        label = label[1:-1]
                        label = "".join(sorted(label))
                        label = "["+label+"]" 
                        new_state = State(label, acceptance)
                        all_labels = [x.label for x in Dstates]
                        if label not in all_labels:
                            Dstates.append(new_state)
                        d.add_transition(Transition(new_state, i))
        editor.build_table(Dstates, automaton.alphabet)

class GrammarOperations:

    def __init__(self, grammars):
        self.grammars = grammars

    def parse_grammar(self, grammar, name, result, update=False, change_name=True):
        result.clear()
        text = grammar.replace(" ", "")
        regex = re.compile(r'([A-Z][0-9]?->([a-z0-9][A-Z]?|\&)([|][a-z0-9][A-Z]?)*(\n|\Z))*')
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

    def convert_to_automaton(self, grammar, editor):
        states = [State(x) for x in grammar.vn]
        alphabet = grammar.vt
        extra = State("$", True)
        states.append(extra)
        productions = grammar.p.split("\n")
        if "&" in productions[0]:
            states[0].set_acceptance(True)
        for state in states:
            rules = []
            if state.label in [x[0] for x in productions]:
                producao = next(x for x in productions if state.label == x[0])
                rules = producao.split(producao[0]+"->")[1].split("|")
            trsts = []
            for i in rules:
                if i != "&":
                    if len(i) > 1:
                        target = next(x for x in states if x.label == i[1])
                        trsts.append(Transition(target, i[0]))
                    else:
                        target = next(x for x in states if x.label == "$")
                        trsts.append(Transition(target, i[0]))
            for i in alphabet:
                if not any(i in str for str in rules):
                    target = State("-")
                    trsts.append(Transition(target, i))
            state.insert_transitions(trsts)
        editor.build_table(states, alphabet)

    def grammar_union(self, grammar1, grammar2, editor):
        p1 = grammar1.p
        p2 = grammar2.p
        union = ""
        epsilon = False
        if "&" in p1:
            p1 = p1.replace("&|", "")
            epsilon = True
        if "&" in p2:
            p2 = p2.replace("&|", "")
            epsilon = True

        if set(grammar1.vn) <= set(grammar2.vn) or set(grammar1.vn) >= set(grammar2.vn):
            editor.show_union("Error while making this union") 
        else:      
            prods1 = p1.split("\n")
            prods2 = p2.split("\n")
            if epsilon:
                union = "Ω->&|"
            else:
                union = "Ω->"
            union += prods1[0].split("->")[1]+"|"+prods2[0].split("->")[1]+"\n"
            for i in prods1:
                union += i+"\n"
            for i in prods2:
                union += i+"\n"
            editor.show_union(union)
            print("Ω".isupper())

    def grammar_concat(self, grammar1, grammar2, editor):
        p1 = grammar1.p
        p2 = grammar2.p

        concat = ""
        epsilon = False
        if "&" in p1:
            p1 = p1.replace("&|", "")
            epsilon = True
        if "&" in p2:
            p2 = p2.replace("&|", "")
            epsilon = True

        if set(grammar1.vn) <= set(grammar2.vn) or set(grammar1.vn) >= set(grammar2.vn):
            print("error concat")
        else:
            

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
