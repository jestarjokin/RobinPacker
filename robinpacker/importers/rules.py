#! /usr/bin/python

import json
import os.path

import robinpacker.script.compiler as compiler
from robinpacker.structs.character import CharacterData
from robinpacker.structs.point import PointData
from robinpacker.structs.rules import RulesData
from robinpacker.structs.rect import RectData
from robinpacker.structs.raw import RawData
from robinpacker.structs.script import ScriptData

class RulesJsonImporter(object):
    def importFile(self, json_file_name):
        def decode_objects(dct):
            try:
                type_val = dct['__type__']
            except KeyError:
                return dct
            if type_val == 'RulesData':
                rules = RulesData()
                rules.chunk1PointArray = dct['chunk1PointArray']
                rules.characters = dct['characters']
                rules.strings = dct['strings']
                rules.scripts = dct['scripts']
                rules.menuScripts = dct['menuScripts']
                #rules.gameScriptIndexes = dct['gameScriptIndexes']
                rules.gameScripts = dct['gameScripts']
                rules.rulesChunk9 = dct['rulesChunk9']
                #rules.chunk10Indexes = dct['chunk10Indexes']
                rules.rulesChunk11 = dct['rulesChunk11']
                rules.rectangles = dct['rectangles']
                rules.interfaceTwoStepAction = dct['hotspots']['interfaceTwoStepAction']
                rules.interfaceHotspotsX = dct['hotspots']['interfaceHotspotsX']
                rules.interfaceHotspotsY = dct['hotspots']['interfaceHotspotsY']
                rules.keyboardMapping = dct['hotspots']['keyboardMapping']
                return rules
            elif type_val == 'PointData':
                point = PointData()
                point.x = dct['x']
                point.y = dct['y']
                return point
            elif type_val == 'CharacterData':
                character = CharacterData()
                character.posX = dct['posX']
                character.posY = dct['posY']
                character.posAltitude = dct['posAltitude']
                character.frameArray = dct['frameArray']
                character._rulesBuffer2_5 = dct['_rulesBuffer2_5']
                character._rulesBuffer2_6 = dct['_rulesBuffer2_6']
                character._rulesBuffer2_7 = dct['_rulesBuffer2_7']
                character.spriteSize = dct['spriteSize']
                character.direction = dct['direction']
                character._rulesBuffer2_10 = dct['_rulesBuffer2_10']
                character._rulesBuffer2_11 = dct['_rulesBuffer2_11']
                character._rulesBuffer2_12 = dct['_rulesBuffer2_12']
                character._rulesBuffer2_13_posX = dct['_rulesBuffer2_13_posX']
                character._rulesBuffer2_14_posY = dct['_rulesBuffer2_14_posY']
                character.variables = dct['variables']
                character._rulesBuffer2_16 = dct['_rulesBuffer2_16']
                return character
            elif type_val == 'RectData':
                rect = RectData()
                rect.maxX = dct['maxX']
                rect.minX = dct['minX']
                rect.maxY = dct['maxY']
                rect.minY = dct['minY']
                rect.topLeftPosY = dct['topLeftPosY']
                rect.topLeftPosX = dct['topLeftPosX']
                rect.bottomRightPosY = dct['bottomRightPosY']
                rect.bottomRightPosX = dct['bottomRightPosX']
                return rect
            elif type_val == 'RawData':
                id = dct['id']
                base_name = dct['path']
                path_name = os.path.split(json_file_name)[0]
                raw_fname = os.path.join(path_name, base_name)
                with file(raw_fname, 'rb') as raw_file:
                    data = raw_file.read()
                return RawData(id, data)
            elif type_val == 'ScriptData':
                id = dct['id']
                base_name = dct['path']
                path_name = os.path.split(json_file_name)[0]
                script_fname = os.path.join(path_name, 'scripts', base_name)
                with file(script_fname, 'rb') as script_file:
                    data = script_file.read()
                data = compiler.compile_to_string(data)
                return ScriptData(id, data)
        with file(json_file_name, 'r') as json_file:
            rules = json.load(json_file, object_hook=decode_objects)
        return rules


