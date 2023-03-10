"""GUI Module for Employee Information

We provide a default form with common Employee information, then inherit and subclass
to create custom forms for each type.

Ira Woodring
Winter 2023
"""

import csv

from PyQt6 import QtWidgets
from PyQt6.QtCore import QAbstractTableModel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QAction
from PyQt6.QtWidgets import QLabel, QLineEdit, QMenu, QHeaderView, QTableView, QMainWindow, QAbstractItemView, \
    QPushButton, QVBoxLayout, QListWidget, QListWidgetItem, QComboBox, QApplication, QMessageBox
import sys
from employee_student import *
from typing import *


class HRTableModel(QAbstractTableModel):
    """The HRTableModel allows us to display our information in a QTableView."""
    def __init__(self, data) -> None:
        super(HRTableModel, self).__init__()
        self._columns = ["ID#", "Type", "Name", "Pay", "Email"]
        self._data = data

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> str:
        """Gives the header info in a format PyQt wants."""
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            # return f"Column {section + 1}"
            return self._columns[section]
        if orientation == Qt.Orientation.Vertical and role == Qt.ItemDataRole.DisplayRole:
            return f"{section + 1}"

    def data(self, index, role) -> str:
        """Returns the data at some table index."""
        if role == Qt.ItemDataRole.DisplayRole:
            e = self._data[index.row()]
            field = e.id_number
            if index.column() == 1:
                field = type(e).__name__
            if index.column() == 2:
                field = e.name
            if index.column() == 3:
                if isinstance(e, Salaried):
                    field = '${:,.2f}'.format(e.yearly)
                else:
                    field = '${:,.2f}'.format(e.hourly)
            if index.column() == 4:
                field = e.email
            return field

    def rowCount(self, index) -> int:
        """Provides the way for PyQt to get our row count."""
        return len(self._data)

    def columnCount(self, index) -> int:
        """Provides the column count, as PyQt expects."""
        return len(self._columns)


class MainWindow(QMainWindow):
    """MainWindow will have menus and a central list widget."""
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Employee Management v1.0.0")
        self.resize(800, 600)
        self._data = []
        self.load_file()
        self._model = HRTableModel(self._data)
        self._table = QTableView()
        self._table.setModel(self._model)
        self._table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self._table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self._table.setAlternatingRowColors(True)
        self._header = self._table.horizontalHeader()
        self._header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.setCentralWidget(self._table)
        self._create_menu_bar()
        self._employee_form = None
        self._about_form = AboutForm()

    def _create_menu_bar(self) -> None:
        # Create the menus.
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        file_menu = QMenu("&File", self)
        edit_menu = QMenu("&Edit", self)
        help_menu = QMenu("&Help", self)
        self._exit_action = QAction("&Exit")
        self._exit_action.triggered.connect(exit)
        self._load_action = QAction("&Load HR Data")
        self._save_action = QAction("&Save HR Data")
        self._save_action.setShortcut('Ctrl+S')
        file_menu.addAction(self._load_action)
        self._load_action.setShortcut('Ctrl+O')
        self._load_action.triggered.connect(self.load_file)
        file_menu.addAction(self._save_action)
        file_menu.addAction(self._exit_action)
        self._edit_action = QAction("&Edit current employee")
        edit_menu.addAction(self._edit_action)
        self._edit_action.triggered.connect(self.edit_employee)
        self._edit_action.setShortcut('Ctrl+E')
        self._save_action.triggered.connect(self.save_file)
        self._about_action = QAction("About this software")
        self._about_action.triggered.connect(self.show_help)
        help_menu.addAction(self._about_action)
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(edit_menu)
        menu_bar.addMenu(help_menu)
        self.setMenuBar(menu_bar)

    def show_help(self) -> None:
        """Our 'help' form merely shows who wrote this, the version, and a description."""
        self._about_form.show()

    def data_to_rows(self) -> List[str]:
        """It is sometimes useful for us to have our model data as a list.  This method
        provides that feature."""
        data = []
        for e in self._data:
            row = [e.id_number, type(e).__name__, e.name]
            if isinstance(e, Salaried):
                row.append(str(e.yearly))
            else:
                row.append(str(e.hourly))
            row.append(e.email)
            data.append(row)
        return data

    def refresh_width(self) -> None:
        """Resize our table to fit our data width."""
        self._header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)

    def edit_employee(self) -> None:
        """Update an employee object by populating the correct type of form with the selected type of
        employee data."""
        index = self._table.selectionModel().selectedIndexes()
        if not index:
            return
        index = index[0].row()
        if isinstance(self._data[index], Executive):
            self._employee_form = ExecutiveForm(self)
        if isinstance(self._data[index], Manager):
            self._employee_form = ManagerForm(self)
        if isinstance(self._data[index], Permanent):
            self._employee_form = PermanentForm(self)
        if isinstance(self._data[index], Temp):
            self._employee_form = TempForm(self)

        self._employee_form.fill_in(index)
        self._employee_form.show()

    def load_file(self) -> None:
        """Read a representation of all of our Employees from a file and store in our
        _data variable.  The table will automatically be populated by this variable.
        ID#", "Type", "Name", "Pay", "Email"""
        with open('./employee.data') as datafile:
            reader = csv.reader(datafile, quoting=csv.QUOTE_MINIMAL)
            
            for row in reader:
                name = row[1]
                image = row[3]
                pay = float(row[4])
                email = row[2]
            
                if row[0] == "Executive":
                    role = row[5]
                    employee = Executive(name, email, pay, role) 
                if row[0] == "Manager":
                    department = row[5]
                    employee = Manager(name, email, pay, department)
                if row[0] == "Permanent":
                    hire_date = row[5]
                    employee = Permanent(name, email, pay, hire_date)
                if row[0] == "Temp":
                    last_Day = row[5]
                    employee = Temp(name, email, pay, last_Day)
                if image != "./images/placeholder.png":
                    employee.image = image
                self._data.append(employee)


    def save_file(self) -> None:
        """Save a representation of all the Employees to a file."""

        f = open("./employeesave.data", "w")
        for employee in self._data:
            employee_department = ""
            if type(employee) is  Executive:
                class_name = "Executive,"
            elif type(employee) is  Manager:
                class_name = "Manager,"
                employee_department = "," + employee.department
            elif type(employee) is  Permanent:
                class_name = "Permanent,"
            else:
                class_name = "Temp,"
            f.write(class_name)  
            f.write(employee.__repr__())
            if employee_department != "":
                f.write(employee_department)
            f.write("\n")
        f.close()

