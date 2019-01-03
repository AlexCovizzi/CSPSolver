from typing import Callable, Dict, Tuple, List
from copy import deepcopy
from CSPNode import CSPNode
from CSPConstraints import CSPConstraints
from CSPVariable import CSPVariable
from CSPAlgorithm import CSPAlgorithm
from CSPPolicy import CSPPolicy

class CSPSolver:
    # init
    def __init__(self, algorithm: Callable[[CSPNode, CSPConstraints, int], bool] = CSPAlgorithm.StandardBacktracking,
                 policy: Callable[[CSPNode, int], bool] = CSPPolicy.InsertOrder,
                 step_arc_consistency: bool = False):
        self._constraints: CSPConstraints = CSPConstraints()
        self._root = CSPNode(None, [])
        self._solutions: List[CSPNode] = []
        self._found_solution = False
        self._algorithm = algorithm
        self._policy = policy
        self._step_arc_consistency = step_arc_consistency
        
    # Add a constraint
    def add_constraint(self, variables: Tuple[str, ...], constraint: Callable):
        variables_len = len(variables)
        if variables_len > 2:
            raise ValueError("Too many variables (max 2)")
        
        # Are there variables not in this problem?
        for v in variables:
            if not self._root.get_variable_by_name(v):
                raise ValueError("The variable " + v + " is not a variable in this problem.")
        
        self._constraints.add_constraint(variables, constraint)

    # Add a variable
    def add_variable(self, name: str, domain: List):
        new_variable = CSPVariable(name, domain)
        self._root.add_variable(new_variable)

    # Print problem variables
    def show_variables(self):
        pass

    # Print problem constraints
    def show_constraints(self):
        pass

    def _next_step(self, current_node: CSPNode, tree_depth: int, one_solution: bool):
        # assegno la variabile e faccio uno snapshot delle variabili
        # in questo modo se quella assegnazione fallisce, posso tornare allo snapshot
        print("Passo " + str(tree_depth))
        variable = self._policy(current_node, tree_depth)
        
        # ciclo sui valori della variabile da assegnare
        for value in variable.domain:
            # Costruiamo il prossimo nodo
            child_node = CSPNode(current_node, deepcopy(current_node.get_variables()))
            current_node.add_child(child_node)

            # Assegna un valore alla variabile da assegnare
            child_node.get_variable_by_name(variable.name).assign_value(value)

            # Algoritmo applicato al child node: i domini delle variabili non assegnate verranno modificati (a seconda dell'algoritmo scelto)
            if self._algorithm(child_node, self._constraints, tree_depth, variable.name):
                if self._step_arc_consistency:
                    if not self.apply_arc_consistency(child_node):
                        child_node.set_failure()
                        continue
                
                if tree_depth + 1 == len(child_node.get_variables()):
                    child_node.set_solution()
                    self._solutions.append(child_node)
                    
                    # Voglio una sola soluzione: blocco tutti i cicli
                    if one_solution: # one_solution è un parametro indicato dal'utente
                        self._found_solution = True
                        break
                else:
                    self._next_step(child_node, tree_depth + 1, one_solution)
                    if self._found_solution:
                        break
            else:
                # Descrizione del fallimento
                print("Fallimento")
                child_node.set_failure()
    
    def solve(self, one_solution: bool = True):
        self._next_step(self._root, 0, one_solution)
        
    
    def apply_arc_consistency(self, node: CSPNode):
        return True

    def apply_node_consistency(self, node: CSPNode):
        return True

    def print_tree(self):
        self._print_node(self._root)
        
    def _print_node(self, node: CSPNode):
        print(node)
        for child in node.get_children():
            self._print_node(child)