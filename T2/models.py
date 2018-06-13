

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

	def set_firsts(self, X):
		p = cfg.productions
		vn = cfg.vn
		vt = cfg.vt
		if X in vt:
			X.first.add(X)
		else:
			prods = p.split("\n")
			print(prods)
			that_prod = next(p for p in prods if (p.split("->")[0]) == X.label)
			that_prod = that_prod.split("->")[1]
			print(that_prod)
			for x in range(len(that_prod)):
				if that_prod[x] in [y.label for y in vt]: 
					if x-1 == -1 or that_prod[(x-1)] == "|":
						symbol = next(s for s in vt if s.label == that_prod[x])
						X.first.add(symbol)
			# se X->S1 S2 S3
			# first(S1) ta em X
			# se epsilon ta em S1, first(S2) ta em X e assim vai
			splitemup = that_prod.split("|")
			print(splitemup)

			for x in splitemup:
				y = x.split(" ")
				previousHadEpsilon=True
				addedTerminal = False
				for k in range(len(y)):
					if y[k] in [z.label for z in vn]:
						yn = next(s for s in vn if s.label == y[k])
						if y[k] != X.label:
							self.set_firsts(yn)
							X.first.update(yn.first)
						if "&" in [l.label for l in yn.first]:
							epsilon = next(s for s in yn.first if s.label == "&")
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

	def __repr__(self):
		return self.label

	
	# def set_follows(self, cfg):
	# 	#passo1
	# 	p = cfg.productions
	# 	vn = cfg.vn
	# 	vt = cfg.vt
	# 	if self.label == cfg.S.label:

	def print_firsts(self):
		print(str(self.first))

grammar = "S1->S1 a|b B|c B|A d|&\nA->B B A w|h|&\nB->f|&"
cfg = ContextFreeGrammar(grammar)
cfg.print_stuff()