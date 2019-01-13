from typing import Callable, Dict, Tuple, List, TextIO, Union, Any, Optional
import sys
from copy import deepcopy
from .node import Node
from .constraints import Constraints
from .variable import Variable
from .algorithm import Algorithm
from .policy import Policy

class CSPSolver:
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
        
    # Add a constraint
    def add_constraint(self, variables: Union[Tuple[str], Tuple[str, str]], constraint: Callable):
        # Are there variables not in this problem?
        for v in variables:
            if not self._root.get_variable_by_name(v):
                raise ValueError("The variable " + v + " is not a variable in this problem.")
        
        self._constraints.add_constraint(variables, constraint)

    # Add a variable
    def add_variable(self, name: str, domain: List):
        new_variable = Variable(name, domain)
        self._root.add_variable(new_variable)

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
    
    def solve(self, one_solution: bool = True, target: Optional[TextIO] = None):
        if target: print(str(self._root), file = target)

        self._next_step(self._root, 0, one_solution, target)
    
    def apply_arc_consistency(self, node: Optional[Node]=None, target: Optional[TextIO] = None):
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
                            return False

        if target: print("Le variabili sono arc-consistenti.", file = target)
        return True

    def apply_node_consistency(self, node: Optional[Node] = None, target: Optional[TextIO] = None):
        if target: print("Applico node-consistency...", file = target)
        if not node:
            node = self._root

        for variable in node.get_variables():
            for value in variable.domain[:]:
                if not self._constraints.verify({variable.name: value}):
                    variable.delete_value(value)
                    if not variable.domain:
                        return False
                
        self.is_node_consistent = True

        if target: print("Le variabili sono node-consistenti.", file = target)
        return True

    def __str__(self):
        return "Nodo radice del problema:\n" + str(self._root)

    def print_decision_tree(self, target: TextIO = sys.stdout):
        self._print_node(self._root, 0, target)
        
    def _print_node(self, node: Node, index: int, target: TextIO = sys.stdout):
        print(str(index) + " - " + str(node), file = target)
        index += 1
        for child in node.get_children():
            index = self._print_node(child, index, target)
        return index
    
    def print_solutions(self, target: TextIO = sys.stdout):
        if self._solutions:
            print("Le soluzioni trovate sono:", file = target)
            for solution in self._solutions:
                print(solution, file = target)
        else:
            print("Non sono state trovate soluzioni", file = target)