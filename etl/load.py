import configparser

class Load():
	
	def __init__(self, result_df):
		config = configparser.ConfigParser()
		config.read('etl.cfg')

		self.BASE_PATH_FOR_RESULT_FILE = config.get('path', 'BASE_PATH_FOR_RESULT_FILE')
		self.RESULT_FILE_NAME = config.get('path', 'RESULT_FILE_NAME')
		
		self.result_df = result_df

	def df_to_csv(self):
		target_path = f"../{self.BASE_PATH_FOR_RESULT_FILE}{self.RESULT_FILE_NAME}"
		self.result_df.to_csv(target_path, sep=',', 
							  encoding='utf-8',
							  index_label='no',
							  na_rep='Empty')

		return True

	def run(self):

		return self.df_to_csv()