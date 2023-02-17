"""Employee Module

Holds very simple information about multiple types of employees at our company.  Our business rules indicate
that we cannot have a generic Employee listed in our system.  We have Salaried and Hourly Employee types,
but cannot have generics of these either.  Our concrete types are Executives and Managers (Salaried),
and Permanent and Temporary (Hourly).  Subtypes may hold custom data (but aren't required to).

Ira Woodring
Winter 2023
"""
import abc
import datetime
from enum import Enum
from abc import ABC

class InvalidRoleException(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidDepartmentException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Role(Enum):
    CEO = 1
    CFO = 2
    CIO = 3


class Department(Enum):
    ACCOUNTING = 1
    FINANCE = 2
    HR = 3
    R_AND_D = 4
    MACHINING = 5


class Employee(abc.ABC):
    """Employee is an abstract class that holds common information about all employees.  We will be
    making heavy use of properties in this project, as is reflected in this code."""
    CURRENT_ID = 1
    def __init__(self, name: str, email: str, CURRENT_ID):
        self._id_number = CURRENT_ID
        self._name = name
        self._email = email
        self._image = "./images/placeholder.png"
        CURRENT_ID += 1

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name) -> None:
        if name:
            self._name = name
        else:
            raise ValueError("Name cannot be blank.")

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email):
        if email:
            if "@acme-machining.com" in email:
                self._email = email
            else:
                raise ValueError("Email must contain company field.")
        else:
            raise ValueError("Email cannot be blank.")

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, link):
        if link:
            self._image = link
        else:
            raise ValueError("Link cannot be blank.")

    @abc.abstractmethod
    def calc_pay(self)-> float:
        """This function calculates the weekly pay for the current
            employee for our pay report."""
        pass

    def __str__(self):
        return str(self._id_number) + ":" + self.name

    def __repr__(self):
        # How would this format cuz this seems wrong to me
        return self._name, self._email, self._image


class Salaried(Employee):
    """A Salaried Employee is one who has a yearly salary."""
    def __init__(self, yearly, name: str, email: str, CURRENT_ID):
        super().__init__(name, email, CURRENT_ID)
        self._yearly = self.yearly(yearly)

    @property
    def yearly(self):
        return self._yearly

    @yearly.setter
    def yearly(self, yearly):
        if yearly:
            if yearly < 50000:
                raise ValueError("Salary must be over $50,000.")
            else:
                self._yearly = yearly
        else:
            raise ValueError("Salary amount cannot be blank.")

    def calc_pay(self) -> float:
        return self._yearly / 52.0

    def __repr__(self):
        return self._name, self._email, self._image, self._yearly


class Executive(Salaried):
    """An Executive is a Salaried Employee with no additional information held."""


class Manager(Salaried):
    """A Manager is a Salaried Employee with no additional information held.  May want to add
    a department, etc. for increased scope."""

class Hourly(Employee):
    """An Hourly Employee adds an hourly wage."""
    def __init__(self, name: str, hourly: float, email: str) -> None:

class Permanent(Hourly):
    """Hourly Employees may be Permanent.  A Permanent Hourly Employee has a hired date."""

class Temp(Hourly):
    """A Temp Employee is paid hourly but has a date they can no longer work past."""
