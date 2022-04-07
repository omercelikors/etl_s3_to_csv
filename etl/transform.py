import configparser
import pandas as pd
import xml.etree.ElementTree as ET
import threading
from clean_values import CleanValues
from model import RateModel
from dataclasses import asdict

class Transform(CleanValues):
	"""
		All data fields are required.
		All fields must be completely provided for data integrity.
	"""
	def __init__(self):
		config = configparser.ConfigParser()
		config.read('etl.cfg')

		self.BASE_PATH_FOR_DOWNLOADING = config.get('path', 'BASE_PATH_FOR_DOWNLOADING')
		self.INFORMATIVE_FILE_NAME = config.get('files', 'INFORMATIVE_FILE_NAME')
		self.INDICATIVE_FILE_NAME = config.get('files', 'INDICATIVE_FILE_NAME')

		self.result_df = pd.DataFrame()

	def parse_informative_object(self):
		target_path = f"../{self.BASE_PATH_FOR_DOWNLOADING}{self.INFORMATIVE_FILE_NAME}"
		tree = ET.parse(target_path)
		root = tree.getroot()

		
		informative_rates = []
		for currency in root.findall("./Currency"):
			# validating of keys module can be added
			try:
				rate_model = RateModel(
            		date = currency.attrib['Tarih'],
            		code = currency.attrib['CurrencyCode'],
            		unit = currency.find('Unit').text,
            		name = currency.find('CurrencyName').text,
            		buying = currency.find('ExchangeRate').text,
            		selling = currency.find('ExchangeRate').text,
        		)

				row_data = self.clean_it(asdict(rate_model))
				if 'error' in row_data.values():
					error_object = f"Error on {currency.attrib} object."
					print(error_object) # can be passed to log system
					continue

				informative_rates.append(row_data)
			except Exception as e: # if a element key does not exist
				error_object = f"Error on {currency.attrib} object."
				error_message = f"Desc: {e} - Object: {error_object}"
				print(error_message) # can be passed to log system
			finally:
				continue
		
		temp_df = pd.DataFrame(informative_rates)
		# Use concat() instead of append. For further details see Deprecated DataFrame.append and Series.append
		self.result_df = pd.concat([self.result_df,temp_df]) 
			
			
	def parse_indicative_object(self):
		target_path = f"../{self.BASE_PATH_FOR_DOWNLOADING}{self.INDICATIVE_FILE_NAME}"
		tree = ET.parse(target_path)
		root = tree.getroot()

		informative_rates = []
		for currency in root.findall("./Currency"):
			# validating of keys module can be added
			try:
				rate_model = RateModel(
            		date = currency.attrib['Tarih'],
            		code = currency.attrib['CurrencyCode'],
            		unit = currency.find('Unit').text,
            		name = currency.find('CurrencyName').text,
            		buying = currency.find('BanknoteBuying').text,
            		selling = currency.find('BanknoteSelling').text,
        		)

				row_data = self.clean_it(asdict(rate_model))
				if 'error' in row_data.values():
					error_object = f"Error on {currency.attrib} object."
					print(error_object) # can be passed to log system
					continue

				informative_rates.append(row_data)
			except Exception as e:# if a element key does not exist
				error_object = f"Error on {currency.attrib} object."
				error_message = f"Desc: {e} - Object: {error_object}"
				print(error_message) # can be passed to log system
			finally:
				continue

		temp_df = pd.DataFrame(informative_rates)
		# Use concat() instead of append. For further details see Deprecated DataFrame.append and Series.append
		self.result_df = pd.concat([self.result_df,temp_df])

	def run(self):
		# Two object are processed in multi threads.
		t1 = threading.Thread(target=self.parse_informative_object())
		t2 = threading.Thread(target=self.parse_indicative_object())

		t1.start()
		t2.start()

		t1.join()
		t2.join()

		self.result_df = self.result_df.sort_values(by="date", ignore_index=True)
		self.result_df.index += 1
		
		return self.result_df