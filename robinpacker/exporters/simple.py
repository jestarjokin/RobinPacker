import array
import json
import os.path

from robinpacker.util import mkdir

class ArrayJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, array.array):
            return obj.tolist()
        return super(ArrayJsonEncoder, self).default(obj)

class ArrayJsonExporter(object):
    def export(self, array_to_export, json_file_name):
        mkdir(os.path.dirname(json_file_name))
        with file(json_file_name, 'w') as json_file:
           json.dump(array_to_export, json_file, cls=ArrayJsonEncoder, indent=1)
