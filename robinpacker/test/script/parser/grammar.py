try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import unittest

import robinpacker.script.ast.elements as ast
import robinpacker.script.parser.grammar as grammar
import robinpacker.script.opcodes as opcodes
import robinpacker.script.argtypes as argtypes
from robinpacker.util import RobinScriptError

class GrammarTest(unittest.TestCase):
    def testParseString(self):
        result = grammar.string_value.parseString('"rule_52"')
        self.assertEqual('rule_52', result[0])

    def testParseInteger(self):
        result = grammar.integer.parseString('52')
        self.assertEqual(52, result[0])

    def testParseHexNumber(self):
        result = grammar.hex_number.parseString('0xA5')
        self.assertEqual(0xA5, result[0])
        result = grammar.hex_number.parseString('0x99')
        self.assertEqual(0x99, result[0])
        result = grammar.hex_number.parseString('0x2B')
        self.assertEqual(0x2B, result[0])

    def testParseNumber(self):
        result = grammar.number.parseString('0xA5')
        self.assertEqual(0xA5, result[0])
        result = grammar.number.parseString('52')
        self.assertEqual(52, result[0])

    def testParseImmediateArg(self):
        result = grammar.immediate_arg.parseString('0xA5')
        arg_node = result[0]
        self.assertEqual(ast.ArgumentNode, type(arg_node))
        self.assertEqual(argtypes.IMMEDIATE_VALUE, arg_node.arg_type)
        self.assertEqual(0xA5, arg_node.value)
        result = grammar.immediate_arg.parseString('13')
        arg_node = result[0]
        self.assertEqual(ast.ArgumentNode, type(arg_node))
        self.assertEqual(argtypes.IMMEDIATE_VALUE, arg_node.arg_type)
        self.assertEqual(13, arg_node.value)

    def testParseMultipleImmediateArguments(self):
        result = grammar.arguments.parseString('0xA5, 52')
        self.assertEqual(2, len(result))
        self.assertEqual(ast.ArgumentNode, type(result[0]))
        self.assertEqual(ast.ArgumentNode, type(result[1]))
        self.assertNotEqual(result[0].value, result[1].value)

    def testParseGetValueArg(self):
        arg_node = grammar.get_value_arg.parseString('_word10804')[0]
        self.assertEqual(argtypes.GET_VALUE_1, arg_node.arg_type)
        self.assertEqual(1004, arg_node.value)
        arg_node = grammar.get_value_arg.parseString('_currentCharacterVariables[6]')[0]
        self.assertEqual(argtypes.GET_VALUE_1, arg_node.arg_type)
        self.assertEqual(1003, arg_node.value)
        arg_node = grammar.get_value_arg.parseString('_word16F00_characterId')[0]
        self.assertEqual(argtypes.GET_VALUE_1, arg_node.arg_type)
        self.assertEqual(1002, arg_node.value)
        arg_node = grammar.get_value_arg.parseString('characterIndex')[0]
        self.assertEqual(argtypes.GET_VALUE_1, arg_node.arg_type)
        self.assertEqual(1001, arg_node.value)
        arg_node = grammar.get_value_arg.parseString('_selectedCharacterId')[0]
        self.assertEqual(argtypes.GET_VALUE_1, arg_node.arg_type)
        self.assertEqual(1000, arg_node.value)
        arg_node = grammar.get_value_arg.parseString('getValue1(0x2B00)')[0]
        self.assertEqual(argtypes.GET_VALUE_1, arg_node.arg_type)
        self.assertEqual(0x2B00, arg_node.value)
        arg_node = grammar.get_value_arg.parseString('val(0x2B)')[0]
        self.assertEqual(argtypes.GET_VALUE_1, arg_node.arg_type)
        self.assertEqual(0x2B, arg_node.value)

    def testParseCompareArg(self):
        arg_node = grammar.compare_arg.parseString('<')[0]
        self.assertEqual(argtypes.COMPARE_OPERATION, arg_node.arg_type)
        self.assertEqual(ord('<'), arg_node.value)
        arg_node = grammar.compare_arg.parseString('>')[0]
        self.assertEqual(argtypes.COMPARE_OPERATION, arg_node.arg_type)
        self.assertEqual(ord('>'), arg_node.value)
        arg_node = grammar.compare_arg.parseString('==')[0]
        self.assertEqual(argtypes.COMPARE_OPERATION, arg_node.arg_type)
        self.assertEqual(ord('='), arg_node.value)

    def testParseComputeArg(self):
        input_str = '-'
        arg_node = grammar.compute_arg.parseString(input_str)[0]
        self.assertEqual(argtypes.COMPUTE_OPERATION, arg_node.arg_type)
        self.assertEqual(ord(input_str), arg_node.value)
        input_str = '+'
        arg_node = grammar.compute_arg.parseString(input_str)[0]
        self.assertEqual(argtypes.COMPUTE_OPERATION, arg_node.arg_type)
        self.assertEqual(ord(input_str), arg_node.value)
        input_str = '*'
        arg_node = grammar.compute_arg.parseString(input_str)[0]
        self.assertEqual(argtypes.COMPUTE_OPERATION, arg_node.arg_type)
        self.assertEqual(ord(input_str), arg_node.value)
        input_str = '/'
        arg_node = grammar.compute_arg.parseString(input_str)[0]
        self.assertEqual(argtypes.COMPUTE_OPERATION, arg_node.arg_type)
        self.assertEqual(ord(input_str), arg_node.value)
        input_str = '%'
        arg_node = grammar.compute_arg.parseString(input_str)[0]
        self.assertEqual(argtypes.COMPUTE_OPERATION, arg_node.arg_type)
        self.assertEqual(ord(input_str), arg_node.value)
        input_str = '='
        arg_node = grammar.compute_arg.parseString(input_str)[0]
        self.assertEqual(argtypes.COMPUTE_OPERATION, arg_node.arg_type)
        self.assertEqual(ord(input_str), arg_node.value)

    def testParsePointArg(self):
        def compare(input_str, expected_value):
            arg_node = grammar.point_arg.parseString(input_str)[0]
            self.assertEqual(argtypes.GET_POS_FROM_SCRIPT, arg_node.arg_type)
            self.assertEqual(expected_value, arg_node.value)
        compare('(_rulesBuffer2_13[currentCharacter], _rulesBuffer2_14[currentCharacter])', 0xFF00)
        compare('_currentScriptCharacterPosition', 0xFD00)
        compare('(characterPositionTileX[_word16F00_characterId], characterPositionTileY[_word16F00_characterId])', 0xFB00)
        compare('(_array10999PosX[currentCharacter], _array109C1PosY[currentCharacter])', 0xFA00)
        compare('(_currentCharacterVariables[4], _currentCharacterVariables[5])', 0xF900)
        compare('(_characterPositionTileX[_currentCharacterVariables[6]], _characterPositionTileY[_currentCharacterVariables[6]])', 0xF700)
        compare('_savedMousePosDivided', 0xF600)
        compare('(_vm->_rulesBuffer2_13[0x21], _vm->_rulesBuffer2_14[0x21])', 0xFE21)
        compare('(characterPositionTileX[0x43], characterPositionTileY[0x43])', 0xFC43)
        compare('_vm->_rulesBuffer12Pos3[0x54]', 0xF854)
        compare('(0x12, 0x34)', 0x1234)
        compare('(56, 78)', 0x384E)

    def testParseActionFunctionWithImmediateHexArgument(self):
        result = grammar.action_function.parseString('sub18213(0xA5)')
        function_node = result[0]
        expected_opcode = opcodes.actionOpcodesLookup['sub18213']
        self.assertEqual(expected_opcode, function_node.opcode)
        self.assertEqual(1, len(function_node.arguments))
        argument_node = function_node.arguments[0]
        self.assertEqual(argtypes.IMMEDIATE_VALUE, argument_node.arg_type)
        self.assertEqual(0xA5, argument_node.value)

    def testParseActionFunctionWithTwoImmediateHexArguments(self):
        result = grammar.action_function.parseString('changeCurrentCharacterSprite(0x64, 0x0A)')
        function_node = result[0]
        expected_opcode = opcodes.actionOpcodesLookup['changeCurrentCharacterSprite']
        self.assertEqual(expected_opcode, function_node.opcode)
        self.assertEqual(2, len(function_node.arguments))
        argument_node = function_node.arguments[0]
        self.assertEqual(argtypes.IMMEDIATE_VALUE, argument_node.arg_type)
        self.assertEqual(0x64, argument_node.value)
        argument_node = function_node.arguments[1]
        self.assertEqual(argtypes.IMMEDIATE_VALUE, argument_node.arg_type)
        self.assertEqual(0x0A, argument_node.value)

    def testParseActionFunctionWithOneImmediateArgAndOneGetValueArg(self):
        result = grammar.action_function.parseString('callScript(0x01, characterIndex)')
        function_node = result[0]
        expected_opcode = opcodes.actionOpcodesLookup['callScript']
        self.assertEqual(expected_opcode, function_node.opcode)
        self.assertEqual(2, len(function_node.arguments))
        argument_node = function_node.arguments[0]
        self.assertEqual(argtypes.IMMEDIATE_VALUE, argument_node.arg_type)
        self.assertEqual(0x01, argument_node.value)
        argument_node = function_node.arguments[1]
        self.assertEqual(argtypes.GET_VALUE_1, argument_node.arg_type)
        self.assertEqual(1001, argument_node.value)

    def testParseActionFunctionFailures(self):
        # Too many arguments
        self.assertRaises(RobinScriptError, grammar.action_function.parseString, 'sub18213(0xA5, 0x12)')
        # Too few arguments
        self.assertRaises(RobinScriptError, grammar.action_function.parseString, 'sub18213()')
        # Unknown function name
        self.assertRaises(RobinScriptError, grammar.action_function.parseString, 'notAKnownFunction(0xA5)')

    def testParseConditionalWithImmediateHexArgument(self):
        result = grammar.conditional.parseString('compWord16EFE(0x27)')
        conditional_node = result[0]
        self.assertEqual(False, conditional_node.negated)
        expected_opcode = opcodes.conditionalOpcodesLookup['compWord16EFE']
        function_node = conditional_node.function
        self.assertEqual(expected_opcode, function_node.opcode)
        self.assertEqual(1, len(function_node.arguments))
        argument_node = function_node.arguments[0]
        self.assertEqual(argtypes.IMMEDIATE_VALUE, argument_node.arg_type)
        self.assertEqual(0x27, argument_node.value)

    def testParseNegatedConditionalWithImmediateHexArgument(self):
        result = grammar.conditional.parseString('not compWord16EFE(0x27)')
        conditional_node = result[0]
        self.assertEqual(True, conditional_node.negated)
        expected_opcode = opcodes.conditionalOpcodesLookup['compWord16EFE']
        function_node = conditional_node.function
        self.assertEqual(expected_opcode, function_node.opcode)
        self.assertEqual(1, len(function_node.arguments))
        argument_node = function_node.arguments[0]
        self.assertEqual(argtypes.IMMEDIATE_VALUE, argument_node.arg_type)
        self.assertEqual(0x27, argument_node.value)

    def testParseMultipleConditionals(self):
        result = grammar.multiple_conditionals.parseString('CurrentCharacterVar0Equals(0x01) and sub17782(0x2B)')
        conditionals = result['conditionals']
        self.assertEqual(2, len(conditionals))
        self.assertEqual(ast.ConditionalNode, type(conditionals[0]))
        self.assertEqual(ast.ConditionalNode, type(conditionals[1]))

    def testParseRule(self):
        input_str = """
            rule "erulesout_gameScript_22-rule-06"
              when
                CurrentCharacterVar0Equals(0x01)
              then
                enableCurrentCharacterScript(0x00)
            end
        """
        result = grammar.rule.parseString(input_str)
        rule_node = result[0]
        self.assertEqual('erulesout_gameScript_22-rule-06', rule_node.name)
        self.assertEqual(1, len(rule_node.conditions))
        conditional_node = rule_node.conditions[0]
        self.assertEqual('CurrentCharacterVar0Equals', conditional_node.function.opcode.name)
        self.assertEqual(1, len(rule_node.actions))
        action_node = rule_node.actions[0]
        self.assertEqual('enableCurrentCharacterScript', action_node.opcode.name)

    def testParseRuleWithMultipleConditionals(self):
        input_str = """
            rule "erulesout_gameScript_22-rule-06"
              when
                CurrentCharacterVar0Equals(0x01) and
                sub17782(0x2B)
              then
                enableCurrentCharacterScript(0x00)
            end
        """
        result = grammar.rule.parseString(input_str)
        rule_node = result[0]
        self.assertEqual('erulesout_gameScript_22-rule-06', rule_node.name)
        self.assertEqual(2, len(rule_node.conditions))
        conditional_node = rule_node.conditions[0]
        self.assertEqual('CurrentCharacterVar0Equals', conditional_node.function.opcode.name)
        conditional_node = rule_node.conditions[1]
        self.assertEqual('sub17782', conditional_node.function.opcode.name)
        self.assertEqual(1, len(rule_node.actions))
        action_node = rule_node.actions[0]
        self.assertEqual('enableCurrentCharacterScript', action_node.opcode.name)

    def testParseRuleWithMultipleConditionalsAndMultipleActions(self):
        input_str = """
            rule "erules_out_gameScript_8-rule-13"
              when
                compWord16EFE(0x6C) and
                IsCurrentCharacterVar0LessEqualThan(0x52) and
                not sub17782(0x2B)
              then
                setCurrentCharacterVar6(0x1B)
                enableCurrentCharacterScript(0x1E)
            end
        """
        result = grammar.rule.parseString(input_str)
        rule_node = result[0]
        self.assertEqual('erules_out_gameScript_8-rule-13', rule_node.name)
        self.assertEqual(3, len(rule_node.conditions))
        self.assertEqual('compWord16EFE', rule_node.conditions[0].function.opcode.name)
        self.assertEqual('IsCurrentCharacterVar0LessEqualThan', rule_node.conditions[1].function.opcode.name)
        self.assertEqual('sub17782', rule_node.conditions[2].function.opcode.name)
        self.assertEqual(True, rule_node.conditions[2].negated)
        self.assertEqual(2, len(rule_node.actions))
        self.assertEqual('setCurrentCharacterVar6', rule_node.actions[0].opcode.name)
        self.assertEqual('enableCurrentCharacterScript', rule_node.actions[1].opcode.name)

    def testParseRuleWithNoConditionals(self):
        input_str = """
            rule "erules_out_gameScript_8-rule-26"
              always
                callScript(0x01, characterIndex)
            end
        """
        result = grammar.rule.parseString(input_str)
        self.assertEqual(1, len(result))
        rule_node = result[0]
        self.assertEqual(0, len(rule_node.conditions))
        self.assertEqual(1, len(rule_node.actions))
        self.assertEqual('callScript', rule_node.actions[0].opcode.name)

    def testParseMultipleRules(self):
        input_str = """
            rule "erulesout_gameScript_22-rule-06"
              when
                CurrentCharacterVar0Equals(0x01) and
                sub17782(0x2B)
              then
                enableCurrentCharacterScript(0x00)
            end

            rule "erulesout_gameScript_22-rule-07"
              when
                CurrentCharacterVar0Equals(0x02) and
                sub17782(0x2C)
              then
                enableCurrentCharacterScript(0x01)
            end
        """
        result = grammar.root.parseString(input_str)
        root_node = result[0]
        self.assertEqual(2, len(root_node.rules))
        self.assertEqual(ast.RuleNode, type(root_node.rules[0]))
        self.assertEqual(ast.RuleNode, type(root_node.rules[1]))

    def testParseMegaScript(self):
        script = MegaScriptCreator().create_script()
        #print script
        grammar.root.parseString(script) # Just check that parsing doesn't throw an exception


