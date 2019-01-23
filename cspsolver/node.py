from typing import List, Optional
from collections import OrderedDict
from .variable import Variable

class Node:
    def __init__(self, parent: Optional["Node"], variables: List[Variable]):
        self._variables = OrderedDict()
        self.parent = parent
        self.children = []
        self.solution = False
        self.failure = False
        self._node_consistent = parent.is_node_consistent() if parent else False
        self._last_assigned_variable = Variable.Null()

        for variable in variables:
            self.add_variable(variable)

    # aggiunge una variabile al nodo
    def add_variable(self, variable: Variable):
        self._variables[variable.name] = variable
    
    # aggiunge un nodo figlio
    def add_child(self, child: "Node"):
        self.children.append(child)

    # restituisce la lista delle variabili
    def get_variables(self):
        return list(self._variables.values())

    # assegna un valore ad una variabile
    def assign_variable(self, name: str, value):
        self._last_assigned_variable = self.get_variable_by_name(name)
        self._last_assigned_variable.assign_value(value)

    # restituisce una variabile dato il nome
    def get_variable_by_name(self, name : str):
        return self._variables[name]

    # restituisce una variabile dato l'indice
    def get_variable_by_index(self, index : int):
        return list(self._variables.items())[index][1]

    def get_last_assigned_variable(self) -> Variable:
        return self._last_assigned_variable

    # restituisce i nodi figli
    def get_children(self):
        return self.children

    # setta questo nodo come nodo di fallimento
    def set_failure(self):
        self.failure = True

    # setta questo nodo come nodo soluzione
    def set_solution(self):
        self.solution = True

    def set_node_consistent(self):
        self._node_consistent = True

    def is_node_consistent(self) -> bool:
        return self._node_consistent
    
    def __str__(self):
        string = ""
        if self.solution:
            string += "Soluzione"
        elif self.failure:
            string += "Fallimento"
        string += "\n"

        string += "\n".join([str(v) for v in self.get_variables()])
        
        return string
