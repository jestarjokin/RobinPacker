#! /usr/bin/python
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import unittest

import robinpacker.script.disasm

class ScriptDisassemblerTest(unittest.TestCase):
    def testMenuScripts(self):
        disasm = robinpacker.script.disasm.ScriptDisassembler()
        with file('erules_out_menuScripts.dmp', 'rb') as bytecode_file:
            script = bytecode_file.read()
        output = StringIO.StringIO()
        disasm.disassemble(script, output, 'testMenuScripts')
        output.seek(0)
        with file('erules_out_menuScripts.rrs', 'r') as rules_file:
            self.assertEqual(rules_file.readline(), output.readline())
