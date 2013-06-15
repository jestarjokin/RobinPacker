#! /usr/bin/python
# Use, distribution, and modification of the RobinPacker binaries, source code,
# or documentation, is subject to the terms of the MIT license.
#
# Copyright (c) 2013 Laurence Dougal Myers
#
# http://opensource.org/licenses/MIT

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
