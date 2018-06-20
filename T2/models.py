import re
class ContextFreeGrammar:
	
	def __init__(self, productions):
		self.productions = productions
		self.vn = set()
		self.vt = set()
		self.S = None
		self.decompose_and_formalize()
	def decompose_and_formalize(self):
		symbols = []
		prods = self.productions.split("\n")
		for p in prods:
			symbol = p.split("->")[0]
			if symbol not in [ss.label for ss in symbols]:
				print(symbol)
				symbols.append(Symbol(symbol))

		prod = self.productions

		for S in symbols:
			prod=prod.replace(S.label, "")

		prod = prod.replace("\n", ",")
		prod = prod.replace("->","")
		prod = prod.replace("|", ",")
		prod = prod.replace(" ", "")
		prod = prod.split(",")
		for p in prod:
			if p not in [ss.label for ss in symbols]:
				symbols.append(Symbol(p))
		for s in symbols:
			if not s.label.isupper() and len(s.label) <2:
				self.vt.add(s)
			else:
				self.vn.add(s)

		self.S = symbols[0]
		self.set_firsts(self.S)


	def set_firsts(self, X, Prev=None):
		p = self.productions
		vn = self.vn
		vt = self.vt

		#passo1
		if X in vt:
			X.first.add(X)
		#passo2
		else:
			prods = p.split("\n")
			that_prod = next(p for p in prods if (p.split("->")[0]) == X.label)
			that_prod = that_prod.split("->")[1]
			for x in range(len(that_prod)):
				if that_prod[x] in [y.label for y in vt]: 
					if x-1 == -1 or that_prod[(x-1)] == "|":
						symbol = next(s for s in vt if s.label == that_prod[x])
						X.first.add(symbol)

			splitemup = that_prod.split("|")

			#passo3
			for x in splitemup:
				y = x.split(" ")
				previousHadEpsilon=True
				addedTerminal = False
				for k in range(len(y)):
					if y[k] in [z.label for z in vn]:
						yn = next(s for s in vn if s.label == y[k])
						if previousHadEpsilon:
							if y[k] != X.label:
								self.set_firsts(yn, X)
								X.first.update(yn.first)
							if "&" in [l.label for l in yn.first]:
								epsilon = next(s for s in yn.first if s.label == "&")
								if "&" not in that_prod:
									X.first.remove(epsilon)
								previousHadEpsilon=True
							else:
								previousHadEpsilon=False
								break
					elif y[k] in [s.label for s in vt]:
						if previousHadEpsilon: 
							X.first.add(next(s for s in vt if s.label == y[k]))
							addedTerminal=True
							break
				if not addedTerminal and previousHadEpsilon:
					X.first.add(next(s for s in vt if s.label == "&"))

			#DEAL WITH DEPENDENCES

	def set_follows(self):
		p = self.productions
		vn = self.vn
		vt = self.vt
		#passo 1
		self.S.follow.add(Symbol("$"))

		#passo2
		prods = p.split("\n")
		for P in prods:
			A = P.split("->")[1]
			A = A.split("|")
			for a in A:
				x = a.split(" ")
				for i in range(len(x)):
					if x[i] not in [k.label for k in vn]:
						continue
					else:
						B = next(symbol for symbol in vn if x[i] == symbol.label)
						if i+1 >= len(x):
							break 
						
						if x[i+1] in [k.label for k in vn]:
							beta = next(symbol for symbol in vn if x[i+1] == symbol.label)
							print(str(beta))
							print(str(beta.first))
							B.follow.update(beta.first)
							if epsilon not in beta.first:
								break
							epsilon = next(symbol for symbol in vt if symbol.label == "&")
							B.follow.remove(epsilon)
						else:
							B.follow.add(next(symbol for symbol in vt if x[i+1] == symbol.label))
							break

		#passo3
		repeat = True
		while repeat:
			repeat = False
			previous = []
			for P in prods:
				A_label = P.split("->")[0]
				C = P.split("->")[1]
				C = C.split("|")
				for c in C:
					x = c.split(" ")
					for i in range(len(x)):
						if x[i] not in [k.label for k in vn]:
							continue
						else:
							B = next(symbol for symbol in vn if x[i] == symbol.label)
							bN = i+1
							while True:
								if bN >= len(x):
									A = next(y for y in vn if y.label == A_label)
									B.follow.update(A.follow)
									if B.label in [prev for prev in previous] and B.follow-A.follow != B.follow:
										repeat = True
									previous.append(A_label)
									break
								else:
									beta = next((symbol for symbol in vn if x[bN] == symbol.label), None)
									if "&" in [k.label for k in vt if k.label == "&"]:
										bN+=1
									else:
										break
									break

	def set_first_nt(self, X):
		p = self.productions
		vn = self.vn
		vt = self.vt

		if X not in vt:

			prods = p.split("\n")
			that_prod = next(p for p in prods if (p.split("->")[0]) == X.label)
			that_prod = that_prod.split("->")[1]
			splitemup = that_prod.split("|")
			for x in splitemup:
				y = x.split(" ")
				previousHadEpsilon=True
				addedTerminal = False
				for k in range(len(y)):
					if y[k] in [z.label for z in vn]:
						yn = next(symbol for symbol in vn if symbol.label == y[k])
						if previousHadEpsilon:
							X.first_nt.add(yn)
							if [symbol for symbol in yn.first if symbol.label == "&"]:
								previousHadEpsilon = True
							else:
								previousHadEpsilon = False
					else:
						break

	def remove_useless_symbols(self):
		nf = self.remove_dead_symbols()
		self.vn = self.vn&nf
		#redefenir prods

		prods = self.productions.split("\n")
		for p in prods:
			nT = p.split("->")[0]
			if nT not in [l.label for l in vn]:
				prods.remove(p)

		self.productions = "\n".join(prods) 

		for p in self.productions:
				A_label = p.split("->")[0]
				rhs = p.split("->")[1]
				for s in range(len(rhs)):
					if rhs[s] not in [l.label for l in vn]:
						self.productions.replace(rhs[s], "")
		# remove_unreachable_symbols()
	
	def remove_dead_symbols(self):
		Nf = set()
		Nprev = set()
		while True:
			Ni = set()
			for p in self.productions:
				A_label = p.split("->")[0]
				rhs = p.split("->")[1]
				for s in range(len(rhs)):
					if rhs[s] in [l.label for l in vt]:
						x = s
						alive = False
						while True:
							if x+1>= len(rhs) or rhs[x+1] == "|":
								alive = True
								break
							elif rhs[x+1] in [l.label for l in vn]:
								B = next(symbol for symbol in vn if rhs[x+1] == symbol.label)
								if B not in Nprev:
									alive = False
									break
								else:
									x+=1
						if alive:
							A = next(symbol for symbol in vn if symbol.label == A_label)
							Ni.add(Ni)
			Ni = Nprev.union(Ni)
			if Ni == Nprev:
				break
			else:
				Nprev = Ni
		Nf = Nprev
		return Nf

	# def remove_unreachable_symbols(self):

	def print_stuff(self):
		print(str(self.vn))
		print(str(self.vt))
		print("Inicial: "+str(self.S))
		self.set_firsts(self.S)
		self.S.print_firsts()

class Symbol:
	def __init__(self, label):
		self.label = label
		self.first = set()
		self.follow = set()
		self.first_nt = set()
		self.dependences = []

	def __repr__(self):
		return self.label

	def add_dependence(self, symbol):
		self.dependences.append(symbol)

	def print_firsts(self):
		print(str(self.first))

grammar = "S1->S1 a|b B|c B|A d\nA->B B A w|h|&\nB->f|&"
grammar2 = "S1->B a|b B|c B|A d\nA->B B A w|h|&\nB->S1 f|&"
grammar3 = "S->b B|A a\nA->b S|&\nB->a"

cfg = ContextFreeGrammar(grammar3)
for i in cfg.vn:
	cfg.set_first_nt(i)
cfg.set_follows()
for i in cfg.vn:
	print(str(i)+" first")
	cfg.set_firsts(i)
	print(i.first)
for i in cfg.vn:
	print(str(i)+" follow")
	print(i.follow)
for i in cfg.vn:
	print(str(i)+" first_nt")
	print(i.first_nt)
'''
							if yn == Prev and yn != X:
								print(Prev)
								print(X)
								X.add_dependence(Prev)
								Prev.add_dependence(X)
							else:	
'''