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
        with file('erules_out_menuScripts.dmp', 'rb') as script_file:
            script = script_file.read()
        output = StringIO.StringIO()
        disasm.disassemble(script, output, 'testMenuScripts')
        print output.getvalue()
