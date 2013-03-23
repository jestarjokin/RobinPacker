import os.path

from robinpacker.util import mkdir

class ArrayBinaryPacker(object):
    def pack(self, array_to_pack, fname):
        mkdir(os.path.dirname(fname))
        with file(fname, 'wb') as output_file:
            array_to_pack.tofile(output_file)
