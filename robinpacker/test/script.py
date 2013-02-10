#! /usr/bin/python
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import unittest

import robinpacker.disasm.script

class ScriptDisassemblerTest(unittest.TestCase):
    def testMenuScripts(self):
        disasm = robinpacker.disasm.script.ScriptDisassembler()
        with file('erules_out_menuScripts.dmp', 'rb') as script_file:
            script = script_file.read()
        output = StringIO.StringIO()
        disasm.disassemble(script, output, 'testMenuScripts')
        print output.getvalue()