class EmployeeForm(QtWidgets.QWidget):
    """There will never be a generic employee form, but we don't want to repeat code
    so we put it all here.  Each subtype of form will add to it."""
    def __init__(self, parent=None, employee: Employee = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        outer_layout = QVBoxLayout()
        self._parent = parent
        self.layout = QtWidgets.QFormLayout()
        self.setLayout(outer_layout)
        self._id_label = QLabel()
        self.layout.addRow(QLabel("ID#"), self._id_label)
        self._name_edit = QLineEdit()
        self.layout.addRow(QLabel("Name: "), self._name_edit)
        self._pay_edit = QLineEdit()
        self._email_edit = QLineEdit()
        self.layout.addRow(QLabel("Email address:"), self._email_edit)
        self._image_path_edit = QLineEdit()
        self.layout.addRow(QLabel("Image path:"), self._image_path_edit)
        self._image = QLabel()
        self._image.setPixmap(QPixmap(Employee.IMAGE_PLACEHOLDER))
        self.layout.addWidget(self._image)
        update = QPushButton("Update")
        update.clicked.connect(self.update_employee)
        outer_layout.addLayout(self.layout)
        outer_layout.addWidget(update)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

    def update_employee(self) -> None:
        """Change the selected employee's data to the updated values."""
        try:
            self._employee.name = self._name_edit.text()
            self._employee.email = self._email_edit.text()
            self._employee.image = self._image_path_edit.text()
            self._parent.refresh_width()
            self.setVisible(False)
        except ValueError as e:
            button = QMessageBox.critical(self, "Incorrect Information", str(e))

    def fill_in(self, index) -> None:
        """Upon opening the form, we wish to add the selected employee's data
        to the fields."""
        self._employee = self._parent._data[index]
        self.setWindowTitle("Edit " + type(self._employee).__name__ + " Employee Information")
        self._id_label.setText(str(self._employee.id_number))
        self._name_edit.setText(self._employee.name)
        self._email_edit.setText(self._employee.email)
        if self._employee.image == "placeholder":
            self._image_path_edit.setText('')
        else:
            self._image_path_edit.setText(self._employee.image)
        self._image.setPixmap(QPixmap(self._employee.image))

# Complete the following forms so that they update and fill-in
# their custom information.

class SalariedForm(EmployeeForm):
    
    def __init__(self, parent) -> None:
        super().__init__(parent)
        #self._pay_edit =  QLineEdit()
        self.layout.addRow(QLabel("Salary: "), self._pay_edit)
    
    
    def fill_in(self, index) -> None:
        """Upon opening the form, we wish to add the selected employee's data to the fields."""
        super().fill_in(index)
        self._pay_edit.setText(str(self._employee.yearly))
        
    def update_employee(self) -> None:
        try:
            self._employee.yearly = float(self._pay_edit.text())
            super().update_employee()
        except ValueError as e:
            button = QMessageBox.critical(self, "Incorrect Information", str(e))



class ExecutiveForm(SalariedForm):
    def __init__(self, parent):
        super().__init__(parent)
        #create combo box drop down
        self.cb = QComboBox()
        #Display combo box with a label
        self.layout.addRow(QLabel("Role"), self.cb)
    
    def fill_in(self, index) -> None:
        """Upon opening the form, we wish to add the selected employee's data
        to the fields."""
        super().fill_in(index)
        #Set first value in combobox to employees current role
        self.cb.addItem(self._employee._role)
        #Fill in the rest of the roles
        for role in (Role):
            if role == Role[self._employee._role]:
                exit
            else:
                self.cb.addItem(role.name)

    def update_employee(self) -> None:
        self._employee.role = (self.cb.currentText())
        super().update_employee()

class ManagerForm(SalariedForm):
    def __init__(self,parent):
        super().__init__(parent)
        #create combo box drop down
        self.cb = QComboBox()
        #Display combo box with a label
        self.layout.addRow(QLabel("Head of Department"), self.cb)
        
    def fill_in(self, index) -> None:
        """Upon opening the form, we wish to add the selected employee's data
        to the fields."""
        super().fill_in(index)
        #Set first value in combobox to employees current role
        self.cb.addItem(self._employee._department)
        #Fill in the rest of the roles
        for department in (Department):
            if department == Department[self._employee._department]:
                exit
            else:
                self.cb.addItem(department.name)

    def update_employee(self) -> None:
        """Change the selected employee's data to the updated values."""
        self._employee._department = (self.cb.currentText())
        super().update_employee()

class HourlyForm(EmployeeForm):
    def __init__(self,parent):
        super().__init__(parent)
        self.layout.addRow(QLabel("Hourly Wage: "), self._pay_edit)

    def fill_in(self, index) -> None:
        """Upon opening the form, we wish to add the selected employee's data to the fields."""
        super().fill_in(index)
        self._pay_edit.setText(str(self._employee.hourly))
    
    def update_employee(self) -> None:
        self._employee._hourly = float(self._pay_edit.text())
        super().update_employee()

class TempForm(HourlyForm):
    def __init__(self,parent):
        super().__init__(parent)
    
    def fill_in(self, index) -> None:
        """Upon opening the form, we wish to add the selected employee's data to the fields."""
        super().fill_in(index)
        self._last_day = QLabel()
        self.layout.addRow(QLabel("Last Day:"), self._last_day)
        self._last_day.setText(str(self._employee.last_Day))

class PermanentForm(HourlyForm):
    def __init__(self,parent):
        super().__init__(parent)
    
    def fill_in(self, index) -> None:
        """Upon opening the form, we wish to add the selected employee's data to the fields."""
        super().fill_in(index)
        self._hire_date = QLabel()
        self.layout.addRow(QLabel("Hired Date:"), self._hire_date)
        self._hire_date.setText(str(self._employee.hire_date))

class AboutForm(QtWidgets.QWidget):
    """An About Form just gives information about our app to users who want to see it.  Automatically
    sets itself visible on creation."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("HR Management System"))
        self.layout.addWidget(QLabel("version 1.0.0"))
        self.layout.addWidget(QLabel("A simple system for storing important pieces of information about employees."))
        self.close = QPushButton("Close")
        self.close.clicked.connect(self.close_form)
        self.layout.addWidget(self.close)
        self.setLayout(self.layout)

    def close_form(self) -> None:
        """Hide the form."""
        self.setVisible(False)

def main():
    #The QApplication Class requires a list parameter of command line arguments
    #the sys.argv contains a list of command line arguments passed into a Python script
    app= QApplication(sys.argv)
    mf= MainWindow()
    #form = EmployeeForm()
    #sf = SalariedForm()
    #sf.show()
    mf.show()
    #form.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()