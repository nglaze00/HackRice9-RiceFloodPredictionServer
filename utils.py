"""
Utility functions.
"""
import datetime

def fmt(n):
    """
    Formats n as a string, with leading 0 if single-digit
    """
    if n < 10:
        return "0" + str(n)
    else:
        return str(n)

def cur_date():
    """
    Returns current date, formatted YYYYMMDD
    """
    now = datetime.datetime.now()
    return fmt(now.year) + fmt(now.month) + fmt(now.day)

def generate_dates():
    """
	Returns a list of all dates between 1/1/2018 and 9/20/2019 as strings in the format YYYYMMDD
	"""
    days_per_mo = [None, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    dates = []
    for yyyy in ["2018", "2019"]:
        for mm in range(1, 13):
            for dd in range(1, days_per_mo[mm] + 1):

                dates.append(yyyy + fmt(mm) + fmt(dd))
    return dates


