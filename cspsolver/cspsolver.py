from typing import Callable, Dict, Tuple, List, TextIO, Union, Any, Optional
import sys
from copy import deepcopy
from .node import Node
from .constraints import Constraints
from .variable import Variable
from .algorithm import Algorithm
from .policy import Policy

class CSPSolver:
    """
    Classe principale per la risoluzione di csp.

    Esempio:
    --------
      # istanzio la classe cspsolver.CSPSolver
      solver = CSPSolver()

      # aggiungo variabili al problema
      solver.add_variable("a", [1, 2, 3])

      # aggiungo vincoli al problema
      solver.add_constraint(("a",), lambda a: a > 1)

      # risolvo
      solver.solve()

    per esempi più complessi vedi la cartella examples/

    Parametri
    -------
    algorithm : Callable[[Node, Constraints, int, str, Optional[TextIO]], bool] = StandardBacktracking
        Funzione che viene chiamata dopo ogni assegnazione.
        Per maggiori info vedi la classe cspsolver.Algorithm,
        nella classe cspsolver.Algorithm sono già implementati questi algoritmi:
          - GenerateAndTest
          - StandardBacktracking (default)
          - ForwardChecking
          - PartialLookAhead
          - FullLookAhead
    policy : Callable[[Node, Constraints, int], Variable] = InsertOrder
        Funzione chiamata prima dell'assegnazione di una variabile,
        serve a decidere quale variabile verrà assegnata.
        Per maggiori info vedi la classe cspsolver.Policy,
        nella classe cspsolver.Policy sono già implementati questi algoritmi:
          - InsertOrder (default)
          - MinimumRemainingValues
          - MostConstrainedPrinciple
    step_arc_consistency: bool = False
        booleano che determina se applicare o no
        la arc-consistency dopo ogni assegnazione

    """
    # init
    def __init__(self, algorithm: Callable[[Node, Constraints, int, str, Optional[TextIO]], bool] = Algorithm.StandardBacktracking,
                 policy: Callable[[Node, Constraints, int], Variable] = Policy.InsertOrder,
                 step_arc_consistency: bool = False):
        self._constraints: Constraints = Constraints()
        self._root = Node(None, [])
        self._solutions: List[Node] = []
        self._found_solution = False
        self._algorithm = algorithm
        self._policy = policy
        self._step_arc_consistency = step_arc_consistency
        self._is_node_consistent = False

    # Add a variable
    def add_variable(self, name: str, domain: List):
        """
        Aggiunge una variabile al problema con il nome e il dominio forniti.

        Esempio
        -------
          # aggiungo la variabile "a" con dominio 1, 2, 3
          solver.add_variable("a", [1, 2, 3])

        Parametri
        -------
        name : str
            nome della variabile da aggiungere
        domain : List
            dominio della variabile da aggiungere.
        """
        new_variable = Variable(name, domain)
        self._root.add_variable(new_variable)

    def add_variables(self, names: List[str], domain: List):
        """
        Aggiunge variabili al problema con i nomi e il dominio forniti.

        Esempio
        -------
          # aggiungo le variabile "a", "b", "c" con dominio 1, 2, 3
          solver.add_variable(["a", "b", "c"], [1, 2, 3])

        Parametri
        -------
        names : List[str]
            i nomi delle variabili da aggiungere.
        domain : List
            dominio delle variabili da aggiungere.
        """
        for name in names:
            self.add_variable(name, domain)
        
    def add_constraint(self, variables: Union[Tuple[str], Tuple[str, str]], constraint: Callable):
        """
        Aggiunge un vincolo tra le variabili fornite nella tupla.
        
        Esempio
        -------
          # aggiungo un vincolo di diverso
          # tra le variabili "a" e "b"
          solver.add_constraint(("a", "b"), lambda a, b: a != b)

        Parametri
        -------
        variables : Tuple[str] or Tuple[str, str]
            tupla che descrive su quali variabili è il vincolo.
        constraint : Callable[..., bool]
            funzione che descrive il vincolo tra le variabili
            (o la variabile) nella tupla.
            Questa funzione deve restituire un booleano.
            Attenzione: l'ordine dei parametri della funzione
            è lo stesso delle variabili fornite nella tupla,
            quindi per esempio:
              solver.add_constraint(("a", "b"), lambda Va, Vb: Va > Vb)
            è diverso da:
              solver.add_constraint(("a", "b"), lambda Vb, Va: Va > Vb)
            Poichè nel primo caso la variabile di nome "a"
            sarà associata al parametro Va, mentre nel secondo caso
            sarà associata al parametro Vb
        
        Errors
        ------
        ValueError
            se la variabile nella tupla non è una variabile del problema
        """
        # Are there variables not in this problem?
        for v in variables:
            if not self._root.get_variable_by_name(v):
                raise ValueError("The variable " + v + " is not a variable in this problem.")
        
        self._constraints.add_constraint(variables, constraint)
    
    def solve(self, one_solution: bool = True, target: Optional[TextIO] = None) -> List[Node]:
        """
        Risolvi il problema costituito dalle variabili e dai vincoli forniti.
        
        Esempio
        -------
          # risolvi il problema e
          # stampa i passi svolti a video
          solver.solve(target: sys.stdout)

        Parametri
        -------
        one_solution : bool = True
            booleano che indica se fermarsi o no alla prima soluzione trovata.
        target : TextIO = None
            indica dove stampare i passi svolti per la risoluzione del problema.
            se il target è None (default) non verrà stampato nulla.
            target può essere qualsiasi output su cui si può scrivere,
            es. sys.stdout, oppure f = open("file.txt", "w+")

        Return
        -------
        List[Node]
            Restituisce la lista delle soluzioni o
            una lista vuota se non ci sono soluzioni
        """
        if target: print(str(self._root), file = target)

        self._next_step(self._root, 0, one_solution, target)

        return self._solutions
    
    def apply_node_consistency(self, node: Optional[Node] = None, target: Optional[TextIO] = None) -> bool:
        """
        Applica la node consistency.

        Parametri
        -------
        node : Node = None
            nodo su cui applicare la node consistency,
            se nessun nodo è passato sarà applicato al
            nodo root, ovvero alla situazione iniziale
        target : TextIO = None
            indica dove stampare i passi svolti dalla node consistency.
            se il target è None (default) non verrà stampato nulla.
            target può essere qualsiasi output su cui si può scrivere,
            es. sys.stdout, oppure f = open("file.txt", "w+")

        Return
        -------
        bool
            True se le variabili sono node consistenti, altrimenti False
        """

        if target: print("Applico node-consistency...", file = target)

        if not node:
            node = self._root

        for variable in node.get_variables():
            for value in variable.domain[:]:
                if not self._constraints.verify({variable.name: value}):
                    variable.delete_value(value)
                    if not variable.domain:
                        if target: print(f"La variabile {variable.name} non è node-consistente.", file = target)
                        return False
                
        self.is_node_consistent = True

        if target: print("Le variabili sono node-consistenti.", file = target)

        return True
    
    def apply_arc_consistency(self, node: Optional[Node]=None, target: Optional[TextIO] = None) -> bool:
        """
        Applica la arc consistency.

        Parametri
        -------
        node : Node = None
            nodo su cui applicare la arc consistency,
            se nessun nodo è passato sarà applicato al
            nodo root, ovvero alla situazione iniziale
        target : TextIO = None
            indica dove stampare i passi svolti dalla node consistency.
            se il target è None (default) non verrà stampato nulla.
            target può essere qualsiasi output su cui si può scrivere,
            es. sys.stdout, oppure f = open("file.txt", "w+")

        Return
        -------
        bool
            True se le variabili sono arc consistenti, altrimenti False
        """

        if target: print("Applico arc-consistency...", file = target)

        if not node:
            node = self._root
        
        if not self.is_node_consistent:
            if not self.apply_node_consistency(node):
                return False

        for variable_1 in node.get_variables():
            for variable_2 in [v for v in node.get_variables() if not v.value and variable_1.name != v.name]:
                # La variabile 1 è assegnata: potrà cambiare solo il dominio della variabile 2
                if variable_1.value:
                    for value_2 in variable_2.domain[:]:
                        if not self._constraints.verify({variable_1.name: variable_1.value, variable_2.name: value_2}):
                            variable_2.delete_value(value_2)

                            if target: print(f"{variable_2.name} = {value_2} non e' compatibile con {variable_1.name} = {variable_1.value}" +
                                                f" -> Nuovo dominio di {variable_2.name}: {variable_2.domain}", file = target)

                            if not variable_2.domain:
                                if target: print("Le variabili non sono arc-consistenti.", file = target)
                                return False
                # La variabile 1 non è assegnata: potranno cambiare entrambi i domini
                else:
                    for value_1 in variable_1.domain[:]:
                        delete_value = True

                        for value_2 in variable_2.domain:
                            if self._constraints.verify({variable_1.name: value_1, variable_2.name: value_2}):
                                delete_value = False
                        
                        if delete_value:
                            variable_1.delete_value(value_1)

                            if target: print(f"{variable_1.name} = {value_1} non e' compatibile con i valori di {variable_2.name}" +
                                                f" -> Nuovo dominio di {variable_1.name}: {variable_1.domain}", file = target)
                    
                        if not variable_1.domain:
                            if target: print("Le variabili non sono arc-consistenti.", file = target)
                            return False

        if target: print("Le variabili sono arc-consistenti.", file = target)
        return True

    def _next_step(self, current_node: Node, tree_depth: int, one_solution: bool, target: Optional[TextIO]):
        # assegno la variabile e faccio uno snapshot delle variabili
        # in questo modo se quella assegnazione fallisce, posso tornare allo snapshot
        variable = self._policy(current_node, self._constraints, tree_depth)
        
        # ciclo sui valori della variabile da assegnare
        for value in variable.domain:
            # Costruiamo il prossimo nodo
            child_node = Node(current_node, deepcopy(current_node.get_variables()))
            current_node.add_child(child_node)

            # Assegna un valore alla variabile da assegnare
            child_node.assign_variable(variable.name, value)

            if target: print(f"Assegno: {variable.name} = {value}", file = target)

            # Algoritmo applicato al child node: i domini delle variabili non assegnate verranno modificati (a seconda dell"algoritmo scelto)
            if self._algorithm(child_node, self._constraints, tree_depth, variable.name, target):
                if self._step_arc_consistency:
                    if not self.apply_arc_consistency(child_node, target):
                        if target: print(f"Assegnamento {variable.name} = {value} fallito", file = target)
                        child_node.set_failure()
                        continue
                
                if tree_depth + 1 == len(child_node.get_variables()):
                    child_node.set_solution()
                    self._solutions.append(child_node)
                    if target: print(str(child_node) + "\n", file = target)
                    
                    # Voglio una sola soluzione: blocco tutti i cicli
                    if one_solution: # one_solution è un parametro indicato dal"utente
                        self._found_solution = True
                        break
                else:
                    self._next_step(child_node, tree_depth + 1, one_solution, target)
                    if self._found_solution:
                        break
            else:
                # Descrizione del fallimento
                if target: print(f"Assegnamento {variable.name} = {value} fallito", file = target)
                child_node.set_failure()

    def __str__(self):
        return "Nodo radice del problema:\n" + str(self._root)

    def print_decision_tree(self, target: TextIO = sys.stdout):
        """
        Stampa l'albero di decisione.
        Verranno stampati tutti nodi dell'albero di decisione,
        seguendo una esplorazione di tipo depth-first
        """
        self._print_node(self._root, 0, target)
    
    def print_solutions(self, target: TextIO = sys.stdout):
        """
        Stampa le soluzioni.
        """
        if self._solutions:
            print("Le soluzioni trovate sono:", file = target)
            for solution in self._solutions:
                print(solution, file = target)
        else:
            print("Non sono state trovate soluzioni", file = target)
        
    def _print_node(self, node: Node, index: int, target: TextIO = sys.stdout):
        print(str(index) + " - " + str(node), file = target)
        index += 1
        for child in node.get_children():
            index = self._print_node(child, index, target)
        return index