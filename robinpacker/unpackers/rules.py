#! /usr/bin/python

import struct

from structs.character import CharacterData
from structs.rules import RulesData
from structs.rect import RectData
from structs.point import PointData

def unpack(rfile, format):
    result = struct.unpack(format, rfile.read(struct.calcsize(format)))
    return result[0] if len(result) == 1 else result

class RulesBinaryUnpacker(object):
    def unpack(self, fname):
        outData = RulesData()
        with file(fname, 'rb') as rfile:
            header = rfile.read(2)
            assert header == '\x00\x00'

            # Chunk 1
            format = '<2H'
            numEntries = unpack(rfile, format)
            chunk1PointArray = []
            for i in xrange(numEntries):
                y, x = rfile.read(numEntries)
                chunk1PointArray.append(PointData(x, y))
            outData.chunk1PointArray = chunk1PointArray

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
            stringIndexes = unpack(rfile, '<' + str(numEntries) + 'H') # not used, because we cheat below
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
                    outData.chunk10Indexes = chunk10Indexes
                    outData.rulesChunk11 = rfile.read(totalSize)

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
            outData.interfaceTwoStepAction = rfile.read(20) # might be a byte array
            format = '<20h'
            outData.interfaceHotspotsX = unpack(rfile, format)
            outData.interfaceHotspotsY = unpack(rfile, format)
            format = '20B'
            outData.keyboardMapping = unpack(rfile, format)

            # TODO: Fix these
#            KEYCODE_SPACE = 'KEYCODE_SPACE'
#            KEYCODE_RETURN = 'KEYCODE_RETURN'
#            KEYCODE_INVALID = 'KEYCODE_INVALID'
#            for i in xrange(20):
#                currByte = unpack(rfile, 'B')
#                if currByte == 0x20:
#                    #keyboardMapping.append(KEYCODE_SPACE)
#                    keyboardMapping.append(0x20)
#                elif currByte == 0x0D:
#                    #keyboardMapping.append(KEYCODE_RETURN)
#                    keyboardMapping.append(0x0D)
#                elif currByte == 0xFF: # hack?
#                    #keyboardMapping.append(KEYCODE_INVALID)
#                    keyboardMapping.append(0xFF)
#                elif currByte == 0x00: # hack?
#                    #keyboardMapping.append(KEYCODE_INVALID)
#                    keyboardMapping.append(0x00)
#                else:
#                    assert (currByte > 0x40 and (currByte <= 0x41 + 26))
#                    keyboardMapping.append(currByte)
                    #keyboardMapping.append("TODO")
                    # Constants from ScummVM
#                    static const Common::KeyCode keybMappingArray[26] = {
#                        Common::KEYCODE_a, Common::KEYCODE_b, Common::KEYCODE_c, Common::KEYCODE_d, Common::KEYCODE_e,
#                        Common::KEYCODE_f, Common::KEYCODE_g, Common::KEYCODE_h, Common::KEYCODE_i, Common::KEYCODE_j,
#                        Common::KEYCODE_k, Common::KEYCODE_l, Common::KEYCODE_m, Common::KEYCODE_n, Common::KEYCODE_o,
#                        Common::KEYCODE_p, Common::KEYCODE_q, Common::KEYCODE_r, Common::KEYCODE_s, Common::KEYCODE_t,
#                        Common::KEYCODE_u, Common::KEYCODE_v, Common::KEYCODE_w, Common::KEYCODE_x, Common::KEYCODE_y,
#                        Common::KEYCODE_z};
                    #keyboardMapping.append(keyboardMappingArray[currByte - 0x41])
#            outData.keyboardMapping = keyboardMapping
        return outData


