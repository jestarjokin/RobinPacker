#! /usr/bin/python
import unittest

import robinpacker.disasm.script

class ScriptDisassemblerTest(unittest.TestCase):
    def testMenuScripts(self):
        disasm = robinpacker.disasm.script.ScriptDisassembler()
        with file('erules_out_menuScripts.dmp', 'rb') as script_file:
            script = script_file.read()
        disasm.disassemble(script)
