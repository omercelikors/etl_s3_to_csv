from extract import Extract
from transform import Transform
from load import Load

class Main():

    def extract_data(self):
        extract = Extract()
        return extract.run()

    def transform_data(self, file_objects):
        transform = Transform(file_objects)
        return transform.run()

    def load_data(self):
        pass
    
    def run(self):
        file_objects = self.extract_data()
        result_data = self.transform_data(file_objects)
        # result = self.load_data(result_data)
        # print(file_objects)

main = Main()
main.run()