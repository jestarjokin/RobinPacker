import array
import json

class ArrayJsonImport(object):
    def import_file(self, json_file_name):
        with file(json_file_name, 'r') as json_file:
            list_data = json.load(json_file)
        array_data = array.array('B', list_data)
        return array_data
