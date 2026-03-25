import sys # modulul sys ne permite sa citim argumentele din linia de comanda
from collections import deque # deque e o coada eficienta, o folosim in bfs pentru lambda-closure

class DFA:
    def __init__(self, states, alphabet, start, final, transitions):
        self.states = states # q: multimea tuturor starilor
        self.alphabet = alphabet # sigma: simbolurile acceptate
        self.start = start # q0: starea de start
        self.final = final # f: starile finale
        self.transitions = transitions # delta: dictionar cu cheia (stare, simbol) si valoarea starea urmatoare

    def simulate(self, word):
        current = self.start # pornim din starea initiala

        for symbol in word: # parcurgem cuvantul simbol cu simbol
            if symbol not in self.alphabet: # daca simbolul nu e in alfabet
                return False # respingem imediat
            if (current, symbol) not in self.transitions: # daca nu exista tranzitie definita
                return False # dfa s-a blocat, deci respins
            current = self.transitions[(current, symbol)] # trecem in starea urmatoare

        return current in self.final # acceptat daca starea finala e in f

    def __repr__(self):
        lines = [ # construim un sir de linii pentru afisare
            "=== DFA ===",
            f"  Stari:          {sorted(self.states)}", # sorted afiseaza sortat alfabetic
            f"  Alfabet:        {sorted(self.alphabet)}",
            f"  Stare initiala: {self.start}",
            f"  Stari finale:   {sorted(self.final)}",
            "  Tranzitii:"
        ]
        for (s, a), t in sorted(self.transitions.items()): # iteram prin toate tranzitiile sortate
            lines.append(f"    delta({s}, {a}) = {t}") # adaugam fiecare tranzitie formatata
        return "\n".join(lines) # unim liniile cu newline si returnam un string

class NFA:
    def __init__(self, states, alphabet, start, final, transitions):
        self.states = states # q: multimea starilor
        self.alphabet = alphabet # sigma: alfabetul
        self.start = start # q0: starea initiala
        self.final = final # f: starile finale
        self.transitions = transitions # delta: dictionar cu cheia (stare, simbol) si valoarea un set de stari

    def _step(self, current_states, symbol):
        # calculeaza multimea starilor urmatoare dintr-o multime de stari curente si un simbol
        next_states = set() # initializam multimea rezultat vida
        for state in current_states: # pentru fiecare stare activa
            next_states |= self.transitions.get((state, symbol), set()) # reuniune cu destinatiile posibile
        return next_states # returnam toate starile posibile dupa acest simbol

    def simulate(self, word):
        current_states = {self.start} # incepem cu multimea ce contine doar starea initiala

        for symbol in word: # parcurgem cuvantul simbol cu simbol
            if symbol not in self.alphabet: # simbol necunoscut, respins
                return False
            current_states = self._step(current_states, symbol) # calculam urmatoarea multime de stari
            if not current_states: # daca multimea e vida, toate ramurile au murit, respins
                return False

        return bool(current_states & self.final) # acceptam daca cel putin o stare curenta e finala

    def __repr__(self):
        lines = [
            "=== NFA ===",
            f"  Stari:          {sorted(self.states)}",
            f"  Alfabet:        {sorted(self.alphabet)}",
            f"  Stare initiala: {self.start}",
            f"  Stari finale:   {sorted(self.final)}",
            "  Tranzitii:"
        ]
        for (s, a), ts in sorted(self.transitions.items()): # ts = multimea de stari destinatie
            lines.append(f"    delta({s}, {a}) = {sorted(ts)}")
        return "\n".join(lines)

class LNFA:
    LAMBDA = '!' # simbolul intern pentru tranzitia vida (lambda/epsilon)

    def __init__(self, states, alphabet, start, final, transitions):
        self.states = states # q: multimea starilor
        self.alphabet = alphabet # sigma: alfabetul
        self.start = start # q0: starea initiala
        self.final = final # f: starile finale
        self.transitions = transitions # delta: dictionar cu seturi, simbolul poate fi ! pentru lambda

    def lambda_closure(self, states):
        # calculeaza toate starile accesibile din states folosind doar tranzitii lambda
        closure = set(states) # inchiderea contine initial starile de pornire
        queue = deque(states) # initializam coada bfs cu starile de pornire

        while queue: # cat timp mai avem stari de explorat
            state = queue.popleft() # scoatem prima stare din coada
            for next_state in self.transitions.get((state, self.LAMBDA), set()): # luam destinatiile pe lambda
                if next_state not in closure: # daca nu am vizitat-o deja, evitam bucle infinite
                    closure.add(next_state) # o adaugam in inchidere
                    queue.append(next_state) # o punem in coada ca s-o exploram

        return closure # returnam multimea completa de stari accesibile pe lambda

    def simulate(self, word):
        current_states = self.lambda_closure({self.start}) # starea initiala e lambda-closure a lui q0

        for symbol in word: # parcurgem cuvantul simbol cu simbol
            if symbol not in self.alphabet: # simbol necunoscut, respins
                return False

            next_states = set() # initializam multimea starilor urmatoare
            for state in current_states: # pentru fiecare stare activa
                next_states |= self.transitions.get((state, symbol), set()) # calculam starile pe simbol

            current_states = self.lambda_closure(next_states) # aplicam lambda-closure pe rezultat

            if not current_states: # nicio stare activa, respins
                return False

        return bool(current_states & self.final) # acceptat daca cel putin o stare finala e activa

    def __repr__(self):
        lines = [
            "=== lambda-NFA ===",
            f"  Stari:          {sorted(self.states)}",
            f"  Alfabet:        {sorted(self.alphabet)}",
            f"  Stare initiala: {self.start}",
            f"  Stari finale:   {sorted(self.final)}",
            "  Tranzitii (! = lambda):"
        ]
        for (s, a), ts in sorted(self.transitions.items()):
            lines.append(f"    delta({s}, {a}) = {sorted(ts)}")
        return "\n".join(lines)

