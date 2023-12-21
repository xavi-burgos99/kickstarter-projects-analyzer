import re
from nltk import download
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer
from nltk.tokenize import word_tokenize

# Define the function to get the stemmer
def get_stemmer():
	download('stopwords')
	download('punkt')
	stemmer = LancasterStemmer()
	return stemmer

# Define the function to get the stopwords
def get_stopwords():
	stop_words = set(stopwords.words('english'))
	return stop_words

# Define the function to clean the text and get the keywords
def get_keywords(text, stemmer, stop_words):
	text = text.lower()	# Lower the text
	text = re.sub(r'[^\w\s]', '', text)	# Remove punctuation
	text = re.sub(r'\d+', '', text)	# Remove numbers
	text = word_tokenize(text)	# Tokenize the text
	text = [word for word in text if word not in stop_words]	# Remove stopwords
	text = [stemmer.stem(word) for word in text]	# Stem the words
	text = ' '.join(text)	# Join the words
	return text