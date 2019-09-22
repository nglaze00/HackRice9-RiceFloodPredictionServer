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

import utils, models, node_api, graphs
import weather



class MongoDB:
	def __init__(self):
		self._mongo = pymongo.MongoClient(
			'mongodb+srv://lbonnage:Mongodb@hackrice9-ricefloodprediction-zqrfo.gcp.mongodb.net/test?retryWrites=true&w=majority',
			maxPoolSize=50, connect=False)
		self._db = pymongo.database.Database(self._mongo, 'test')
		self._nodes = pymongo.collection.Collection(self._db, 'node')
		self._graph = graphs.Graph(graphs.GRAPH_FILENAME)

		self.linear_model = models.LinearRainModel()
		# Demo XGBoost models on these nodes
		self.XGB_models = {6: models.NodeFloodPredictor(6),
						   8: models.NodeFloodPredictor(8),
						   32: models.NodeFloodPredictor(32),
						   22: models.NodeFloodPredictor(22)}
		for model in self.XGB_models.values():
			model.train()
			model.test()

	def graph(self):
		return self._graph

	def get_node(self, key, value):
		"""
		Queries the mongoDB database for one node
		:param key: string representing node variable
		:param value: value of that node variable
		:return: node dict
		"""
		return self._nodes.find_one({key : value}, {'_id': False})

	def sorted_nodes(self):
		return list(self._nodes.find({}, {'_id': False}).sort("id"))
	def get_nodes(self):
		"""
		Queries the mongoDB database for all nodes
		:return:
		"""
		for node in self.sorted_nodes():
			self._update_avg_level(utils.cur_date(), node)
		self.update_is_flooded()
		return list(self._nodes.find({}, {'_id': False}).sort("id"))


	def predict_is_flooded(self):
		"""
			Predicts the value of all nodes with no reported data, using either the linear or XGBoost models.
			Uses reported values for those that have it.
			"""
		queried_nodes = self.sorted_nodes()
		reported_is_flooded = [node["is_flooded"] for node in queried_nodes]
		linear_predictions = self.linear_model.fit(weather.get_precipitation(utils.cur_date()))

		reported_with_linear = list(reported_is_flooded)
		# Insert linear prediction for values with no reported data
		for node in queried_nodes:
			if node["id"] == 6:
				print(node["avg_levels"][utils.cur_date()])
				print(node["is_flooded"][utils.cur_date()])
			# No reports; pred w linear
			if len(node["rain_data"][utils.cur_date()]) == 0:
				if linear_predictions[node["id"]] == True:
					reported_with_linear[node["id"]] = 2
				else:
					reported_with_linear[node["id"]] = 0
			# Reports; use existing
			else:
				if reported_is_flooded[node["id"]][utils.cur_date()] == 1:
					reported_with_linear[node["id"]] = 1
				else:
					reported_with_linear[node["id"]] = 0

		reported_with_linear_and_XGB = list(reported_with_linear)
		# Replace linear predictions with XGB predictions when possible
		for node_id in self.XGB_models.keys():
			if len(queried_nodes[node_id]["rain_data"][utils.cur_date()]) == 0:
				xgb_prediction = self.XGB_models[node_id].predict([reported_with_linear[:node_id]
																  + reported_with_linear[node_id+1:]])
				print(xgb_prediction)
				if xgb_prediction:
					reported_with_linear_and_XGB[node_id] = 2
				else:
					reported_with_linear_and_XGB[node_id] = 0
		print(reported_with_linear_and_XGB[6])
		return reported_with_linear_and_XGB


	def update_is_flooded(self):
		"""
			Predicts is_flooded for all nodes and uploads the data to the mongoDB server.
			:return:
			"""
		reports_plus_predictions = self.predict_is_flooded()
		for node in self._nodes.find({}, {'_id': False}):
			node["is_flooded"][utils.cur_date()] = reports_plus_predictions[node["id"]]
			update = {"$set": {"is_flooded": node["is_flooded"]}}
			self._nodes.update({"id": node["id"]}, update)

	def report_rain_level(self, date, node, lvl):
		"""
		Adds the measured rain level @ coords on date to that node's rain level dataset in mongoDB.
		Also updates avg level & is_flooded for that date.
		:param date: YYYYMMDD
		:param node: node id
		:param lvl: integer (inches)
		"""

		node = self._nodes.find_one({"id" : node}, {'_id': False})

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
		if len(node["rain_data"][date]) != 0:
			node["avg_levels"][date] = np.mean(node["rain_data"][date])
		else:
			node["avg_levels"][date] = 0
		if node["avg_levels"][date] >= utils.FLOODED_THRESHOLD:
			node["is_flooded"][date] = 1
		else:
			node["is_flooded"][date] = 0

		update = {"$set": {"avg_levels" : node["avg_levels"], "is_flooded" : node["is_flooded"]}}
		self._nodes.update({"id": node["id"]}, update)

	def add_all_nodes(self):
		"""
		Clears all data from database, then adds all nodes from filename to the mongoDB database
		:param filename: string
		"""
		self._nodes.delete_many({})
		empty_date_lists = {date: [] for date in utils.generate_dates()}
		empty_date_scalars = {date: 0 for date in utils.generate_dates()}
		empty_date_bools = {date: False for date in utils.generate_dates()}

		for id, data in self._graph.nodes():
			node_dict = {
				"id": id,
				"coords": data["coords"],
				"rain_data": empty_date_lists,
				"avg_levels": empty_date_scalars,
				"is_flooded": empty_date_scalars,
				"entrance": data["entrance"]
			}
			self._nodes.insert(node_dict)


