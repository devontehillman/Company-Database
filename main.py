from abc import ABC, abstractmethod

class Employee(ABC):
    def __init__(self, name, email):
        self._id: int = 0
        self.name = name
        self.email = email


class Salaried(Employee):
    def __init__(self, name, email):
        super().__init__(name, email)

class Hourly(Employee):
    pass