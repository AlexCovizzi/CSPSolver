from typing import TextIO, Optional
from .node import Node
from .constraints import Constraints
from .variable import Variable

str_value_not_compatible = "{not_assigned} = {not_assigned_value} non e' compatibile con {variable} = {value} -> Nuovo dominio di {not_assigned}: {not_assigned_domain}"
str_var_not_compatible = "{not_assigned} = {not_assigned_value} non e' compatibile con i valori di {variable} -> Nuovo dominio di {not_assigned}: {not_assigned_domain}"

class Algorithm:
    """
    Ad ogni passo di risoluzione viene applicata una funzione
    che ha lo scopo di verificare se gli assegnamernti effettutati sono validi ed
    eventualmente di modificare i domini delle variabili,
    tale funzione è caratterizzata dall'interfaccia:

    Parametri
    -------
    node : cspsolver.node.Node
        La situazione attuale del problema (variabili e domini),
        il dominio delle variabili può essere modificato
    constraints : cspsolver.constraints.Constraints
        I vincoli del problema
    tree_depth: int
        L'attuale profondità dell'albero di decisione,
        corrisponde anche al numero di variabili già assegnate
    target: TextIO
        Dove stampare l'output (es. sys.stdout)

    Return
    -------
    bool
        True se l'algoritmo ha successo, altrimenti False
    """

    @staticmethod
    def GenerateAndTest(node: Node, constraints: Constraints, tree_depth: int, target: Optional[TextIO]) -> bool:
        """
        La funzione ha successo ad ogni passo (Generate) eccetto l'ultimo,
        nel quale vengono testate le assegnaziononi effettuate (Test),
        se ci sono incompatibilità restituisce False
        """

        if target: print("Applico l'algoritmo Generate and Test...", file = target)

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
    def StandardBacktracking(node: Node, constraints: Constraints, tree_depth: int, target: Optional[TextIO]) -> bool:
        """
        Ad ogni passo (assegnamento) viene testata la compatibilità dell'ultima variabile assegnata
        con le variabili assegnate precedentemente, se ci sono incompatibilità restituisce False
        """

        if target: print("Applico l'algoritmo Standard Backtracking...", file = target)

        variable = node.get_last_assigned_variable()
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
    def ForwardChecking(node: Node, constraints: Constraints, tree_depth: int, target: Optional[TextIO]) -> bool:
        """
        Ad ogni passo (assegnamento) elimino dai domini delle variabili non ancora assegnate
        i valori non compatibili con l'ultima variabile assegnata.
        Se rimangono domini vuoti la funzione restituisce False
        """

        if target: print("Applico l'algoritmo Forward Checking...", file = target)

        variable = node.get_last_assigned_variable()
        # verifico vincoli unari
        if not constraints.verify({variable.name: variable.value}):
            return False
        
        for variable_not_assigned in [v for v in node.get_variables() if not v.value]:
            for value in variable_not_assigned.domain[:]:
                if not constraints.verify({variable.name: variable.value, variable_not_assigned.name: value}):
                    variable_not_assigned.delete_value(value)

                    if target:
                        data = {"not_assigned": variable_not_assigned.name, "not_assigned_value": value,
                                "variable": variable.name, "value": variable.value, "not_assigned_domain": variable_not_assigned.domain}
                        print(str_value_not_compatible.format(**data), file = target)
            
            if not variable_not_assigned.domain:
                return False

        return True

    @staticmethod
    def PartialLookAhead(node: Node, constraints: Constraints, tree_depth: int, target: Optional[TextIO]) -> bool:
        """
        Ad ogni passo (assegnamento) applico il forward checking,
        successivamente per ogni variabile non assegnata elimino i valori che non sono compatibili
        con nessuno dei valori delle variabili non assegnate successive.
        Se rimangono domini vuoti la funzione restituisce False
        """
            
        variable = node.get_last_assigned_variable()

        if not Algorithm.ForwardChecking(node, constraints, tree_depth, target):
            return False
            
        if target: print("Applico l'algoritmo Partial Look Ahead...", file = target)

        for index, variable_not_assigned in enumerate([v for v in node.get_variables() if not v.value]):
            for value in variable_not_assigned.domain[:]:

                for next_variable_not_assigned in [v for v in node.get_variables() if not v.value][index + 1:]:
                    delete_value = True

                    for next_value in next_variable_not_assigned.domain:
                        if constraints.verify({variable_not_assigned.name: value, next_variable_not_assigned.name: next_value}):
                            delete_value = False

                    if delete_value:
                        variable_not_assigned.delete_value(value)

                        if target:
                            data = {"not_assigned": variable_not_assigned.name, "not_assigned_value": value,
                                    "variable": next_variable_not_assigned.name, "not_assigned_domain": variable_not_assigned.domain}
                            print(str_var_not_compatible.format(**data), file = target)

                    if not variable_not_assigned.domain:
                        return False

        return True
        
    @staticmethod
    def FullLookAhead(node: Node, constraints: Constraints, tree_depth: int, target: Optional[TextIO]) -> bool:
        """
        Ad ogni passo (assegnamento) applico il forward checking,
        successivamente per ogni variabile non assegnata elimino i valori che non sono compatibili
        con nessuno dei valori delle altre variabili non assegnate.
        Se rimangono domini vuoti la funzione restituisce False
        """

        variable = node.get_last_assigned_variable()

        if not Algorithm.ForwardChecking(node, constraints, tree_depth, target):
            return False
        
        if target: print("Applico l'algoritmo Full Look Ahead...", file = target)

        for variable_not_assigned in [v for v in node.get_variables() if not v.value]:
            for value in variable_not_assigned.domain[:]:

                for next_variable_not_assigned in [v for v in node.get_variables() if not v.value and v.name != variable_not_assigned.name]:
                    delete_value = True

                    for next_value in next_variable_not_assigned.domain:
                        if constraints.verify({variable_not_assigned.name: value, next_variable_not_assigned.name: next_value}):
                            delete_value = False

                    if delete_value:
                        variable_not_assigned.delete_value(value)

                        if target:
                            data = {"not_assigned": variable_not_assigned.name, "not_assigned_value": value,
                                    "variable": next_variable_not_assigned.name, "not_assigned_domain": variable_not_assigned.domain}
                            print(str_var_not_compatible.format(**data), file = target)

                    if not variable_not_assigned.domain:
                        return False

        return True
