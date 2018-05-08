

class RegularGrammar:

    def __init__(self, name, P):
        self.name = name
        self.p = P
        self._definition(P)

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
