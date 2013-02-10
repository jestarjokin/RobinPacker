#! /usr/bin/python

from collections import OrderedDict
import json
import logging
import os.path

from script import ScriptExporter
import structs.rules


class RulesJsonExporter(object):
    def export(self, rules, json_file_name):
        script_exporter = ScriptExporter()
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
                    logging.debug('Dumping raw data to {}'.format(raw_fname))
                    with file(raw_fname, 'wb') as raw_file:
                        raw_file.write(obj.data)
                    relative_fname = os.path.basename(raw_fname)
                    result = OrderedDict()
                    result['__type__'] = 'RawData'
                    result['id'] = obj.id
                    result['path'] = relative_fname
                    return result
                elif isinstance(obj, structs.script.ScriptData):
                    script_fname = os.path.splitext(json_file_name)[0]  + '_' + obj.id + '.rrs'
                    logging.debug('Disassembling script data to {}'.format(script_fname))
                    script_exporter.export(obj, script_fname)
                    relative_fname = os.path.basename(script_fname)
                    result = OrderedDict()
                    result['__type__'] = 'ScriptData'
                    result['id'] = obj.id
                    result['path'] = relative_fname
                    return result
                return super(RulesJsonEncoder, self).default(obj)
        with file(json_file_name, 'w') as json_file:
            json.dump(rules, json_file, cls=RulesJsonEncoder, indent=1)

