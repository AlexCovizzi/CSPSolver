from typing import List

class Variable:

    def __init__(self, name: str, domain: List):
        self.name = name
        self.domain = domain
        self.value = None
    
    # assegna un valore a questa variabile,
    # se tale valore è nel dominio
    def assign_value(self, value):
        if value in self.domain:
            self.value = value
    
    # rimuove un valore dal dominio di questa variabile,
    # se tale valore è nel dominio
    def delete_value(self, value):
        if value in self.domain:
            self.domain.remove(value)

    # null variable (no name, no domain)
    @staticmethod
    def Null() -> "Variable":
        return Variable("", [])

    def __str__(self):
        if self.value:
            return "{0}: {1}".format(self.name, self.value)
        else:
            return "{0}: {1}".format(self.name, self.domain)