# Import libraries
import os
import time
import re
import json
import pickle
import pandas as pd
import eda
import pp
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
from nltk import download
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer
from nltk.tokenize import word_tokenize

# Set up the dataset
dataset = {
	'path': '../data/csv/ks-projects-201801.csv',
	'encoding': 'ISO-8859-1'
}

# Get the dataframe
print("Reading the dataset and generating the dataframe...")
df = eda.get_dataframe(dataset['path'], encoding = dataset['encoding'])

# Create a copy of the dataframe
print("Starting the preprocessing...")
new_df = df.copy()

# Remove rows with NaN values in the "name" and "usd pledged" columns
new_df = new_df.dropna(subset = ['name'])
new_df = new_df.dropna(subset = ['usd pledged'])

# Remove the "ID" column
new_df = new_df.drop(['ID'], axis = 1)

# Get current currencies
currencies = new_df['currency'].value_counts()
currencies = currencies.index.values
currencies = sorted(currencies)

# Create "json" and "models" directories if they don't exist
if not os.path.exists('../data/json'):
	os.makedirs('../data/json')
if not os.path.exists('../data/models'):
	os.makedirs('../data/models')

# Save the "currencies" list into a "data/json/currencies.json" file
print("Saving \"currencies.json\" file...")
with open('../data/json/currencies.json', 'w') as file:
	json.dump(currencies, file)

# Convert the "currency" column to an integer column using the "currencies" list
new_df['currency'] = new_df.apply(lambda x: currencies.index(x['currency']), axis = 1)

# Remove the "goal", "pledged" and "usd pledged" columns
new_df = new_df.drop(['goal', 'pledged', 'usd pledged'], axis = 1)

# Get current categories
categories = new_df['category'].value_counts()
categories = categories.index.values
categories = sorted(categories)

# Save the "categories" list into a "data/json/categories.json" file
print("Saving \"categories.json\" file...")
with open('../data/json/categories.json', 'w') as file:
	json.dump(categories, file)

# Convert the "category" column to an integer column using the "categories" list
new_df['category'] = new_df.apply(lambda x: categories.index(x['category']), axis = 1)

# Get current main categories
main_categories = new_df['main_category'].value_counts()
main_categories = main_categories.index.values
main_categories = sorted(main_categories)

# Save the "main_categories" list into a "data/json/main_categories.json" file
print("Saving \"main_categories.json\" file...")
with open('../data/json/main_categories.json', 'w') as file:
	json.dump(main_categories, file)

# Convert the "main_category" column to an integer column using the "main_categories" list
new_df['main_category'] = new_df.apply(lambda x: main_categories.index(x['main_category']), axis = 1)

# Get current countries
countries = new_df['country'].value_counts()
countries = countries.index.values
countries = sorted(countries)

# Save the "countries" list into a "data/json/countries.json" file
print("Saving \"countries.json\" file...")
with open('../data/json/countries.json', 'w') as file:
	json.dump(countries, file)

# Convert the "country" column to an integer column using the "countries" list
new_df['country'] = new_df.apply(lambda x: countries.index(x['country']), axis = 1)

# Get the "days" column from the "deadline" and "launched" columns
new_df['days'] = (pd.to_datetime(new_df['deadline']) - pd.to_datetime(new_df['launched'])).dt.days

# Set days ranges to get more information
days_ranges = [0, 1, 2, 3, 5, 7, 10, 14, 21, 30, 45]

# Save the "days_ranges" list into a "data/json/days_ranges.json" file
print("Saving \"days_ranges.json\" file...")
with open('../data/json/days_ranges.json', 'w') as file:
	json.dump(days_ranges, file)
 
# Define the function to get the days range
def get_days_range(days):
	for i in range(len(days_ranges)):
		if days <= days_ranges[i]:
			return i
	return len(days_ranges)

# Convert the "days" column to an integer column using the "days_ranges" list
new_df['days'] = new_df.apply(lambda x: get_days_range(x['days']), axis = 1)

# Get the launched month from the "launched" column
new_df['launched'] = pd.to_datetime(new_df['launched']).dt.month

# Remove the "launched" and "deadline" columns
new_df = new_df.drop(columns = ['deadline'])

# Get the "cancelled" column from the "state" column
new_df['cancelled'] = new_df.apply(lambda x: 1 if x['state'] == 'canceled' else 0, axis = 1)

# Get the "success" column from the "state" column
new_df['successful'] = new_df.apply(lambda x: 1 if x['state'] == 'successful' else 0, axis = 1)

