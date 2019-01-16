from typing import TextIO, Optional
from .node import Node
from .constraints import Constraints
from .variable import Variable

str_value_not_compatible = "{not_assigned} = {not_assigned_value} non e' compatibile con {variable} = {value} -> Nuovo dominio di {not_assigned}: {not_assigned_domain}"
str_var_not_compatible = "{not_assigned} = {not_assigned_value} non e' compatibile con i valori di {variable} -> Nuovo dominio di {not_assigned}: {not_assigned_domain}"

class Algorithm:
    """
    Ad ogni passo di risoluzione viene applicata una funzione
    che ha lo scopo di verificare se gli assegnamenti effettutati sono validi ed
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
        Viene testata la compatibilità dell'ultima variabile assegnata
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
        Elimino dai domini delle variabili non ancora assegnate
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
        Applico il forward checking, successivamente per ogni variabile non assegnata
        elimino i valori che non sono compatibili con nessuno dei valori
        delle variabili non assegnate successive.
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
        Applico il forward checking, successivamente per ogni variabile non assegnata
        elimino i valori che non sono compatibili
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

    @staticmethod
    def AC3(node: Node, constraints: Constraints, tree_depth: int, target: Optional[TextIO]):
        """
        Verifico i vincoli ed elimino dai domini delle variabili i valori non compatibili,
        fino a che non ci sono più domini che cambiano.
        Se rimangono domini vuoti la funzione restituisce False
        """
        
        # metodo privato
        def verify_arc_consistency(variable_1: Variable, variable_2: Variable, constraints: Constraints, target: Optional[TextIO]):
            changed = False

            # Ciclo sul dominio di variable_1
            for value_1 in variable_1.domain[:]:
                delete_value = True

                # variable_2 non è assegnata
                if not variable_2.value:
                    # Cerco un valore di variable_2 che soddisfi il vincolo se variable_1 = value_1
                    for value_2 in variable_2.domain:
                        if constraints.verify({variable_1.name: value_1, variable_2.name: value_2}):
                            delete_value = False
                            break
                
                # variable_2 è assegnata: verifico che variable_1 = value_1 soddisfi il vincolo con la variabile già assegnata
                elif constraints.verify({variable_1.name: value_1, variable_2.name: variable_2.value}):
                    delete_value = False

                # variable_1 = value_1 non soddisfa alcun vincolo con variable_2
                if delete_value:
                    changed = True
                    variable_1.delete_value(value_1)

                    if target:
                        data = {"var1": variable_1.name, "value1": value_1, "var2": variable_2.name, "domain1": variable_1.domain}
                        s = "{var1} = {value1} non e' compatibile con i valori di {var2} -> Nuovo dominio di {var1}: {domain1}"
                        print(s.format(**data), file=target)
                
            return changed
        # fine definizione verify_arc_consistency
        
        # applico la node consistenza solo se il nodo che sto considerando non è node-consistente
        if not node.is_node_consistent():
            if not node_consistency(node, constraints, tree_depth, target):
                return False
        else:
            # verifico se l'assegnamento effettuato è compatibile con i vincoli unari
            variable = node.get_last_assigned_variable()
            # verifico vincoli unari
            if not constraints.verify({variable.name: variable.value}):
                return False
        
        if target: print("Applico AC3...", file = target)
        

        # Aggiungo tutti i vincoli del problema
        worklist = []
        for index, v1 in enumerate(node.get_variables()):
            for v2 in node.get_variables()[index + 1:]:
                c1, c2 = constraints.get_binary_constraints(v1.name, v2.name)
                if c1 or c2:
                    worklist.append([v1.name, v2.name])

        # Ciclo sui vincoli
        while worklist:
            couple = worklist.pop(0)

            variable_1 = node.get_variable_by_name(couple[0])
            variable_2 = node.get_variable_by_name(couple[1])

            variable_1_changed = False
            variable_2_changed = False

            # Entrambe le variabili non assegnate
            if not variable_1.value and not variable_2.value:
                variable_1_changed = verify_arc_consistency(variable_1, variable_2, constraints, target)
                
                variable_2_changed = verify_arc_consistency(variable_2, variable_1, constraints, target)

            # variable_1 assegnata, variable_2 non assegnata
            elif variable_1.value and not variable_2.value:
                variable_2_changed = verify_arc_consistency(variable_2, variable_1, constraints, target)
            
            # variable_1 non assegnata, variable_2 assegnata
            elif not variable_1.value and variable_2.value:
                variable_1_changed = verify_arc_consistency(variable_1, variable_2, constraints, target)
            
            # Se entrambe sono assegnate, non fa nulla

            if variable_1_changed:
                if not variable_1.domain:
                    return False
                    
                for v in [v for v in node.get_variables() if v.name != variable_2.name and v.name != variable_1.name]:
                    c1, c2 = constraints.get_binary_constraints(variable_1.name, v.name)
                    if c1 or c2:
                        worklist.append([variable_1.name, v.name])

            if variable_2_changed:
                if not variable_2.domain:
                    return False
                
                for v in [v for v in node.get_variables() if v.name != variable_2.name and v.name != variable_1.name]:
                    c1, c2 = constraints.get_binary_constraints(variable_2.name, v.name)
                    if c1 or c2:
                        worklist.append([variable_2.name, v.name])

        if target: print("I vincoli sono arc-consistenti.", file = target)

        return True

# applica node-consistenza, inserito insieme agli algoritmi poichè utilizzato da uno di essi e perchè l'interfaccia è la stessa
def node_consistency(node: Node, constraints: Constraints, tree_depth: int, target: Optional[TextIO]) -> bool:
    """
    Elimino dai domini delle variabili i valori
    che non verificano i vincoli unari per tale variabile.
    """

    if target: print("Applico node-consistency...", file = target)

    for variable in node.get_variables():
        for value in variable.domain[:]:
            if not constraints.verify({variable.name: value}):
                variable.delete_value(value)

                if target:
                    data = {"variable": variable.name, "value": value, "domain": variable.domain}
                    s = "{variable} = {value} non e' compatibile con i vincoli unari -> Nuovo dominio di {variable}: {domain}"
                    print(s.format(**data), file = target)

                if not variable.domain:
                    return False

    node.set_node_consistent()

    if target: print("Le variabili sono node-consistenti.", file = target)

    return True
