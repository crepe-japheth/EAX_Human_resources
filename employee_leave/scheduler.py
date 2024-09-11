from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from .models import Employee
from decouple import config

def carryover_leave():
    # Get all employees
    employees = Employee.objects.all()

    for employee in employees:
        # Calculate remaining leave days
        remaining_leave = employee.allowed_leave

        if remaining_leave > 10:
            # Carry over only 10 days plus the usual 18 days
            employee.initial_leave = 18 + 10
        else:
            # Carry over all remaining days plus 18
            employee.initial_leave = 18 + remaining_leave

        # Reset taken leave and update allowed leave for the new year
        employee.taken_leave = 0
        employee.allowed_leave = employee.initial_leave
        employee.save()

    print(f"Carryover process completed at {datetime.now()}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Schedule the carryover_leave task to run once a year, at midnight on January 1st
    scheduler.add_job(carryover_leave, 'cron', year=config("YEAR"), month=config("MONTH"), day=config("DAY"), hour=config("HOUR"), minute=config("MINUTE"))
    # scheduler.add_job(carryover_leave, 'cron', year=2024, month=9, day=6, hour=9, minute=51)
    scheduler.start()
