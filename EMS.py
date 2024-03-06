import sqlite3
import re
import itertools

DB_NAME = 'ems.db'

# Colors used to change font color in CLI 
class bcolors:
      HEADER = '\033[95m'
      OKBLUE = '\033[94m'
      OKCYAN = '\033[96m'
      OKGREEN = '\033[92m'
      WARNING = '\033[93m'
      FAIL = '\033[91m'
      ENDC = '\033[0m'
      BOLD = '\033[1m'
      UNDERLINE = '\033[4m'

# Employee class will hold employee info
class Employee:
      def __init__(self, id, firstName, lastName, employmentDate, salary, department):
            self.id = id
            self.firstName = firstName
            self.lastName = lastName
            self.employmentDate = employmentDate
            self.salary = salary
            self.department = department

      def printEmployee(self):
            print("Employee ID: " + bcolors.OKCYAN + str(self.id) + bcolors.ENDC)
            print("Employee name: " + bcolors.OKCYAN + self.firstName + " " + self.lastName + bcolors.ENDC)
            print("Employment date: " + bcolors.OKCYAN + self.employmentDate + bcolors.ENDC)
            print("Employee salary: " + bcolors.OKCYAN + "{:.2f}".format(self.salary) + bcolors.ENDC)
            print("Department name: " + bcolors.OKCYAN + self.department + "\n" + bcolors.ENDC)
      
      def getName(self):
            return str(self.firstName + " " + self.lastName)

