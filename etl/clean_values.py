import re
import datetime

class CleanValues:
	"""
		This class checks format and type of values.
		It tries to convert value to convenient type.
		if there is any problem about type or format, 
		it produces 'error' string instead of obtained value.
	"""

	def clean_date(self, val):
		if val == 'None' or val == '' or val == None: # this field is required
			return False

		# validate date format according to '12.12.2021'
		date_pattern = "^[0-9]{2}\\.[0-9]{2}\\.[0-9]{4}$"
		if not re.match(date_pattern, val):
			return False
			
		try:
			val = datetime.datetime.strptime(val, "%d.%m.%Y").date() # convert from string to date object
			return val
		except:
			return False

	def clean_code(self, val):
		if val == 'None' or val == '' or val == None: # this field is required
			return False
		try:
			return str(val)
		except ValueError:
			return False

	def clean_unit(self, val):
		if val == 'None' or val == '' or val == None: # this field is required
			return False
		try:
			return int(val)
		except ValueError:
			return False

	def clean_name(self, val):
		if val == 'None' or val == '' or val == None: # this field is required
			return False
		try:
			return str(val)
		except ValueError:
			return False

	def clean_buying(self, val):
		if val == 'None' or val == '' or val == None: # this field is required
			return False
		try:
			return float(val)
		except ValueError:
			return False

	def clean_selling(self, val):
		if val == 'None' or val == '' or val == None: # this field is required
			return False
		try:
			return float(val)
		except ValueError:
			return False

	def clean_it(self, data):
		output_data = data.copy()
		structure = {
			'date' : 'clean_date',
			'code' : 'clean_code',
			'unit' : 'clean_unit',
			'name' : 'clean_name',
			'buying' : 'clean_buying',
			'selling' : 'clean_selling'
		}

		for key, val in data.items():
			if key not in structure:
				# do not clean
				continue

			cleaned_val = getattr(self, structure[key])(val)
			if cleaned_val is False:
				output_data[key] = 'error'
				continue

			output_data[key] = cleaned_val

		return output_data