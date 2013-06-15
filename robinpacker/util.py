#! /usr/bin/python
# Use, distribution, and modification of the RobinPacker binaries, source code,
# or documentation, is subject to the terms of the MIT license.
#
# Copyright (c) 2013 Laurence Dougal Myers
#
# http://opensource.org/licenses/MIT

import os
import struct

def pack(rfile, data, format):
    if type(data) == tuple or type(data) == list:
        result = struct.pack(format, *data)
    else:
        result = struct.pack(format, data)
    rfile.write(result)

def unpack(rfile, format):
    result = struct.unpack(format, rfile.read(struct.calcsize(format)))
    return result[0] if len(result) == 1 else result

def mkdir(dir_name):
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)

class RobinPackerException(Exception):
    pass

class RobinScriptError(Exception):
    pass

class RobinPackerJsonIdentified(Exception):
    def __init__(self, json_type_string, *args, **kwargs):
        super(RobinPackerJsonIdentified, self).__init__(*args, **kwargs)
        self.json_type_string = json_type_string
