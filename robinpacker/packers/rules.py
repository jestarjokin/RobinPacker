#! /usr/bin/python

from robinpacker.util import pack

packedStringLookup = ['I am ', 'You are ', 'you are ', 'hou art ', 'in the ', 'is the ', 'is a ', 'in a ', 'To the ',
                      'to the ', 'by ', 'going ', 'here ', 'The', 'the', 'and ', 'some ', 'build', 'not ', 'way', 'I ',
                      'a ', 'an ', 'from ', 'of ', 'him', 'her', 'by ', 'his ', 'ing ', 'tion', 'have ', 'you', "I've ",
                      "can't ", 'up ', 'to ', 'he ', 'she ', 'down ', 'what', 'What', 'with', 'are ', 'and', 'ent',
                      'ian', 'ome', 'ed ', 'me', 'my', 'ai', 'it', 'is', 'of', 'oo', 'ea', 'er', 'es', 'th', 'we',
                      'ou', 'ow', 'or', 'gh', 'go', 'er', 'st', 'ee', 'th', 'sh', 'ch', 'ct', 'on', 'ly', 'ng', 'nd',
                      'nt', 'ty', 'll', 'le', 'de', 'as', 'ie', 'in', 'ss', "'s ", "'t ", 're', 'gg', 'tt', 'pp',
                      'nn', 'ay', 'ar', 'wh']

class RulesBinaryPacker(object):
    def pack(self, rules, fname):
        with file(fname, 'wb') as rfile:
            # Header
            rfile.write('\x00\x00')

            # Chunk 1
            format = '<H'
            numEntries = len(rules.chunk1PointArray) * 2
            pack(rfile, numEntries, format)
            format = '<2B'
            for point in rules.chunk1PointArray:
                pack(rfile, (point.y, point.x), format)

            # Chunk 2 - character data
            format = '<H'
            numEntries = len(rules.characters)
            assert numEntries <= 40
            pack(rfile, numEntries, format)
            for character in rules.characters:
                format = '<4H2b8B'
                pack(rfile,
                    (
                        character.posX if character.posX == 0xFFFF else ((character.posX - 4) >> 3),
                        character.posY if character.posY == 0xFFFF else ((character.posY - 4) >> 3),
                        character.posAltitude,
                        character.frameArray,
                        character._rulesBuffer2_5,
                        character._rulesBuffer2_6,
                        character._rulesBuffer2_7,
                        character.spriteSize,
                        character.direction,
                        character._rulesBuffer2_10,
                        character._rulesBuffer2_11,
                        character._rulesBuffer2_12,
                        character._rulesBuffer2_13_posX,
                        character._rulesBuffer2_14_posY
                        ),
                    format
                )
                format = '32B'
                pack(rfile, character.variables, format)
                pack(rfile, character._rulesBuffer2_16, format)

            # Chunk 3 & 4 - packed strings and associated indexes
            packedStrings = []
            stringIndexes = []
            totalSize = 0
            for stringVal in rules.strings:
                stringVal = stringVal.encode('latin_1') # may not be quite right
                global packedStringLookup
                for i, lookupValue in enumerate(packedStringLookup):
                    stringVal = stringVal.replace(lookupValue, chr(0xFF - i))
                stringVal += '\x00'
                packedStrings.append(stringVal)
                stringIndexes.append(totalSize)
                totalSize += len(stringVal)
            format = '<2H'
            numEntries = len(packedStrings)
            pack(rfile, (numEntries, totalSize), format)
            format = '<' + str(numEntries) + 'H'
            pack(rfile, stringIndexes, format)
            for packedString in packedStrings:
                rfile.write(packedString)

            # Chunk 5 - scripts
            format = '<H'
            numEntries = len(rules.scripts.data) / 2
            pack(rfile, numEntries, format)
            rfile.write(rules.scripts.data)

            # Chunk 6 - menu scripts
            format = '<H'
            numEntries = len(rules.menuScripts.data) / 2
            pack(rfile, numEntries, format)
            rfile.write(rules.menuScripts.data)

            # Chunk 7 & 8 - game scripts and sizes
            format = '<H'
            numEntries = len(rules.gameScripts)
            pack(rfile, numEntries, format)
            totalSize = 0
            for script_data in rules.gameScripts:
                pack(rfile, totalSize, format)
                totalSize += len(script_data.data)
            pack(rfile, totalSize, format)
            for script_data in rules.gameScripts:
                rfile.write(script_data.data)

            # Chunk 9
            assert(len(rules.rulesChunk9) == 60)
            format = '60B'
            pack(rfile, rules.rulesChunk9, format)

            # Chunk 10 & 11
            format = 'B'
            numEntries = len(rules.rulesChunk11)
            assert numEntries <= 20
            pack(rfile, numEntries, format)
            for chunk in rules.rulesChunk11:
                size = len(chunk)
                assert size <= 0xFF
                pack(rfile, size, format)
            for chunk in rules.rulesChunk11:
                format = '{}B'.format(len(chunk))
                pack(rfile, chunk, format)

            # Chunk 12 - rectangles
            format = '<H'
            numEntries = len(rules.rectangles)
            pack(rfile, numEntries, format)
            format = '8B'
            for rect in rules.rectangles:
                pack(rfile,
                    (
                        rect.maxX,
                        rect.minX,
                        rect.maxY,
                        rect.minY,
                        rect.topLeftPosY,
                        rect.topLeftPosX,
                        rect.bottomRightPosY,
                        rect.bottomRightPosX
                    ),
                    format
                )

            # Chunk 13 - interface hotspots
            format = '20B'
            assert len(rules.interfaceTwoStepAction) == 20
            pack(rfile, rules.interfaceTwoStepAction, format)
            format = '<20h'
            pack(rfile, rules.interfaceHotspotsX, format)
            pack(rfile, rules.interfaceHotspotsY, format)
            format = '20B'
            pack(rfile, rules.keyboardMapping, format)
