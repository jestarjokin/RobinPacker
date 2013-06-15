#! /usr/bin/python
# Use, distribution, and modification of the RobinPacker binaries, source code,
# or documentation, is subject to the terms of the MIT license.
#
# Copyright (c) 2013 Laurence Dougal Myers
#
# http://opensource.org/licenses/MIT

class StringTable(object):
    def __init__(self, string_list_or_map):
        if type(string_list_or_map) in (list, tuple):
            self.string_lookup = {s : i for i, s in enumerate(string_list_or_map)}
            self.max_index = len(string_list_or_map) - 1
            self.index_lookup = string_list_or_map
        else:
            self.string_lookup = string_list_or_map
            self.max_index = max(string_list_or_map.values()) if len(string_list_or_map) else -1
            self.index_lookup = {i : s for s, i in string_list_or_map.items()}

    def __contains__(self, item):
        return item in self.string_lookup

    def __getitem__(self, item):
        if type(item) == int:
            return self.index_lookup[item]
        else:
            return self.string_lookup[item]

    def __len__(self):
        return self.max_index + 1 #hmmm, not quite right...

    def append(self, item):
        self.max_index += 1
        self.string_lookup[item] = self.max_index
        # this next bit is crap
        if type(self.index_lookup) == dict:
            self.index_lookup[self.max_index - 1] = item
        else:
            self.index_lookup.append(item)


class ParserContext(object):
    def __init__(self, string_list_or_table):
        if type(string_list_or_table) in (list, tuple):
            self.string_table = StringTable(string_list_or_table)
        else:
            self.string_table = string_list_or_table
