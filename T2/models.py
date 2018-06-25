import re


class ContextFreeGrammar:
	
	FINITE = "finite"
	INFINITE = "infinite"
	EMPTY = "empty"

	def __init__(self, name, productions):
		self.name = name
		self.p_string = productions
		self.productions = []
		self.vn = set()
		self.vt = set()
		self.S = None
		self.decompose_and_formalize()
	
	##not working
	def parse_cfg(self):
		
		regex = re.compile(r'([A-Z][0-9]?->(([a-z] |[0-9] )*([A-Z][0-9]? )*([a-z]| [0-9])*|[&])([|]([a-z] |[0-9] )*([A-Z][0-9]?)*( [a-z]| [0-9])*|[&])*(\n|\Z))*')
		match = regex.match(self.p_string)
		print(match.group())
		try:
			if (match.group() == self.p_string):
				return True
			else:
				return False
		except AttributeError:
			return False


	def finiteness(self):
		self.remove_useless_symbols()
		if self.p_string == "VAZIO":
			return self.EMPTY
		elif self.isInfinite():
			return self.INFINITE
		else:
			return self.FINITE


	def isInfinite(self):
		for i in self.vn:
			i.calculate_nt_reachables(self.productions, self.vn)
			if i in i.nt_reachables:
				return True
		return False

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
		for nt in self.vn:
			nt.calculate_first_nt(self.productions, self.vn)

	def remove_useless_symbols(self):
		nf = self.remove_dead_symbols()
		self.vn = self.vn.intersection(nf)
		#redefenir prods
		if self.S not in self.vn:
			self.productions = []
			self.p_string = "VAZIO"
		else:
			self.redefine_productions()
			vf = self.remove_unreachable_symbols()
			self.vn = self.vn&vf
			self.vt = self.vt&vf
			self.redefine_productions()
			print(self.productions)


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
		return Nf

	def remove_unreachable_symbols(self):
		Vf = set()
		Vprev = {self.S}
		while True:
			Vi = set()
			for prods in self.productions:
				if prods.lhs in Vprev:
						Vi.update(prods.rhs)
				else:
					continue
			Vi = Vprev.union(Vi)
			if Vi == Vprev:
				break
			else:
				Vprev = Vi
		Vf = Vprev
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
		
		e_freeProds = [r for r in self.productions]
		for prod in self.productions:
			if prod.rhs[0] == epsilon:
				e_freeProds.remove(prod)
		for prod in self.productions:
			x = 0
			removals = []
			while x < len(prod.rhs):
				if prod.rhs[x] in Ne and (x-1==-1 or prod.rhs[x] not in self.vt):
					removals.append(prod.rhs[x])
					for i in removals:
						newRhs = [r for r in prod.rhs]
						del newRhs[newRhs.index(i)]
						newP = Production(prod.lhs, newRhs)
						if newP not in e_freeProds:
							e_freeProds.append(newP)
				x+=1
		print(e_freeProds)
		print(self.productions)

	def remove_simple_productions(self):
		for prod in self.productions:
			prod.lhs.calculate_simple_productions(self.productions, self.vn)
		for prod in self.productions:
			if len(prod.rhs) == 1 and prod.rhs[0] in self.vn:
				self.productions.remove(prod)
				for s in prod.lhs.simple:
					non_simple = [p.rhs for p in self.productions if p.lhs == s]
					for p in non_simple:
						if len(p) == 1 and p[0] in self.vn:
							continue
						else:
							new_prod = Production(prod.lhs, p)
							self.productions.append(new_prod)
		self.stringify_productions()

	def stringify_productions(self):
		productions = []
		for nt in self.vn:
			prods_per_nt = [prod for prod in self.productions if prod.lhs == nt]
			string = nt.label+"->"
			for p in prods_per_nt:
				for rhs in p.rhs:
					string+=rhs.label+" "
				string += "|"
			string = string.replace(" |", "|")
			string = string.replace("| ", "|")
			string = string[:-1]
			productions.append(string)
		productions = list(reversed(productions))
		for p in productions:
			if p.split("->")[0] == self.S.label:
				self.p_string = p+"\n"
				productions.remove(p)
		self.p_string += "\n".join(productions)
	
	def redefine_productions(self):

		for p in self.productions:
			if p.lhs not in self.vn:
				self.productions.remove(p)
			for r in p.rhs:
				if r not in self.vn and r not in self.vt:
					p.rhs.remove(r)
		self.stringify_productions()
