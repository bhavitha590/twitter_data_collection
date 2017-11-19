from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask,render_template,jsonify,json,request
from fabric.api import *

application = Flask(__name__)

client = MongoClient('localhost:27017')
db = client.twitterdb_1

@application.route("/gettwitterdata",methods = ['POST'])
def gettwitterdata():
	try:
		collection = db.twitter_search.find()

		collection_list = []
		for data in collection:
			print(data)
			collection_item = {
				'text' : data['text'],
				'image_url' : data['image_url'],
				'location' : data['location'],
				'created_at' : data['created_at']
				#'twitter_url' : 'https://twitter.com/barakobama/status/'+ data['_id']
			}
			collection_list.append(collection_item)
	except e:
		return str(e)
	return json.dumps(collection_list)

@application.route('/')
def showMachineList():
    return render_template('sample.html')	

if __name__ == "__main__":
    application.run(host='0.0.0.0')    
