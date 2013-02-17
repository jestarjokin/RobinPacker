import itertools
import unittest

import robinpacker.script.compiler as compiler
import robinpacker.script.parser.parser as parser

class RobinRulesCompilerTest(unittest.TestCase):
    def testCompileMenuScripts(self):
        with file('erules_out_menuScripts.rrs', 'r') as script_file:
            input_str = script_file.read()
        root_node = parser.parse_string(input_str)
        result = compiler.compile_to_string(root_node)
        with file('erules_out_menuScripts.dmp', 'rb') as bytecode_file:
            expected_bytecode = bytecode_file.read()
        print repr(result)
        for i, (expected, actual) in enumerate(itertools.izip(expected_bytecode, result)):
            self.assertEqual(expected, actual, 'Values don\'t match: expected {0}, vs actual {1}, pos {2} (0x{2:X})'.format(
                repr(expected), repr(actual), i
            ))
