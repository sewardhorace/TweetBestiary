import csv

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
	return 'Hello, World!'



def loadData(filename):
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

# test = loadData('data.csv')

# print(len(test[1]))

def processText(text, categories):
	output = ""
	selections = []
	#initialize
	for i in range(len(categories)):
		selections.append(0)

	for i, char in enumerate(input):
		selections[i % len(categories)] += ord(char)

	for i, val in enumerate(selections):
		selections[i] = val % len(categories[i])
		output += " " + categories[i][selections[i]]
		#print(categories[i][selections[i]])
	return output

input = 'People are going to have consternation about what happens in the first year of STL City/County unification, but there’s just no question a unified government is better for everyone in the region 10, 20, 30 years down the road.'
categories = loadData('data.csv')
result = processText(input, categories)
print(len(result))
print(result)