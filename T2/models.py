import re
import itertools

'''
	Classe de definição das linguagens livre de contexto
'''
class ContextFreeGrammar:
	

	FINITE = "Finita"
	INFINITE = "Infinita"
	EMPTY = "Vazia"

	'''
		Construtor
	'''
	def __init__(self, name, productions):
		self.name = name
		self.p_string = productions
		self.productions = []
		self.vn = set()
		self.vt = set()
		self.S = None
		self.decompose_and_formalize()

	'''
		Método que retorna se a gramatica é finita, infinita ou vazia.
	'''
	def finiteness(self):
		self.remove_useless_symbols()
		if self.p_string == "VAZIO":
			return self.EMPTY
		elif self.isInfinite():
			return self.INFINITE
		else:
			return self.FINITE

	'''
		Método que checa se a gramática é infinita.
		buscando por se existe a derivação do tipo A => aAb por 1 ou mais passos.		
		ele busca pelos os não terminais que são alcançaveis do simbolo, se o estado estiver nesse conjunto
		a gramática é infinita.
	'''
	def isInfinite(self):
		for i in self.vn:
			i.calculate_nt_reachables(self.productions, self.vn)
			if i in i.nt_reachables:
				return True
		return False

	'''
		Verifica se a gramática tem produções simples.
		buscando produções do tipo S->A na gramática.
	'''
	def has_simple_productions(self):
		for p in self.productions:
			if len(p.rhs) == 1 and p.rhs[0] in self.vn:
				return True
		return False

	'''
		Verifica se a gramática é epsilon livre.
		uma glc é &-livre se a gramática não deriva épsilon.
		ou apenas o simbolo inicial deriva épsilon sendo que ele não pode aparecer no lado
		direito de nenhuma produção.
	'''
	def is_epsilon_free(self):
		if "&" in [k.label for k in self.vt]:
			for p in self.productions:
				if "&" in [rhs.label for rhs in p.rhs] and p.lhs != self.S:
					return False
			
			prods_for_S = [prods for prods in self.productions if prods.lhs == self.S]
			epsilon = next(s for s in self.vt if s.label == "&")
			for k in prods_for_S:
				if epsilon in k.rhs:
					for p in self.productions:	
						if self.S in p.rhs:
							return False
		return True

	'''
		Verifica se a GLC tem simbolos inúteis.
		simplesmente verifica se algum dos métodos para remover simbolos inuteis retorna vazio.
	'''
	def has_useless_symbols(self):
		if len(self.remove_dead_symbols()) != len(self.vn) or len(self.remove_unreachable_symbols()) != len(self.vt)+len(self.vn):
			return True
		return False


	'''
		Verifica se a GLC tem recursão a esquerda.
		simplesmente ele verifica se os first nt das produções são iguais
		ou se o próprio símbolo é um first nt 
	'''
	def has_leftmost_recursion(self):
		for p in self.vn:
			for j in self.vn:
				if p != j:
					if p.first_nt == j.first_nt:
						return True
		for p in self.vn:
			if p in p.first_nt:
				return True
		return False

	'''
		Verifica se a gramática ta fatorada.
		Pega os firsts de cada produção do lado direito de um símbolo,
		a intersecção dos firsts dos lados direitos das produções deve ser vazio
		para ela não ser fatorada, caso não seja vazio ela não está fatorada.
	'''
	def is_factored(self):
		if self.has_leftmost_recursion():
			return False
		for nt in self.vn:
			prods = [p for p in self.productions if p.lhs == nt]
			firsts = []
			for p in prods:
				firsts.append(p.production_first(self.vn, self.vt))
			print(firsts)	
			for a, b in itertools.combinations(firsts, 2):
				if a&b:
					return False
		return True

	#método terrível, se me pergutarem não fui eu que fiz.
	def decompose_and_formalize(self):
		prods = self.p_string.split("\n")
		self.vn = set()
		self.vt = set()
		self.productions = []
		vn_temp = []
		for p in prods:
			x = p.split("->")
			lhs = Symbol(x[0])
			vn_temp.append(lhs)

		self.vn = set(vn_temp)
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


	'''
		método para setar os firsts de cada simbolo
	'''
	def set_firsts(self):
		
		#passo1
		for terminal in self.vt:
			terminal.first.add(terminal)
		for non_terminal in self.vn:
			non_terminal.calculate_first(self.productions, self.vn, self.vt)

		for non_terminal in self.vn:
			epsilon = next((x for x in self.vt if x.label == "&"), None)
			non_terminal.update_first_of_equals(epsilon)

	'''
		Método para setar os follows de cada símbolo, utilizando o algoritmo visto em sala.
	'''
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

	'''
		método para setar os first_nt de cada símbolo.
	'''
	def set_first_nt(self):
		for nt in self.vn:
			nt.calculate_first_nt(self.productions, self.vn)

	'''
		remove os símbolos inúteis de uma glc.
		tira os símbolos mortos, redefine a gramática.
		tira os símbolos inalcançáveis, redefine a gramática.
		gramática sem símbolos inúteis.
	'''
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

	'''
		Método que retorna Nf, o conjunto símbolos da gramática que são férteis. 
	'''
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

	'''
		Método que retorna Vf, conjunto de símbolos que são alcançáveis.
	'''
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


	'''
		Método que transforma uma gramatica em epsilon livre.
		utiliza o algoritmo visto em aula,
		cria o conjunto Ne de símbolos que derivam & direto ou indiretamente.
		a partir desse conjunto são removidas as produções & diretas e são redefinidas as produções
		conforme o algoritmo.
	'''
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
		if self.S in Ne:
			e_freeProds.add(Production(Symbol("S0"), [self.S, epsilon]))
		for prod in self.productions:
			if prod.rhs[0] == epsilon:
				e_freeProds.remove(prod)
		for prod in self.productions:
			x = 0
			while True:
				removals = []
				while x < len(prod.rhs):
					if prod.rhs[x] in self.vt:
						break
					if prod.rhs[x] in Ne and (x-1==-1 or prod.rhs[x] not in self.vt) and len(prod.rhs) > 1:
						removals.append(x)
					x+=1
				sizo = 1
				while True:	
					if sizo > len(removals):
						break
					a = list(itertools.combinations(removals, sizo))
					for i in a:
						newRhs = [r for r in prod.rhs]
						for s in i:
							newRhs[s]=Symbol("$at")
						newRhs = [r for r in newRhs if r.label != "$at"]
						newP = Production(prod.lhs, newRhs)
						if newP not in e_freeProds:
							e_freeProds.append(newP)
					sizo+=1
				x+=1
				if x >= len(prod.rhs):
					break
		self.productions = e_freeProds
		self.stringify_productions()
	

	'''
		Remove as produções simples.
		S->T
		calculando as produções simples de cada conjunto
		e adicionando as produções desse não terminais simples no não terminal que derivava o simples anteriormente
		(algoritmo visto em aula)
	'''
	def remove_simple_productions(self):
		simples = []
		for prod in self.productions:
			prod.lhs.calculate_simple_productions(self.productions, self.vn)
		for prod in self.productions:
			if len(prod.rhs) == 1 and prod.rhs[0] in self.vn:
				simples.append(prod)
				for s in prod.lhs.simple:
					if s.label == prod.lhs.label:
						continue
					else:
						non_simple = [p.rhs for p in self.productions if p.lhs == s]
						for p in non_simple:
							new_prod = Production(prod.lhs, p)
							if len(p) == 1 and p[0] in self.vn:
								continue
							elif new_prod not in self.productions:
								self.productions.append(new_prod)
		self.productions = [prod for prod in self.productions if prod not in simples]
		self.stringify_productions()


	'''
		Transforma uma gramática em própria
		Transforma em epsilon livre -> remove produções simples -> remove símbolos inúteis = Gramatica propria.
	'''
	def into_proper_grammar(self):
		intermediary = dict()
		if not self.is_epsilon_free():
			self.into_epsilon_free()
			self.decompose_and_formalize()
			print("EPSILON FREE")
			print(self.p_string)
			intermediary["e-free"] = self.p_string
		if self.has_simple_productions():		
			self.remove_simple_productions()
			self.productions = []
			self.decompose_and_formalize()
			print("sem prods simples")
			print(self.p_string)
			intermediary["no-simple"] = self.p_string
		self.remove_useless_symbols()
		self.productions = []
		self.decompose_and_formalize()
		print("propra")
		print(self.p_string)
		intermediary["no-useless"]=self.p_string
		return intermediary

	'''
		Método que vai remover as recursões a esquerda, diretas ou indiretas
	'''
	def remove_leftmost_recursion(self):
		epsilon = next((symbol for symbol in self.vt if symbol.label == "&"), None)
		if epsilon == None:
			epsilon = Symbol("&")
			self.vt.add(epsilon)

		for nt in self.vn:
			nt_prods = [prod for prod in self.productions if nt == prod.lhs]
			if nt in nt.first_nt:
				self.remove_direct_recursion(nt_prods, nt, epsilon)
		
		for p in self.productions:
			if p.lhs not in self.vn:
				self.vn.add(p.lhs)

		self.stringify_productions()
		self.decompose_and_formalize()
		print(self.p_string)
		# self.into_proper_grammar()
		# if not self.has_simple_productions() and self.is_epsilon_free() and not self.has_useless_symbols():	
		# 	for i in range(1, len(self.vn)):
		# 		j = 0
		# 		Ai = list(self.vn)[i]
		# 		Ai_prods = [prods for prods in self.productions if prods.lhs == Ai]
		# 		Ai_rhs = [prods.rhs for prods in Ai_prods]
		# 		while j <= i-1:
		# 			Aj = list(self.vn)[j]
		# 			for rhs in Ai_rhs:
		# 				if Aj in rhs:
		# 					if len(rhs) > 1:
		# 						reusable_rhs = [symbol for symbol in rhs if symbol != Aj]
		# 					Aj_prods = [prods for prods in  self.productions if prods.lhs == Aj]
		# 					Aj_rhs = [prods.rhs for prods in Aj_prods]
		# 					new_rhs = [r for r in Ai_rhs if rhs != r]
		# 					for skr in Aj_rhs:
		# 						new_rhs.append(skr+reusable_rhs)
		# 					newProds = []
		# 					Ai_prods = []
		# 					for r in new_rhs:
		# 						newProds.append(Production(Ai, r))
		# 					Ai_prods += newProds
		# 			j+=1
		# 		self.remove_direct_recursion(Ai_prods, Ai, epsilon)
		# self.stringify_productions()
		# self.decompose_and_formalize()
		# print(self.p_string)
	'''
		Remover recursão a esquerda diretas
	'''
	def remove_direct_recursion(self, prod, nt, epsilon):
		prods_without_recursion = []
		prods_with_recursion = []
		for p in prod:
			if nt not in p.rhs:
				prods_without_recursion.append(p)
			else:
				prods_with_recursion.append(p)
		
		new_nt = self.new_nt(nt)
		newProd = Production(new_nt, [])
		newProd.rhs = [rhs for rhs in p.rhs] 
		if prods_with_recursion:
			for p in prods_with_recursion:
				x = 0
				while True:
					if newProd.rhs[x].has_epsilon_in_first() and newProd.rhs[x] != nt:
						x+=1
					elif newProd.rhs[x] == nt:
						newProd.rhs[x] = Symbol("$at")
					else:
						break
				newProd.rhs = [rhs for rhs in newProd.rhs if rhs.label != "$at"]
				newProd.rhs.append(new_nt)
		newProd_eps = Production(new_nt, [epsilon])
		starter = Production(nt, [])
		if prods_without_recursion:
			for p in prods_without_recursion:
				starter.rhs += p.rhs
				starter.rhs.append(new_nt)
		else:
			starter = Production(nt, [new_nt])
		self.productions = [prod for prod in self.productions if nt != prod.lhs]
		self.productions.append(starter)
		self.productions.append(newProd)
		self.productions.append(newProd_eps)
		print(self.productions)
	'''
		Método auxiliar que pega a lista de Produções e transforma em uma string.
	'''
	def stringify_productions(self):
		productions = []
		for nt in self.vn:
			prods_per_nt = [prod for prod in self.productions if prod.lhs == nt]
			if prods_per_nt:
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

	'''
		Método auxiliar para tirar os símbolos que não são ferteis e alcançáveis.
	'''
	def redefine_productions(self):

		for p in self.productions:
			if p.lhs not in self.vn:
				self.productions.remove(p)
			for r in p.rhs:
				if r not in self.vn and r not in self.vt:
					p.rhs.remove(r)
		self.stringify_productions()
	'''
		Método auxiliar para criar um novo NT (usado na fatoração, remoção de recursão e etc.)
	'''
	def new_nt(self, nt):
		label1 = nt.label[0]
		contador = 1
		new_nt = None
		while True:
			if label1+str(contador) in [k.label for k in self.vn]:
				contador+=1
				continue
			else:
				new_nt = Symbol(label1+str(contador))
				break
		return new_nt


