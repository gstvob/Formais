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
			if s.label.islower() or s.label.isdigit() or s.label == "&":
				self.vt.add(s)
			else:
				self.vn.add(s)

		self.S = symbols[0]

	def set_firsts(self, X, Prev=None):
		p = cfg.productions
		vn = cfg.vn
		vt = cfg.vt

		if X in vt:
			X.first.add(X)
		else:
			prods = p.split("\n")
			that_prod = next(p for p in prods if (p.split("->")[0]) == X.label)
			that_prod = that_prod.split("->")[1]
			for x in range(len(that_prod)):
				if that_prod[x] in [y.label for y in vt]: 
					if x-1 == -1 or that_prod[(x-1)] == "|":
						symbol = next(s for s in vt if s.label == that_prod[x])
						X.first.add(symbol)


			#aqui o first do A é {&,h}
			# se X->S1 S2 S3
			# first(S1) ta em X
			# se epsilon ta em S1, first(S2) ta em X e assim vai

			splitemup = that_prod.split("|")

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

					elif y[k] in [s.label for s in vt]:
						if previousHadEpsilon: 
							X.first.add(next(s for s in vt if s.label == y[k]))
							addedTerminal=True
				if not addedTerminal:
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
						epsilon = next(symbol for symbol in vt if symbol.label == "&")
						if i+1 >= len(x):
							break 
						
						if x[i+1] in [k.label for k in vn]:
							beta = next(symbol for symbol in vn if x[i+1] == symbol.label)
							print(str(beta))
							print(str(beta.first))
							B.follow.update(beta.first)
							if epsilon not in beta.first:
								break
							B.follow.remove(epsilon)
						else:
							B.follow.add(next(symbol for symbol in vt if x[i+1] == symbol.label))
							break

		#passo3
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
							if bN == len(x):
								A = next(y for y in vn if y.label == A_label)
								B.follow.update(A.follow)
								break
							else:
								beta = next((symbol for symbol in vn if x[bN] == symbol.label), None)
								if beta == None:
									break
								elif "&" in [k.label for k in vt if k.label == "&"]:
									bN+=1
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
		self.dependences = []

	def __repr__(self):
		return self.label

	def add_dependence(self, symbol):
		self.dependences.append(symbol)

	def print_firsts(self):
		print(str(self.first))

grammar = "S1->S1 a|b B|c B|A d\nA->B B A w|h|&\nB->f|&"
grammar2 = "S1->B a|b B|c B|A d\nA->B B A w|h|&\nB->S1 f|&"

cfg = ContextFreeGrammar(grammar)
cfg.print_stuff()
cfg.set_follows()
for i in cfg.vn:
	print(str(i)+" follow")
	print(i.follow)

'''
							if yn == Prev and yn != X:
								print(Prev)
								print(X)
								X.add_dependence(Prev)
								Prev.add_dependence(X)
							else:	
'''