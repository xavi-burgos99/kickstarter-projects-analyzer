"""Preprocessing module"""

import src.eda as eda

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

def print_nans(df, column, rows=5):
	"""Print the NaN rows of a column

	Args:
		df (pd.DataFrame): The dataframe to check
		column (string): The column to check
		rows (int, optional): The number of rows to print. Defaults to 5.
	"""
	print(df[df[column].isna()].head(rows))

def remove_duplicates(df):
	"""Remove duplicated rows from a dataframe

	Args:
		df (pd.DataFrame): The dataframe to check

	Returns:
		pd.DataFrame: The dataframe without duplicated rows
	"""
	return df.drop_duplicates()

