# Finite Automata Simulator

## Informații

| | |
|---|---|
| **Student** | Samoilă Rareș |
| **Laborant** | Mocanu Ștefan |
| **Disciplina** | Limbaje Formale și Automate |
| **Facultatea** | Matematică și Informatică, UniBuc |
| **An / Semestru** | Anul I, Semestrul II |

---

## Descriere

Temă numărul 1 — implementarea unui simulator de automate finite în Python, capabil să lucreze cu trei tipuri de automate: **DFA** (Automat Finit Determinist), **NFA** (Automat Finit Nedeterminist) și **λ-NFA** (Automat Finit Nedeterminist cu tranziții lambda).

Simulatorul citește definiția automatului dintr-un fișier text și testează o listă de cuvinte, afișând pentru fiecare dacă este **ACCEPTAT** sau **RESPINS**.

---

## Clase implementate

### `DFA` — Automat Finit Determinist
Modelează un automat în care din fiecare stare, pe fiecare simbol, există cel mult o tranziție.

| Membru | Tip | Descriere |
|--------|-----|-----------|
| `states` | `set` | Mulțimea stărilor Q |
| `alphabet` | `set` | Alfabetul Σ |
| `start` | `str` | Starea inițială q₀ |
| `final` | `set` | Mulțimea stărilor finale F |
| `transitions` | `dict` | δ: (stare, simbol) → stare |

**Funcții publice:** `simulate(word)`, `__repr__()`

---

### `NFA` — Automat Finit Nedeterminist
Modelează un automat în care dintr-o stare, pe un simbol, pot exista mai multe tranziții posibile.

| Membru | Tip | Descriere |
|--------|-----|-----------|
| `states` | `set` | Mulțimea stărilor Q |
| `alphabet` | `set` | Alfabetul Σ |
| `start` | `str` | Starea inițială q₀ |
| `final` | `set` | Mulțimea stărilor finale F |
| `transitions` | `dict` | δ: (stare, simbol) → mulțime de stări |

**Funcții publice:** `simulate(word)`, `_step(current_states, symbol)`, `__repr__()`

---

### `LNFA` — Automat Finit Nedeterminist cu tranziții λ
Extinde NFA-ul cu suport pentru tranziții lambda (tranziții pe cuvântul vid), reprezentate intern prin `!`.

| Membru | Tip | Descriere |
|--------|-----|-----------|
| `states` | `set` | Mulțimea stărilor Q |
| `alphabet` | `set` | Alfabetul Σ |
| `start` | `str` | Starea inițială q₀ |
| `final` | `set` | Mulțimea stărilor finale F |
| `transitions` | `dict` | δ: (stare, simbol/λ) → mulțime de stări |
| `LAMBDA` | `str` | Constanta `'!'` pentru tranziția vidă |

**Funcții publice:** `simulate(word)`, `lambda_closure(states)`, `__repr__()`

---

## Funcționalități

- Parsare automată a tipului de automat din fișier (`type DFA / NFA / LNFA`)
- Simulare pas cu pas a cuvintelor pe automat
- Calcul **λ-closure** prin BFS pentru λ-NFA
- Suport pentru **cuvântul vid** (`lambda` sau `!` în fișierul de cuvinte)
- Afișare formatată a automatului (stări, alfabet, tranziții)

---

## Format fișiere de intrare

### Fișier automat (ex: `automat_dfa.txt`)
```
type DFA
states q0 q1
alphabet a b
start q0
final q1
transitions
q0 a q0
q0 b q1
q1 a q0
q1 b q1
```

> Pentru λ-NFA, tranzițiile lambda se specifică cu `lambda` sau `!` ca simbol.

### Fișier cuvinte (ex: `cuvinte.txt`)
```
lambda
a
ab
aab
```

> `lambda` sau `!` reprezintă cuvântul vid ε.

---

## Exemple incluse

| Fișier | Tip | Limbaj acceptat |
|--------|-----|-----------------|
| `automat_dfa.txt` | DFA | Cuvinte peste `{a,b}` care se termină în `b` |
| `automat_nfa.txt` | NFA | Cuvinte peste `{a,b}` care conțin `ab` ca subșir |
| `automat_lnfa.txt` | λ-NFA | Cuvinte de forma `a*b*` |

---

## Rulare

```bash
python main.py <fisier_automat> <fisier_cuvinte>
```

**Exemple:**
```bash
python main.py automat_dfa.txt cuvinte.txt
python main.py automat_nfa.txt cuvinte.txt
python main.py automat_lnfa.txt cuvinte.txt
```

**Ieșire exemplu:**
```
=== DFA ===
  Stari:          ['q0', 'q1']
  Alfabet:        ['a', 'b']
  Stare initiala: q0
  Stari finale:   ['q1']
  Tranzitii:
    delta(q0, a) = q0
    delta(q0, b) = q1
    ...

=== Rezultate ===
  'lambda' -> RESPINS
  'ab'     -> ACCEPTAT
  'ba'     -> RESPINS
```

---

## Structura repository

```
lfa-tema1/
├── main.py              # Codul sursă principal
├── automat_dfa.txt      # Exemplu DFA
├── automat_nfa.txt      # Exemplu NFA
├── automat_lnfa.txt     # Exemplu λ-NFA
├── cuvinte.txt          # Cuvinte de testat
└── README.md
```
