#! /usr/bin/python
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import os.path
import unittest

import robinpacker.script.disasm as disasm

class ScriptDisassemblerTest(unittest.TestCase):
    def testMenuScripts(self):
        with file(os.path.join('data', 'erules_out_menuScripts.dmp'), 'rb') as bytecode_file:
            script = bytecode_file.read()
        output = StringIO.StringIO()
        disasm.disassemble(script, output, 'testMenuScripts')
        output.seek(0)
        with file(os.path.join('data', 'erules_out_menuScripts.rrs'), 'r') as rules_file:
            while True:
                val1 = rules_file.readline()
                val2 = output.readline()
                self.assertEqual(val1, val2)
                if val1 == '':
                    break