def parse_automat(filename):
    automat_type = None # tipul automatului: dfa, nfa sau lnfa
    states = set() # multimea starilor q
    alphabet = set() # alfabetul sigma
    start = None # starea initiala q0
    final = set() # starile finale f
    transitions_dfa = {} # pentru dfa: cheia (stare,simbol) valoarea starea urmatoare
    transitions_nfa = {} # pentru nfa/lnfa: cheia (stare,simbol) valoarea un set de stari
    reading_transitions = False # flag care indica daca suntem in sectiunea de tranzitii

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip() # eliminam spatiile si newline-urile de la capete

            if not line or line.startswith('#'): # sarim liniile goale si comentariile
                continue

            if line == 'transitions': # am ajuns la sectiunea de tranzitii
                reading_transitions = True # activam flag-ul
                continue # trecem la linia urmatoare

            if reading_transitions: # daca suntem in sectiunea de tranzitii
                parts = line.split() # impartim linia in cuvinte
                if len(parts) < 3: # o tranzitie valida are 3 parti
                    continue # linie invalida, o sarim

                from_state = parts[0] # prima parte: starea sursa
                symbol = parts[1] # a doua parte: simbolul
                to_state = parts[2] # a treia parte: starea destinatie

                if symbol == 'lambda': # normalizam lambda in !
                    symbol = '!'

                transitions_dfa[(from_state, symbol)] = to_state # pentru dfa ultimul suprascrie

                key = (from_state, symbol) # cheia pentru dictionarul nfa
                if key not in transitions_nfa: # daca e prima tranzitie cu aceasta cheie
                    transitions_nfa[key] = set() # initializam un set gol
                transitions_nfa[key].add(to_state) # adaugam destinatia in set
                continue

            parts = line.split() # impartim linia in cuvinte
            keyword = parts[0].lower() # primul cuvant e keyword-ul
            values = parts[1:] # restul sunt valorile

            if keyword == 'type': # linia type dfa/nfa/lnfa
                automat_type = values[0].upper()

            elif keyword == 'states': # linia states q0 q1 q2 ...
                states = set(values)

            elif keyword == 'alphabet': # linia alphabet a b c ...
                alphabet = set(values)

            elif keyword == 'start': # linia start q0
                start = values[0]

            elif keyword == 'final': # linia final q2 q3 ...
                final = set(values)

    if automat_type is None:
        raise ValueError("lipseste type dfa/nfa/lnfa din fisier.")
    if start is None:
        raise ValueError("lipseste start stare din fisier.")
    if not states:
        raise ValueError("lipseste states din fisier.")

    if automat_type == 'DFA':
        return DFA(states, alphabet, start, final, transitions_dfa) # construim dfa cu dict simplu
    elif automat_type == 'NFA':
        return NFA(states, alphabet, start, final, transitions_nfa) # construim nfa cu dict de seturi
    elif automat_type == 'LNFA':
        return LNFA(states, alphabet, start, final, transitions_nfa) # construim lnfa cu dict de seturi
    else:
        raise ValueError(f"tip necunoscut: {automat_type}. foloseste dfa, nfa sau lnfa.")

def read_words(filename):
    words = [] # lista in care acumulam cuvintele
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip() # eliminam spatiile si newline-urile
            if not line or line.startswith('#'): # sarim liniile goale si comentariile
                continue
            if line in ('lambda', '!'): # lambda sau ! reprezinta cuvantul vid
                words.append('') # adaugam sirul gol
            else:
                words.append(line) # adaugam cuvantul normal
    return words # returnam lista de cuvinte

def main():
    if len(sys.argv) != 3: # verificam ca avem exact 2 argumente in linia de comanda
        print("utilizare: python main2.py <fisier_automat> <fisier_cuvinte>")
        sys.exit(1) # iesim cu eroare

    automat_file = sys.argv[1] # primul argument: fisierul cu automatul
    words_file = sys.argv[2] # al doilea argument: fisierul cu cuvintele de testat

    automat = parse_automat(automat_file) # citim si construim automatul din fisier
    words = read_words(words_file) # citim lista de cuvinte

    print(automat) # afisam automatul
    print()

    print("=== Rezultate ===")
    for word in words: # iteram prin fiecare cuvant
        result = automat.simulate(word) # simulam automatul pe cuvant
        verdict = "ACCEPTAT" if result else "RESPINS" # convertim true/false in text
        display = word if word else "lambda" # afisam lambda in loc de sir gol
        print(f"  '{display}' -> {verdict}")

if __name__ == '__main__': # rulam main doar daca fisierul e executat direct
    main()
