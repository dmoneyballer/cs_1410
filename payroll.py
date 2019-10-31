from abc import ABC, abstractmethod
import shutil
import os
employees = []
EMPLOYEE_FILE = 'employees.csv'
TIMECARD_FILE = 'timecards.txt'
RECEIPTS_FILE = 'receipts.txt'
pay_logfile = 'payroll.txt'
def load_employees():
    reader = open(EMPLOYEE_FILE, 'r')
    reader.readline()
    line = reader.readline()
    while line:
        vals = str(line).strip('\n').split(',')
        employees.append(Employee(vals))
        line = reader.readline()
    reader.close()


def process_timecards():
    reader = open(TIMECARD_FILE, 'r')
    line = reader.readline()
    while line:
        vals = str(line).strip('\n').split(',')
        emp = find_employee_by_id(vals[0])
        vals = vals[1:]
        if emp:
            clas = emp.classification
            # assert isinstance(clas, Hourly)
            if isinstance(clas, Hourly):
                for val in vals:
                    clas.add_timecard(float(val))
        line = reader.readline()
    reader.close()

def process_receipts():
    with open(RECEIPTS_FILE, 'r') as f:
        line = f.readline()
        while line:
            vals = str(line).strip('\n').split(",")
            emp = find_employee_by_id(vals.pop(0))
            if emp:
                if isinstance(emp.classification, Commissioned):
                    for rec in vals:
                        emp.classification.add_receipt(float(rec))
            line = f.readline()

def run_payroll():
    if os.path.exists(pay_logfile): # pay_log_file is a global variable holding ‘payroll.txt’
        os.remove(pay_logfile)
    with open('payroll.txt', 'w') as f:
        for emp in employees: # employees is the global list of Employee objects
            emp.issue_payment() 


def find_employee_by_id(id):
    for emp in employees:
        if emp.id == id:
            return emp

class Employee:
    def __init__(self, *args):
        self.id = args[0][0]
        self.name = args[0][1]
        self.address = args[0][2]
        self.city = args[0][3]
        self.state = args[0][4]
        self.zipCode = args[0][5]
        self.classification = None
        self.method = args[0][7]
        self.hourlyWage = float(args[0][9])
        self.salary = float(args[0][8])
        self.commissioned = float(args[0][10]) *.1
        if int(args[0][6]) == 1:
            self.make_hourly(args[0][9])
        if int(args[0][6]) == 2:
            self.make_salaried(args[0][8])
        if int(args[0][6]) == 3:
            self.make_commissioned(args[0][8], args[0][10])
        self.routing = args[0][-2]
        self.account = args[0][-1]
        
    def issue_payment(self):
        if self.method == '1':
            self.direct_method(self.routing, self.account)
            self.payment.issue_payment(self.classification)
        else:
            self.mail_method(self.address)
            self.payment.issue_payment(self.classification)
    
    def make_salaried(self, salary):
        self.classification = Salary(self, salary)

    def make_hourly(self, hourlyWage):
        self.classification = Hourly(self, self.hourlyWage)
    
    def make_commissioned(self, salary, commission):
        self.classification = Commissioned(self, salary, commission)
    
    def direct_method(self, route, account):
        self.method = '1'
        self.payment = DirectMethod(self, route, account)
    
    def mail_method(self, address):
        self.method = '2'
        self.payment = MailMethod(self, address)

class DirectMethod(Employee):
    def __init__(self, emp, route, account):
        self.emp = emp
        self.routing = route
        self.account = account

    def issue_payment(self, classification):
        money = classification.issue_payment()
        with open(pay_logfile, 'a') as writer:
            writer.write(f'${round(money,2)} mailed to {self.emp.name} at {self.emp.address}\n')

class MailMethod(Employee):
    def __init__(self, emp, address):
        self.emp = emp
        self.address = address

    def issue_payment(self, classification):
        money = classification.issue_payment()
        with open(pay_logfile, 'a') as writer:
            writer.write(f'${round(money,2)} mailed to {self.emp.name} at {self.emp.address}\n')

class Classification(ABC):
    def __init__(self, emp):
        self.emp = emp
    
    @abstractmethod
    def issue_payment(self):
        pass

class Hourly(Classification):
    def __init__(self, emp, hourlWage):
        super().__init__(emp)
        self.hourlyWage = hourlWage
        self.hoursWorked = []

    def issue_payment(self):
        money = 0
        for hours in self.hoursWorked:
            money += float(hours) * self.hourlyWage
        return money

    def add_timecard(self, hoursWorked):
        self.hoursWorked.append(hoursWorked)

class Salary(Classification):
    def __init__(self, emp, salary):
        super().__init__(emp)
        self.salary = salary
    
    def issue_payment(self):
        return float(self.salary)/24 

class Commissioned(Classification):
    def __init__(self, emp, salary, commission):
        super().__init__(emp)
        self.salary = salary
        self.commission = float(commission) * .01
        self.receipts = []

    def issue_payment(self):
        money = float(self.salary)/24
        for rec in self.receipts:
            money += float(rec) * float(self.commission)
        return money

    def add_receipt(self, receipt):
        self.receipts.append(receipt)