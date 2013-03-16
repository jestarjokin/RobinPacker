#! /usr/bin/python

import os.path

import robinpacker.script.disasm as disasm

class ScriptExporter(object):
    def __init__(self):
        pass

    def export(self, script_data, output_file_name, string_table):
        with file(output_file_name, 'w') as output_file:
            script_base_name = os.path.splitext(os.path.basename(output_file_name))[0]
            disasm.disassemble(script_data.data, output_file, script_base_name, string_table)
