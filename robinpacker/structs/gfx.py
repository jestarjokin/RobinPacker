#! /usr/bin/python
# Use, distribution, and modification of the RobinPacker binaries, source code,
# or documentation, is subject to the terms of the MIT license.
#
# Copyright (c) 2013 Laurence Dougal Myers
#
# http://opensource.org/licenses/MIT

import collections

GfxMetadata = collections.namedtuple('GfxMetadata', 'max_size, has_palette, width, height')

class GfxData(object):
    def __init__(self):
        self.data = None
        self.palette = None
        self.original_file_name = None
        self.metadata = None
