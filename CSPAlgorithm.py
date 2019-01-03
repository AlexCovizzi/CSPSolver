from CSPNode import CSPNode
from CSPConstraints import CSPConstraints

class CSPAlgorithm:
    @staticmethod
    def GenerateAndTest(node: CSPNode, constraints: CSPConstraints, tree_depth: int):
        return True

    @staticmethod
    def StandardBacktracking(node: CSPNode, constraints: CSPConstraints, tree_depth: int, last_assigned_variable_name: str):
        variable = node.get_variable_by_name(last_assigned_variable_name)
        # verifico vincoli unari
        if not constraints.verify({variable.name: variable.value}):
            print("Vincolo unario violato")
            return False
        
        # verifico vincoli binari
        # prendo variabili assegnate diverse da quella appena assegnata
        for assigned_var in [v for v in node.get_variables() if v.value and not variable.name == v.name]:
            print("Considero la variabile " + assigned_var.name)
            if not constraints.verify({variable.name: variable.value, assigned_var.name: assigned_var.value}):
                print("Vincolo binario con variabile " + assigned_var.name + " violato")
                return False

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