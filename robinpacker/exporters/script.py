#! /usr/bin/python

import os.path

import robinpacker.script.disasm as disasm

class ScriptExporter(object):
    def __init__(self):
        self.disassembler = disasm.ScriptDisassembler()

    def export(self, scriptData, output_file_name):
        with file(output_file_name, 'w') as output_file:
            script_base_name = os.path.splitext(os.path.basename(output_file_name))[0]
            self.disassembler.disassemble(scriptData.data, output_file, script_base_name)
