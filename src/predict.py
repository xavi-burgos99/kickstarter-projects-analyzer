# Import libraries
import os
import json
import pickle
import pandas as pd
import pp


def read_json_files():

	# Check if the "json" directory exists
	if not os.path.exists('../data/json'):
		raise Exception("The \"json\" directory doesn't exist.")

	# Check if the "currencies.json" file exists
	if not os.path.exists('../data/json/currencies.json'):
		raise Exception("The \"currencies.json\" file doesn't exist.")

	# Check if the "categories.json" file exists
	if not os.path.exists('../data/json/categories.json'):
		raise Exception("The \"categories.json\" file doesn't exist.")

	# Check if the "main_categories.json" file exists
	if not os.path.exists('../data/json/main_categories.json'):
		raise Exception("The \"main_categories.json\" file doesn't exist.")

	# Check if the "countries.json" file exists
	if not os.path.exists('../data/json/countries.json'):
		raise Exception("The \"countries.json\" file doesn't exist.")

	# Check if the "keywords.json" file exists
	if not os.path.exists('../data/json/keywords.json'):
		raise Exception("The \"keywords.json\" file doesn't exist.")

	# Check if the "backers_ranges.json" file exists
	if not os.path.exists('../data/json/backers_ranges.json'):
		raise Exception("The \"backers_ranges.json\" file doesn't exist.")

	# Check if the "days_ranges.json" file exists
	if not os.path.exists('../data/json/days_ranges.json'):
		raise Exception("The \"days_ranges.json\" file doesn't exist.")

	# Check if the "price_ranges.json" file exists
	if not os.path.exists('../data/json/price_ranges.json'):
		raise Exception("The \"price_ranges.json\" file doesn't exist.")

	# Read the "currencies.json" file
	with open('../data/json/currencies.json', 'r') as file:
		currencies = json.load(file)
  
	# Read the "categories.json" file
	with open('../data/json/categories.json', 'r') as file:
		categories = json.load(file)
  
	# Read the "main_categories.json" file
	with open('../data/json/main_categories.json', 'r') as file:
		main_categories = json.load(file)
  
	# Read the "countries.json" file
	with open('../data/json/countries.json', 'r') as file:
		countries = json.load(file)
  
  # Read the "keywords.json" file
	with open('../data/json/keywords.json', 'r') as file:
		keywords = json.load(file)
  
  # Read the "backers_ranges.json" file
	with open('../data/json/backers_ranges.json', 'r') as file:
		backers_ranges = json.load(file)
  
  # Read the "days_ranges.json" file
	with open('../data/json/days_ranges.json', 'r') as file:
		days_ranges = json.load(file)
  
  # Read the "price_ranges.json" file
	with open('../data/json/price_ranges.json', 'r') as file:
		price_ranges = json.load(file)
  
	# Return the lists
	return currencies, categories, main_categories, countries, keywords, backers_ranges, days_ranges, price_ranges


def load_model():
  
	# Check if the "models" directory exists
	if not os.path.exists('../data/models'):
		raise Exception("The \"models\" directory doesn't exist.")

	# Check if the "random_forest.pkl" file exists
	if not os.path.exists('../data/models/random_forest.pkl'):
		raise Exception("The \"random_forest.pkl\" file doesn't exist.")

	# Load the model
	with open('../data/models/random_forest.pkl', 'rb') as file:
		model = pickle.load(file)
  
	# Return the model
	return model


def predict(name, main_category, category, currency, country, launched, days, goal, backers):
  
	# Read the "currencies.json", "categories.json", "main_categories.json", "countries.json" and "keywords.json" files
	currencies, categories, main_categories, countries, keywords, backers_ranges, days_ranges, price_ranges = read_json_files()
 
	# Load the model
	model = load_model()
 
	# Check if the main category is valid
	if main_category not in main_categories:
		raise Exception("The main category is not valid.")

	# Check if the category is valid
	if category not in categories:
		raise Exception("The category is not valid.")

	# Check if the currency is valid
	if currency not in currencies:
		raise Exception("The currency is not valid.")

	# Check if the country is valid
	if country not in countries:
		raise Exception("The country is not valid.")

	# Check if the launched date is valid
	if launched < 1 or launched > 12:
		raise Exception("The launched date is not valid.")

	# Convert the "main_category" column to an integer column using the "main_categories" list
	main_category = main_categories.index(main_category)
 
	# Convert the "category" column to an integer column using the "categories" list
	category = categories.index(category)
 
	# Convert the "currency" column to an integer column using the "currencies" list
	currency = currencies.index(currency)
 
	# Convert the "country" column to an integer column using the "countries" list
	country = countries.index(country)
 
	# Convert the "days" column to an integer column using the "days_ranges" list
	days = len(days_ranges)
	for i in range(len(days_ranges)):
		if days <= days_ranges[i]:
			days = i
			break
 
	# Convert the "goal" column to an integer column using the "price_ranges" list
	goal = len(price_ranges)
	for i in range(len(price_ranges)):
		if goal <= price_ranges[i]:
			goal = i
			break
 
	# Convert the "backers" column to an integer column using the "backers_ranges" list
	backers = len(backers_ranges)
	for i in range(len(backers_ranges)):
		if backers <= backers_ranges[i]:
			backers = i
			break
 
	# Extract the keywords from the name
	stemmer = pp.get_stemmer()
	stop_words = pp.get_stopwords()
	name_keywords = pp.get_keywords(name, stemmer, stop_words)
	name_keywords = ' '.split(name_keywords)
 
	# Loop through the keywords
	keywords_mapping = {}
	for keyword in keywords:
		if keyword in name_keywords:
			keywords_mapping[keyword] = 1
		else:
			keywords_mapping[keyword] = 0
   
	# Create the dataframe
	data = pd.DataFrame({
		'category': [category],
		'main_category': [main_category],
		'currency': [currency],
		'launched': [launched],
		'backers': [backers],
		'country': [country],
		'days': [days],
		'cancelled': [0],
		'goal': [goal]
	})
 
	# Add the keywords to the dataframe
	new_keywords = {}
	for keyword in keywords:
		new_keywords[keyword] = keywords_mapping[keyword]
	new_keywords = pd.DataFrame(new_keywords, index = [0])
 
	# Concatenate the dataframes
	data = pd.concat([data, new_keywords], axis = 1)
  
	# Predict the result
	result = model.predict(data)[0]
 
	# Convert the result to "pledged" price (inverse as the "goal" price)
	if result >= len(price_ranges):
		pledged = price_ranges[-1]
	else:
		pledged = price_ranges[result]
 
	# Convert the "pledged" price into a message
	if result == 0:
		message = "This project will not be funded."
	elif result == len(price_ranges):
		message = "This project will be funded more than {}.".format(pledged)
	else:
		pledged_min = price_ranges[result - 1] + 1
		message = "This project will be funded between {} and {}.".format(pledged_min, pledged)
	
	# Return the pledged price and the message
	return pledged, message
