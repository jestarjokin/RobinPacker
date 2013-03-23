import array
from collections import OrderedDict
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
        wrapper_obj = OrderedDict()
        wrapper_obj['__json_type__'] = 'array'
        wrapper_obj['data'] = array_to_export
        mkdir(os.path.dirname(json_file_name))
        with file(json_file_name, 'w') as json_file:
           json.dump(wrapper_obj, json_file, cls=ArrayJsonEncoder, indent=1)
