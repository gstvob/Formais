

class ContextFreeGrammar:
	
	def __init__(self, productions):
		self.productions = productions
		self.vn = set()
		self.vt = set()
		self.S = None
		self.decompose_and_formalize()

	def decompose_and_formalize(self):
		symbols = []
		for p in self.productions:
			if p not in [symbol.label for symbol in symbols] and (p.isalpha() or p == "&"):
				symbols.append(Symbol(p))
		for s in symbols:
			if s.label.isalpha() or s.label == "&":
				if s.label.isupper():
					self.vn.add(s)
				else:
					self.vt.add(s)
		self.S = symbols[0]

	def print_stuff(self):
		print(str(self.vn))
		print(str(self.vt))
		print("Inicial: "+str(self.S))
		self.S.set_firsts(self)
		self.S.print_firsts()

class Symbol:
	def __init__(self, label):
		self.label = label
		self.first = set()
		self.follow = set()

	def __repr__(self):
		return self.label

	#needs tweaking about the epsilons
	def set_firsts(self, cfg):
		p = cfg.productions
		vn = cfg.vn
		vt = cfg.vt
		if self in vt:
			self.first.add(self)
		else:
			prods = p.split("\n")
			print(prods)
			that_prod = next(p for p in prods if p[0] == self.label)
			that_prod = that_prod.split("->")[1]
			for x in range(len(that_prod)):
				if that_prod[x] in [y.label for y in vt]: 
					if x-1 == -1 or that_prod[(x-1)] == "|":
						symbol = next(s for s in vt if s.label == that_prod[x])
						self.first.add(symbol)

			for x in range(len(that_prod)):
				if that_prod[x] in [y.label for y in vn]:
					if x-1 == -1 or that_prod[(x-1)] == "|":
						symbol = next(s for s in vn if s.label == that_prod[x])
						print(symbol)
						if symbol.label != self.label:
							symbol.set_firsts(cfg)
							self.first.update(symbol.first)
						if "&" in [y.label for y in symbol.first]:
							epsilon = next(s for s in symbol.first if s.label == "&")
							self.first.remove(epsilon)
							index = x
							while True:
								if (index+1) <= len(that_prod)-1 and that_prod[index+1] != "|" :
									next_symbol = next(s for s in vt|vn if s.label == that_prod[index+1])
								else:
									self.first.add(epsilon)
									break
								if "&" in that_prod:
									self.first.add(epsilon)
								if next_symbol in vt:
									self.first.add(next_symbol)
									break
								else:
									if next_symbol.label != self.label:
										next_symbol.set_firsts(cfg)
										self.first.update(next_symbol.first)
									index+=1
	def print_firsts(self):
		print(str(self.first))

grammar = "S->Sa|bB|cC|Ad|\nA->BBAw|h|&\nB->f|&"
cfg = ContextFreeGrammar(grammar)
cfg.print_stuff()