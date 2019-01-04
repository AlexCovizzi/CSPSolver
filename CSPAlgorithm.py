from CSPNode import CSPNode
from CSPConstraints import CSPConstraints
from CSPVariable import CSPVariable

class CSPAlgorithm:
    @staticmethod
    def GenerateAndTest(node: CSPNode, constraints: CSPConstraints, tree_depth: int, last_assigned_variable_name: str):
        if tree_depth + 1 == len(node.get_variables()):
            for index, variable in enumerate(node.get_variables()):
                # verifico vincoli unari
                if not constraints.verify({variable.name: variable.value}):
                    return False
                    
                # verifico vincoli binari
                for variable_2 in node.get_variables()[index + 1:]:
                    if not constraints.verify({variable.name: variable.value, variable_2.name: variable_2.value}):
                        return False

        return True

    @staticmethod
    def StandardBacktracking(node: CSPNode, constraints: CSPConstraints, tree_depth: int, last_assigned_variable_name: str):
        variable = node.get_variable_by_name(last_assigned_variable_name)
        # verifico vincoli unari
        if not constraints.verify({variable.name: variable.value}):
            return False
        
        # verifico vincoli binari
        # prendo variabili assegnate diverse da quella appena assegnata
        for assigned_var in [v for v in node.get_variables() if v.value and not variable.name == v.name]:
            if not constraints.verify({variable.name: variable.value, assigned_var.name: assigned_var.value}):
                return False

        return True

    @staticmethod
    def ForwardChecking(node: CSPNode, constraints: CSPConstraints, tree_depth: int, last_assigned_variable_name: str):
        variable = node.get_variable_by_name(last_assigned_variable_name)
        # verifico vincoli unari
        if not constraints.verify({variable.name: variable.value}):
            return False
        
        for variable_not_assigned in [v for v in node.get_variables() if not v.value]:
            for value in variable_not_assigned.domain[:]:
                if not constraints.verify({variable.name: variable.value, variable_not_assigned.name: value}):
                    variable_not_assigned.delete_value(value)
            
            if not variable_not_assigned.domain:
                return False

        return True

    @staticmethod
    def PartialLookAhead(node: CSPNode, constraints: CSPConstraints, tree_depth: int, last_assigned_variable_name: str):
        variable = node.get_variable_by_name(last_assigned_variable_name)

        if not CSPAlgorithm.ForwardChecking(node, constraints, tree_depth, last_assigned_variable_name):
            return False

        for index, variable_not_assigned in enumerate([v for v in node.get_variables() if not v.value]):
            for value in variable_not_assigned.domain[:]:

                for next_variable_not_assigned in [v for v in node.get_variables() if not v.value][index + 1:]:
                    delete_value = True

                    for next_value in next_variable_not_assigned.domain:
                        if constraints.verify({variable_not_assigned.name: value, next_variable_not_assigned.name: next_value}):
                            delete_value = False

                    if delete_value:
                        variable_not_assigned.delete_value(value)

                    if not variable_not_assigned.domain:
                        return False

        return True
        
    @staticmethod
    def FullLookAhead(node: CSPNode, constraints: CSPConstraints, tree_depth: int, last_assigned_variable_name: str):
        variable = node.get_variable_by_name(last_assigned_variable_name)

        if not CSPAlgorithm.ForwardChecking(node, constraints, tree_depth, last_assigned_variable_name):
            return False

        for variable_not_assigned in [v for v in node.get_variables() if not v.value]:
            for value in variable_not_assigned.domain[:]:

                for next_variable_not_assigned in [v for v in node.get_variables() if not v.value and v.name != variable_not_assigned.name]:
                    delete_value = True

                    for next_value in next_variable_not_assigned.domain:
                        if constraints.verify({variable_not_assigned.name: value, next_variable_not_assigned.name: next_value}):
                            delete_value = False

                    if delete_value:
                        variable_not_assigned.delete_value(value)

                    if not variable_not_assigned.domain:
                        return False

        return True