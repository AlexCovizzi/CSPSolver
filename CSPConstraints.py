from typing import Callable, Dict, Tuple, List, Any

class CSPConstraints:
    def __init__(self):
        self._constraints : Dict[Tuple[str, ...], List[Callable]] = {}

    def add_constraint(self,variables: Tuple[str, ...], constraint: Callable):
        if not variables in self._constraints.keys():
            self._constraints[variables] = []

        self._constraints[variables].append(constraint)

    def verify(self, values: Dict[str, Any]):
        n_keys = len(values.keys())

        if n_keys == 1:
            name = list(values.keys())[0]
            for constraint in self.get_unary_constraints(name):
                if not constraint(values[name]):
                    return False
        
        elif n_keys == 2:
            name_1 = list(values.keys())[0]
            name_2 = list(values.keys())[1]

            constraints_1, constraints_2 = self.get_binary_constraints(name_1, name_2)

            for constraint in constraints_1:
                if not constraint(values[name_1], values[name_2]):
                    return False
            
            for constraint in constraints_2:
                if not constraint(values[name_2], values[name_1]):
                    return False
        
        return True
    
    def get_unary_constraints(self, variable_name):
        if (variable_name,) in self._constraints.keys():
            return self._constraints[(variable_name,)]
        else:
            return []

    def get_binary_constraints(self, variable_name_1, variable_name_2):
        constraints_12 = []
        constraints_21 = []
        if (variable_name_1, variable_name_2) in self._constraints.keys():
            constraints_12 = self._constraints[(variable_name_1, variable_name_2)]
        if (variable_name_2, variable_name_1) in self._constraints.keys():
            constraints_21 = self._constraints[(variable_name_2, variable_name_1)]
        
        return (constraints_12, constraints_21)

    def get_variable_constraints(self, variable_name):
        constraints_list = [item[1] for item in list(self._constraints.items()) if variable_name in item[0]]
        return [constraint for constraints in constraints_list for constraint in constraints]