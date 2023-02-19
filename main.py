"""Employee Module

Holds very simple information about multiple types of employees at our company.  Our business rules indicate
that we cannot have a generic Employee listed in our system.  We have Salaried and Hourly Employee types,
but cannot have generics of these either.  Our concrete types are Executives and Managers (Salaried),
and Permanent and Temporary (Hourly).  Subtypes may hold custom data (but aren't required to).

Ira Woodring
Winter 2023
"""
from abc import ABC, abstractmethod
from datetime import datetime
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


class Employee(ABC):
    """
    Employee is an abstract class that holds common information about all employees.  We will be
    making heavy use of properties in this project, as is reflected in this code.
    
    Attributes:
        name(str):The name of employee. (cannot be blank).
        email (str): The email of employee(cannot be blank and must include @acme-machining.com).
        id_number(int):The unique id of employee.
        image(str):The string representation of where employee photo is stored.
    """

    CURRENT_ID = 1

    def __init__(self, name: str, email: str, CURRENT_ID: int):
        self.name = name
        self.email = email
        self.id_number = CURRENT_ID
        self.image: str = "./images/placeholder.png"
        CURRENT_ID += 1

    @property
    def name(self)-> str:
        """Getter for name."""
        return self.name
    
    @name.setter
    def name(self, value: str)-> None:
        """
        Setter for name.
        
        Parameters:
            value (str): User entered name for employee.
        """
        if value == " " or "":
            raise ValueError("Name cannot be blank.")
        else:
            self.name = value
    
    @property
    def email(self):
        """Getter for email."""
        return self.email
    
    @email.setter
    def email(self, value:str) -> None:
        """
        Setter for email.
        
        Parameters:
            value(str): User entered value for email.
        
        Raises:
            ValueError: If value entered in is blank or does not include "@acme-machining.com"
        """
        if value == " " or "":
            raise ValueError("Email cannot be blank.")
        elif "@acme-machining.com" not in value:
            raise ValueError('Email must contain "@acme-machining.com"')
        else:
            self.email = value
    
    @property
    def id_number(self)-> int:
        """
        Getter for employee id.
        """
        return self.id_number
    
    def __str__(self)-> str:
        """
        Formatting for the employee class.

        Returns:
            Employees id and name
        """
        id_name = "{}:{}".format(self.id_number, self.name)
        return id_name

    def __repr__(self)-> list:
        """
        Used for saving employee to disk.

        Returns 
            list containing employee name, email and their image.
        """
        #When do add generating that id with a static variable?
        return f'{self.name}, {self.email}, {self.image}'

    @abstractmethod
    def calc_pay(self)-> float:
        """This function calculates the weekly pay for the current employee for our pay report."""
        pass


class Salaried(Employee):
    """
    A Salaried Employee is one who has a yearly salary.
    
    Attributes:
        yearly(int): The salary for the employee(cannot be negative and be over $50,000).
    
    """

    def __init__(self, name: str, email: str, image:(str), id_number: int, _yearly: int):
        super().__init__(name, email, image,id_number)
        self._yearly = _yearly

    @property
    def yearly(self)-> int:
        """
        Getter for yearly salary.
        
        Returns:
            _yearly(int): Salaried employees yearly salary.
        """
        return self._yearly
    
    def __repr__(self)-> str:
        """
        Used for saving employee to disk.

        Returns 
            list containing employee name, email and their image, yearly salary.
        """
        
        return f'{self.name}, {self.email}, {self.image}, {self._yearly}'

    @yearly.setter
    def yearly(self, value: int)-> None:
        """
        The yearly salary cannot be negative, and must be over $50,000.
            
        Returns:
            yearly salary
        """
        # check user val
        if value < 0:
            raise ValueError("Yearly Salary cannot be less than 0.")
        elif value < 50000:
            raise ValueError("Yearly Salary to must be over $50,000.")
        else:
            self._yearly = value

    @property
    def calc_pay(self):
        """
        Calculates the salaried employees weekly pay. 
        """
        return self._yearly / 52.0

    def __repr__(self):
        """
        Used for saving employee to disk.

        Returns 
            list containing employee name, email, their image, yearly salary.
        """
        #When do add generating that id with a static variable?
        return f'{self.name}, {self.email}, {self.image}, {self._yearly}'


