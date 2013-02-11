#! /usr/bin/python

import struct

from robinpacker.structs.character import CharacterData
from robinpacker.structs.point import PointData
from robinpacker.structs.rules import RulesData
from robinpacker.structs.rect import RectData
from robinpacker.structs.raw import RawData
from robinpacker.structs.script import ScriptData

def unpack(rfile, format):
    result = struct.unpack(format, rfile.read(struct.calcsize(format)))
    return result[0] if len(result) == 1 else result

packedStringLookup = ['I am ', 'You are ', 'you are ', 'hou art ', 'in the ', 'is the ', 'is a ', 'in a ', 'To the ',
                      'to the ', 'by ', 'going ', 'here ', 'The', 'the', 'and ', 'some ', 'build', 'not ', 'way', 'I ',
                      'a ', 'an ', 'from ', 'of ', 'him', 'her', 'by ', 'his ', 'ing ', 'tion', 'have ', 'you', "I've ",
                      "can't ", 'up ', 'to ', 'he ', 'she ', 'down ', 'what', 'What', 'with', 'are ', 'and', 'ent',
                      'ian', 'ome', 'ed ', 'me', 'my', 'ai', 'it', 'is', 'of', 'oo', 'ea', 'er', 'es', 'th', 'we',
                      'ou', 'ow', 'or', 'gh', 'go', 'er', 'st', 'ee', 'th', 'sh', 'ch', 'ct', 'on', 'ly', 'ng', 'nd',
                      'nt', 'ty', 'll', 'le', 'de', 'as', 'ie', 'in', 'ss', "'s ", "'t ", 're', 'gg', 'tt', 'pp',
                      'nn', 'ay', 'ar', 'wh']

class RulesBinaryUnpacker(object):
    def unpack(self, fname):
        outData = RulesData()
        with file(fname, 'rb') as rfile:
            header = rfile.read(2)
            assert header == '\x00\x00'

            # Chunk 1
            format = '<H'
            numEntries = unpack(rfile, format)
            format = '<2B'
            chunk1PointArray = []
            for i in xrange(numEntries / 2):
                y, x = unpack(rfile, format)
                chunk1PointArray.append(PointData(x, y))
            outData.chunk1PointArray = chunk1PointArray

            # Chunk 2 - character data
            format = '<H'
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
                characters.append(cData)
            outData.characters = characters

            # Chunk 3 & 4 - packed strings and associated indexes
            format = '<2H' # this might actually be signed, going by the ScummVM Robin code.
            numEntries, size = unpack(rfile, format)
            stringIndexes = unpack(rfile, '<' + str(numEntries) + 'H') # not used, because we cheat below
            stringData = rfile.read(size)
            # Assume all strings are terminated by \x00, and all strings are used/listed in the index table.
            strings = stringData.split('\x00')
            del strings[-1]
            def unpackString(inChar):
                global packedStringLookup
                val = ord(inChar)
                if val < 0x80:
                    return inChar
                return packedStringLookup[0xFF - val]
            for i, packedString in enumerate(strings):
                strings[i] = ''.join(map(unpackString, packedString))
            outData.strings = strings

            # Chunk 5 - scripts
            format = '<H'
            numEntries = unpack(rfile, format)
            scripts = rfile.read(numEntries * 2) # each entry is a uint16
            outData.scripts = ScriptData('scripts', scripts)

            # Chunk 6 - menu scripts
            format = '<H'
            numEntries = unpack(rfile, format)
            menuScripts = rfile.read(numEntries * 2) # each entry is a uint16
            outData.menuScripts = ScriptData('menuScripts', menuScripts)

            # Chunk 7 & 8 - game scripts and indexes
            format = '<H'
            numEntries = unpack(rfile, format)
            gameScriptIndexes = unpack(rfile, '<' + str(numEntries) + 'H')
            size = unpack(rfile, format)
            # Here's an unnecessarily clever way to calculate the sizes of each script block.
            script_sizes = map(lambda x, y: (y if y is not None else size) - x, gameScriptIndexes, gameScriptIndexes[1:])
            gameScripts = []
            for i, script_size in enumerate(script_sizes):
                script_data = ScriptData('gameScript_{}'.format(i + 1), rfile.read(script_size))
                gameScripts.append(script_data)
            outData.gameScripts = gameScripts

            # Chunk 9
            outData.rulesChunk9 = RawData('rulesChunk9', rfile.read(60))

            # Chunk 10 & 11
            numEntries = unpack(rfile, 'B')
            assert numEntries <= 20
            chunk10Sizes = []
            if numEntries:
                totalSize = 0
                for i in xrange(numEntries):
                    val = unpack(rfile, 'B')
                    chunk10Sizes.append(val)
                    totalSize += val
                if totalSize:
                    #outData.chunk10Indexes = chunk10Indexes
                    rulesChunk11 = []
                    for i, size in enumerate(chunk10Sizes):
                        data = RawData('rulesChunk11_{}'.format(i + 1), rfile.read(size))
                        rulesChunk11.append(data)
                    outData.rulesChunk11 = rulesChunk11

            # Chunk 12 - rectangles
            format = '<H'
            numEntries = unpack(rfile, format)
            rectangles = []
            format = '8B'
            for i in xrange(numEntries):
                rectData = RectData(
                    *(unpack(rfile, format))
                )
                rectangles.append(rectData)
            outData.rectangles = rectangles

            # Chunk 13 - interface hotspots
            format = '20B' # I think the first entry is actually numEntries, since it's 19
            outData.interfaceTwoStepAction = unpack(rfile, format) # might be a byte array
            format = '<20h'
            outData.interfaceHotspotsX = unpack(rfile, format)
            outData.interfaceHotspotsY = unpack(rfile, format)
            format = '20B'
            outData.keyboardMapping = unpack(rfile, format)
        return outData


