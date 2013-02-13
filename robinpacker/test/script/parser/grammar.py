import unittest

import robinpacker.script.ast.elements as ast
import robinpacker.script.parser.grammar as grammar
import robinpacker.script.opcodes as opcodes
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

    def testParseImmediateArg(self):
        result = grammar.immediate_arg.parseString('0xA5')
        arg_node = result[0]
        self.assertEqual(ast.ArgumentNode, type(arg_node))
        self.assertEqual(ast.ARG_TYPE_IMMEDIATE_VALUE, arg_node.arg_type)
        self.assertEqual(0xA5, arg_node.value)

    def testParseActionFunctionWithImmediateHexArgument(self):
        result = grammar.action_function.parseString('OC_sub18213(0xA5)')
        function_node = result[0]
        opcode_val, expected_opcode = opcodes.actionOpCodesLookup['OC_sub18213']
        self.assertEqual(expected_opcode, function_node.opcode)
        self.assertEqual(1, len(function_node.arguments))
        argument_node = function_node.arguments[0]
        self.assertEqual(ast.ARG_TYPE_IMMEDIATE_VALUE, argument_node.arg_type)
        self.assertEqual(0xA5, argument_node.value)

    def testParseActionFunctionWithTwoImmediateHexArguments(self):
        result = grammar.action_function.parseString('OC_changeCurrentCharacterSprite(0x64, 0x0A)')
        function_node = result[0]
        opcode_val, expected_opcode = opcodes.actionOpCodesLookup['OC_changeCurrentCharacterSprite']
        self.assertEqual(expected_opcode, function_node.opcode)
        self.assertEqual(2, len(function_node.arguments))
        argument_node = function_node.arguments[0]
        self.assertEqual(ast.ARG_TYPE_IMMEDIATE_VALUE, argument_node.arg_type)
        self.assertEqual(0x64, argument_node.value)
        argument_node = function_node.arguments[1]
        self.assertEqual(ast.ARG_TYPE_IMMEDIATE_VALUE, argument_node.arg_type)
        self.assertEqual(0x0A, argument_node.value)

    def testParseActionFunctionFailures(self):
        # Too many arguments
        self.assertRaises(RobinScriptError, grammar.action_function.parseString, 'OC_sub18213(0xA5, 0x12)')
        # Too few arguments
        self.assertRaises(RobinScriptError, grammar.action_function.parseString, 'OC_sub18213()')
        # Unknown function name
        self.assertRaises(RobinScriptError, grammar.action_function.parseString, 'OC_notAKnownFunction(0xA5)')

    def testParseConditionalWithImmediateHexArgument(self):
        result = grammar.conditional.parseString('OC_compWord16EFE(0x27)')
        conditional_node = result[0]
        self.assertEqual(False, conditional_node.negated)
        opcode_val, expected_opcode = opcodes.conditionalOpCodesLookup['OC_compWord16EFE']
        function_node = conditional_node.function
        self.assertEqual(expected_opcode, function_node.opcode)
        self.assertEqual(1, len(function_node.arguments))
        argument_node = function_node.arguments[0]
        self.assertEqual(ast.ARG_TYPE_IMMEDIATE_VALUE, argument_node.arg_type)
        self.assertEqual(0x27, argument_node.value)

    def testParseNegatedConditionalWithImmediateHexArgument(self):
        result = grammar.conditional.parseString('not OC_compWord16EFE(0x27)')
        conditional_node = result[0]
        self.assertEqual(True, conditional_node.negated)
        opcode_val, expected_opcode = opcodes.conditionalOpCodesLookup['OC_compWord16EFE']
        function_node = conditional_node.function
        self.assertEqual(expected_opcode, function_node.opcode)
        self.assertEqual(1, len(function_node.arguments))
        argument_node = function_node.arguments[0]
        self.assertEqual(ast.ARG_TYPE_IMMEDIATE_VALUE, argument_node.arg_type)
        self.assertEqual(0x27, argument_node.value)

    def testParseRule(self):
        input = """
            rule "erulesout_gameScript_22-rule-06"
              when
                OC_CurrentCharacterVar0Equals(0x01)
              then
                OC_enableCurrentCharacterScript(0x00)
            end
        """
        result = grammar.rule.parseString(input)
        rule_node = result[0]
        self.assertEqual('erulesout_gameScript_22-rule-06', rule_node.name)
        self.assertEqual(1, len(rule_node.conditions))
        conditional_node = rule_node.conditions[0]
        self.assertEqual('OC_CurrentCharacterVar0Equals', conditional_node.function.opcode.opName)

    def testParseRuleWithMultipleConditionals(self):
        input = """
            rule "erulesout_gameScript_22-rule-06"
              when
                OC_CurrentCharacterVar0Equals(0x01) and
                OC_sub17782(0x2B)
              then
                OC_enableCurrentCharacterScript(0x00)
            end
        """
        result = grammar.rule.parseString(input)
        rule_node = result[0]
        self.assertEqual('erulesout_gameScript_22-rule-06', rule_node.name)
        self.assertEqual(1, len(rule_node.conditions))
        conditional_node = rule_node.conditions[0]
        self.assertEqual('OC_CurrentCharacterVar0Equals', conditional_node.function.opcode.opName)