'''
	Classe que define uma produção, que é formada por um lado esquerdo, um simbolo NT, e por um lado direito, que é
	uma lista de simbolos terminais e não terminais.
'''
class Production:
	def __init__(self, lhs, rhs):
		self.lhs = lhs
		self.rhs = rhs

	def __cmp__(self, other):
		if self.lhs > other.lhs:
			return 1
		elif self.lhs < other.lhs:
			return -1
		else:
			return 0
	def __repr__(self):
		return str(self.lhs)+"->"+str(self.rhs)
	def __eq__(self, other):
		return self.rhs == other.rhs and self.lhs == other.lhs
	
	'''
		Método que calcula o first de todos os lados direitos de uma produção
		(auxiliar na detecção de fatoração)
	'''
	def production_first(self, vn, vt):
		p_first = set()
		for rhs in self.rhs:
			if rhs in vn:
				p_first.update(rhs.first)
				if "&" not in [k.label for k in rhs.first]:
					if "&" in [k.label for k in p_first]:
						epsilon = next(symbol for symbol in vt if symbol.label == "&")
						p_first.remove(epsilon)
					break
			elif rhs in vt:
				if "&" in [k.label for k in p_first]:
					epsilon = next(symbol for symbol in vt if symbol.label == "&")
					p_first.remove(epsilon)
				p_first.add(rhs)
				break
		return p_first

