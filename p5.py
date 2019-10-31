
from payroll import *
import shutil

def main():
    load_employees()
    process_timecards()
    process_receipts()
    run_payroll()

    # Save copy of payroll file
    shutil.copyfile('payroll.txt', 'paylog1.txt')

    # Change Karina Gay to Salaried and DirectMethod by changing her Employee object:
    emp = find_employee_by_id('688997')
    emp.make_salaried(45884.99)
    emp.direct_method('30417353-K', '465794-3611')

    # Change TaShya Snow to Commissioned and MailMethod; add some receipts
    emp = find_employee_by_id('522759')
    emp.make_commissioned(50005.50, 25)
    emp.direct_method('30417353-K', '465794-3611')
    clas = emp.classification
    clas.add_receipt(1109.73)
    clas.add_receipt(746.10)

    # Change Rooney Alvarado to Hourly; add some hour entries
    emp = find_employee_by_id('165966')
    emp.make_hourly(21.53)
    clas = emp.classification
    clas.add_timecard(8.0)
    clas.add_timecard(8.0)
    clas.add_timecard(8.0)
    clas.add_timecard(8.0)
    clas.add_timecard(8.0)

    # Rerun payroll
    run_payroll()

if __name__ == '__main__':
    main()
