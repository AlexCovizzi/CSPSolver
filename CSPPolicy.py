from CSPNode import CSPNode
from CSPConstraints import CSPConstraints
import math

class CSPPolicy:
    @staticmethod
    def InsertOrder(node: CSPNode, constraints: CSPConstraints, tree_depth: int):
        return node.get_variable_by_index(tree_depth)

    @staticmethod
    def MinimumRemainingValues(node: CSPNode, constraints: CSPConstraints, tree_depth: int):
        min_values = math.inf
        chosen_variable = None
        for variable in [v for v in node.get_variables() if not v.value]:
            domain_len = len(variable.domain)
            if domain_len < min_values:
                min_values = domain_len
                chosen_variable = variable
        
        return chosen_variable

    @staticmethod
    def MostConstrainedPrinciple(node: CSPNode, constraints: CSPConstraints, tree_depth: int):
        max_constraints = -1
        chosen_variable = None
        for variable in [v for v in node.get_variables() if not v.value]:
            n_constraints = len(constraints.get_variable_constraints(variable.name))
            if n_constraints > max_constraints:
                max_constraints = n_constraints
                chosen_variable = variable

        return chosen_variable