import configparser
import pandas as pd
import xml.etree.ElementTree as ET
import threading
from clean_values import CleanValues

class Transform(CleanValues):
	
	RESULT_COLUMN_NAMES = [
		'date',
		'code',
		'unit',
		'name', 
		'buying',
		'selling'
	]

	result_df = pd.DataFrame(columns=RESULT_COLUMN_NAMES)

	def __init__(self):
		config = configparser.ConfigParser()
		config.read('etl.cfg')

		self.BASE_PATH_FOR_DOWNLOADING = config.get('path', 'BASE_PATH_FOR_DOWNLOADING')
		self.INFORMATIVE_FILE_NAME = config.get('files', 'INFORMATIVE_FILE_NAME')
		self.INDICATIVE_FILE_NAME = config.get('files', 'INDICATIVE_FILE_NAME')

	def parse_informative_object(self):
		target_path = f"../{self.BASE_PATH_FOR_DOWNLOADING}{self.INFORMATIVE_FILE_NAME}"
		tree = ET.parse(target_path)
		root = tree.getroot()
		
		for currency in root.findall("./Currency"):
			row_data = {}
			row_data['date'] = currency.attrib['Tarih']
			row_data['code'] = currency.attrib['CurrencyCode']
			row_data['unit'] = currency.find('Unit').text
			row_data['name'] = currency.find('CurrencyName').text
			row_data['buying'] = currency.find('ExchangeRate').text
			row_data['selling'] = currency.find('ExchangeRate').text

			row_data = self.clean_it(row_data)

			self.result_df = self.result_df.append(row_data, ignore_index=True)
			
	def parse_indicative_object(self):
		target_path = f"../{self.BASE_PATH_FOR_DOWNLOADING}{self.INDICATIVE_FILE_NAME}"
		tree = ET.parse(target_path)
		root = tree.getroot()
		
		for currency in root.findall("./Currency"):
			
			row_data = {}
			row_data['date'] = currency.attrib['Tarih']
			row_data['code'] = currency.attrib['CurrencyCode']
			row_data['unit'] = currency.find('Unit').text
			row_data['name'] = currency.find('CurrencyName').text
			row_data['buying'] = currency.find('BanknoteBuying').text
			row_data['selling'] = currency.find('BanknoteSelling').text

			row_data = self.clean_it(row_data)

			self.result_df = self.result_df.append(row_data, ignore_index=True)

	def run(self):
		# self.parse_informative_object()
		# self.parse_indicative_object()

		t1 = threading.Thread(target=self.parse_informative_object())
		t2 = threading.Thread(target=self.parse_indicative_object())

		t1.start()
		t2.start()

		t1.join()
		t2.join()

		return self.result_df