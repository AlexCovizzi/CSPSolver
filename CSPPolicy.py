from CSPNode import CSPNode

class CSPPolicy:
    @staticmethod
    def InsertOrder(node: CSPNode, tree_depth: int):
        return node.get_variable_by_index(tree_depth)

    @staticmethod
    def MinimumRemainingValues(node: CSPNode, tree_depth: int):
        return variable

    @staticmethod
    def MostConstrainedPrinciple(node: CSPNode, tree_depth: int):
        return variable