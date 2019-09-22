"""
API for interacting with Rice campus nodes
"""
import server
import utils, weather
import numpy as np

DB = server.db
linear_model = server.linear_model

# INPUT

def report_water_level(node, lvl):
    """
    Reports a water level at the given coordinates; adds value to mongoDB database
    :param node: node id
    :param lvl: integer representing water level @ node
    """
    DB.report_rain_level(utils.cur_date(), node, lvl)

# OUTPUT

def get_reported_water_levels():
    """
    Returns a dictionary of reported water levels. Indexed rain_data[node coords][date][report #]
    """
    nodes = DB.get_nodes()
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

def get_average_water_levels(date):
    """
    Returns a dictionary with key: node id, value: average water level on that date TODO
    """
    return {node["id"] : node["avg_levels"][date] for node in DB.get_nodes()}

# OBSELETE
def get_is_flooded(date):
    """
    Returns a dictionary with key: node id, value: whether the node is flooded on the given date.
    # 0: not flooded
    # 1: reported flooded
    # 2: predicted flooded
    """
    is_flooded = {}
    for node in DB.get_nodes():
        if len(node["rain_data"][date]) == 0:
            # If no reports on this day, use the linear model
            if server.linear_model.fit(weather.get_precipitation(date)):
                is_flooded[node["id"]] = 2
            else:
                is_flooded[node["id"]] = 0
        elif node["is_flooded"][date]:
            is_flooded[node["id"]] = 1
        else:
            is_flooded[node["id"]] = 0
    return {node["id"] : node["is_flooded"][date] for node in DB.get_nodes()}

# OBSELETE