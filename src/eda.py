"""Exploratory Data Analysis (EDA) module"""

import pandas as pd
import os

def get_dataframe(filename):
	"""Get dataframe from a CSV file

	Args:
		filename (string): The path to the CSV file

	Raises:
		ValueError: The file is not a CSV
		FileNotFoundError: The file does not exist

	Returns:
		pd.DataFrame: The dataframe from the CSV file
	"""
	if not filename.endswith(".csv"):
		raise ValueError("File is not a CSV")
	if not os.path.exists(filename):
		raise FileNotFoundError("File not found")
	return pd.read_csv(filename)

def get_nans(df):
	"""Get a list of columns with NaN columns

	Args:
		df (pd.DataFrame): The dataframe to check

	Returns:
		list: A list of columns with NaN count respect to the dataframe total count
	"""
	nans_list = []
	for col in df.columns:
		nans_list.append(df[col].isna().sum() / len(df))
	return nans_list

