from typing import Callable, Dict, Tuple, List
from copy import deepcopy
from CSPNode import CSPNode
from CSPConstraints import CSPConstraints
from CSPVariable import CSPVariable
from CSPAlgorithm import CSPAlgorithm
from CSPPolicy import CSPPolicy

class CSPSolver:
    # init
    def __init__(self, algorithm: Callable[[CSPNode, CSPConstraints, int, str], bool] = CSPAlgorithm.StandardBacktracking,
                 policy: Callable[[CSPNode, int], bool] = CSPPolicy.InsertOrder,
                 step_arc_consistency: bool = False):
        self._constraints: CSPConstraints = CSPConstraints()
        self._root = CSPNode(None, [])
        self._solutions: List[CSPNode] = []
        self._found_solution = False
        self._algorithm = algorithm
        self._policy = policy
        self._step_arc_consistency = step_arc_consistency
        self.is_node_consistent = False
        
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
        variable = self._policy(current_node, self._constraints, tree_depth)
        
        # ciclo sui valori della variabile da assegnare
        for value in variable.domain:

            # Costruiamo il prossimo nodo
            child_node = CSPNode(current_node, deepcopy(current_node.get_variables()))
            current_node.add_child(child_node)

            # Assegna un valore alla variabile da assegnare
            child_node.assign_variable(variable.name, value)

            # Algoritmo applicato al child node: i domini delle variabili non assegnate verranno modificati (a seconda dell"algoritmo scelto)
            if self._algorithm(child_node, self._constraints, tree_depth, variable.name):
                if self._step_arc_consistency:
                    if not self.apply_arc_consistency(child_node):
                        child_node.set_failure()
                        continue
                
                if tree_depth + 1 == len(child_node.get_variables()):
                    child_node.set_solution()
                    self._solutions.append(child_node)
                    
                    # Voglio una sola soluzione: blocco tutti i cicli
                    if one_solution: # one_solution è un parametro indicato dal"utente
                        self._found_solution = True
                        break
                else:
                    self._next_step(child_node, tree_depth + 1, one_solution)
                    if self._found_solution:
                        break
            else:
                # Descrizione del fallimento
                child_node.set_failure()
    
    def solve(self, one_solution: bool = True):
        self._next_step(self._root, 0, one_solution)
        
    
    def apply_arc_consistency(self, node: CSPNode=None):
        if not node:
            node = self._root
        
        if not self.is_node_consistent:
            self.apply_node_consistency(node)

        for variable_1 in node.get_variables():
            for variable_2 in [v for v in node.get_variables() if not v.value and variable_1.name != v.name]:
                # La variabile 1 è assegnata: potrà cambiare solo il dominio della variabile 2
                if variable_1.value:
                    for value_2 in variable_2.domain[:]:
                        if not self._constraints.verify({variable_1.name: variable_1.value, variable_2.name: value_2}):
                            variable_2.delete_value(value_2)

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
                    
                        if not variable_1.domain:
                            return False

        return True

    def apply_node_consistency(self, node: CSPNode=None):
        if not node:
            node = self._root

        for variable in node.get_variables():
            for value in variable.domain[:]:
                if not self._constraints.verify({variable.name: value}):
                    variable.delete_value(value)
                    if not variable.domain:
                        return False
                
        self.is_node_consistent = True
        return True

    def __str__(self):
        return "Nodo radice del problema:\n" + str(self._root)

    def print_tree(self):
        self._print_node(self._root)
        
    def _print_node(self, node: CSPNode):
        print(node)
        for child in node.get_children():
            self._print_node(child)
    
    def print_solutions(self):
        print("Le soluzioni trovate sono:")
        for solution in self._solutions:
            print(solution)