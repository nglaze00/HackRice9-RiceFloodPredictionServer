"""
Functions for querying the mongoDB database.

Node signature:
node_dict = {
				"id": node_id,
				"coords": coords,
				"rain_data": reported rain data, indexed by date
				"avg_levels": average reported rain data, indexed by date
				"is_flooded": whether a node is flooded on a given day, indexed by date
				"entrance": -1 if node is not a campus entrance, entrance number if it is
			}
"""



import pymongo, numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from threading import Thread
import time

import utils, testdeyda, model, node_api
import weather


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
		return self._nodes.find_one({key : value}, {'_id': False})

	def get_nodes(self):
		"""
		Queries the mongoDB database for all nodes
		:return:
		"""
		self.update_is_flooded()
		return list(self._nodes.find({}, {'_id': False}))

	def update_is_flooded(self):
		for node in self.get_nodes():
			if len(node["rain_data"][utils.cur_date()]) == 0:
				# If no reports on this day, use the linear model
				if linear_model.fit(weather.get_precipitation(utils.cur_date())):
					node["is_flooded"][node["id"]] = 2
				else:
					node["is_flooded"][node["id"]] = 0
			elif node["is_flooded"][utils.cur_date()]:
				node["is_flooded"][node["id"]] = 1
			else:
				node["is_flooded"][node["id"]] = 0

		update = {"$set": {"is_flooded": node["is_flooded"]}}
		self._nodes.update({"id": node["id"]}, update)

	def report_rain_level(self, date, coords, lvl):
		"""
		Adds the measured rain level @ coords on date to that node's rain level dataset in mongoDB.
		Also updates avg level & is_flooded for that date.
		:param date: YYYYMMDD
		:param coords: (lat, long)
		:param lvl: integer (inches)
		"""
		node = self._nodes.find_one({"coords" : coords}, {'_id': False})

		if not node:
			raise KeyError()

		node["rain_data"][date].append(lvl)

		update = {"$set": {"rain_data": node["rain_data"]}}
		self._nodes.update({"id" : node["id"]}, update)

		self._update_avg_level(date, node)


	def _update_avg_level(self, date, node):
		"""
		Updates the average water level & binary is_flooded at given node, for given date.
		"""

		node["avg_levels"][date] = np.mean(node["rain_data"][utils.cur_date()])
		if node["avg_levels"][date] > utils.FLOODED_THRESHOLD:
			node["is_flooded"][date] = True
		else:
			node["is_flooded"][date] = False

		update = {"$set": {"avg_levels" : node["avg_levels"], "is_flooded" : node["is_flooded"]}}
		self._nodes.update({"id": node["id"]}, update)

	def clear_rain_level(self, date, coords): # todo remove
		node = self._nodes.find_one({"coords": coords})

		if not node:
			raise KeyError()

		node["rain_data"][date] = []

		update = {"$set": {"rain_data": node["rain_data"]}}
		self._nodes.update({"id": node["id"]}, update)

	def add_all_nodes(self, filename):
		"""
		Clears all data from database, then adds all nodes from filename to the mongoDB database
		:param filename: string
		"""
		self._nodes.delete_many({})

		empty_date_lists = {date: [] for date in utils.generate_dates()}
		empty_date_scalars = {date: 0 for date in utils.generate_dates()}
		empty_date_bools = {date: False for date in utils.generate_dates()}
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
				"rain_data": empty_date_lists,
				"avg_levels": empty_date_scalars,
				"is_flooded": empty_date_scalars,
				"entrance": -1
			}
			self._nodes.insert(node_dict)


db = MongoDB()
linear_model = model.LinearRainModel()

# print(get_nodes())

def server_app(db):
	"""
	Runner for server.
	"""
	# db.add_all_nodes("coords.txt")
	global linear_model
	while True:
		# Each day, add date as key to dataset and drop the oldest day
		for i in range(7):
			time.sleep(86400)

			date_to_drop = utils.days_ago(utils.DAYS_TO_KEEP + 1)
			nodes = db.get_nodes()
			for node in nodes:
				node["rain_data"].pop(date_to_drop)
				node["avg_levels"].pop(date_to_drop)
				node["is_flooded"].pop(date_to_drop)

				node["rain_data"][utils.cur_date()] = []
				node["avg_levels"][utils.cur_date()] = 0
				node["is_flooded"][utils.cur_date()] = 0

		# Each week, retrain the model
		# In production, use weather API data. For now, use generated values to test.
		# model = RFModel(weather.get_precips(start_date, end_date), db.get_nodes())
		linear_model = model.LinearRainModel()



flask_app = Flask(__name__)
CORS(flask_app, support_credentials=True)

@flask_app.route('/')
def hello():
	return "Hello world!"

@flask_app.route('/click', methods=["POST"])
@cross_origin(supports_credentials=True)
def handleClick():
	print(request.data)
	return request.form

@flask_app.route('/floodreport', methods=["POST"])
@cross_origin(supports_credentials=True)
def handleFloodReport():
	print(request.data)
	print(request.get_json(force=True)["node"])

	##
	# Data contains:
	# node
	# type (0 is lowest, 3 is worst severity)
	##
	data = request.get_json(force=True)
	node = data["node"]
	water_level = data["type"]
	node_api.report_water_level(node["coords"], water_level * 2) # convert to inches


	return request.form

@flask_app.route('/nodes')
def getNodes():
	return jsonify(db.get_nodes())


if __name__ == '__main__':
	# db = MongoDB()

	Thread(target=flask_app.run, args=[]).start()
	Thread(target=server_app, args=[db]).start()


