

class RegularGrammar:

    def __init__(self, name, P):
        self.name = name
        self.p = P
        self._definition(P)

    def set_name(self, name):
        self.name = name
    def set_productions(self, productions):
        self.p = productions
        self._definition(productions)

    def _definition(self, productions):
        self.s = productions[0]
        self.vn = []
        self.vt = []

        for i in productions :
            if i.isupper() and i not in self.vn:
                self.vn.append(i)
            elif (i.islower() or i.isdigit()) and i not in self.vt:
                self.vt.append(i)

class RegularExpression:

    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def set_name(self, name):
        self.name = name

    def set_expression(self, exp):
        self.expression = exp

class Automaton:

    def __init__(self, name, states,alphabet):
        self.name = name
        self.states = states
        self.alphabet = alphabet
        self.q0 = states[0]
        self._set_finals()
        self.dfa_or_ndfa()


    def _set_finals(self):
        self.f = [x for x in self.states if x.acceptance == True]

    def dfa_or_ndfa(self):
        self.non_deterministic = False
        for state in self.states:
            for trst in state.transitions:
                if any(x for x in state.transitions if trst.target != x.target and
                                                    x.symbol == trst.symbol and
                                                    trst != x):
                    self.non_deterministic = True



class State:
    #se em um estado eu tenho duas transições com o mesmo simbolo para estados
    #diferentes eu sei que se trata de um automato não deterministico

    def __init__(self, label, acceptance=False):
        self.acceptance = acceptance
        self.label = label
        self.transitions = []
    def __repr__(self):
        return self.label
    def set_acceptance(self, status):
        self.acceptance = status
    def change_label(self, nL):
        self.label = nL
    def insert_transitions(self, transitions):
        self.transitions=transitions
    def add_transition(self, transition):
        self.transitions.append(transition)
    def replace_transition(self, new_t, old_t):
        self.transitions[self.transitions.index(old_t)] = new_t  


class Transition:
    def __init__(self, target, symbol):
        self.symbol = symbol
        self.target = target
