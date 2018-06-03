import re
import random
import string
import itertools

'''

AUTOR : GUSTAVO BORGES FRANÇA


'''


'''
	Classe das gramáticas regulares, aqui se encontram
	as lógicas para as operações que são possíveis com 
	as gramáticas e as definições da mesma.
'''

class RegularGrammar:
	#Construtor que inicializa com o nome da gr e suas produções.
	def __init__(self, name, P):
		self.name = name
		self.p = P
		self._definition(P)

	def set_name(self, name):
		self.name = name
	def set_productions(self, productions):
		self.p = productions
		self._definition(productions)
	
	'''
		O método que pega as produções de uma gramática regular
		e transforma em uma definição formal para facilitar em algumas operações.
	'''
	def _definition(self, productions):
		self.s = productions[0]
		self.vn = []
		self.vt = []

		for i in productions :
			if i.isupper() and i not in self.vn:
				self.vn.append(i)
			elif (i.islower() or i.isdigit()) and i not in self.vt:
				self.vt.append(i)


	'''
		Método que recebe as produções de uma gramática e verifica
		com o uso de uma expressão regular se a gramática está ok.
	'''
	def validate_grammar(self, productions):
		productions = productions.replace(" ", "")
		regex = re.compile(r'([A-Z]->([a-z0-9][A-Z]?|\&)([|][a-z0-9][A-Z]?)*(\n|\Z))*')
		match = regex.match(productions)

		try:
			if (match.group() == productions):
				return self._check_epsilon(productions)
			else:
				return False
		except AttributeError:
			return False

	'''
		Esse método verifica se existe épsilon na gramática
		e se existe, se ele está sendo utilizado de forma correta.
		Por simplicidade, para definir uma gramática com épsilon
		o épsilon deve ser a primeira produção
		S->&|etc...
	'''
	def _check_epsilon(self, productions):
		if "&" in productions:
			first_enter = productions.find('\n')
			last_epsilon= productions.rfind('&')
			if last_epsilon > first_enter and first_enter != -1:
				return False
			for i in range(len(productions)):
				if productions[i] == productions[0] and i != 0:
					return False
		return True


	'''
		Conversão de gramática regular para autômato finito.
		os estados é o conjunto de não terminais, o alfabeto os terminais
		é criado um estado novo que é final, e o algoritmo é o
		visto em aula.
		retorna um autômato(determínisto ou não determínistico dependendo da gramática)
	'''
	def convert(self):
		states = [State(x) for x in self.vn]
		alphabet = self.vt
		extra = State("$", True)
		states.append(extra)
		productions = self.p.split("\n")
		if "&" in productions[0]:
			states[0].set_acceptance(True)
		for state in states:
			rules = []
			if state.label in [x[0] for x in productions]:
				producao = next(x for x in productions if state.label == x[0])
				rules = producao.split(producao[0]+"->")[1].split("|")
			trsts = []
			for i in rules:
				if i != "&":
					if len(i) > 1:
						target = next(x for x in states if x.label == i[1])
						trsts.append(Transition(target, i[0]))
					else:
						target = next(x for x in states if x.label == "$")
						trsts.append(Transition(target, i[0]))
			for i in alphabet:
				if not any(i in str for str in rules):
					target = State("-")
					trsts.append(Transition(target, i))
			state.insert_transitions(trsts)
		return Automaton(states, alphabet)

	'''
		Realização de união de duas gramáticas
		por simplicidade é necessário que os não terminais das gramáticas
		sejam diferentes(não é realizado um renomeamento).
		e então as produções são retiradas das gramáticas para definir uma nova
		retorna uma gramática regular.
	'''
	def union(self, grammar):
		p1 = self.p
		p2 = grammar.p
		union = ""
		epsilon = False
		if "&" in p1:
			p1 = p1.replace("&|", "")
			epsilon = True
		if "&" in p2:
			p2 = p2.replace("&|", "")
			epsilon = True
		if set(self.vn) <= set(grammar.vn) or set(self.vn) >= set(grammar.vn):
			return None 
		else:      
			prods1 = p1.split("\n")
			prods2 = p2.split("\n")
			if epsilon:
				union = "Ω->&|"
			else:
				union = "Ω->"
			union += prods1[0].split("->")[1]+"|"+prods2[0].split("->")[1]+"\n"
			for i in prods1:
				union += i+"\n"
			for i in prods2:
				union += i+"\n"
		return RegularGrammar("$at", union)


	'''
		Operação de concatenação de duas gramáticas.
		similar a operação de união, as gr's não podem ter o mesmo
		não terminal(não há renomeamento)
		algoritmo executado o que foi visto em aula.
		retorna uma gramática regular.
	'''
	def concatenate(self, grammar):
		p1 = self.p
		p2 = grammar.p
		concat = ""
		epsilon = False
		if "&" in p1:
			p1 = p1.replace("&|", "")
			epsilon = True
		if "&" in p2:
			p2 = p2.replace("&|", "")
			epsilon = True
		if set(self.vn) <= set(grammar.vn) or set(self.vn) >= set(grammar.vn):
			return None
		else:
			g2s = p2[0];
			for i in range(len(p1)):            
				try :
					if p1[i].islower() and (p1[i+1] == "|" or p1[i+1] == "\n"):
						concat += p1[i]+g2s
					else:
						concat += p1[i]
				except IndexError:
					concat += p1[i]+g2s 
			if epsilon:
				epsilon_concat = "Ω->&|"
				prods1 = concat.split("\n")
				for i in prods1:
					epsilon_concat+=i
				concat = epsilon_concat+"\n"+concat
			concat += "\n"+p2
		return RegularGrammar("$at", concat)


	'''
		Operação estrela em uma gramática
		simplesmente pega uma gramática regular e realiza a operação estrela
		retornando uma gramática regular que é o fecho.
	'''
	def kleene_star(self):
		p = self.p
		S = p[0]
		new_p = ""
		prods = p.split("\n")
		new_prods = []
		epsilon = False
		if "&" in p:
			p = p.replace("&|", "")
			epsilon = True
		for i in prods:
			terminals = i[0]
			rules = i.split("->")[1].split("|")
			new_rules = rules
			added = 0
			for j in rules:
				if len(j)==1:
					added=1
					rules.append(j+S)
			prod = terminals+"->"
			for r in rules:
				prod += r+"|"
			prod = prod[:-1]
			new_prods.append(prod)
		for i in new_prods:
			new_p += i+"\n"
		new_p = new_p[:-1]
		if epsilon:
			new_p = "Ω->&|"+new_p
		return RegularGrammar("$at", new_p)


