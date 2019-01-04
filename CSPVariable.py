from typing import List

class CSPVariable:
    def __init__(self, name: str, domain: List):
        self.name = name
        self.domain = domain
        self.value = None
    
    def assign_value(self, value):
        self.value = value
    
    def delete_value(self, value):
        if value in self.domain:
            self.domain.remove(value)

    def __str__(self):
        if self.value:
            return "{0}: {1}".format(self.name, self.value)
        else:
            return "{0}: {1}".format(self.name, self.domain)