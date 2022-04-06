from extract import Extract
from transform import Transform
from load import Load
import logging

class Main():

    def extract_data(self):
        extract = Extract()
        return extract.run()

    def transform_data(self):
        transform = Transform()
        return transform.run()

    def load_data(self, result_df):
        load = Load(result_df)
        return load.run()
    
    def run(self):
        if self.extract_data():
            result_df = self.transform_data()
            process_result = self.load_data(result_df)

            return process_result
        else:

            return False

if __name__ == "__main__":
    main = Main()
    main.run()