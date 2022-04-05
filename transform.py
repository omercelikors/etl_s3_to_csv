import configparser

class Transform():
	
	RESULT_COLUMN_NAMES = [
		'date',
		'currency_code', 
		'currency_name', 
		'bank_note_buying',
		'bank_note_selling'
	]

	def __init__(self, file_objects):
		config = configparser.ConfigParser()
		config.read('config.cfg')

		self.INFORMATIVE_FILE_NAME = config.get('files', 'INFORMATIVE_FILE_NAME')
		self.INDICATIVE_FILE_NAME = config.get('files', 'INDICATIVE_FILE_NAME')

		for key, val in file_objects.items():
			if key == self.INFORMATIVE_FILE_NAME:
				self.INFORMATIVE_FILE_OBJECT = val
			elif key == self.INDICATIVE_FILE_NAME:
				self.INDICATIVE_FILE_OBJECT = val

		print(self.INFORMATIVE_FILE_OBJECT)
		print(self.INDICATIVE_FILE_OBJECT)

	
	def run(self):
		pass