class MegaScriptCreator(object):
    def __init__(self):
        self.conditional_i = 0
        self.action_i = 0
        self.immediate_arg_i = 0
        self.get_value_arg_i = 0
        self.compute_operation_i = 0
        self.compare_operation_i = 0
        self.point_arg_i = 0
        self.negated = False

    def _getArgumentString(self, arg_type):
        out_str = None
        if arg_type == argtypes.IMMEDIATE_VALUE:
            if self.immediate_arg_i % 2:
                out_str = "0x{0:02X}".format(self.immediate_arg_i % 0xFFFF)
            else:
                out_str = "{}".format(self.immediate_arg_i)
            self.immediate_arg_i += 1
        elif arg_type == argtypes.GET_VALUE_1:
            variation = self.get_value_arg_i % 7
            value = self.get_value_arg_i % 0xFFFF
            if variation == 0:
                out_str = "val(0x{0:02X})".format(value)
            elif variation == 1:
                out_str = "getValue1(0x{0:02X})".format(value)
            elif variation == 2:
                out_str = "_selectedCharacterId"
            elif variation == 3:
                out_str = "characterIndex"
            elif variation == 4:
                out_str = "_word16F00_characterId"
            elif variation == 5:
                out_str = "_currentCharacterVariables[6]"
            elif variation == 6:
                out_str = "_word10804"
            self.get_value_arg_i += 1
        elif arg_type == argtypes.GET_POS_FROM_SCRIPT:
            variation = self.point_arg_i % 11
            value = self.point_arg_i % 0xFFFF
            if variation == 0:
                out_str = "(_rulesBuffer2_13[currentCharacter], _rulesBuffer2_14[currentCharacter])"
            elif variation == 1:
                value %= 40
                out_str = "(_vm->_rulesBuffer2_13[{0}], _vm->_rulesBuffer2_14[{0}])".format(value)
            elif variation == 2:
                out_str = "_currentScriptCharacterPosition"
            elif variation == 3:
                value %= 40
                out_str = "(characterPositionTileX[{0}], characterPositionTileY[{0}])".format(value)
            elif variation == 4:
                out_str = "(characterPositionTileX[_word16F00_characterId], characterPositionTileY[_word16F00_characterId])"
            elif variation == 5:
                out_str = "(_array10999PosX[currentCharacter], _array109C1PosY[currentCharacter])"
            elif variation == 6:
                out_str = "(_currentCharacterVariables[4], _currentCharacterVariables[5])"
            elif variation == 7:
                value %= 40
                out_str = "_vm->_rulesBuffer12Pos3[{0}]".format(value)
            elif variation == 8:
                out_str = "(_characterPositionTileX[_currentCharacterVariables[6]], _characterPositionTileY[_currentCharacterVariables[6]])"
            elif variation == 9:
                out_str = "_savedMousePosDivided"
            elif variation == 10:
                value %= 0xFE
                out_str = "(0x{0:02X}, 0x{0:02X})".format(value, value + 1)
            self.point_arg_i += 1
        elif arg_type == argtypes.COMPARE_OPERATION:
            values = ['<', '>', '==']
            out_str = values[self.compare_operation_i % len(values)]
            self.compare_operation_i += 1
        elif arg_type == argtypes.COMPUTE_OPERATION:
            values = ['-', '+', '*', '/', '%', '=']
            out_str = values[self.compute_operation_i % len(values)]
            self.compute_operation_i += 1
        return out_str

    def _write_function_call(self, opcode, output):
        output.write(opcode.name)
        output.write("(")
        for i, arg_type in enumerate(opcode.arguments):
            output.write(self._getArgumentString(arg_type))
            if i < len(opcode.arguments) - 1:
                output.write(", ")
        output.write(")")

    def create_script(self):
        output = StringIO.StringIO()
        output.write('rule "Mega Script"\n')
        output.write('  when\n')
        for opcode in opcodes.conditionalOpcodes:
            output.write('    ')
            self._write_function_call(opcode, output)
            if opcode != opcodes.conditionalOpcodes[-1]:
                output.write(" and")
            output.write("\n")
        output.write('  then\n')
        for opcode in opcodes.actionOpcodes:
            output.write('    ')
            self._write_function_call(opcode, output)
            output.write("\n")
        output.write('end\n')
        return output.getvalue()
