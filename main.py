from typing import Callable, Dict, Tuple, List

class CSPSolver:

    # init
    def __init__(self):
        self._variables: Dict[str, CSPVariable]
        self._ordered_variables_keys: List[str]
        self._constraints: Dict[Tuple, Callable]

    # Add a constraint
    def add_constraint(self, variables: Tuple[str, ...], constraint: Callable):
        variables_len = variables.len()
        if variables_len > 2:
            raise ValueError("Too many variables (max 2)")
        
        # Are there variable not in this problem?
        for v in variables:
            if not self._variables[v]:
                raise ValueError("The variable " + v + " is not a variable in this problem.")

        if variables_len == 1:
            self.constraint[variables] = constraint
        elif variables_len == 2:
            # Two versions of the same constraint to make search faster
            self.constraint[(variables[0],variables[1])] = constraint
            self.constraint[(variables[1],variables[0])] = constraint

    # Add a variable
    def add_variable(self, name: str, domain: List):
        self._variables[name] = CSPVariable(name, domain)
        self._ordered_variables_keys.append(name)

    # Print problem variables
    def show_variables(self):
        pass

    # Print problem constraints
    def show_constraints(self):
        pass

    def _assign_variable(self, name):
        # assegno la variabile e faccio uno snapshot delle variabili non assegnate
        # in questo modo se quella assegnazione fallisce, posso tornare allo snapshot
        for v in valori:
            Xi = v
            snapshot
            # algoritmo
            if variabile futura vuota:
                return False
            if ultima variabile:
                return True
            if _assign_variable(self._choose_variable_to_assign(self._policy, variabili_future, variaibili_future_keys)):
                return True
            ripristino_snapshot
    
    def solve(self):
        variable_to_assign = self._choose_variable_to_assign(self._policy, self._variables, self._ordered_variables_keys)
        self._assign_variable(variable_to_assign)

        print_solutions

    def _choose_variable_to_assign(self, policy, variables, ordered_variables_keys):
        # policy: Ordine di inserimento, minimum remaining values, most constrained
        return next_variable_name

class CSPVariable:
    def __init__(self, name: str, domain: List)
        self.name = name
        self.domain = domain
        self.value = None