'''
	Classe que define um símbolo.
'''
class Symbol:
	def __init__(self, label):
		self.label = label
		self.first = set()
		self.follow = set()
		self.first_nt = set()
		self.dependences = []
		self.simple = set()
		self.nt_reachables = set()
		self.equals = set()
	def __repr__(self):
		return self.label


	'''
		Se uma produção deriva epsilon, ela tem epsilon no first
	'''
	def has_epsilon_in_first(self):
		return "&" in [x.label for x in self.first]

	'''
		calcula as produções simples de um símbolo NT.
	'''
	def calculate_simple_productions(self, productions, vn):
		all_prods_nt = [p for p in productions if p.lhs.label == self.label]
		for p in all_prods_nt:
			if len(p.rhs) == 1 and p.rhs[0] in vn:
				self.simple.add(p.rhs[0])
				if p.rhs[0].label != self.label:
					p.rhs[0].calculate_simple_productions(productions, vn)
					if len(p.rhs[0].simple) > 0:
						self.simple.update(p.rhs[0].simple)

	'''
		Calcula o first de um NT, pegando as produções que ele deriva, e então executando
		o algoritmo de calculo de first visto em aula.
	'''
	def calculate_first(self, productions, vn, vt, visited=[]):
		visited.append(self)
		myprods = [prod for prod in productions if prod.lhs.label == self.label]
		for prod in myprods:
			if prod.rhs[0] in vt:
				self.first.add(prod.rhs[0])

		epsilon = next((symbol for symbol in vt if symbol.label == "&"), None)
		for prod in myprods:
			previousHadEpsilon = True
			for x in range(len(prod.rhs)):
				if previousHadEpsilon:
					if prod.rhs[x] not in vt and prod.rhs[x]:
						if prod.rhs[x].label != self.label: 
							if prod.rhs[x].label not in [l.label for l in visited]:
								prod.rhs[x].calculate_first(productions, vn, vt, visited)
								self.first.update(prod.rhs[x].first-{epsilon})
							elif prod.rhs[x] in visited and prod:
								self.equals.add(prod.rhs[x])
						if prod.rhs[x].has_epsilon_in_first():
							previousHadEpsilon = True
						else:
							previousHadEpsilon = False
					else:
						self.first.update(prod.rhs[x].first)
						break


	'''
		Método para auxiliar no cálculo dos firsts, quando se tem produções do tipo
		S->A b
		A->S a
		quando isso ocorre os firsts são iguais
	'''
	def update_first_of_equals(self, epsilon):
		if self.equals:
			for s in self.equals:
				if epsilon != None:
					self.first.update(s.first-{epsilon})
				else:
					self.first.update(s.first)
	'''
		Método similar ao first, mas calcula o first_nt que são os não terminais que aparecem no começo
		de uma produção(definição meio fraca, não consigo me expressar direito)
	'''
	def calculate_first_nt(self, productions, vn):
		myprods = [prod for prod in productions if prod.lhs.label == self.label]
		for prods in myprods:
			x = 0
			while True:
				if x >= len(prods.rhs):
					break
				else:
					if prods.rhs[x] in vn:
						self.first_nt.add(prods.rhs[x])
						if prods.rhs[x].label != self.label:
							if prods.rhs[x] not in self.first_nt:
								prods.rhs[x].calculate_first_nt(productions, vn)
								self.first_nt.update(prods.rhs[x].first_nt)
						if prods.rhs[x].has_epsilon_in_first():
							x+=1
						else:
							break
					else:
						break
	'''
		calcula os NT que um não terminal alcança
	'''
	def calculate_nt_reachables(self, productions, vn):
		myprods = [prod for prod in productions if prod.lhs.label == self.label]
		for prod in myprods:
			for rhs in prod.rhs:
				if rhs not in self.nt_reachables and rhs in vn:
					self.nt_reachables.add(rhs)
					if rhs.label != self.label:
						rhs.calculate_nt_reachables(productions, vn)
						self.nt_reachables.update(rhs.nt_reachables)


