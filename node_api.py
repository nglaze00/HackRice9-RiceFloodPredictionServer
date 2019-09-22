"""
API for interacting with Rice campus nodes
"""
import server
import utils, weather
import numpy as np

DB = server.db

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
