from pandas import DataFrame
import pandas as pd


class Df:
	def __init__(self, df: DataFrame):
		self.df = df
		self.df['Дата'] = pd.to_datetime(self.df['Дата'], errors='coerce')
		# return df

	def date_min(self):
		return self.df['Дата'].min()

	def date_max(self):
		return self.df['Дата'].max()

	def data(self):
		return self.df



if __name__ == '__main__':
	df = Df(pd.read_excel('РФМ анализ тест Гермес.xlsx'))

	print(df.data())