# grammar = "S1->S1 a|b B|c B|A d\nA->B B A w|h|&\nB->f|&"
# grammar2 = "S1->B a|b B|c B|A d\nA->A w|h|&\nB->S1 f|&"
# grammar3 = "S->b B|A a\nA->b S|B a|&\nB->x"
# grammar4 = "S->a S|B C|B D\nA->c C|A B\nB->b B|&\nC->a A|B C\nD->d D d|c"
# grammar5 = "E->T E1\nE1->+ T E1|&\nT->F T1\nT1->* F T1|&\nF->( E )|i"
# grammar6 = "E->E + T|T\nT->T * F|F\nF->( E )|a"
# grammar7 = "S1->S1 a|b B|c B|A d\nA->B B A w A|h|&\nB->f|&"
# grammar8 = "S->B a\nB->B"
# grammar9 = "S->a A|B b\nA->a A|&\nB->b B|A|&"
# grammar10 = "S->&|a A\nA->a|&"
# grammar11 = "S->A b|a\nA->S b|a"
# grammar12 = "E->E + T|( E )|a|T * F\nT->T * F|( E )|a\nF->( E )|a"
# grammar13 = "S->A b\nA->S a"
# grammar14 = "S->A a|S b\nA->S c|d"
# cfg = ContextFreeGrammar(" ",grammar14)
# #cfg.set_firsts()
# #cfg.set_follows()
# # for i in cfg.vn:
# # 	cfg.set_first_nt(i)
# # cfg.set_follows()
# cfg.set_firsts()
# cfg.set_follows()
# cfg.set_first_nt()
# for i in cfg.vn:
# 	print(str(i)+" first")
# 	print(i.first)
# for i in cfg.vn:
# 	print(str(i)+" follow")
# 	print(i.follow)
# for i in cfg.vn:
# 	print(str(i)+" first_nt")
# 	print(i.first_nt)
# cfg.remove_leftmost_recursion()