class Executive(Salaried):
    """An Executive is a Salaried Employee with no additional information held."""

    def __init__(self, name: str, email: str, image: str, id_number: int, salary:float, role: Enum):
        super().__init__(name, email, image, id_number, salary)
        self._role = role

    @property
    def role(self) -> Enum:
        """
        Getter for executive role.

        Returns:
            Executive's role.
        """
        return self._role
    
    @role.setter
    def role(self, value: str)-> None:
        """
        Setter for executive's role.

        Parameters:
            value(Enum): User value for executive's role.
        
        Raise:
            InvalidRoleException: if value does not match enum values.
        """
        #how to check for ENUMS?
        pass

    def __repr__(self):
        """
        Used for storing saving employee to disk.

        Returns 
            list containing executives name, email, their image, salary, and role.
        """
        return f'{self.name}, {self.email}, {self.image}, {self._yearly}, {self._role}'
        

class Manager(Salaried):
    """A Manager is a Salaried Employee with no additional information held.  May want to add
    a department, etc. for increased scope."""

    def __init__(self, name: str, email: str, image: str, id_number: int, salary:float, department: Enum):
        super().__init__(name, email, image, id_number, salary)
        self._department = Department
    
    @property
    def department(self):
        """
        Getter for manager's department
        
        Returns:
            Manager's department
        """
        return self._department
    
    @department.setter
    def department(self, value: int)-> None:
        """
        Setter for managers department.

        Parameters
            value(int): Integer representation for what department the manager belongs to.
        """


class Hourly(Employee):
    """
    An Hourly Employee adds an hourly wage.
    
    Attributes:
        _hourly(Float): Hourly employee's wage(must be between $15 and $99.99).
    """

    def __init__(self, name: str, email: str, id_number:int, _hourly: float) -> None:
        super().__init__(name, email, id_number)
        self._hourly = _hourly

    @property
    def hourly(self):
        """
        Setter for hourly rate of employee.

        Returns:
            Hourly employees rate.
        """
        return self._hourly
    
    @hourly.setter
    def hourly(self, value:float)-> float:
        """
        Setter for hourly rate of employee.
        
        Parameters:
            value(float): User entered hourly employee wage.
        
        Raises:
            ValueError: if hourly rate is not between $15 and $99.99.
        """
        if value < 15:
            raise ValueError("Wage is too Low.")
        if value > 99.99:
            raise ValueError("Wage is too high.")
        else:
            self._hourly = value
    
    
    def calc_pay(self):
        """
        Calculates the hourly employees weekly pay. 

        Returns:
            Hourly employees weekly pay.
        """
        return self._hourly * 40

    def __repr__(self):
        """
        Used for saving employee to disk.

        Returns 
            list containing employee name, email and their image and hourly rate.
        """
        #When do add generating that id with a static variable?
        return f'{self.name}, {self.email}, {self.image}, {self._hourly}'


class Permanent(Hourly):
    """Hourly Employees may be Permanent.  A Permanent Hourly Employee has a hired date."""

    def __init__(self, name: str, email: str, id_number:int, _hourly: float, hire_date) -> None:
        super().__init__(name, email, id_number, _hourly)
        self._hire_date = hire_date

    @property
    def hire_date(self):
        """ 
        Getter for hire date.
        
        Returns: 
            Hire date.
        """
        
        return self._hire_date
    
    @hire_date.setter
    def hire_date(self, value: str)-> datetime:
        """
        Setter for hire date.

        Parameters:
            value(str): User value that is a string representation of a date.
        
        Returns:
            datetime conversion of user entered string.
        """
        #coverts date string into a datetime object
        value = datetime.strptime(value,'%m/%d/%y')
        self._hire_date = value

    def __repr__(self):
        """
        Used for saving employee to disk.

        Returns 
            list containing employee name, email, their image, hourly rate, and hire date.
        """
        return f'{self.name}, {self.email}, {self.image}, {self._hourly}, {self._hire_date}'


class Temp(Hourly):
    """A Temp Employee is paid hourly but has a date they can no longer work past."""

    def __init__(self, name: str, email: str, id_number:int, _hourly: float, last_Day) -> None:
        super().__init__(name, email, id_number, _hourly)
        self._last_Day = last_Day

    @property
    def last_Day(self)-> None:
        """ 
        Getter for last day.
        
        Returns: 
            Last Day.
        """
        return self._last_Day
    
    @last_Day.setter
    def last_Day(self, value:str )-> datetime:
        """
        Setter for last day.

        Parameters:
            value(str): User value that is a string representation of a last day.
        
        Returns:
            datetime conversion of user entered string.
        """
        #coverts date string into a datetime object
        value = datetime.strptime(value,'%m/%d/%y')
        self._last_day = value



    def __repr__(self):
        """
        Used for saving employee to disk.

        Returns 
            list containing employee name, email, their image, hourly rate, last day.
        """
        return f'{self.name}, {self.email}, {self.image}, {self._hourly}, {self._last_Day}'
