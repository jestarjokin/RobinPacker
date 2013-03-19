import array
import os.path

class ArrayBinaryUnpacker(object):
    def __init__(self):
        pass

    def unpack(self, fname):
        data_size = os.path.getsize(fname)
        data = array.array('B')
        with file(fname, 'rb') as input_file:
            data.fromfile(input_file, data_size)
        return data
