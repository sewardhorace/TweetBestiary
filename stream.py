import csv
from os import environ

from flask import Flask 
import tweepy

#web server needed to host on heroku
app = Flask(__name__)
app.run(environ.get('PORT'))

#twitter API keys
CONSUMER_KEY = environ.get('CONSUMER_KEY')
CONSUMER_SECRET = environ.get('CONSUMER_SECRET')
ACCESS_KEY = environ.get('ACCESS_KEY')
ACCESS_SECRET = environ.get('ACCESS_SECRET')

def loadCategories(filename):
	categories = []
	with open(filename) as file: 
		reader = csv.reader(file)
		for i, row in enumerate(reader):
			for j, col in enumerate(row):
				#skip header row
				if i == 0:
					categories.append([])
				#skip blanks
				elif col != '':
					categories[j].append(col)
	return categories

def processText(text, categories):
	output = ""
	selections = []
	#initialize values to 0
	for i in range(len(categories)):
		selections.append(0)

	#add each character's integer value
	for i, char in enumerate(text):
		selections[i % len(categories)] += ord(char)

	#select an option in each category based on the total integer values
	for i, val in enumerate(selections):
		selections[i] = val % len(categories[i])
		output += " " + categories[i][selections[i]]
	return output

categories = loadCategories('data.csv')

class MyStreamListener(tweepy.StreamListener):

	def on_status(self, status):
		#print(status.text)
		response = processText(status.text, categories)
		#print(response)
		api.update_status(response, in_reply_to_status_id = status.id)
		#TODO: this does not correctly reply

	def on_error(self, status_code):
		if status_code == 420:
			#disconnects the stream
			return False


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=['@fabricreature'])

#myStream.filter(track=['python'], async=True)
#TODO: make this async so I can periodically wake up the heroku dyno (if necessary)
#test1