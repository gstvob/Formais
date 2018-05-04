

class RegularGrammar:

    def __init__(self, name, P):
        self.name = name
        self.p = P
        self.Definition(P)

    def Definition(self, productions):
        self.s = productions[0]
        self.vn = []
        self.vt = []

        for i in productions :
            if i.isupper() and i not in self.vn:
                self.vn.append(i)
            elif (i.islower() or i.isdigit()) and i not in self.vt:
                self.vt.append(i)
