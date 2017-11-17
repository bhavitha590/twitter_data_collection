from flask import Flask,render_template
from pymongo import MongoClient
import os
import webbrowser
import json
from bson import json_util

application = Flask(__name__)

client = MongoClient('localhost:27017')

db = client.twitter
cursor = db.random.find({})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
webbrowser.open('file://' + os.path.join(BASE_DIR, 'list.html'))
#@application.route("/")
#def getList():
	#return render_template('test.html')
@application.route('/twitters', methods = ['GET'])
def getMachineList():
	    return json.dumps(cursor, default = json_util.default)
	    #return jsonify()
	    #return render_template('list.html')

if __name__ == "__main__":
    application.run(host='0.0.0.0')
