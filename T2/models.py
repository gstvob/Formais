import re


class ContextFreeGrammar:
	
	def __init__(self, productions):
		self.p_string = productions
		self.productions = []
		self.vn = set()
		self.vt = set()
		self.S = None
		self.decompose_and_formalize()
	
	#método terrível, se me pergutarem não fui eu que fiz.
	def decompose_and_formalize(self):
		prods = self.p_string.split("\n")
		for p in prods:
			x = p.split("->")
			lhs = Symbol(x[0])
			self.vn.add(lhs)

		for p in prods:
			lhs = p.split("->")
			lhs = next(symbol for symbol in self.vn if symbol.label == lhs[0])
			x = p.split("->")[1].split("|")
			for s in x:
				rhs = []
				y = s.split(" ")
				for l in y:
					if len(l)<2 and not(l.isupper()):
						k = next((symbol for symbol in self.vt if symbol.label == l), Symbol(l))
						self.vt.add(k)
						rhs.append(k)
					else:
						k = next(symbol for symbol in self.vn if symbol.label == l)
						rhs.append(k)
				self.productions.append(Production(lhs, rhs))
		self.S = self.productions[0].lhs
		print(self.productions)
		self.set_firsts()
		self.set_follows()
		self.set_first_nt()

	def set_firsts(self):
		
		#passo1
		for terminal in self.vt:
			terminal.first.add(terminal)
		for non_terminal in self.vn:
			non_terminal.calculate_first(self.productions, self.vn, self.vt)

	def set_follows(self):
		
		#passo1
		self.S.follow.add(Symbol("$"))
		#passo2
		epsilon = next((symbol for symbol in self.vt if symbol.label == "&"), None)
		for prods in self.productions:
			for x in range(len(prods.rhs)):
				if prods.rhs[x] in self.vt:
					continue
				else:
					i = x
					while True:
						if i+1 >= len(prods.rhs):
							break
						elif prods.rhs[i+1] in self.vt:
							prods.rhs[i].follow.add(prods.rhs[i+1])
							break
						else:
							prods.rhs[i].follow.update(prods.rhs[i+1].first-{epsilon})
							if prods.rhs[i+1].has_epsilon_in_first():
								i+=1
							else:
								break

		changed = True
		while changed:
			changed = False
			for prods in self.productions:
				for x in range(len(prods.rhs)):
					i = x+1
					hasToAdd = False
					if prods.rhs[x] not in self.vt:
						while True:
							if i >= len(prods.rhs):
								hasToAdd = True
								break
							elif prods.rhs[i].has_epsilon_in_first():
								i+=1
							else:
								hasToAdd = False
								break
					if hasToAdd:
						before = prods.rhs[x].follow
						prods.rhs[x].follow.update(prods.lhs.follow)
						if len(before) != len(prods.rhs[x].follow):
							changed = True

	def set_first_nt(self):
		
		for prods in self.productions:
			x = 0
			while True:
				if x >= len(prods.rhs):
					break
				else:	
					if prods.rhs[x] not in self.vt:
						prods.lhs.first_nt.add(prods.rhs[x])
						if prods.rhs[x].has_epsilon_in_first():
							x+=1
						else:
							break
					else:
						break

	def remove_useless_symbols(self):
		nf = self.remove_dead_symbols()
		self.vn = self.vn&nf
		#redefenir prods
		if self.S not in self.vn:
			self.productions = []
			self.p_string = "VAZIO"
			print("VAZIO")
		else:
			self.redefine_productions()
			self.productions = []
			self.decompose_and_formalize()
			vf = self.remove_unreachable_symbols()
			self.vn = self.vn&vf
			self.vt = self.vt&vf
			self.redefine_productions()
			self.productions = []
			self.decompose_and_formalize()


	def remove_dead_symbols(self):
		Nf = set()
		Nprev = set()
		while True:
			Ni = set()
			for prods in self.productions:
				A = prods.lhs
				if prods.rhs[0] in self.vt or prods.rhs[0] in Nprev:
					x = 1
					while True:
						if x >= len(prods.rhs):
							Ni.add(prods.lhs)
							break
						elif prods.rhs[x] in self.vt or prods.rhs[x] in Nprev:
							x+=1
						else:
							break
			Ni = Nprev.union(Ni)
			if Ni == Nprev:
				break
			else:
				Nprev = Ni
		Nf = Nprev
		print(Nf)
		return Nf

	def remove_unreachable_symbols(self):
		Vf = set()
		Vprev = {self.S}
		while True:
			Vi = set()
			for prods in self.productions:
				A = prods.lhs
				if A in Vprev:
					for rhs in prods.rhs:
						Vi.add(rhs)
				else:
					continue
			if Vi == Vprev:
				break
			else:
				Vprev = Vi
		Vf = Vprev
		print(Vf)
		return Vf

	def into_epsilon_free(self):
		Ne = set()
		Nprev = set()
		epsilon = next(symbol for symbol in self.vt if symbol.label == "&")
		while True:
			Ni = set()
			for prods in self.productions:
				A = prods.lhs
				if prods.rhs[0] == epsilon or prods.rhs[0] in Nprev:
					x = 1
					while True:
						if x >= len(prods.rhs):
							Ni.add(prods.lhs)
							break
						elif prods.rhs[x] in Nprev:
							x+=1
						else:
							break
			Ni = Nprev.union(Ni)
			if Ni == Nprev:
				break
			else:
				Nprev = Ni
		Ne = Nprev
		
		for prod in self.productions:
			if prod.rhs[0] == epsilon:
				self.productions.remove(prod)
		

	def redefine_productions(self):
		prods = self.p_string.split("\n")
		for p in prods:
			nT = p.split("->")[0]
			if nT not in [l.label for l in self.vn]:
				prods.remove(p)

		self.p_string = "\n".join(prods) 
		for p in self.p_string.split("\n"):
				A_label = p.split("->")[0]
				rhs = p.split("->")[1]
				for s in range(len(rhs)):
					if rhs[s] != "|" and rhs[s] != " ":
						if rhs[s] not in [l.label for l in self.vt] and rhs[s] not in [l.label for l in self.vn]:
							print(rhs[s])
							self.p_string = self.p_string.replace(rhs[s], "")
							self.p_string = self.p_string.replace("| ", "|")
							self.p_string = self.p_string.replace(" |", "|")


