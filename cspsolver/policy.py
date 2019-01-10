import math
from .node import Node
from .constraints import Constraints
from .variable import Variable

class Policy:
    
    @staticmethod
    def InsertOrder(node: Node, constraints: Constraints, tree_depth: int) -> Variable:
        return node.get_variable_by_index(tree_depth)

    @staticmethod
    def MinimumRemainingValues(node: Node, constraints: Constraints, tree_depth: int) -> Variable:
        min_values = math.inf
        chosen_variable = Variable.Null()
        for variable in [v for v in node.get_variables() if not v.value]:
            domain_len = len(variable.domain)
            if domain_len < min_values:
                min_values = domain_len
                chosen_variable = variable
        
        return chosen_variable

    @staticmethod
    def MostConstrainedPrinciple(node: Node, constraints: Constraints, tree_depth: int) -> Variable:
        max_constraints = -1
        chosen_variable = Variable.Null()
        for variable in [v for v in node.get_variables() if not v.value]:
            n_constraints = len(constraints.get_variable_constraints(variable.name))
            if n_constraints > max_constraints:
                max_constraints = n_constraints
                chosen_variable = variable

        return chosen_variable
