"""
Functions for querying the mongoDB database.

Node signature:
node_dict = {
			"id": node_id,
			"coords": coords (latitude, longitude),
			"rain_data": {date : [reported rain values]}
		}
"""



import pymongo, numpy as np
from flask import Flask
import utils

class MongoDB:
	def __init__(self):
		self._mongo = pymongo.MongoClient(
			'mongodb+srv://lbonnage:Mongodb@hackrice9-ricefloodprediction-zqrfo.gcp.mongodb.net/test?retryWrites=true&w=majority',
			maxPoolSize=50, connect=False)
		self._db = pymongo.database.Database(self._mongo, 'test')
		self._nodes = pymongo.collection.Collection(self._db, 'node')


	def get_node(self, key, value):
		"""
		Queries the mongoDB database for one node
		:param key: string representing node variable
		:param value: value of that node variable
		:return: node dict
		"""
		return self._nodes.find_one({key : value})

	def get_nodes(self):
		"""
		Queries the mongoDB database for all nodes
		:return:
		"""
		return list(self._nodes.find())



	def report_rain_level(self, date, coords, lvl):
		"""
		Adds the measured rain level @ coords on date to that node's rain level dataset in mongoDB.
		:param date: YYYYMMDD
		:param coords: (lat, long)
		:param lvl: integer (inches)
		"""
		node = self._nodes.find_one({"coords" : coords})

		if not node:
			raise KeyError()

		node["rain_data"][date].append(lvl)

		update = {"$set": {"rain_data": node["rain_data"]}}
		self._nodes.update({"id" : node["id"]}, update)

	def clear_rain_level(self, date, coords): # todo remove
		node = self._nodes.find_one({"coords": coords})

		if not node:
			raise KeyError()

		node["rain_data"][date] = []

		update = {"$set": {"rain_data": node["rain_data"]}}
		self._nodes.update({"id": node["id"]}, update)

	def add_all_nodes(self, filename):
		"""
		Adds all nodes from filename to the mongoDB database
		:param filename: string
		"""
		empty_dates_dict = {date: [] for date in utils.generate_dates()}

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
			self._nodes.insert(node_dict)



db = MongoDB()

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


