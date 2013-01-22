#! /usr/bin/python

import struct

from robinpacker.structs.character import CharacterData
from robinpacker.structs.rules import RulesData

def unpack(rfile, format):
    result = struct.unpack(format, rfile.read(struct.calcsize(format)))
    return result[0] if len(result) == 1 else result

class RulesUnpacker(object):
    def unpack(self, fname):
        outData = RulesData()
        with file(fname, 'rb') as rfile:
            header = rfile.read(2)
            assert header == '\x00\x00'

            # Chunk 1
            format = '<H'
            numEntries = unpack(rfile, format)
            outData.chunk1 = rfile.read(numEntries)

            # Chunk 2 - character data
            numEntries = unpack(rfile, format)
            assert numEntries <= 40
            characters = []
            for i in xrange(numEntries):
                cData = CharacterData()
                format = '<4H2b8B'
                (posX, posY, posAltitude, frameArray, _rulesBuffer2_5, _rulesBuffer2_6, _rulesBuffer2_7,
                    spriteSize, direction, _rulesBuffer2_10, _rulesBuffer2_11, _rulesBuffer2_12,
                    _rulesBuffer2_13_posX, _rulesBuffer2_14_posY) = unpack(rfile, format)
                cData.posX = posX if posX == 0xFFFF else ((posX << 3) + 4)
                cData.posY = posY if posY == 0xFFFF else ((posY << 3) + 4)
                cData.posAltitude = posAltitude & 0xFF
                cData.frameArray = frameArray
                cData._rulesBuffer2_5 = _rulesBuffer2_5
                cData._rulesBuffer2_6 = _rulesBuffer2_6
                cData._rulesBuffer2_7 = _rulesBuffer2_7
                cData.spriteSize = spriteSize
                cData.direction = direction
                cData._rulesBuffer2_10 = _rulesBuffer2_10
                cData._rulesBuffer2_11 = _rulesBuffer2_11
                cData._rulesBuffer2_12 = _rulesBuffer2_12
                cData._rulesBuffer2_13_posX = _rulesBuffer2_13_posX
                cData._rulesBuffer2_14_posY = _rulesBuffer2_14_posY
                format = '32B'
                cData.variables = unpack(rfile, format)
                cData._rulesBuffer2_16 = unpack(rfile, format)
            outData.characters = characters

            # Chunk 3 & 4 - packed strings and associated indexes
            format = '<2H' # this might actually be signed, going by the ScummVM Robin code.
            numEntries, size = unpack(rfile, format)
            stringIndexes = unpack(rfile, '<' + str(numEntries) + 'H')
            stringData = rfile.read(size)
            # Assume all strings are terminated by \x00, and all strings are used.
            outData.strings = stringData.split('\x00')

            # Chunk 5 - scripts
            format = '<H'
            numEntries = unpack(rfile, format)
            scripts = rfile.read(numEntries * 2) # each entry is a uint16
            outData.scripts = scripts

            # Chunk 6 - menu scripts
            numEntries = unpack(rfile, format)
            menuScripts = rfile.read(numEntries * 2) # each entry is a uint16
            outData.menuScripts = menuScripts

            # Chunk 7 & 8 - game scripts and indexes
            numEntries = unpack(rfile, format)
            gameScriptIndexes = unpack(rfile, '<' + str(numEntries) + 'H')
            size = unpack(rfile, format)
            gameScriptData = rfile.read(size)
            outData.gameScriptIndexes = gameScriptIndexes
            outData.gameScriptData = gameScriptData

            # Chunk 9
            outData.rulesChunk9 = rfile.read(60)

            # Chunk 10 & 11
            numEntries = unpack(rfile, 'B')
            assert numEntries <= 20
            chunk10Indexes = []
            if numEntries:
                totalSize = 0
                for i in xrange(numEntries):
                    chunk10Indexes.append(totalSize)
                    totalSize += unpack(rfile, 'B')
                if totalSize:
                    outData.rulesChunk11 = rfile.read(totalSize)

            # Chunk 12



