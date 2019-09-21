import pymongo
from flask import Flask


mongo = pymongo.MongoClient('mongodb+srv://lbonnage:Mongodb@hackrice9-ricefloodprediction-zqrfo.gcp.mongodb.net/test?retryWrites=true&w=majority', maxPoolSize=50, connect=False)

db = pymongo.database.Database(mongo, 'test')
col = pymongo.collection.Collection(db, 'node')

print(col.find_one())

newdoc = {
	"name": "test2",
	"location": [1, 2]
}

col.insert_one(newdoc)

app = Flask(__name__)

@app.route('/')
def hello():
	return "Hello world!"

# @app.route('/click')
# def handle_click(click):
# 	coll.add(click)


if __name__ == '__main__':
	app.run()