class Production:
	def __init__(self, lhs, rhs):
		self.lhs = lhs
		self.rhs = rhs
	def __repr__(self):
		return str(self.lhs)+"->"+str(self.rhs)

	def __eq__(self, other):
		return self.rhs == other.rhs

class Symbol:
	def __init__(self, label):
		self.label = label
		self.first = set()
		self.follow = set()
		self.first_nt = set()
		self.dependences = []
		self.simple = set()
		self.nt_reachables = set()
	def __repr__(self):
		return self.label

	def has_epsilon_in_first(self):
		return "&" in [x.label for x in self.first]
	def calculate_simple_productions(self, productions, vn):
		all_prods_nt = [p for p in productions if p.lhs.label == self.label]
		for p in all_prods_nt:
			if len(p.rhs) == 1 and p.rhs[0] in vn:
				self.simple.add(p.rhs[0])
				p.rhs[0].calculate_simple_productions(productions, vn)
				if len(p.rhs[0].simple) > 0:
					self.simple.update(p.rhs[0].simple)

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
	def calculate_first_nt(self, productions, vn):
		myprods = [prod for prod in productions if prod.lhs.label == self.label]
		for prods in myprods:
			x = 0
			while True:
				if x >= len(prods.rhs):
					break
				else:
					if prods.rhs[x] in vn and prods.rhs[x] not in self.first_nt:
						self.first_nt.add(prods.rhs[x])
						if prods.rhs[x].label != self.label:
							prods.rhs[x].calculate_first_nt(productions, vn)
							self.first_nt.update(prods.rhs[x].first_nt)
						if prods.rhs[x].has_epsilon_in_first():
							x+=1
						else:
							break
					else:
						break
	def calculate_nt_reachables(self, productions, vn):
		myprods = [prod for prod in productions if prod.lhs.label == self.label]
		for prod in myprods:
			for rhs in prod.rhs:
				if rhs not in self.nt_reachables and rhs in vn:
					self.nt_reachables.add(rhs)
					if rhs.label != self.label:
						rhs.calculate_nt_reachables(productions, vn)
						self.nt_reachables.update(rhs.nt_reachables)

grammar = "S1->S1 a|b B|c B|A d\nA->B B A w|h|&\nB->f|&"
grammar2 = "S1->B a|b B|c B|A d\nA->B B A w|h|&\nB->S1 f|&"
grammar3 = "S->b B|A a\nA->b S|B a|&\nB->a"
grammar4 = "S->a S|B C|B D\nA->c C|A B\nB->b B|&\nC->a A|B C\nD->d D d|c"
grammar5 = "E->T E1\nE1->+ T E1|&\nT->F T1\nT1->* F T1|&\nF->( E )|i"
grammar6 = "E->E + T|T\nT->T * F|F\nF->( E )|a"
grammar7 = "S1->S1 a|b B|c B|A d\nA->B B A w A|h|&\nB->f|&"
grammar8 = "S->B a\nB->B"
cfg = ContextFreeGrammar(" ",grammar)
#cfg.set_firsts()
#cfg.set_follows()
# for i in cfg.vn:
# 	cfg.set_first_nt(i)
# cfg.set_follows()
for i in cfg.vn:
  	print(str(i)+" first")
  	print(i.first)
for i in cfg.vn:
  	print(str(i)+" follow")
  	print(i.follow)
for i in cfg.vn:
	print(str(i)+" first_nt")
	print(i.first_nt)

print(cfg.finiteness())
