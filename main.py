from typing import Callable, Dict, Tuple, List


class CSPSolver:


    # init
    def __init__(self, algorithm: Callable[[CSPNode, int], bool] = CSPAlgorithm.StandardBacktracking,
                 policy: Callable[[CSPNode, int], bool] = CSPPolicy.InsertOrder
                 step_arc_consistency: bool = False):
        self._constraints: Dict[Tuple, Callable]
        self._root = CSPNode(None, [])
        self._solutions: List[CSPNode] = []
        self._found_solution = False
        self._algorithm = algorithm
        self._policy = policy
        self._step_arc_consistency = step_arc_consistency
        
    # Add a constraint
    def add_constraint(self, variables: Tuple[str, ...], constraint: Callable):
        variables_len = variables.len()
        if variables_len > 2:
            raise ValueError("Too many variables (max 2)")
        
        # Are there variables not in this problem?
        for v in variables:
            if not self._root.get_variable_by_name(v.name):
                raise ValueError("The variable " + v + " is not a variable in this problem.")

        if variables_len == 1:
            self.constraint[variables] = constraint
        elif variables_len == 2:
            # Two versions of the same constraint to make search faster
            self.constraint[(variables[0],variables[1])] = constraint
            self.constraint[(variables[1],variables[0])] = constraint

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

    def _next_step(self, current_node: CSPNode, tree_depth: int):
        # assegno la variabile e faccio uno snapshot delle variabili
        # in questo modo se quella assegnazione fallisce, posso tornare allo snapshot
        variable = self._choose_variable_to_assign(self._policy, current_node, tree_depth)        
        
        # ciclo sui valori della variabile da assegnare
        for value in variable.domain:
            # Costruiamo il prossimo nodo
            child_node = CSPNode(current_node, current_node.get_variables_list) # TODO: Il costruttore vuole una lista di variabili, sistema!
            current_node.add_child(child_node)

            # Assegna un valore alla variabile da assegnare
            child_node.get_variable_by_name(variable.name).assign_value(value)

            # Algoritmo applicato al child node: i domini delle variabili non assegnate verranno modificati (a seconda dell'algoritmo scelto)
            if self.alg(child_node, tree_depth):
                if vuoi_applicare_consistenza_ad_ogni_passo:
                    applica_consistenza
                
                if tree_depth + 1 == len(child_node.get_variables_list()):
                    child_node.set_solution()
                    self._solutions.append(child_node)
                    
                    # Voglio una sola soluzione: blocco tutti i cicli
                    if one_solution: # one_solution è un parametro indicato dal'utente
                        self._found_solution = True
                        break
                else:
                    self._next_step(child_node, tree_depth + 1)
                    if self._found_solution:
                        break
            else:
                # Descrizione del fallimento
                child_node.set_failure()
    
    def solve(self):
        self._next_step(self._root, 0)
        
    
    def apply_arc_consistency(self, node: CSPNode):
        return True

    def apply_node_consistency(self, node: CSPNode):
        return True


class CSPVariable:
    def __init__(self, name: str, domain: List):
        self.name = name
        self.domain = domain
        self.value = None
    
    def assign_value(self, value):
        self.value = value


class CSPNode:
    def __init__(self, parent: CSPNode, variables: List[CSPVariable]):
        self._ordered_variables: List[CSPVariable] = []
        self._variables: Dict[str, CSPVariable] = {}
        self.parent = parent
        self.children = []
        self.solution = False
        self.failure = False

        for variable in variables:
            self.add_variable(variable)

    def add_variable(self, variable: CSPVariable):
        self._variables[variable.name] = variable
        self._ordered_variables.append(variable)
    
    def add_child(self, child: CSPNode):
        self.children.append(child)

    def get_variables_dict(self):
        return self._variables
    
    def get_variables_list(self):
        return self._ordered_variables

    def get_variable_by_name(self, name : str):
        return self._variables[name]

    def get_variable_by_index(self, index : int):
        name = self._ordered_variables_keys[index]
        return self.get_variable_by_name(name)

    def set_failure(self):
        self.failure = True

    def set_solution(self):
        self.solution = True


class CSPAlgorithm:
    @staticmethod
    def GenerateAndTest(node: CSPNode, tree_depth: int):
        return True

    @staticmethod
    def StandardBacktracking(node: CSPNode, tree_depth: int):
        return True

    @staticmethod
    def ForwardChecking(node: CSPNode, tree_depth: int):
        return True

    @staticmethod
    def PartialLookAhead(node: CSPNode, tree_depth: int):
        return True
        
    @staticmethod
    def FullLookAhead(node: CSPNode, tree_depth: int):
        return True


class CSPPolicy:
    @staticmethod
    def InsertOrder(node: CSPNode, tree_depth: int):
        return variable

    @staticmethod
    def MinimumRemainingValues(node: CSPNode, tree_depth: int):
        return variable

    @staticmethod
    def MostConstrainedPrinciple(node: CSPNode, tree_depth: int):
        return variable