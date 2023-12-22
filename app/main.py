import eel;
import predict as pr

# Read the JSON files
currencies, categories, main_categories, countries, keywords, backers_ranges, days_ranges, price_ranges = pr.read_json_files()

@eel.expose
def get_countries():
	return countries

@eel.expose
def get_categories():
	return main_categories

@eel.expose
def get_subcategories():
	return categories

@eel.expose
def get_currencies():
	return currencies

@eel.expose
def predict(name, country, days, main_category, category, goal, currency, backers, launched):
	return pr.predict(name, main_category, category, currency, country, launched, days, goal, backers)

eel.init('www')
eel.start('templates/index.html', size=(1100, 800), port=8800, jinja_templates='templates')