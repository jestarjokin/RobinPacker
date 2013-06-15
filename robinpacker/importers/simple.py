#! /usr/bin/python
# Use, distribution, and modification of the RobinPacker binaries, source code,
# or documentation, is subject to the terms of the MIT license.
#
# Copyright (c) 2013 Laurence Dougal Myers
#
# http://opensource.org/licenses/MIT

import array
import json

class ArrayJsonImporter(object):
    def import_file(self, json_file_name):
        with file(json_file_name, 'r') as json_file:
            wrapper_obj = json.load(json_file)
        list_data = wrapper_obj['data']
        array_data = array.array('B', list_data)
        return array_data
