class CleanValues():

    def clean_name(self, val):
        if val == 'None' or val == '' or val == None:
            return False
        try:
            return str(val)
        except ValueError:
            return False

    def clean_code(self, val):
        if val == 'None' or val == '' or val == None:
            return False
        try:
            return str(val)
        except ValueError:
            return False

    def clean_buying(self, val):
        if val == 'None' or val == '' or val == None:
            return False
        try:
            return float(val)
        except ValueError:
            return False

    def clean_selling(self, val):
        if val == 'None' or val == '' or val == None:
            return False
        try:
            return float(val)
        except ValueError:
            return False

    def clean_it(self, data):
        output_data = data.copy()
        structure = {
            'name': 'clean_name',
            'code': 'clean_code',
            'buying' : 'clean_buying',
            'selling' : 'clean_selling'
        }

        for key, val in data.items():
            if key not in structure:
                # do not clean
                continue

            cleaned_val = getattr(self, structure[key])(val)
            if cleaned_val is False:
                output_data[key] = 'Error'
                continue

            output_data[key] = cleaned_val

        return output_data