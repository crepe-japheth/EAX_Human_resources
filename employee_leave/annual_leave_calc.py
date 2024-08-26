from datetime import datetime

def calc_annual(leave_date, returning_date):
    date_format = "%Y-%m-%d"
    difference = datetime.strptime(returning_date, date_format) - datetime.strptime(leave_date, date_format)
    if difference.days > 18:
        return False
    return True


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

def calc_parternity_leave(leave_date, returning_date):
    date_format = "%Y-%m-%d"
    difference = datetime.strptime(returning_date, date_format) - datetime.strptime(leave_date, date_format)
    if difference.days > 4:
        return False
    return True

def calc_sabbatical_leave(leave_date, returning_date):
    date_format = "%Y-%m-%d"
    difference = datetime.strptime(returning_date, date_format) - datetime.strptime(leave_date, date_format)
    if difference.days > 90:
        return False
    return True