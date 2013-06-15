#! /usr/bin/python
# Use, distribution, and modification of the RobinPacker binaries, source code,
# or documentation, is subject to the terms of the MIT license.
#
# Copyright (c) 2013 Laurence Dougal Myers
#
# http://opensource.org/licenses/MIT

import os.path

import robinpacker.script.disasm as disasm

class ScriptExporter(object):
    def __init__(self):
        pass

    def export(self, script_data, output_file_name, string_table):
        with file(output_file_name, 'w') as output_file:
            script_base_name = os.path.splitext(os.path.basename(output_file_name))[0]
            disasm.disassemble(script_data.data, output_file, script_base_name, string_table)
