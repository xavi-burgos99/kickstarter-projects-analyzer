"""Exploratory Data Analysis (EDA) module"""

import pandas as pd
import os

def get_dataframe(csv_path):
	"""Get dataframe from a CSV file

	Args:
		csv_path (string): The path to the CSV file

	Raises:
		ValueError: The file is not a CSV
		FileNotFoundError: The file does not exist

	Returns:
		pd.DataFrame: The dataframe from the CSV file
	"""
	if not csv_path.endswith(".csv"):
		raise ValueError("File is not a CSV")
	path = os.path.join(os.getcwd(), csv_path)
	if not os.path.exists(path):
		raise FileNotFoundError("File does not exist")
	return pd.read_csv(path, encoding="cp1252")

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

def print_nans(df, column, rows=5):
	"""Print the NaN rows of a column

	Args:
		df (pd.DataFrame): The dataframe to check
		column (string): The column to check
		rows (int, optional): The number of rows to print. Defaults to 5.
	"""
	print(df[df[column].isna()].head(rows))
 
def print_non_nans(df, column, rows=5):
	"""Print the non-NaN rows of a column

	Args:
		df (pd.DataFrame): The dataframe to check
		column (string): The column to check
		rows (int, optional): The number of rows to print. Defaults to 5.
	"""
	print(df[df[column].notna()].head(rows))