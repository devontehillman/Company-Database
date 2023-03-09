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
from datetime import *

import pytest
from pytest import *
from enum import Enum


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

    def __init__(self, name: str, email: str):
        self.id_number = Employee.CURRENT_ID
        self.name = name
        self.email = email
        self.image = "./images/placeholder.png"
        Employee.CURRENT_ID += 1

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name) -> None:
        if name and isinstance(name, str):
            self._name = name
        else:
            raise ValueError("Name cannot be blank and must be str.")

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email):
        if email and isinstance(email, str):
            if "@acme-machining.com" in email:
                self._email = email
            else:
                raise ValueError("Email must contain company field.")
        else:
            raise ValueError("Email cannot be blank and must be str.")

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, link):
        if link and isinstance(link, str):
            self._image = link
        else:
            raise ValueError("Link cannot be blank and must be str.")

    @abc.abstractmethod
    def calc_pay(self) -> float:
        """This function calculates the weekly pay for the current
            employee for our pay report."""
        pass

    def __str__(self):
        return str(self._id_number) + ":" + self.name

    def __repr__(self):
        # How would this format cuz this seems wrong to me
        return f'{self._name}, {self._email}, {self._image}'


class Salaried(Employee):
    """A Salaried Employee is one who has a yearly salary."""

    def __init__(self, yearly: float, name: str, email: str):
        super().__init__(name, email)
        self.yearly = yearly

    @property
    def yearly(self):
        return self._yearly

    @yearly.setter
    def yearly(self, yearly: float):
        if yearly:
            if yearly < 50000:
                raise ValueError("Salary must be over $50,000.")
            else:
                self._yearly = yearly
        else:
            raise ValueError("Salary amount cannot be blank.")

    def calc_pay(self) -> float:
        return self.yearly / 52.0

    def __repr__(self):
        return f'{super().__repr__()}, {self._yearly}'


class Executive(Salaried):
    """An Executive is a Salaried Employee with no additional information held."""

    def __init__(self, role: str, yearly: float, name: str, email: str):
        super().__init__(yearly, name, email)
        self.role = role

    @property
    def role(self):
        return self._role

    #  No idea of this is how to set the role and raise exception, this is what came to mind
    @role.setter
    def role(self, role) -> int:
        """
        if role == Role.CEO or Role.CFO or Role.CIO:
            self._role = role
        else:
            raise InvalidRoleException("Invalid role, please provide a valid role.")
        """
        if role not in Role._value2member_map_:
            raise InvalidRoleException("Invalid role, please provide a valid role.")
        else:
            self._role = role

    def __repr__(self):
        return f'{super().__repr__()}, {self._role}'


class Manager(Salaried):
    """A Manager is a Salaried Employee with no additional information held.  May want to add
    a department, etc. for increased scope."""

    def __init__(self, department: str, yearly: float, name: str, email: str):
        super().__init__(yearly, name, email)
        self.department = department

    @property
    def department(self):
        return self._department

    @department.setter
    def department(self, department):
        if department not in Department._value2member_map_:
            raise InvalidDepartmentException("Invalid department, please "
                                             "provide a valid deparment.")
        else:
            self._department = department


    def __repr__(self):
        return f'{super().__repr__()}, {self._department}'


class Hourly(Employee):
    """An Hourly Employee adds an hourly wage."""

    def __init__(self, hourly: float, name: str, email: str):
        super().__init__(name, email)
        self.hourly = hourly

    @property
    def hourly(self):
        return self._hourly

    @hourly.setter
    def hourly(self, hourly):
        if isinstance(hourly,float) or isinstance(hourly,int):
            if 15.0 <= hourly <= 99.99:
                self._hourly = hourly
            else:
                raise ValueError("Hourly Wage cannot be less than $15 and more"
                                     "than $99.99.")
        else:
            raise ValueError("Hourly cannot be a string or blank")


    def calc_pay(self) -> float:
        return self._hourly * 40.0

    def __repr__(self):
        return f'{super().__repr__()}, {self._hourly}'


class Permanent(Hourly):
    """Hourly Employees may be Permanent.  A Permanent Hourly Employee has a hired date."""

    def __init__(self, hourly: float, name:str, email:str,hired_date =
    date.today()):
        super().__init__(hourly, name, email)
        self.hired_date = hired_date

    @property
    def hired_date(self):
        return self._hired_date

    #  Need to use datetime
    @hired_date.setter
    def hired_date(self, hired_date):
        if isinstance(hired_date, datetime):
            date = datetime.datetime.strptime(hired_date, '%Y-%m-%d %H: %M: %S')
            self._hired_date = date
        else:
            return ValueError("Invalid date")

    def __repr__(self):
        return f'{super().__repr__()}, {self._hired_date}'


class Temp(Hourly):
    """A Temp Employee is paid hourly but has a date they can no longer work past."""
    def __init__(self, last_day, hourly: float, name: str, email: str):
        super().__init__(hourly, name, email)
        self.last_day = last_day

    @property
    def last_day(self):
        return self._last_day

    @last_day.setter
    def last_day(self, last_day):
        if last_day:
            """
            last = datetime.date.today()
            last = last + datetime.timedelta(days=250)
            """
            last = datetime.datetime.strptime(last_day, '%Y-%m-%d %H: %M: %S')
            self._last_day = last

    def __repr__(self):
        return f'{super().__repr__()}, {self._last_day}'

