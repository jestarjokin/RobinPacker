import array
import json

class ArrayJsonImporter(object):
    def import_file(self, json_file_name):
        with file(json_file_name, 'r') as json_file:
            wrapper_obj = json.load(json_file)
        list_data = wrapper_obj['data']
        array_data = array.array('B', list_data)
        return array_data
