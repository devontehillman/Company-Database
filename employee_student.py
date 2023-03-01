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
print()

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
    IMAGE_PLACEHOLDER = "./images/placeholder.png"

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self._id_number = Employee.CURRENT_ID
        self.image: str = Employee.IMAGE_PLACEHOLDER
        Employee.CURRENT_ID += 1

    @property
    def name(self)-> str:
        """Getter for name."""
        return self._name
    
    @name.setter
    def name(self, value: str)-> None:
        """
        Setter for name.
        
        Parameters:
            value (str): User entered name for employee.
        """
        if (value == " ") or (value == ""):
            raise ValueError("Name cannot be blank.")
        elif type(value) != str:
            raise ValueError("Name must be a string.")
        else:
            self._name = value
    
    @property
    def email(self):
        """Getter for email."""
        return self._email
    
    @email.setter
    def email(self, value:str) -> None:
        """
        Setter for email.
        
        Parameters:
            value(str): User entered value for email.
        
        Raises:
            ValueError: If value entered in is blank or does not include "@acme-machining.com"
        """
        if (value == " ") or (value == ""):
            raise ValueError("Email cannot be blank.")
        elif "@acme-machining.com" not in value:
            raise ValueError('Email must contain "@acme-machining.com"')
        else:
            self._email = value
    
    @property
    def id_number(self)-> int:
        """Getter for employee id."""
        return self._id_number
    
    def __str__(self)-> str:
        """
        Formatting for the employee class.

        Returns:
            Employees id and name
        """
        id_name = "ID:{} Name:{}".format(self._id_number, self._name)
        return id_name

    def __repr__(self)-> str:
        """
        Used for saving employee to disk.

        Returns 
            list containing employee name, email and their image.
        """
        #When do add generating that id with a static variable?
        return f'{self._name}, {self._email}, {self._image}'
    
    @property
    def image(self) -> None:
        """Getter for image"""
        return self._image
    
    @image.setter
    def image(self, link: str):
        
        if (link == " ") or (link == ""):
            raise ValueError("Image path cannot be blank")
        elif not isinstance(link, str):
            raise ValueError("Image path must be a string")
        else:
            self._image = link
        

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

    def __init__(self, name: str, email: str, yearly: int):
        super().__init__(name, email)
        self.yearly = yearly

    @property
    def yearly(self)-> int:
        """
        Getter for yearly salary.
        
        Returns:
            _yearly(int): Salaried employees yearly salary.
        """
        return self._yearly
    
    @yearly.setter
    def yearly(self, value: int)-> None:
        """
        The yearly salary cannot be negative, and must be over $50,000.
            
        Returns:
            yearly salary
        """
        # check user val
        if type(value) == str:
            raise ValueError("Yearly Salary must be a number")
        elif value < 0:
            raise ValueError("Yearly Salary cannot be less than 0.")
        elif value < 50000:
            raise ValueError("Yearly Salary to must be over $50,000.")
        else:
            self._yearly = value
    
    def __repr__(self)-> str:
        """
        Used for saving employee to disk.

        Returns 
            list containing employee name, email and their image, yearly salary.
        """
        
        return f'{super().__repr__(self)}, {self._yearly}'


    @property
    def calc_pay(self)-> float:
        """
        Calculates the salaried employees weekly pay. 
        
        Returns:
            Salaried employees weekly pay
        """
        return self._yearly / 52.0

    def __repr__(self)-> str:
        """
        Used for saving employee to disk.

        Returns 
            list containing employee name, email, their image, yearly salary.
        """
        #When do add generating that id with a static variable?
        return f'{super().__repr__()}, {self._yearly}'

salary1 = Salaried("g","John@acme-machining.com",60000)


class Executive(Salaried):
    """An Executive is a Salaried Employee with no additional information held."""

    def __init__(self, name: str, email: str, salary:float, role: Enum):
        super().__init__(name, email, salary)
        self.role = role

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
        #try to set role if value not found in ROLE then raise exception
        try:
            self._role = Role[value].name
        except:
            print(InvalidRoleException(f'{value} not in Roles'))

    def __repr__(self)-> str:
        """
        Used for storing saving employee to disk.

        Returns 
            list containing executives name, email, their image, salary, and role.
        """
        return f'{super().__repr__()}, {self._role}'

executive1 = Executive("Elon","John@acme-machining.com",60000, "CEO")

class Manager(Salaried):
    """A Manager is a Salaried Employee with no additional information held.  May want to add
    a department, etc. for increased scope."""

    def __init__(self, name: str, email: str, salary:float, department: Enum):
        super().__init__(name, email, salary)
        self.department = department
    
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
         #try to set role if value not found in ROLE then raise exception
        try:
            self._department = Department[value].name
        except:
            print(InvalidDepartmentException(f'{value} not in Departments'))

manager1 = Manager("Steve Carell","John@acme-machining.com",70000, "FINANCE")

class Hourly(Employee):
    """
    An Hourly Employee adds an hourly wage.
    
    Attributes:
        _hourly(Float): Hourly employee's wage(must be between $15 and $99.99).
    """

    def __init__(self, name: str, email: str, hourly: float) -> None:
        super().__init__(name, email)
        self.hourly = hourly

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

    def __repr__(self)-> str:
        """
        Used for saving employee to disk.

        Returns 
            list containing employee name, email and their image and hourly rate.
        """
        #When do add generating that id with a static variable?
        return f'{super().__repr__()}, {self._hourly}'

hourly1 = Hourly("Ray","John@acme-machining.com", 16)

class Permanent(Hourly):
    """Hourly Employees may be Permanent.  A Permanent Hourly Employee has a hired date."""

    def __init__(self, name: str, email: str, _hourly: float, hire_date) -> None:
        super().__init__(name, email, _hourly)
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

    def __repr__(self)-> str:
        """
        Used for saving employee to disk.

        Returns 
            list containing employee name, email, their image, hourly rate, and hire date.
        """
        return f'{super().__repr__()}, {self._hire_date}'

permanent1 = Permanent("Wayne","John@acme-machining.com", 16.21, "09/27/1982" )
#print(permanent1.hire_date)

class Temp(Hourly):
    """A Temp Employee is paid hourly but has a date they can no longer work past."""

    def __init__(self, name: str, email: str, _hourly: float, last_Day) -> None:
        super().__init__(name, email, _hourly)
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



    def __repr__(self)-> str:
        """
        Used for saving employee to disk.

        Returns 
            list containing employee name, email, their image, hourly rate, last day.
        """
        return f'{super().__repr__()}, {self._last_Day}'

temp1 = Temp("Peter","John@acme-machining.com", 16.00, "02/19/2023" )
#print(temp1.last_Day)

""" Salaried Test """
#s1 = Salaried("John","John@acme-machining.com",60000)
#print(s1._id_number)

# salary under 50K
#s2 = Salaried("John","John@acme-machining.com",30000)
#print(s2._id_number)
#print(s2._yearly)

#salary is negative


#Executive 
#Permanent
#Temp


