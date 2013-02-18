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

class RobinScriptError(Exception):
    pass
