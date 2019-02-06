import csv
import os

import tweepy

#twitter API keys
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')

print(ACCESS_SECRET)

def zip_keys(word, n=2):
    # Zip a tuple of the each set of <n> consecutive letters with the letter after that
    return zip(zip(*[word[i:] for i in range(n)]), word[n:])

class Fabricreature(object):
	def __init__(self, names_filename, descriptions_csvname):
		self.markov_tuples = {}
		self.name_starts = []
		self.descriptions = []
		self.load_names(names_filename)
		self.load_descriptions(descriptions_csvname)

	def make_creature(self, text):
		name = self.generate_name(text)
		description = self.generate_description(text)
		return name.capitalize() + ": " + description

	#generate descriptions
	def load_descriptions(self, filename):
		with open(filename) as file: 
			reader = csv.reader(file)
			for i, row in enumerate(reader):
				for j, col in enumerate(row):
					#skip header row
					if i == 0:
						self.descriptions.append([])
					#skip blanks
					elif col != '':
						self.descriptions[j].append(col)

	def generate_description(self, text):
		output = ""
		selections = []
		#initialize values to 0
		for i in range(len(self.descriptions)):
			selections.append(0)

		#add each character's integer value
		for i, char in enumerate(text):
			selections[i % len(self.descriptions)] += ord(char)

		#select an option in each category based on the total integer values
		for i, val in enumerate(selections):
			selections[i] = val % len(self.descriptions[i])
			output += " " + self.descriptions[i][selections[i]]
		return output

	def load_names(self, filename):
		with open(filename) as file:
			for name in file.read().splitlines():
				name = name.lower()
				for i, (key, letter) in enumerate(zip_keys(name)):
					self.markov_tuples.update( [(key, self.markov_tuples.get(key, []) + [letter])] )
					if i == 0:
						self.name_starts.append(key)

	def generate_name(self, text):
		#value between 1 and 12; total length will be between 3 and 14
		length = self.generate_length(text)
		print(length)

		selections = []
		#initialize values to 0
		for i in range(length):
			selections.append(0)

		#add each character's integer value
		for i, char in enumerate(text):
			selections[i % (length)] += ord(char)
		
		idx = selections[0] % len(self.name_starts)
		key = self.name_starts[idx]

		name = ''.join(key).lstrip() #name starts 2 characters long
		#so total length is length + 2

		for i in range(length):
			if not key in self.markov_tuples:
				break;
			idx = selections[i] % len(self.markov_tuples.get(key))
			character = self.markov_tuples.get(key)[idx]
			name += character
			key = key[1:] + (character,)

		return name

	def generate_length(self, text, minimum=1, maximum=12):
		#returns a value between 1 (inclusive) and 12 (exclusive)
		span = maximum - minimum
		arr = []
		for i in range( span ):
			arr.append(0)

		for i, char in enumerate(text):
			arr[i % (span)] += ord(char)

		max_idx = 0
		max_val = 0
		for i in range ( span ):
			if arr[i] > max_val:
				max_val = arr[i]
				max_idx = i
		return max_idx + minimum

fc = Fabricreature('names.txt', 'data.csv')
text = 'hank 5 feet gaunt four legged rusty scales bands plateau fungi talons frostproof valuable glands? uncommon reclusive small nests'
print(fc.make_creature(text))

class MyStreamListener(tweepy.StreamListener):

	def on_status(self, status):
		response = fc.make_creature(status.text)
		api.update_status(response, in_reply_to_status_id = status.id)
		#TODO: this does not correctly reply (just posts)

	def on_error(self, status_code):
		if status_code == 420:
			#disconnects the stream
			return False


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
#myStream.filter(track=['@fabricreature'])

#myStream.filter(track=['python'], async=True)
#TODO: make this async so I can periodically wake up the heroku dyno (if necessary)