from datetime import datetime

def calc_annual(leave_date, returning_date):
    date_format = "%Y-%m-%d"
    difference = datetime.strptime(returning_date, date_format) - datetime.strptime(leave_date, date_format)
    if difference.days > 18:
        return False
    return True