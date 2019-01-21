# CSPSolver
Libreria in python per risolvere e rappresentare problemi di soddisfacimento di vincoli.

## Requisiti

Python versione >= 3.6

Per **Linux** e **MacOS** sono necessarie le librerie python [pycairo](https://cairographics.org/pycairo/) e [python-igraph](https://igraph.org/python/).

Per **Ubuntu** e derivati, seguire questi passi:
```
sudo apt-get install libcairo2-dev
sudo apt-get install libigraph0-dev

# da fare solo se su Ubuntu 16.04
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update

sudo apt-get install python3.6
sudo apt-get install python3-pip
sudo apt-get install python3.6-dev

python3.6 -m pip install pycairo
python3.6 -m pip install python-igraph
```

## Installazione

questa libreria può essere installata direttamente da github con il comando:

```
pip install git+https://github.com/AlexCovizzi/CSPSolver
```

## Esempio di utilizzo

```
import cspsolver

# instanzio il solver con algoritmo forward checking
solver = cspsolver.CSPSolver(cspsolver.Algorithm.ForwardChecking)

# aggiungo le variabili "a" e "b"
solver.add_variable("a", [1, 2, 3, 4])
solver.add_variable("b", [1, 2, 3, 4])

# aggiungo un vincolo unario per "a"
solver.add_constraint(("a",), lambda a: a == 4)
# aggiungo un vincolo binario tra "a" e "b"
solver.add_constraint(("a", "b"), lambda a, b: a == b + 2)

# risolvo il problema
solution = solver.solve()

# disegno il grafo dei vincoli
cspsolver.draw_constraint_graph(solver)
# disegno l'albero di decisione
cspsolver.draw_decision_tree(solver)

```