db = MongoDB()

# print(get_nodes())

def server_app(db):
	"""
	Runner for server.
	"""

	# db.add_all_nodes()
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

		# Each week, retrain the models using new data.
		# In production, use weather API data. For now, use generated values to test.

		# Dump updated nodewise average water level data to depths_train.txt
		depths_dict = node_api.get_reported_water_levels()
		depths = np.empty((len(depths_dict.keys()), len(depths_dict[0].keys())))
		for date_idx, date in enumerate(sorted(depths_dict[0].keys())):
			for node_id in sorted(depths_dict.keys()):
				this_mean = np.mean(depths_dict[node_id][date])
				if not this_mean:
					this_mean = 0
				depths[date_idx][node_id] = this_mean
		np.savetxt("depths_train.txt", depths)

		# Retrain models
		db.linear_model = models.LinearRainModel()
		for model in db.XGB_models.values():
			model.train()
			model.test()



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
	# node is the id number
	# type (0 is lowest, 3 is worst severity)
	##
	data = request.get_json(force=True)
	node = data["node"]
	water_level = data["type"]
	node_api.report_water_level(int(node), water_level * 2) # convert to inches


	return request.form

@flask_app.route('/path', methods=["POST"])
@cross_origin(supports_credentials=True)
def handlePath():
	print(request.data)
	print(request.get_json(force=True)["firstNode"])
	print(request.get_json(force=True)["secondNode"])


	##
	# Data contains:
	# startNode is the id number
	# endNode is the id number
	##
	data = request.get_json(force=True)
	startnode = int(data["firstNode"])
	endnode = int(data["secondNode"])

	# make the path here
	wet_nodes = []
	for node in db.get_nodes():
		if node["is_flooded"][utils.cur_date()]:
			wet_nodes.append(node["id"])
	path_type, path = db.graph().shortest_path(startnode, endnode, wet_nodes)

	return jsonify({"path_type": path_type, "path": path, "path_coords" : [db.get_node("id", node_id)["coords"] for node_id in path]})

@flask_app.route('/nodes')
def getNodes():
	return jsonify(db.get_nodes())



if __name__ == '__main__':
	# db = MongoDB()

	Thread(target=flask_app.run, args=[]).start()
	Thread(target=server_app, args=[db]).start()