class Production:
	def __init__(self, lhs, rhs):
		self.lhs = lhs
		self.rhs = rhs

	def __repr__(self):
		return str(self.lhs)+"->"+str(self.rhs)

class Symbol:
	def __init__(self, label):
		self.label = label
		self.first = set()
		self.follow = set()
		self.first_nt = set()
		self.dependences = []

	def __repr__(self):
		return self.label

	def has_epsilon_in_first(self):
		return "&" in [x.label for x in self.first]
	def calculate_first(self, productions, vn, vt):
		myprods = [prod for prod in productions if prod.lhs.label == self.label]
		for prod in myprods:
			if prod.rhs[0] in vt:
				self.first.add(prod.rhs[0])

		epsilon = next((symbol for symbol in vt if symbol.label == "&"), None)
		for prod in myprods:
			previousHadEpsilon = True
			for x in range(len(prod.rhs)):
				if previousHadEpsilon:
					if prod.rhs[x] not in vt:
						if prod.rhs[x].label != self.label:
							prod.rhs[x].calculate_first(productions, vn, vt)
							self.first.update(prod.rhs[x].first-{epsilon})
						if prod.rhs[x].has_epsilon_in_first():
							previousHadEpsilon = True
						else:
							previousHadEpsilon = False
					else:
						self.first.update(prod.rhs[x].first)
						break
	def add_dependence(self, symbol):
		self.dependences.append(symbol)

	def print_firsts(self):
		print(str(self.first))

grammar = "S1->S1 a|b B|c B|A d\nA->B B A w|h|&\nB->f|&"
grammar2 = "S1->B a|b B|c B|A d\nA->B B A w|h|&\nB->S1 f|&"
grammar3 = "S->b B|A a\nA->b S|&\nB->a"
grammar4 = "S->a S|B C|B D\nA->c C|A B\nB->b B|&\nC->a A|B C\nD->d D d|c"
cfg = ContextFreeGrammar(grammar)
# for i in cfg.vn:
# 	cfg.set_first_nt(i)
# cfg.set_follows()
# for i in cfg.vn:
#  	print(str(i)+" first")
#  	print(i.first)
# for i in cfg.vn:
#  	print(str(i)+" follow")
#  	print(i.follow)
# for i in cfg.vn:
#  	print(str(i)+" first_nt")
#  	print(i.first_nt)
cfg.into_epsilon_free()
'''
							if yn == Prev and yn != X:
								print(Prev)
								print(X)
								X.add_dependence(Prev)
								Prev.add_dependence(X)
							else:	
'''