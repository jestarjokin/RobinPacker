#! /usr/bin/python

from collections import OrderedDict
import json
import logging
import os.path
try:
    import xml.etree.cElementTree as etree
except ImportError:
    import xml.etree.ElementTree as etree

import structs.rules


class RulesJsonExporter(object):
    def export(self, rules, json_file_name):
        class RulesJsonEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, structs.rules.RulesData):
                    result = OrderedDict()
                    result['__type__'] = 'RulesData'
                    result['chunk1PointArray'] = obj.chunk1PointArray
                    result['characters'] = obj.characters
                    result['strings'] =  obj.strings
                    result['scripts'] = obj.scripts
                    result['menuScripts'] = obj.menuScripts
                    result['gameScriptIndexes'] = obj.gameScriptIndexes
                    result['gameScriptData'] = obj.gameScriptData
                    result['rulesChunk9'] = obj.rulesChunk9
                    result['chunk10Indexes'] = obj.chunk10Indexes
                    result['rulesChunk11'] = obj.rulesChunk11
                    result['rectangles'] = obj.rectangles
                    result['hotspots'] = OrderedDict()
                    result['hotspots']['interfaceTwoStepAction'] = obj.interfaceTwoStepAction
                    result['hotspots']['interfaceHotspotsX'] = obj.interfaceHotspotsX
                    result['hotspots']['interfaceHotspotsY'] = obj.interfaceHotspotsY
                    result['hotspots']['keyboardMapping'] = obj.keyboardMapping
                    return result
                elif isinstance(obj, structs.point.PointData):
                    result = OrderedDict()
                    result['__type__'] = 'PointData'
                    result['x'] = obj.x
                    result['y'] = obj.y
                    return result
                elif isinstance(obj, structs.character.CharacterData):
                    result = OrderedDict()
                    result['__type__'] = 'CharacterData'
                    result['posX'] = obj.posX
                    result['posY'] = obj.posY
                    result['posAltitude'] = obj.posAltitude
                    result['frameArray'] = obj.frameArray
                    result['_rulesBuffer2_5'] = obj._rulesBuffer2_5
                    result['_rulesBuffer2_6'] = obj._rulesBuffer2_6
                    result['_rulesBuffer2_7'] = obj._rulesBuffer2_7
                    result['spriteSize'] = obj.spriteSize
                    result['direction'] = obj.direction
                    result['_rulesBuffer2_10'] = obj._rulesBuffer2_10
                    result['_rulesBuffer2_11'] = obj._rulesBuffer2_11
                    result['_rulesBuffer2_12'] = obj._rulesBuffer2_12
                    result['_rulesBuffer2_13_posX'] = obj._rulesBuffer2_13_posX
                    result['_rulesBuffer2_14_posY'] = obj._rulesBuffer2_14_posY
                    result['variables'] = obj.variables
                    result['_rulesBuffer2_16'] = obj._rulesBuffer2_16
                    return result
                elif isinstance(obj, structs.rect.RectData):
                    result = OrderedDict()
                    result['__type__'] = 'RectData'
                    result['maxX'] = obj.maxX
                    result['minX'] = obj.minX
                    result['maxY'] = obj.maxY
                    result['minY'] = obj.minY
                    result['topLeftPosY'] = obj.topLeftPosY
                    result['topLeftPosX'] = obj.topLeftPosX
                    result['bottomRightPosY'] = obj.bottomRightPosY
                    result['bottomRightPosX'] = obj.bottomRightPosX
                    return result
                elif isinstance(obj, structs.raw.RawData):
                    raw_fname = os.path.splitext(json_file_name)[0]  + '_' + obj.id + '.dmp'
                    logging.debug('Dumping raw data to %s' % (raw_fname, ))
                    with file(raw_fname, 'wb') as raw_file:
                        raw_file.write(obj.data)
                    relative_fname = os.path.basename(raw_fname)
                    result = OrderedDict()
                    result['__type__'] = 'RawData'
                    result['id'] = obj.id
                    result['path'] = relative_fname
                    return result
                return super(RulesJsonEncoder, self).default(obj)
        with file(json_file_name, 'w') as json_file:
            json.dump(rules, json_file, cls=RulesJsonEncoder, indent=1)


