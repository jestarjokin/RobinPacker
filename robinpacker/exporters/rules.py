#! /usr/bin/python

from collections import OrderedDict
import json
import logging
import os.path

from script import ScriptExporter
import robinpacker.structs.character
import robinpacker.structs.point
import robinpacker.structs.raw
import robinpacker.structs.rect
import robinpacker.structs.rules
import robinpacker.structs.script
from robinpacker.structs.parser import StringTable
from robinpacker.util import mkdir

class RulesJsonExporter(object):
    def __init__(self, dump_scripts=False):
        self.dump_scripts = dump_scripts

    def export(self, rules, json_file_name):
        string_table = StringTable(rules.strings)
        script_exporter = ScriptExporter()
        this = self
        class RulesJsonEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, robinpacker.structs.rules.RulesData):
                    result = OrderedDict()
                    result['__type__'] = 'RulesData'
                    result['chunk1PointArray'] = obj.chunk1PointArray
                    result['characters'] = obj.characters
                    result['strings'] =  obj.strings
                    result['scripts'] = obj.scripts
                    result['menuScripts'] = obj.menuScripts
                    #result['gameScriptIndexes'] = obj.gameScriptIndexes
                    result['gameScripts'] = obj.gameScripts
                    result['rulesChunk9'] = obj.rulesChunk9
                    #result['chunk10Indexes'] = obj.chunk10Indexes
                    result['rulesChunk11'] = obj.rulesChunk11
                    result['rectangles'] = obj.rectangles
                    result['hotspots'] = OrderedDict()
                    result['hotspots']['interfaceTwoStepAction'] = obj.interfaceTwoStepAction
                    result['hotspots']['interfaceHotspotsX'] = obj.interfaceHotspotsX
                    result['hotspots']['interfaceHotspotsY'] = obj.interfaceHotspotsY
                    result['hotspots']['keyboardMapping'] = obj.keyboardMapping
                    return result
                elif isinstance(obj, robinpacker.structs.point.PointData):
                    result = OrderedDict()
                    result['__type__'] = 'PointData'
                    result['x'] = obj.x
                    result['y'] = obj.y
                    return result
                elif isinstance(obj, robinpacker.structs.character.CharacterData):
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
                elif isinstance(obj, robinpacker.structs.rect.RectData):
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
                elif isinstance(obj, robinpacker.structs.raw.RawData) or (
                    isinstance(obj, robinpacker.structs.script.ScriptData) and
                    this.dump_scripts
                ):
                    raw_fname = os.path.splitext(json_file_name)[0]  + '_' + obj.id + '.dmp'
                    logging.debug('Dumping raw data to {}'.format(raw_fname))
                    with file(raw_fname, 'wb') as raw_file:
                        raw_file.write(obj.data)
                    relative_fname = os.path.basename(raw_fname)
                    result = OrderedDict()
                    result['__type__'] = 'RawData'
                    result['id'] = obj.id
                    result['path'] = relative_fname
                    return result
                elif isinstance(obj, robinpacker.structs.script.ScriptData):
                    # Scripts are written to a "scripts" sub-directory, and each script's name is derived
                    #  from the JSON file's name and the script's ID property.
                    dir_name, base_name = os.path.split(json_file_name)
                    base_name = os.path.splitext(base_name)[0]
                    dir_name = os.path.join(dir_name, 'scripts')
                    mkdir(dir_name)
                    script_fname = os.path.join(dir_name, '{}_{}.rrs'.format(base_name, obj.id))
                    logging.debug('Disassembling script data to {}'.format(script_fname))
                    script_exporter.export(obj, script_fname, string_table)
                    relative_fname = os.path.basename(script_fname)
                    result = OrderedDict()
                    result['__type__'] = 'ScriptData'
                    result['id'] = obj.id
                    result['path'] = relative_fname
                    return result
                return super(RulesJsonEncoder, self).default(obj)
        mkdir(os.path.dirname(json_file_name))
        with file(json_file_name, 'w') as json_file:
            json.dump(rules, json_file, cls=RulesJsonEncoder, indent=1)

