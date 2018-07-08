from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask,render_template,jsonify,json,request
from fabric import *
from operator import itemgetter
application = Flask(__name__)

client = MongoClient('localhost:27017')
db = client.twitterdb

@application.route("/gettwitterdata",methods = ['POST'])


def gettwitterdata():
	try:
		collection = db.twitter_search.find()

		collection_list = []
		not_words = ["missing you","movie","episode"]
		s = set();
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
				skip = False
				for word in not_words:
					if(word in data['text']):
						skip = True
				if tweet_text[0] not in s and skip == False:
					s.add(tweet_text[0])
					collection_list.append(collection_item)

		def str2int2(s):
				time = s.split(" ")
				year = 2000;
				time[5] = int(time[5])
				value = time[5] - year;
				if time[1] == 'Jan':
					value = (value * 365) + (1 * 30) + (int(time[2]))
				elif time[1] == 'Feb':
					value = (value * 365) + (2 * 30) + (int(time[2]))
				elif time[1] == 'Mar':
					value = (value * 365) + (3 * 30) + (int(time[2]))
				elif time[1] == 'Apr':
					value = (value * 365) + (4 * 30) + (int(time[2]))
				if time[1] == 'May':
					value = (value * 365) + (5 * 30) + (int(time[2]))
				if time[1] == 'Jun':
					value = (value * 365) + (6 * 30) + (int(time[2]))
				if time[1] == 'Jul':
					value = (value * 365) + (7 * 30) + (int(time[2]))
				if time[1] == 'Aug':
					value = (value * 365) + (8 * 30) + (int(time[2]))
				if time[1] == 'Sep':
					value = (value * 365) + (9 * 30) + (int(time[2]))
				if time[1] == 'Oct':
					value = (value * 365) + (10 * 30) + (int(time[2]))
				if time[1] == 'Nov':
					value = (value * 365) + (11 * 30) + (int(time[2]))
				if time[1] == 'Dec':
					value = (value * 365) + (12 * 30) + (int(time[2]))
				return value

		def compare(item1, item2):
			if(str2int2(item1['created_at']) > str2int2(item2['created_at'])):
				return -1
			elif str2int2(item1['created_at']) < str2int2(item2['created_at']):
				return 1
			return 0

		sorted(collection_list, key = lambda item: str2int2(item["created_at"]), reverse = True)
		# sorted(collection_list, cmp = compare)
	except Exception as e:
		print('Exception caught' + str(e))
		return str(e)
	return json.dumps(collection_list)

@application.route('/')
def showMachineList():
	return render_template('sample.html')	

if __name__ == "__main__":
	application.run(host='0.0.0.0')    
