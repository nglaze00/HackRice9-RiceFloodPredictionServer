"""
Functions for querying the mongoDB database.
"""



import pymongo, numpy as np
from flask import Flask
import model


mongo = pymongo.MongoClient('mongodb+srv://lbonnage:Mongodb@hackrice9-ricefloodprediction-zqrfo.gcp.mongodb.net/test?retryWrites=true&w=majority', maxPoolSize=50, connect=False)

db = pymongo.database.Database(mongo, 'test')
col = pymongo.collection.Collection(db, 'node')

def get_node(key, value):
	"""
	Queries the mongoDB database for one node
	:param key: string representing node variable
	:param value: value of that node variable
	:return: node dict
	"""
	return col.find_one({key : value})

def get_nodes():
	"""
	Queries the mongoDB database for all nodes
	:return:
	"""
	return list(col.find())



def add_all_nodes(filename):
	"""
	Adds all nodes from filename to the mongoDB database
	:param filename: string
	"""
	empty_dates_dict = {date : [] for date in model.generate_dates()}

	f = open(filename)
	coords = []
	for node_id, line in enumerate(f.readlines()):
		if line == "\n":
			continue
		coords_str = line.split(", ")
		coords_str[1] = coords_str[1][:-2]
		coords = tuple(map(np.float, line.split(", ")))
		node_dict = {
			"id": node_id,
			"coords": coords,
			"rain_data": empty_dates_dict
		}
		col.insert(node_dict)

# add_all_nodes("coords.txt")
# print(get_nodes())


app = Flask(__name__)

@app.route('/')
def hello():
	return "Hello world!"

# @app.route('/click')
# def handle_click(click):
# 	coll.add(click)


if __name__ == '__main__':
	app.run()

