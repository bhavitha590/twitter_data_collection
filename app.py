from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask,render_template,jsonify,json,request
from fabric.api import *

application = Flask(__name__)

client = MongoClient('localhost:27017')
db = client.twitterdb

@application.route("/gettwitterdata",methods = ['POST'])
def gettwitterdata():
	try:
		collection = db.twitter_search.find()

		collection_list = []

		for data in collection:
			

			tweet_text = [data['text']]
			tweet_text.append('')
			twitter_url = 'https://twitter.com/' + data['user_name'] + '/status/' +data['_id']
			if 'https' in data['text']:
				tweet_text = data['text'].split('https')
			collection_item = {
				'text' : tweet_text[0],
				'image_url' : data['image_url'],
				'url': twitter_url,
				'created_at' : data['created_at']
				#'twitter_url' : 'https://twitter.com/barakobama/status/'+ data['_id']
			}
			if collection_item['image_url'] != '':
				collection_list.append(collection_item)
	except Exception as e:
		print('Exception caught' + str(e))
		return str(e)
	return json.dumps(collection_list)

@application.route('/')
def showMachineList():
	return render_template('sample.html')	

if __name__ == "__main__":
	application.run(host='0.0.0.0')    
