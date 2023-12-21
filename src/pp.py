import re

"""Preprocessing module"""

import eda

def remove_nans(df, threshold=0.5):
	"""Remove columns with NaN count respect to the dataframe total count greater than a threshold

	Args:
		df (pd.DataFrame): The dataframe to check
		threshold (float, optional): The threshold to remove the columns. Defaults to 0.5.

	Returns:
		pd.DataFrame: The dataframe without the columns with NaN count respect to the dataframe total count greater than a threshold
	"""
	nans_list = eda.get_df_nans(df)
	return df.drop(df.columns[nans_list > threshold], axis=1)

def remove_duplicates(df):
	"""Remove duplicated rows from a dataframe

	Args:
		df (pd.DataFrame): The dataframe to check

	Returns:
		pd.DataFrame: The dataframe without duplicated rows
	"""
	return df.drop_duplicates()

def to_keywords(text):
	"""Convert a text to a list of keywords

	Args:
		text (str): The text to convert

	Returns:
		list: The list of keywords
	"""
	text = text.lower()
	text = re.sub(r'[^a-z0-9\s]', '', text)
	text = re.sub(r'\s+', ' ', text).strip()
	words = [word for word in text.split(' ') if len(word) > 3]
	text = ', '.join(words)
	return text
