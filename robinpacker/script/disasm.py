#! /usr/bin/python
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import struct

from opcodes import *
import robinpacker.script.ast.elements as ast

def unpack(rfile, format):
    result = struct.unpack(format, rfile.read(struct.calcsize(format)))
    return result[0] if len(result) == 1 else result


class BytecodeToTreeConverter(object):
    def __init__(self):
        pass

    def _parse_function_call(self, opcode, script):
        function_node = ast.FunctionNode()
        function_node.opcode = opcode
        for arg_type in opcode.arguments:
            value = unpack(script, '<H')
            argument_node = ast.ArgumentNode()
            argument_node.value = value
            argument_node.arg_type = arg_type
            function_node.arguments.append(argument_node)
        return function_node

    def convert(self, script_byte_string, script_base_name):
        script = StringIO.StringIO(script_byte_string)
        eof = False
        rule_counter = 0
        root_node = ast.RootNode()
        while not eof:
            val = unpack(script, '<H')
            if val == 0xFFF6: # end of script
                break

            rule_counter += 1
            rule_node = ast.RuleNode()
            rule_node.name = "{0}-rule-{1:02d}".format(script_base_name, rule_counter)

            # check the conditions.
            while val != 0xFFF8:
                conditional_node = ast.ConditionalNode()
                is_negative_condition = val >= 1000
                if is_negative_condition:
                    val -= 1000
                    conditional_node.negated = True

                # op code type 1
                assert val < len(conditionalOpcodes)
                opcode = conditionalOpcodes[val]

                function_node = self._parse_function_call(opcode, script)
                conditional_node.function = function_node
                rule_node.conditions.append(conditional_node)
                val = unpack(script, '<H')

            val = unpack(script, '<H')
            while val != 0xFFF7:
                # op code type 2
                assert val < len(actionOpcodes)
                opcode = actionOpcodes[val]
                function_node = self._parse_function_call(opcode, script)
                rule_node.actions.append(function_node)
                val = unpack(script, '<H')

            root_node.rules.append(rule_node)
        script.close()
        return root_node


class TreeToRulesScriptWriter(object):
    def __init__(self):
        pass

    def _getArgumentString(self, argument_node):
        out_str = ""
        if argument_node.arg_type == argtypes.IMMEDIATE_VALUE:
            out_str = "0x{0:02X}".format(argument_node.value)
        elif argument_node.arg_type == argtypes.GET_VALUE_1:
            val = argument_node.value
            if val < 1000:
                out_str = "val(0x{0:02X})".format(val) # might need to change this, for easier parsing
            elif val > 1004:
                out_str = "getValue1(0x{0:02X})".format(val)
            elif val == 1000:
                out_str = "_selectedCharacterId"
            elif val == 1001:
                out_str = "characterIndex"
            elif val == 1002:
                out_str = "_word16F00_characterId"
            elif val == 1003:
                out_str = "_currentCharacterVariables[6]"
            elif val == 1004:
                out_str = "_word10804"
        elif argument_node.arg_type == argtypes.GET_POS_FROM_SCRIPT:
            curWord = argument_node.value
            tmpVal = curWord >> 8
            # switch statement
            if tmpVal == 0xFF:
                out_str = "(_rulesBuffer2_13[currentCharacter], _rulesBuffer2_14[currentCharacter])"
            elif tmpVal == 0xFE:
                index = curWord & 0xFF
                assert 0 <= index < 40
                out_str = "(_vm->_rulesBuffer2_13[{0}], _vm->_rulesBuffer2_14[{0}])".format(index)
            elif tmpVal == 0xFD:
                out_str = "_currentScriptCharacterPosition"
            elif tmpVal == 0xFC:
                index = curWord & 0xFF
                assert index < 40
                out_str = "(characterPositionTileX[{0}], characterPositionTileY[{0}])".format(index)
            elif tmpVal == 0xFB:
                out_str = "(characterPositionTileX[_word16F00_characterId], characterPositionTileY[_word16F00_characterId])"
            elif tmpVal == 0xFA:
                out_str = "(_array10999PosX[currentCharacter], _array109C1PosY[currentCharacter])"
            elif tmpVal == 0xF9:
                out_str = "(_currentCharacterVariables[4], _currentCharacterVariables[5])"
            elif tmpVal == 0xF8:
                index = curWord & 0xFF
                assert 0 <= index < 40
                out_str = "_vm->_rulesBuffer12Pos3[{0}]".format(index)
            elif tmpVal == 0xF7:
                out_str = "(_characterPositionTileX[_currentCharacterVariables[6]], _characterPositionTileY[_currentCharacterVariables[6]])"
            elif tmpVal == 0xF6:
                out_str = "_savedMousePosDivided"
            else:
                out_str = "(0x{0:02X}, 0x{0:02X})".format(curWord >> 8, curWord & 0xFF)
        elif argument_node.arg_type == argtypes.COMPARE_OPERATION:
            comp = argument_node.value
            if comp != ord('<') and comp != ord('>'):
                out_str = '=='
            else:
                out_str = "{0:c}".format(comp)
        elif argument_node.arg_type == argtypes.COMPUTE_OPERATION:
            comp = argument_node.value
            out_str = "{0:c}".format(comp)
        return out_str

    def _convert_function_call(self, function_node, output_file):
        output_file.write(function_node.opcode.name)
        output_file.write("(")
        for i, argument_node in enumerate(function_node.arguments):
            output_file.write(self._getArgumentString(argument_node))
            if i < len(function_node.arguments) - 1:
                output_file.write(", ")
        output_file.write(")")

    def write_tree_to_file(self, tree, output_file):
        for rule in tree.rules:
            output_file.write("rule \"{}\"\n".format(rule.name))
            if len(rule.conditions):
                output_file.write("  when\n")
            for i, conditional_node in enumerate(rule.conditions):
                output_file.write("    ")
                if conditional_node.negated:
                    output_file.write("not ")
                self._convert_function_call(conditional_node.function, output_file)
                if i < len(rule.conditions) - 1:
                    output_file.write(" and")
                output_file.write("\n")
            if len(rule.conditions):
                output_file.write("  then\n")
            else:
                output_file.write("  always\n")
            for function_node in rule.actions:
                output_file.write("    ")
                self._convert_function_call(function_node, output_file)
                output_file.write("\n")
            output_file.write("end\n\n")


class ScriptDisassembler(object):
    def __init__(self):
        self.to_tree_converter = BytecodeToTreeConverter()
        self.script_writer = TreeToRulesScriptWriter()

    def disassemble(self, script_byte_string, output_file, script_base_name):
        """
        script should be a string of bytes.
        """
        root_node = self.to_tree_converter.convert(script_byte_string, script_base_name)
        self.script_writer.write_tree_to_file(root_node, output_file)