# Function to initialize db if it does not already exist, run at beginning of program
def initialize_db():
      conn = sqlite3.connect(DB_NAME)
      cursor = conn.cursor()
      cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                     id INTEGER PRIMARY KEY,
                     first_name TEXT NOT NULL,
                     last_name TEXT NOT NULL,
                     employment_date TEXT NOT NULL,
                     salary REAL NOT NULL,
                     department TEXT NOT NULL
      )''')
      conn.commit()
      conn.close()


# Function to add an employee object to the database
def add_employee(employee):
      conn = sqlite3.connect(DB_NAME)
      cursor = conn.cursor()

      cursor.execute("INSERT INTO employees (first_name, last_name, employment_date, salary, department) VALUES (?, ?, ?, ?, ?)", (employee.firstName, employee.lastName, employee.employmentDate, employee.salary, employee.department))

      conn.commit()
      conn.close()

# Function to add an employee object to the database
def edit_employee(employee, id):
      conn = sqlite3.connect(DB_NAME)
      cursor = conn.cursor()

      cursor.execute("UPDATE employees SET first_name = ?, last_name = ?, employment_date = ?, "
                  "salary = ?, department = ? WHERE id = ?", (employee.firstName, employee.lastName, employee.employmentDate, employee.salary, employee.department, id))

      conn.commit()
      conn.close()

def delete_employee(id):
      conn = sqlite3.connect(DB_NAME)
      cursor = conn.cursor()

      cursor.execute("DELETE FROM employees WHERE id = ?", (id))

      conn.commit()
      conn.close()

def get_employee():
      conn = sqlite3.connect(DB_NAME)
      cursor = conn.cursor()

      name = get_employee_logic()

      # retrieves 
      cursor.execute("SELECT * FROM employees WHERE first_name = ? AND last_name = ?", (name[0], name[1]))

      matching = cursor.fetchall()
      employees = []

      for employee_data in matching:
            id, first_name, last_name, date_of_employment, salary, department = employee_data
            employee = Employee(id, first_name, last_name, date_of_employment, salary, department)
            employees.append(employee)

      conn.close()
      return employees

def get_employee_by_id(id):
      conn = sqlite3.connect(DB_NAME)
      cursor = conn.cursor()

      # retrieves 
      cursor.execute("SELECT * FROM employees WHERE id = ?", (id))

      matching = cursor.fetchall()
      employees = []

      for employee_data in matching:
            id, first_name, last_name, date_of_employment, salary, department = employee_data
            employee = Employee(id, first_name, last_name, date_of_employment, salary, department)
            employees.append(employee)

      conn.close()
      return employees

def get_employee_logic():
      
      # Get a valid first and last name
      while True:
            fullName = input(bcolors.OKGREEN + "What employee do you want to search for? Type the first and last name separated by a space.\n" + bcolors.ENDC).strip()

            if re.match("^[a-zA-z]+ [a-zA-Z]+$", fullName):
                  div = fullName.split()
                  firstName = div[0]
                  lastName = div[1]

                  return firstName, lastName
            else:
                  print(bcolors.FAIL + "Error: invalid input.\n" + bcolors.ENDC)

def create_employee():

      # Loop for getting valid first name
      while True:
            firstName = input(bcolors.OKGREEN + "What is your employee's first name? Not case sensitive, alphabetical characters only.\n" + bcolors.ENDC).strip()

            if re.match("^[a-zA-Z]+$", firstName):
                  firstName = firstName.capitalize()
                  break
            else:
                  print(bcolors.FAIL + "Error: invalid input.\n" + bcolors.ENDC)
      
      # Loop for getting valid last name
      while True:
            lastName = input(bcolors.OKGREEN + "What is your employee's last name? Not case sensitive, alphabetical characters only.\n" + bcolors.ENDC).strip()

            if re.match("^[a-zA-Z]+$", firstName):
                  lastName = lastName.capitalize()
                  break
            else:
                  print(bcolors.FAIL + "Error: invalid input.\n" + bcolors.ENDC)

      # Loop for getting valid date
      while True:
            date = input(bcolors.OKGREEN + "What is your employee's date of employment? Format: mm/dd/yyyy\n" + bcolors.ENDC).strip()

            if re.match(r"^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/\d{4}$", date):
                  break
            else:
                  print(bcolors.FAIL + "Error: invalid input.\n" + bcolors.ENDC)

      # Loop for getting valid salary
      while True:
            salary = input(bcolors.OKGREEN + "What is your employee's salary? Example: 100.00\n" + bcolors.ENDC).strip()

            if re.match(r"^[0-9]+\.[0-9][0-9]$", salary):
                  break
            else:
                  print(bcolors.FAIL + "Error: invalid input.\n" + bcolors.ENDC)
      
      dept = input(bcolors.OKGREEN + "What is your employee's department?\n" + bcolors.ENDC).strip()

      employee = Employee(0, firstName, lastName, date, salary, dept)

      return employee

def handle_multiple_employees(employees):
      print(bcolors.WARNING + "\nThere are multiple employees with the name " + employees[0].getName() + ". Here they are: " + bcolors.ENDC)
      for item in employees:
            item.printEmployee()


def menu():
      userInput = input("What would you like to do? Please select an option below:\n1. Add new employee\n2. Update existing employee\n3. Remove existing employee\n4. List employee information\nq. Quit the application\n")
      match userInput:
            case "1":
                  add_employee(create_employee())
            case "2":
                  empId = input("Please enter the employee's ID: ")
                  employees = get_employee_by_id(empId)

                  if len(employees) == 1:
                        newEmp = create_employee()
                        edit_employee(newEmp, empId)
                        print(bcolors.OKGREEN + "\nEmployee successfully edited!\n" + bcolors.ENDC)
                  else:
                        print(bcolors.FAIL + "\nThis employee does not exist.\n" + bcolors.ENDC)

            case "3":
                  empId = input("Please enter the employee's ID whom you wish to delete: ")
                  employees = get_employee_by_id(empId)

                  if len(employees) == 1:
                        delete_employee(empId)
                        print(bcolors.OKGREEN + "\nEmployee successfully deleted!\n" + bcolors.ENDC)
                  else:
                        print(bcolors.FAIL + "\nThis employee does not exist.\n" + bcolors.ENDC)


            case "4":
                  employees = get_employee()

                  # Print employee info if it is the only one
                  if len(employees) > 1:
                        handle_multiple_employees(employees)
                  elif len(employees) == 0:
                        print(bcolors.FAIL + "\nThis Employee does not exist.\n" + bcolors.ENDC)
                  else:
                        employees[0].printEmployee()
            case "q":
                  exit()
            case _:
                  print(bcolors.FAIL + "\nError: invalid option selected. Please try again with a valid input.\n" + bcolors.ENDC)

while True:
      initialize_db()
      menu()