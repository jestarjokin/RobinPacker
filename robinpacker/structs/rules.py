#! /usr/bin/python
# Use, distribution, and modification of the RobinPacker binaries, source code,
# or documentation, is subject to the terms of the MIT license.
#
# Copyright (c) 2013 Laurence Dougal Myers
#
# http://opensource.org/licenses/MIT

class RulesData(object):
    def __init__(self):
        self.chunk1PointArray = None
        self.characters = None
        self.strings = None
        self.scripts = None
        self.menuScripts = None
        #self.gameScriptIndexes = None
        self.gameScripts = None
        self.rulesChunk9 = None
        self.chunk10Indexes = None
        self.rulesChunk11 = None
        self.rectangles = None
        self.interfaceTwoStepAction = None
        self.interfaceHotspotsX = None
        self.interfaceHotspotsY = None
        self.keyboardMapping = None

