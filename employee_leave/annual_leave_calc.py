from datetime import datetime, timedelta

def calc_annual(leave_date, returning_date):
    date_format = "%Y-%m-%d"
    start_date = datetime.strptime(leave_date, date_format)
    end_date = datetime.strptime(returning_date, date_format)

    total_days = (end_date - start_date).days + 1  # Include both start and end date
    weekdays_count = 0

    for single_date in (start_date + timedelta(n) for n in range(total_days)):
        if single_date.weekday() < 5:  # Monday=0, Sunday=6, exclude weekends
            weekdays_count += 1

    if weekdays_count > 18:
        return False, weekdays_count

    return True, weekdays_count

# def calc_annual(leave_date, returning_date):
#     date_format = "%Y-%m-%d"
#     difference = datetime.strptime(returning_date, date_format) - datetime.strptime(leave_date, date_format)
#     if difference.days > 18:
#         return False, difference.days
#     return True, difference.days


def calc_sick_leave(leave_date, returning_date):
    date_format = "%Y-%m-%d"
    difference = datetime.strptime(returning_date, date_format) - datetime.strptime(leave_date, date_format)
    if difference.days > 90:
        return False
    return True

def calc_marternity_leave(leave_date, returning_date):
    date_format = "%Y-%m-%d"
    difference = datetime.strptime(returning_date, date_format) - datetime.strptime(leave_date, date_format)
    if difference.days > 90:
        return False
    return True

# def calc_parternity_leave(leave_date, returning_date):
#     date_format = "%Y-%m-%d"
#     difference = datetime.strptime(returning_date, date_format) - datetime.strptime(leave_date, date_format)
#     if difference.days > 4:
#         return False
#     return True

def calc_parternity_leave(leave_date, returning_date):
    date_format = "%Y-%m-%d"
    start_date = datetime.strptime(leave_date, date_format)
    end_date = datetime.strptime(returning_date, date_format)

    total_days = (end_date - start_date).days + 1  # Include both start and end date
    weekdays_count = 0

    for single_date in (start_date + timedelta(n) for n in range(total_days)):
        if single_date.weekday() < 5:  # Monday=0, Sunday=6, exclude weekends
            weekdays_count += 1

    if weekdays_count > 4:
        return False, weekdays_count

    return True, weekdays_count

def calc_sabbatical_leave(leave_date, returning_date):
    date_format = "%Y-%m-%d"
    difference = datetime.strptime(returning_date, date_format) - datetime.strptime(leave_date, date_format)
    if difference.days > 90:
        return False
    return True