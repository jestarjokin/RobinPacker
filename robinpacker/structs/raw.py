#! /usr/bin/python

class RawData(object):
    def __init__(self, id, data):
        self.id = id
        self.data = data

    def __len__(self):
        return len(self.data)