class RulesXmlExporter(object):
    def export(self, rules, xml_file_name):
        """
        Exports a Rules object to an XML file, located at xml_file_name.

        INCOMPLETE! DO NOT USE.
        @type rules RulesData
        @type xml_file_name str
        """
        root = etree.Element('rules')

        # Chunk 1
        # Used in sub16C5C and sub16C86. Seems to be value pairs of bytes. Used to create a point? (Might just be a
        #  tuple.)
        # Later used in sub16626. Might be a function array, or to do with character positions?
        child = etree.SubElement(root, 'chunk1PointArray')
        for point in rules.chunk1PointArray:
            pointNode = etree.SubElement(child, 'point',
                attrib=dict(
                    x = repr(point.x),
                    y = repr(point.y),
                )
            )

        # Chunk 2 - character data
        child = etree.SubElement(root, 'characters')
        assert len(rules.characters) <= 40
        for charData in rules.characters:
            charNode = etree.SubElement(child, 'character',
                attrib=dict(
                    posX = repr(charData.posX), # default value is -1
                    posY = repr(charData.posY), # default value is -1
                    posAltitude = repr(charData.posAltitude), # default value is 0
                    frameArray = repr(charData.frameArray), # default value is 0
                    rulesBuffer2_5 = repr(charData._rulesBuffer2_5), # default value is -1
                    rulesBuffer2_6 = repr(charData._rulesBuffer2_6), # default value is 4
                    rulesBuffer2_7 = repr(charData._rulesBuffer2_7), # default value is 0
                    spriteSize = repr(charData.spriteSize), # default value is 20
                    direction = repr(charData.direction), # default value is 0
                    rulesBuffer2_10 = repr(charData._rulesBuffer2_10), # default value is 0
                    rulesBuffer2_11 = repr(charData._rulesBuffer2_11), # default value is 0
                    rulesBuffer2_12 = repr(charData._rulesBuffer2_12), # default value is 0
                    rulesBuffer2_13_posX = repr(charData._rulesBuffer2_13_posX), # default value is 0
                    rulesBuffer2_14_posY = repr(charData._rulesBuffer2_14_posY), # default value is 0
                )
            )
            variablesNode = etree.SubElement(charNode, 'variables')
            for variable in charData.variables:
                variableNode = etree.SubElement(variablesNode, 'variable')
                variableNode.text = repr(variable)
            rulesBuffer2_16sNode = etree.SubElement(charNode, 'rulesBuffer2_16s')
            for rulesBuffer2_16 in charData._rulesBuffer2_16:
                rulesBuffer2_16Node = etree.SubElement(rulesBuffer2_16sNode, 'rulesBuffer2_16')
                rulesBuffer2_16Node.text = repr(rulesBuffer2_16)

        # Chunk 3 (and 4) - strings
        child = etree.SubElement(root, 'strings')
        for string in rules.strings:
            stringNode = etree.SubElement(child, 'string')
            stringNode.text = repr(string).rstrip('\x00') # remove null-terminating character

        # Chunk 5 - scripts
        child = etree.SubElement(root, 'scripts')
        child.text = repr(rules.scripts)

        # Chunk 6 - menu scripts
        child = etree.SubElement(root, 'menuScripts')
        child.text = repr(rules.menuScripts)

        # Chunk 7 & 8 - game scripts and indexes
        child = etree.SubElement(root, 'gameScriptIndexes')
        for gs_index in rules.gameScriptIndexes:
            gs_indexNode = etree.SubElement(child, 'index')
            gs_indexNode.text = repr(gs_index)
        gs_data = etree.SubElement(child, 'gameScriptData')
        gs_data.text = repr(rules.gameScriptData)

        # Chunk 9 - might be flags to do with the landscape.
        # Used in sub1693A_chooseDirections, prepareGameArea, renderCharacters, and sub16B8F_moveCharacter.
        child = etree.SubElement(root, 'rulesChunk9')
        child.text = repr(rules.rulesChunk9)

        # Chunk 10 & 11 - maybe constants? used in opcode 0x2A, OC_sub17EC5, and uses the lookup value in
        #  computeOperation. Might be arrays of values?
        child = etree.SubElement(root, 'chunk10Indexes')
        for c10_index in rules.chunk10Indexes:
            c10_indexNode = etree.SubElement(child, 'index')
            c10_indexNode.text = repr(c10_index)
        child = etree.SubElement(root, 'rulesChunk11')
        child.text = repr(rules.rulesChunk11)

        # Chunk 12 - rectangles
        child = etree.SubElement(root, 'rectangles')
        for rectangle in rules.rectangles:
            rectangleNode = etree.SubElement(child, 'rectangle',
                attrib=dict(
                    maxX = repr(rectangle.maxX),
                    minX = repr(rectangle.minX),
                    maxY = repr(rectangle.maxY),
                    minY = repr(rectangle.minY),
                    topLeftPosX = repr(rectangle.topLeftPosX), # NOTE: different order
                    topLeftPosY = repr(rectangle.topLeftPosY), # NOTE: different order
                    bottomRightPosX = repr(rectangle.bottomRightPosX), # NOTE: different order
                    bottomRightPosY = repr(rectangle.bottomRightPosY), # NOTE: different order
                )
            )

        # Chunk 13 - interface hotspots
        child = etree.SubElement(root, 'hotspots')
        subNode = etree.SubElement(child, 'interfaceTwoStepAction')
        subNode.text = rules.interfaceTwoStepAction
        subNode = etree.SubElement(child, 'interfaceHotspotsX')
        for hotspotX in rules.interfaceHotspotsX:
            hotspotXNode = etree.SubElement(subNode, 'hotspotX')
            hotspotXNode.text = repr(hotspotX)
        subNode = etree.SubElement(child, 'interfaceHotspotsY')
        for hotspotY in rules.interfaceHotspotsY:
            hotspotYNode = etree.SubElement(subNode, 'hotspotY')
            hotspotYNode.text = repr(hotspotY)
        subNode = etree.SubElement(child, 'keyboardMapping')
        subNode.text = rules.keyboardMapping

        with file(xml_file_name, 'w') as xml_file:
            etree.ElementTree(root).write(xml_file)