'''
	Classe com as definições e operações de expressão regular.
'''
class RegularExpression:

	'''
		construtor que inicializa uma expressão com seu nome e a expressão em si.
	'''
	def __init__(self, name, expression):
		self.name = name
		self.expression = expression

	def set_name(self, name):
		self.name = name

	def set_expression(self, exp):
		self.expression = exp

	'''
		método para validar uma expressão.
		utiliza outra expressão para ver se algumas coisas estão certo
		(apesar de não dar para ver tudo por conta do "()")
		depois verifica se o número de "(" é igual ao número de ")"
	'''
	def validate_expression(self, expression):
		expression = expression.replace(" ", "")
		regex = re.compile(r'[(]?[a-z0-9]+([?+*]?([)][?+*]?)?)([|]?[(]?[a-z0-9]+([?+*]?([)][?+*]?[)]?)?))*')
		match = regex.match(expression)

		open_count = expression.count("(")
		close_count = expression.count(")")

		if (open_count != close_count):
			return False
		try :
			if (match.group() == expression):
				return True
			else:
				return False
		except AttributeError:
			return False


'''
	
	Classe para definição de autômatos finitos determínisticos e não determínisticos
	e suas respectivas operações.

'''
class Automaton:
	'''
		Construtor que inicializa autômato com uma lista de estados(classe)
		e uma lista de símbolos do alfabeto
		verifica se é deterministico ou não , define o estado inicial(sempre o primeiro estado da lista de estados)
		e cria a lista de estados finais
	'''
	def __init__(self, states, alphabet):
		self.name = ""
		self.states = states
		self.alphabet = alphabet
		self.q0 = states[0]
		self.minimized = False
		self._set_finals()
		self.dfa_or_ndfa()
	def set_name(self, name):
		self.name = name
	def set_minimized(self):
		self.minimized = not self.minimized
	def _set_finals(self):
		self.f = [x for x in self.states if x.acceptance == True]
	def dfa_or_ndfa(self):
		self.non_deterministic = False
		for state in self.states:
			for trst in state.transitions:
				if any(x for x in state.transitions if trst.target != x.target and
													x.symbol == trst.symbol and
													trst != x):
					self.non_deterministic = True

	'''
		método para realização da determinização de autômatos.
		o algoritmo utilizado é o visto em sala
		o estado inicial é "copiado" para os estados determínisticos
		e suas transições por símbolo são unidas como se fossem um estado apenas.
		essas transições são então adicionadas ao conjunto de estados
		determínisticos e então são construídas suas transições
		a partir dos estados não deterministicos que compõem o estado
		determínistico.

		retorna então um AFD
	'''
	def ndfa_to_dfa(self):
		NDstates = self.states
		Dstates = []
		Dstates.append(State("["+NDstates[0].label+"]", NDstates[0].acceptance))
		for j in self.alphabet:
			tx = [x for x in NDstates[0].transitions if x.symbol == j]
			label = ""
			acceptance = False
			for k in tx:
				if k.target.acceptance:
					acceptance = True
				if k.target.label != "-":
					label += k.target.label
			if label == "":
				label = "-"
				new_state = State(label, acceptance)
			else :
				label = "".join(sorted(label))
				label = "["+label+"]"
				new_state = State(label, acceptance)
				Dstates.append(new_state)
			Dstates[0].add_transition(Transition(new_state, j))

		for d in Dstates:
			state = d.label
			if d != Dstates[0]:
				state = state[1:-1]
				for i in self.alphabet:
					tx = []
					label = ""
					acceptance = False
					for k in state:
						if k.isalpha():
							nd = next(x for x in NDstates if x.label == k or x.label == "["+k+"]")
							tx += [x for x in nd.transitions if x.symbol == i]
					for l in tx:
						if l.target.acceptance:
							acceptance = True
						if l.target.label != "-":
							if l.target.label not in label:
								label += l.target.label
					if label == "":
						label = "-"
						new_state = State(label, acceptance)
						d.add_transition(Transition(new_state, i))
					else:
						label = "".join(sorted(label))
						label = "["+label+"]" 
						new_state = State(label, acceptance)
						all_labels = [x.label for x in Dstates]
						if label not in all_labels:
							Dstates.append(new_state)
						d.add_transition(Transition(new_state, i))
		return Automaton(Dstates, self.alphabet)


	'''
		Método para minimizar um autômato.
		algoritmo utilizado é o algoritmo de Brzozowski.
		que consiste em inversões e determinizações seguidas
		para minimizar

		afd(min) = alc(det(rev(alc(det(rev(afd))))))
		o algoritmo diz que se eu inverter, determinizar um autômato
		e construir apenas os estados alcançaveis ei obtenho um afd
		minimo para o reverso daquela linguagem, repetindo o processo mais uma
		vez, eu obtenho o afd minimo para a linguagem inicial.

		retorna um AFD mínimo.
	'''
	def minimize(self):
		a1 = self.reverse()
		a2 = a1.ndfa_to_dfa() if a1.non_deterministic else a1
		a2.remove_unreachable_states()
		a2 = a2.reverse()
		a3 = a2.ndfa_to_dfa() if a2.non_deterministic else a2
		a3.merge_equal_states()
		a3.remove_unreachable_states()
		a3.remove_dead_states()
		return a3

	'''
		converte um autômato em uma gramática regular
		algoritmo utilizado o que foi visto em aula.
		onde os estados são os símbolos não terminais
		e o alfabeto os simbolos terminais
		as produções então são definidas
		se um estado S vai para um estado A por um símbolo a e esse estado não é final
		na gramática esse estado fica S-> aA
		se A for final
		S-> aA|a 
		e se o estado inicial S for de aceitação.
		S->&

		retorna uma gramática regular.
	'''
	def convert(self):
		vn = [x.label for x in self.states]
		vt = self.alphabet
		productions = ""
		if self.states[0].acceptance:
			productions += vn[0]+"->&|"
		else:
			productions += vn[0]+"->"

		empty_labels = [x.label for x in self.states if not any(y for y in x.transitions if y.target.label != "-")]
		for i in vn:
			transitions = next(x.transitions for x in self.states if x.label == i)
			non_empty = [y for y in transitions if y.target.label != "-"]
			if non_empty:
				if i != vn[0]:
					productions += i+"->"
				for j in transitions:
					if j.target.label != "-":
						if j.target.label not in empty_labels:
							productions += j.symbol+j.target.label+"|"
						if j.target.acceptance:
							productions += j.symbol+"|"
				productions = productions[:-1] + "\n"
		return RegularGrammar("$at", productions)

	'''
		Dado uma entrada, e um AFD
		verifica se a entrada inp é aceita por esse AFD
		completa o automato e vai percorrendo os estados.
		quando a entrada termina verifica se o estado no qual parou é de aceitação.
		e retorna true ou false
	'''
	def parse_input(self, inp):
		self.complete_automata()
		currState = self.q0
		for c in inp:
			txs = currState.transitions
			for x in txs:
				if x.symbol == c:
					currState = next(y for y in self.states if x.target.label == y.label)
					break
		if currState.acceptance:
			return True
		else:
			return False

	'''
		Gera todas as sequencias de tamanho n de caracteres do alfabeto
		e verifica quais são aceitos, juntando-os numa lista
		retorna essa lista.
	'''
	def enumerate(self, size):
		enum = []
		for item in itertools.product(self.alphabet, repeat=int(size)):
			if self.parse_input("".join(item)):
				enum.append("".join(item))
		return enum

	'''
		Completa o autômato.
		arruma as transições que não existem, colocando um '-'
		cria um estado phi (estado de erro)
		e todo estado que vai para o estado - agora vai para phi
		e phi vai para ele mesmo por todos os simbolos de alfabeto.

	'''
	def complete_automata(self):
		self.fix_transitions()
		phi = State("Ψ", False)
		alive = False
		if phi not in self.states:
			for a in self.alphabet:
				phi.add_transition(Transition(phi, a))
			for s in self.states:
				for t in s.transitions:
					if t.target.label == "-":
						alive = True
						t.target = phi
			if alive:
				self.states.append(phi)

	'''
		Operação de reverso no automato.
		cria um novo estado inicial.
		se o estado inicial de M é final o estado inicial de M' (novo estado criado)
		também é.
		para cada estado então as transições são invertidas
		se A vai para B por a em M, B vai para A por a em M'
		os finais de M não são mais finais em M'
		o inicial de M agora é final em M'
		o estado inicial novo de M' clona as transições dos que eram finais em M
		retorna M^r 
	'''
	def reverse(self):
		start_final = self.q0.acceptance
		new_q = State("Ω", start_final)
		states = [State(x.label) for x in self.states]

		for s in self.states:
			for t in s.transitions:
				if t.target.label != "-":
					state = next(x for x in states if x.label == t.target.label)
					target = next(x for x in states if s.label == x.label)
					state.add_transition(Transition(target, t.symbol))
				else:
					continue
		for s in states:
			if s.label == self.q0.label:
				s.set_acceptance(True)
			if s.label in [x.label for x in self.f]:
				for t in s.transitions:
					new_q.add_transition(Transition(t.target, t.symbol))

		new_states = []
		new_states.append(new_q)
		for x in states:
			new_states.append(x)

		for s in new_states:
			for c in self.alphabet:
				if c not in [t.symbol for t in s.transitions]:
					s.add_transition(Transition(State("-"), c))
		self.prettify(new_states)
		return Automaton(new_states, self.alphabet)

	'''
		realiza a união de dois automatos
		automaton = automato2
		é criado um estado inicial novo que é de aceitação se o estado de M1 ou de M2 são de aceitação
		são copiadas as transições do q0 de M1 e do q0 de M2 para esse estado novo
		os estados todos são copiados para M3
		retorna M3
	'''
	def union(self, automaton):
		new_start = State("Ω", (self.q0.acceptance or automaton.q0.acceptance))
		t1 = self.q0.transitions
		t2 = automaton.q0.transitions
		t3 = list(set(t1+t2))
		new_start.insert_transitions(t3)
		new_states = []
		new_states.append(new_start)
		new_states += self.states
		new_states += automaton.states

		automaton = Automaton(new_states, list(set(self.alphabet+automaton.alphabet)))
		automaton.fix_transitions()
		return automaton


	'''
		Complemento de AF
		completa o automato e transforma estados que são de aceitação em não aceitação
		e os de não aceitação em de aceitação.
	'''
	def complement(self):
		self.complete_automata()
		new_states = [State(x.label, not x.acceptance) for x in self.states]
		for s in new_states:
			s.insert_transitions(next(x.transitions for x in self.states if s.label == x.label))
		new_automaton = Automaton(new_states, self.alphabet)
		return new_automaton

	'''
		Método de intersecção de autômatos.
		A ∩ B = not(not(A) U not(b))
	'''
	def intersection(self, automaton):
		nota = self.complement()
		notb = automaton.complement()
		notaunotb = nota.union(notb)
		notaunotb.complete_automata()
		det_notaunotb = notaunotb.ndfa_to_dfa() if notaunotb.non_deterministic else notaunotb
		mini = det_notaunotb.minimize()
		final = mini.complement()
		intersect = []
		intersect.append(nota)
		intersect.append(notb)
		intersect.append(det_notaunotb)
		intersect.append(final)
		return intersect


	'''
		Método para realização da diferença de dois autômatos
		que aceitam duas LR's diferentes.

		L1-L2 = L1 ∩ NOT(L2) = NOT(NOT(L1) U L2)

	'''
	def difference(self, automaton):
		automaton.complete_automata()
		return self.intersection(self, automaton.complement())

	'''
		Método para remoção de estados mortos.
		cria uma lista de estados vivos e vai adicionando a esta lista
		estados que
		são finais / alcançam estados finais por 1 ou mais passos.
	'''
	def remove_dead_states(self):
		alive_states = []
		alive_states_before = 0
		while True:
			alive_states_before = len(alive_states)
			for sT in self.states:
				if sT.acceptance:
					if sT not in alive_states:
						alive_states.append(sT)
				for t in sT.transitions:
					if t.target.acceptance or t.target in alive_states:
						if sT not in alive_states:
							alive_states.append(sT)
			if len(alive_states) == alive_states_before:
				break
        
		self.states = [x for x in self.states if x in alive_states]
		
		if not self.states:
			self.states = State("ϴ")
		else:		
			for s in self.states:
				for t in s.transitions:
					if t.target.label not in [x.label for x in self.states]:
						s.replace_transition(Transition(State("-"), t.symbol), t)

	'''
		remoção de estados inalcançáveis.
		cria uma lista de estados alcançaveis.
		partindo de q0 os estados que são alcançáveis são adicionados a esta lista
		remove os que não estão nessa lista.
	'''
	def remove_unreachable_states(self):
		new_states = self.states
		reachable_states = []
		reachable_states.append(self.states[0])
		for s in reachable_states:
			for t in s.transitions:
				if t.target not in reachable_states:
					reachable_states.append(t.target)

		new_states = [x for x in self.states if x.label in [y.label for y in reachable_states]]
		self.states = new_states

	'''
		Fusão de estados iguais.
		o algoritmo de minimização em alguns casos cria estados que são iguais
		estaodos que vão para os mesmos estados por um mesmo símbolo.
		esses estados são juntados em um só, e não altera a linguagem.
	'''
	def merge_equal_states(self):
		new_states = []
		new_states.append(self.q0)
		for s in self.states:
			hit = False
			u = [x for x in new_states]
			tuples = [(t.target.label, t.symbol) for t in s.transitions]
			for x in u:
				if not set(tuples)-set([(y.target.label, y.symbol) for y in x.transitions]):
					hit = True
					if s.acceptance:
						x.set_acceptance(True)
					for k in self.states:
						for t in k.transitions:
							if t.target.label == s.label:
								k.replace_transition(Transition(x, t.symbol), t)
			if not hit:
				if s not in new_states:
					new_states.append(s)		
		self.states = new_states
	'''
	S->aS|a|b|bB
	B->bB|b
	A->0B|1C|1
	B->0A|1D|1
	C->0E|0|1F
	D->0E|0|1F
	E->0E|0|1F
	F->0F|1F

	S->aA|bS|b
	A->aS|bA|a
	'''

	'''
		"Embelezamento" dos nomes dos estados.
		altera o nome dos estados para facilitar leitura.
		algumas operações geram estados com nomes esquisitos.
	'''
	def prettify(self, states):
		for s in states:
			while True:
				new_label = random.choice(string.ascii_uppercase)
				if new_label not in [x.label for x in states]:
					s.change_label(new_label)
					break
	'''
		arruma as transições dos estados que teoricamente não existem
		coloca um estado "-"
	'''
	def fix_transitions(self):
		for c in self.alphabet:
			for s in self.states:
				if c not in (t.symbol for t in s.transitions):
					s.add_transition(Transition(State("-"), c))
	

'''
	Definição do estado dos AF's
'''
class State:
    def __init__(self, label, acceptance=False):
        self.acceptance = acceptance
        self.label = label
        self.transitions = []
    def __repr__(self):
        return self.label
    def set_acceptance(self, status):
        self.acceptance = status
    def change_label(self, nL):
        self.label = nL
    def insert_transitions(self, transitions):
        self.transitions=transitions
    def add_transition(self, transition):
        self.transitions.append(transition)
    def replace_transition(self, new_t, old_t):
        self.transitions[self.transitions.index(old_t)] = new_t
'''
	Definição das transições dos estados dos AF's
'''
class Transition:
    def __init__(self, target, symbol):
        self.symbol = symbol
        self.target = target
    def __eq__(self, other):
    	return self.target.label == other.target.label and self.symbol == other.symbol
    def __hash__(self):
    	return hash(('target_label', self.target.label, 'symbol', self.symbol))