"""
API for interacting with Rice campus nodes
"""
import datetime
import server
import utils
import numpy
db = server.MongoDB() # todo remove


# INPUT

def report_water_level(coords, lvl):
    """
    Reports a water level at the given coordinates; adds value to mongoDB database
    :param coords: (latitude, longitude)
    :param lvl: integer representing water level @ node
    """

    now = datetime.datetime.now()
    cur_date = utils.fmt(now.year) + utils.fmt(now.month) + utils.fmt(now.day)
    db.report_rain_level(cur_date, coords, lvl)


# OUTPUT

def rain_data_to_array():
    """
    Returns a numpy array of daily rain level data. Indexed rain_data[node_id][date].
    :return: numpy array
    """