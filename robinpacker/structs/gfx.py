#! /usr/bin/python
import collections

GfxMetadata = collections.namedtuple('GfxMetadata', 'max_size, has_palette, width, height')

class GfxData(object):
    def __init__(self):
        self.data = None
        self.palette = None
        self.original_file_name = None
        self.metadata = None
