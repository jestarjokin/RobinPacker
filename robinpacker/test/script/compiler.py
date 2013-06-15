#! /usr/bin/python
# Use, distribution, and modification of the RobinPacker binaries, source code,
# or documentation, is subject to the terms of the MIT license.
#
# Copyright (c) 2013 Laurence Dougal Myers
#
# http://opensource.org/licenses/MIT

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import itertools
import os.path
import unittest

import robinpacker.script.disasm as disasm
import robinpacker.script.compiler as compiler
from robinpacker.structs.parser import ParserContext, StringTable

class RobinRulesCompilerTest(unittest.TestCase):
    def __compare_scripts(self, expected_script, actual_bytecode, script_fname, string_table):
        # From a "unit" test perspective, it's probably a bit silly to also test
        # the disassembly here, but it's very handy to ensure we get 1:1 copies.
        disasm_script = StringIO.StringIO()
        disasm.disassemble(actual_bytecode, disasm_script, os.path.splitext(script_fname)[0], string_table)
        actual_script = disasm_script.getvalue()
        expected_script_file = StringIO.StringIO(expected_script)
        actual_script_file = StringIO.StringIO(actual_script)
        while True:
            val1 = expected_script_file.readline()
            val2 = actual_script_file.readline()
            self.assertEqual(val1, val2)
            if val1 == '':
                break

    def __read_and_compare(self, script_fname, bytecode_fname, string_map):
        with file(os.path.join('data', script_fname), 'r') as script_file:
            input_str = script_file.read()
        string_table = StringTable(string_map)
        external_parser_context = ParserContext(string_table)
        result = compiler.compile_to_string(input_str, external_parser_context)
        with file(os.path.join('data', bytecode_fname), 'rb') as bytecode_file:
            expected_bytecode = bytecode_file.read()
        self.__compare_scripts(input_str, result, script_fname, string_table)
        self.assertEqual(len(expected_bytecode), len(result))
        for i, (expected, actual) in enumerate(itertools.izip(expected_bytecode, result)):
            self.assertEqual(expected, actual, 'Values don\'t match: expected 0x{0:X}, vs actual 0x{1:X}, pos {2} (0x{2:X})'.format(
                ord(expected), ord(actual), i
            ))

    def testCompileGameScript102(self):
        string_map = {}
        self.__read_and_compare('erules_out_gameScript_102.rrs', 'erules_out_gameScript_102.dmp', string_map)

    def testCompileGameScript157(self):
        string_map = {
            "Oh my god! I'm off!!!" : 347
        }
        self.__read_and_compare('erules_out_gameScript_157.rrs', 'erules_out_gameScript_157.dmp', string_map)

    def testCompileGameScript89(self):
        string_map = {
            "[[They are all rich, successful and handsome men; except Robin of Loxley!]Pig-swill is at least attractive to pigs!]Three: one to tap him on the shoulder, and two to shout Boo!" : 203
        }
        self.__read_and_compare('erules_out_gameScript_89.rrs', 'erules_out_gameScript_89.dmp', string_map)

    def testCompileMenuScripts(self):
        string_map = {}
        self.__read_and_compare('erules_out_menuScripts_1.rrs', 'erules_out_menuScripts_1.dmp', string_map)

    def testCompileAllMenuScripts(self):
        string_map = {
            "PAUSE.GFX" : 354,
            "GALLOWS.GFX" : 79,
            "[[This poor devil is beyond even Robin Hood's help!]It is too late to help this poor creature!]A brave attempt, but once they're dead, there's little you can do!" :355,
            "Um..... No, I am too shy to do that!" : 356,
            "If it's a fight you want, then a fight you shall have!" : 357,
            "Nay sir, I see no reason to fight thee." : 108,
            "Who is this that dares to stare at Robin Hood?!" : 358,
            "Here Sir, have this money as a token that I mean thee no harm." : 359,
            "[Help me someone!!!!!] Down with the Norman pigs!" : 360,
            "Toot! Toot!" : 144,
            "[You're not taking me anywhere!]Get your hands off me, pig!" : 361,
            "[I think I will follow him for a while.]I wonder where he is going." : 362,
            "[The sight of a pretty maid would cheer me greatly. I shall follow her.]I wonder where she is going." : 363,
            "I think I'll follow that animal." : 364,
            "Where is that animal going?" : 365,
            "[Go forth, my merry fellow, and find a wealthy man, that ye might relieve him of his riches for our cause!]Go ye forth sir, and find a man to rob. Bring the spoils back to me, that we might profit from them!" : 366,
            "['Tis time you earned your keep, Sir. Go ye forth and spill the blood of our enemy!]Methinks 'tis time for heads to roll! Go forth and rid this land of another filthy Norman swine!" : 367,
            "SOUL.GFX" : 368,
            "[[Take this!]Have at ye knave!]Have a taste of my knuckles!" : 369,
        }
        self.__read_and_compare('erules_out_menuScripts.rrs', 'erules_out_menuScripts.dmp', string_map)
