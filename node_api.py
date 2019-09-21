"""
API for interacting with Rice campus nodes
"""
import server
import utils
import numpy as np

DB = server.db

# INPUT

def report_water_level(coords, lvl):
    """
    Reports a water level at the given coordinates; adds value to mongoDB database
    :param coords: (latitude, longitude)
    :param lvl: integer representing water level @ node
    """
    DB.report_rain_level(utils.cur_date(), coords, lvl)

# OUTPUT

def get_reported_water_levels():
    """
    Returns a dictionary of reported water levels. Indexed rain_data[node coords][date][report #]
    """
    nodes = DB.get_nodes()
    dates = utils.generate_dates()
    water_levels = {}
    for node in nodes:
        water_levels[tuple(node["coords"])] = node["rain_data"]
    return water_levels

def count_nonempty_lists():
    """
    Counts node & date combinations with a reported value
    :return:
    """
    c = 0
    water_levels = get_reported_water_levels()
    print(water_levels)
    for node in water_levels.values():
        for lst in node.values():
            if lst:
                c += 1
    return c
def get_reported_water_levels_today():
    """
    Returns reported water levels on the current date.
    :return:
    """
    today = utils.cur_date()
    return {node["coords"] : node["rain_data"][today] for node in DB.get_nodes()}
def compute_water_level_avgs():
    """
    Returns a 2-D Numpy array of nodewise daily average water levels. Indexed rain_data[node_id][date].
    :return: rain_data (numpy array) TODO
    """
    pass
def drop_old_data():
    """
    Drops data older than 1.5 yrs.
    # TODO
    """
    pass

# TODO remove the one value in current day, first node