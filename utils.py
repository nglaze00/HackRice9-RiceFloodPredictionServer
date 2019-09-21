"""
Utility functions.
"""
import datetime
import numpy as np

FLOODED_THRESHOLD = 4 # inches
DAYS_TO_KEEP = 628 # number of days to use in training data

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

def days_ago(n):
    """
    Returns the date n days ago
    """
    old_date = datetime.datetime.now() - datetime.timedelta(days=n)
    return fmt(old_date.year) + fmt(old_date.month) + fmt(old_date.day)

def generate_dates():
    """
	Returns a list of all dates between 1/1/2018 and 9/22/2019 as strings in the format YYYYMMDD
	"""
    days_per_mo = [None, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    dates = []
    for yyyy in ["2018", "2019"]:
        for mm in range(1, 13):
            for dd in range(1, days_per_mo[mm] + 1):
                if mm == 9 and dd == 22 and yyyy == "2019":
                    return dates
                dates.append(yyyy + fmt(mm) + fmt(dd))
    return dates


def coords_to_id():
    """
    Returns a dictionary mapping node coordinates to their ID
    """
    m = {}
    for id, line in enumerate(open("coords.txt").readlines()):
        if line == "\n":
            continue
        coords_str = line.split(", ")
        coords_str[1] = coords_str[1][:-2]
        coords = tuple(map(np.float, line.split(", ")))
        m[coords] = id
    return m