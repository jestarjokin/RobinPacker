try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import itertools
import os.path
import unittest

import robinpacker.script.disasm as disasm
import robinpacker.script.compiler as compiler
import robinpacker.script.parser.parser as parser

class RobinRulesCompilerTest(unittest.TestCase):
    def __compare_scripts(self, expected_script, actual_bytecode, script_fname):
        # From a "unit" test perspective, it's probably a bit silly to also test
        # the disassembly here, but it's very handy to ensure we get 1:1 copies.
        disasm_script = StringIO.StringIO()
        disasm.disassemble(actual_bytecode, disasm_script, os.path.splitext(script_fname)[0])
        actual_script = disasm_script.getvalue()
        expected_script_file = StringIO.StringIO(expected_script)
        actual_script_file = StringIO.StringIO(actual_script)
        while True:
            val1 = expected_script_file.readline()
            val2 = actual_script_file.readline()
            self.assertEqual(val1, val2)
            if val1 == '':
                break

    def __read_and_compare(self, script_fname, bytecode_fname):
        with file(os.path.join('data', script_fname), 'r') as script_file:
            input_str = script_file.read()
        root_node = parser.parse_string(input_str)
        result = compiler.compile_to_string(root_node)
        with file(os.path.join('data', bytecode_fname), 'rb') as bytecode_file:
            expected_bytecode = bytecode_file.read()
        self.__compare_scripts(input_str, result, script_fname)
        self.assertEqual(len(expected_bytecode), len(result))
        for i, (expected, actual) in enumerate(itertools.izip(expected_bytecode, result)):
            self.assertEqual(expected, actual, 'Values don\'t match: expected 0x{0:X}, vs actual 0x{1:X}, pos {2} (0x{2:X})'.format(
                ord(expected), ord(actual), i
            ))

    def testCompileGameScript102(self):
        self.__read_and_compare('erules_out_gameScript_102.rrs', 'erules_out_gameScript_102.dmp')

    def testCompileGameScript157(self):
        self.__read_and_compare('erules_out_gameScript_157.rrs', 'erules_out_gameScript_157.dmp')

    def testCompileGameScript89(self):
        self.__read_and_compare('erules_out_gameScript_89.rrs', 'erules_out_gameScript_89.dmp')

    def testCompileMenuScripts(self):
        self.__read_and_compare('erules_out_menuScripts.rrs', 'erules_out_menuScripts.dmp')

    def testCompileMenuScripts(self):
        self.__read_and_compare('erules_out_menuScripts_1.rrs', 'erules_out_menuScripts_1.dmp')

    def testCompileAllMenuScripts(self):
        self.__read_and_compare('erules_out_menuScripts.rrs', 'erules_out_menuScripts.dmp')
