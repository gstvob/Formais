

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

    def __init__(self, name, k, states, transitions, alphabet, f):
        self.name = name
        self.k = k
        self.states = states
        self.transitions = transitions
        self.alphabet = alphabet
        self.q0 = states[0]
        self.f = f

class State:
    #se em um estado eu tenho duas transições com o mesmo simbolo para estados
    #diferentes eu sei que se trata de um automato não deterministico

    def __init__(self, label, acceptance=False):
        self.acceptance = acceptance
        self.label = label
        self.transitions = []

    def insert_transition(self, transition):
        self.transitions.append(transition)

class Transition:
    def __init__(self, target, symbol):
        self.symbol = symbol
        self.target = target
