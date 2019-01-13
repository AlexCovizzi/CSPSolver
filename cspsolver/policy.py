import math
from .node import Node
from .constraints import Constraints
from .variable import Variable

class Policy:
    """
    Ad ogni passo di risoluzione, prima di assegnare una variabile,
    viene applicata una funzione che ha lo scopo di decidere la variabile da assegnare,
    tale funzione è caratterizzata dall'interfaccia:

    Parametri
    -------
    node : cspsolver.node.Node
        La situazione attuale del problema (variabili e domini)
    constraints : cspsolver.constraints.Constraints
        I vincoli del problema
    tree_depth: int
        L'attuale profondità dell'albero di decisione,
        corrisponde anche al numero di variabili già assegnate

    Restituisce
    -------
    cspsolver.variable.Variable
        La variabile da assegnare
    """
    
    @staticmethod
    def InsertOrder(node: Node, constraints: Constraints, tree_depth: int) -> Variable:
        """
        Viene scelta la variabile successiva in base all'inserimento nel problema.
        """

        return node.get_variable_by_index(tree_depth)

    @staticmethod
    def MinimumRemainingValues(node: Node, constraints: Constraints, tree_depth: int) -> Variable:
        """
        Viene restituita la variabile non assegnata con meno valori rimasti nel dominio
        """

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
        """
        Viene restituita la variabile non assegnata con più vincoli
        """

        max_constraints = -1
        chosen_variable = Variable.Null()
        for variable in [v for v in node.get_variables() if not v.value]:
            n_constraints = len(constraints.get_variable_constraints(variable.name))
            if n_constraints > max_constraints:
                max_constraints = n_constraints
                chosen_variable = variable

        return chosen_variable