# Remove the "state" column
new_df = new_df.drop(columns = ['state'])

# Set price ranges to get more information
price_ranges = [0, 100, 500, 1000, 5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000, 5000000, 10000000]

# Define the function to get the price range
def get_price_range(x):
	for i in range(len(price_ranges)):
		if x <= price_ranges[i]:
			return i
	return len(price_ranges)

# Get the "pledged" column from the "usd_pledged_real" column
new_df['pledged'] = new_df.apply(lambda x: get_price_range(x['usd_pledged_real']), axis = 1)

# Get the "goal" column from the "usd_goal_real" column
new_df['goal'] = new_df.apply(lambda x: get_price_range(x['usd_goal_real']), axis = 1)

# Remove the "usd_pledged_real" and "usd_goal_real" columns
new_df = new_df.drop(columns = ['usd_pledged_real', 'usd_goal_real'])

# Set backers ranges to get more information
backers_ranges = [0, 1, 2, 3, 5, 7, 10, 14, 21, 30, 45, 60, 90, 120, 150, 200, 300, 500, 1000, 5000, 10000]

# Define the function to get the backers range
def get_backers_range(x):
	for i in range(len(backers_ranges)):
		if x <= backers_ranges[i]:
			return i
	return len(backers_ranges)

# Get the "backers" column from the "backers" column
new_df['backers'] = new_df.apply(lambda x: get_backers_range(x['backers']), axis = 1)

# Download stopwords and punkt
download('stopwords')
download('punkt')

# Initialize the LancasterStemmer
stemmer = LancasterStemmer()

# Initialize the stopwords
stop_words = set(stopwords.words('english'))

# Define the function to clean the text
def get_keywords(text):
	text = text.lower()	# Lower the text
	text = re.sub(r'[^\w\s]', '', text)	# Remove punctuation
	text = re.sub(r'\d+', '', text)	# Remove numbers
	text = word_tokenize(text)	# Tokenize the text
	text = [word for word in text if word not in stop_words]	# Remove stopwords
	text = [stemmer.stem(word) for word in text]	# Stem the words
	text = ' '.join(text)	# Join the words
	return text

# Apply the function to the "info" column to get the "keywords" column
timestart = time.time()
print("Getting the keywords...")
new_df['keywords'] = new_df['name'].apply(get_keywords)
timeend = time.time()
timeres = round(timeend - timestart, 2)
print("Keywords got in {} seconds".format(timeres))

# Remove the "name" column
new_df = new_df.drop(columns = ['name'])

# Create the bag of words
timestart = time.time()
print("Creating the bag of words...")
vectorizer = CountVectorizer(max_features = 1000)
bag_of_words = vectorizer.fit_transform(new_df['keywords'])

# Convert the bag of words into a DataFrame
bow_df = pd.DataFrame(bag_of_words.toarray(), columns=vectorizer.get_feature_names_out())
timeend = time.time()
timeres = round(timeend - timestart, 2)
print("Bag of words created in {} seconds".format(timeres))

# Remove the "keywords" column
new_df = new_df.drop(columns = ['keywords'])

# Concatenate the two dataframes
final_df = pd.concat([new_df.reset_index(drop=True), bow_df.reset_index(drop=True)], axis=1)

# Split the dataframe into train and test sets
target = 'pledged'
X_train, X_test, y_train, y_test = train_test_split(
  final_df.drop(target, axis=1),
  final_df[target],
  test_size=0.2,
  random_state=42
)

# Initialize the random forest classifier
rf = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
timestart = time.time()
print("Fitting the model...")
rf.fit(X_train, y_train)
timeend = time.time()
timeres = round(timeend - timestart, 2)
print("Model fitted in {} seconds".format(timeres))

# Realize the predictions on the test set
timestart = time.time()
print("Predicting the test set...")
y_pred = rf.predict(X_test)
timeend = time.time()
timeres = round(timeend - timestart, 2)
print("Test set predicted in {} seconds".format(timeres))

# Save the model into a "data/models/random_forest.pkl" file
print("Saving \"random_forest.pkl\" file...")
with open('../data/models/random_forest.pkl', 'wb') as file:
	pickle.dump(rf, file)
 
# Finish model training
print("\n\nMODEL TRAINED SUCCESSFULLY\n")

# Print the accuracy score
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy: {}".format(accuracy))

# Print the F1 score
f1 = f1_score(y_test, y_pred, average='weighted')
print("F1: {}".format(f1))
