#! /usr/bin/python
# Use, distribution, and modification of the RobinPacker binaries, source code,
# or documentation, is subject to the terms of the MIT license.
#
# Copyright (c) 2013 Laurence Dougal Myers
#
# http://opensource.org/licenses/MIT

import os.path

from robinpacker.util import mkdir

class ArrayBinaryPacker(object):
    def pack(self, array_to_pack, fname):
        mkdir(os.path.dirname(fname))
        with file(fname, 'wb') as output_file:
            array_to_pack.tofile(output_file)
