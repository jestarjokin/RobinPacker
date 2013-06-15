#! /usr/bin/python
# Use, distribution, and modification of the RobinPacker binaries, source code,
# or documentation, is subject to the terms of the MIT license.
#
# Copyright (c) 2013 Laurence Dougal Myers
#
# http://opensource.org/licenses/MIT

class RawData(object):
    def __init__(self, id, data):
        self.id = id
        self.data = data

    def __len__(self):
        return len(self.data)
