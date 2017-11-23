from __future__ import print_function
import tweepy
import json
from pymongo import MongoClient
import pprint

MONGO_HOST= 'mongodb://localhost/twitterdb'  # assuming you have mongoDB installed locally
											 # and a database called 'twitterdb'

WORDS = ['#missing', '#lost', '#found']
CONSUMER_KEY = "xxxxxxxxxxxxxxxxx"
CONSUMER_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
ACCESS_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
ACCESS_TOKEN_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

class StreamListener(tweepy.StreamListener):    
	#This is a class provided by tweepy to access the Twitter Streaming API. 

	def on_connect(self):
		# Called initially to connect to the Streaming API
		print("You are now connected to the streaming API.")
 
	def on_error(self, status_code):
		# On error - if an error occurs, display the error / status code
		print('An Error has occured: ' + repr(status_code))
		return False
 
	def on_data(self, data):
		#This is the meat of the script...it connects to your mongoDB and stores the tweet
		try:
			client = MongoClient(MONGO_HOST)
			media_url =''
			# Use twitterdb database. If it doesn't exist, it will be created.
			db = client.twitterdb_1
	
			# Decode the JSON from Twitter
			datajson = json.loads(data)
			pp = pprint.PrettyPrinter(indent=4)
			
			
			if 'retweeted_status' not in datajson:
				# pp.pprint (datajson)
				#grab the 'created_at' data from the Tweet to use for display
				created_at = datajson['created_at']
				#print out a message to the screen that we have collected a tweet
				print("Got Tweet at " + str(created_at))
				
				# Pull important data from the tweet to store in the database.
				tweet_id = datajson['id_str']  # The Tweet ID from Twitter in string format            
				text = datajson['text']  # The entire text in tweet of the Tweet
				hashtags = datajson['entities']['hashtags']  # Any hashtags used in the Tweet
				dt = datajson['created_at']  # The timestamp of when the Tweet was created
				language = datajson['lang']  # The language of the Tweet
				location = datajson['coordinates'] # The coordinates of the tweet
				user_name = datajson['user']['name']

				if location is not None: # if not a Nonetype
					location = location['coordinates']

				#media url 
				image_url = ""
				media = datajson["entities"].get('media', [])
				if(len(media) >0):
					image_url = media[0]['media_url']
			   
				print ("image_url", image_url)

				# Load all of the extracted Tweet data into the variable "tweet" that will be stored into the database
				
				tweet = {   '_id':tweet_id,
							'created_at':created_at, 
							'user_name':user_name , 
							'text':text, 
							'hashtags':hashtags,
							'language':language, 
							'location':location, 
							'image_url':image_url
						}

				print(tweet_id)

				#insert the data into the mongoDB into a collection called twitter_search
				print("Adding tweet to database")
				db.twitter_search.insert(tweet)

			else:
				#pp.pprint (datajson)
				 #grab the 'created_at' data from the Tweet to use for display
				retweet = datajson['retweeted_status']
				created_at = retweet['created_at']
				#print out a message to the screen that we have collected a tweet
				print("Got Re-Tweet at " + str(created_at))
				#pprint(datajson)

				tweet_id = retweet['id_str']  # The Tweet ID from Twitter in string format            
				text = retweet['text']  # The entire body of the Tweet
				hashtags = retweet['entities']['hashtags']  # Any hashtags used in the Tweet
				dt = retweet['created_at']  # The timestamp of when the Tweet was created
				language = retweet['lang']  # The language of the Tweet
				location = retweet['coordinates'] #The coordinates of Tweet
				user_name = retweet['user']['name']
				#media url 
				image_url = ""
				entities = retweet["entities"]
				media_entities = entities.get('media',[])
				if len(media_entities)>0:
					extended_tweet = retweet["extended_tweet"]
					media = extended_tweet["entities"].get('media', [])
					if(len(media) >0):
						image_url = media[0]['media_url']
					
					if location is not None:  #if not a Nonetype
						location = location['coordinates']
			   
				# Load all of the extracted Tweet data into the variable "tweet" that will be stored into the database
				
				tweet = {   '_id':tweet_id,
							'created_at':created_at,
							'user_name':user_name,  
							'text':text,
							'hashtags':hashtags,
							'language' :language, 
							'location':location, 
							'image_url':image_url
						} 

			   
				print(tweet_id)

				#insert the data into the mongoDB into a collection called twitter_search
				if db.twitter_search.find({"_id":tweet_id}).count() == 0 :
					print("Adding retweet to database")
					db.twitter_search.insert(tweet)
				else:
					print("Retweet already in db, skipping")
		except Exception as e:
			print("exception caught")
			print(e)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
#Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True)) 
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: " + str(WORDS))
streamer.filter(track=WORDS,languages=["en"])
