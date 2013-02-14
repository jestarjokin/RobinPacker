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
        self.assertEqual(ast.ARG_TYPE_IMMEDIATE_VALUE, arg_node.arg_type)
        self.assertEqual(0xA5, arg_node.value)
        result = grammar.immediate_arg.parseString('13')
        arg_node = result[0]
        self.assertEqual(ast.ArgumentNode, type(arg_node))
        self.assertEqual(ast.ARG_TYPE_IMMEDIATE_VALUE, arg_node.arg_type)
        self.assertEqual(13, arg_node.value)

    def testParseMultipleImmediateArguments(self):
        result = grammar.arguments.parseString('0xA5, 52')
        self.assertEqual(2, len(result))
        self.assertEqual(ast.ArgumentNode, type(result[0]))
        self.assertEqual(ast.ArgumentNode, type(result[1]))
        self.assertNotEqual(result[0].value, result[1].value)

    def testParseGetValueArg(self):
        arg_node = grammar.get_value_arg.parseString('_word10804')[0]
        self.assertEqual(ast.ARG_TYPE_GET_VALUE_1, arg_node.arg_type)
        self.assertEqual(1004, arg_node.value)
        arg_node = grammar.get_value_arg.parseString('_currentCharacterVariables[6]')[0]
        self.assertEqual(ast.ARG_TYPE_GET_VALUE_1, arg_node.arg_type)
        self.assertEqual(1003, arg_node.value)
        arg_node = grammar.get_value_arg.parseString('_word16F00_characterId')[0]
        self.assertEqual(ast.ARG_TYPE_GET_VALUE_1, arg_node.arg_type)
        self.assertEqual(1002, arg_node.value)
        arg_node = grammar.get_value_arg.parseString('characterIndex')[0]
        self.assertEqual(ast.ARG_TYPE_GET_VALUE_1, arg_node.arg_type)
        self.assertEqual(1001, arg_node.value)
        arg_node = grammar.get_value_arg.parseString('_selectedCharacterId')[0]
        self.assertEqual(ast.ARG_TYPE_GET_VALUE_1, arg_node.arg_type)
        self.assertEqual(1000, arg_node.value)
        arg_node = grammar.get_value_arg.parseString('getValue1(0x2B00)')[0]
        self.assertEqual(ast.ARG_TYPE_GET_VALUE_1, arg_node.arg_type)
        self.assertEqual(0x2B00, arg_node.value)
        arg_node = grammar.get_value_arg.parseString('val(0x2B)')[0]
        self.assertEqual(ast.ARG_TYPE_GET_VALUE_1, arg_node.arg_type)
        self.assertEqual(0x2B, arg_node.value)

    def testParseCompareArg(self):
        arg_node = grammar.compare_arg.parseString('<')[0]
        self.assertEqual(ast.ARG_TYPE_COMPARE_OPERATION, arg_node.arg_type)
        self.assertEqual(ord('<'), arg_node.value)
        arg_node = grammar.compare_arg.parseString('>')[0]
        self.assertEqual(ast.ARG_TYPE_COMPARE_OPERATION, arg_node.arg_type)
        self.assertEqual(ord('>'), arg_node.value)
        arg_node = grammar.compare_arg.parseString('==')[0]
        self.assertEqual(ast.ARG_TYPE_COMPARE_OPERATION, arg_node.arg_type)
        self.assertEqual(ord('='), arg_node.value)

    def testParseComputeArg(self):
        input = '-'
        arg_node = grammar.compute_arg.parseString(input)[0]
        self.assertEqual(ast.ARG_TYPE_COMPUTE_OPERATION, arg_node.arg_type)
        self.assertEqual(ord(input), arg_node.value)
        input = '+'
        arg_node = grammar.compute_arg.parseString(input)[0]
        self.assertEqual(ast.ARG_TYPE_COMPUTE_OPERATION, arg_node.arg_type)
        self.assertEqual(ord(input), arg_node.value)
        input = '*'
        arg_node = grammar.compute_arg.parseString(input)[0]
        self.assertEqual(ast.ARG_TYPE_COMPUTE_OPERATION, arg_node.arg_type)
        self.assertEqual(ord(input), arg_node.value)
        input = '/'
        arg_node = grammar.compute_arg.parseString(input)[0]
        self.assertEqual(ast.ARG_TYPE_COMPUTE_OPERATION, arg_node.arg_type)
        self.assertEqual(ord(input), arg_node.value)
        input = '%'
        arg_node = grammar.compute_arg.parseString(input)[0]
        self.assertEqual(ast.ARG_TYPE_COMPUTE_OPERATION, arg_node.arg_type)
        self.assertEqual(ord(input), arg_node.value)
        input = '='
        arg_node = grammar.compute_arg.parseString(input)[0]
        self.assertEqual(ast.ARG_TYPE_COMPUTE_OPERATION, arg_node.arg_type)
        self.assertEqual(ord(input), arg_node.value)

    def testParsePointArg(self):
        self.fail()

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

    def testParseActionFunctionWithOneImmediateArgAndOneGetValueArg(self):
        result = grammar.action_function.parseString('OC_callScript(0x01, characterIndex)')
        function_node = result[0]
        opcode_val, expected_opcode = opcodes.actionOpCodesLookup['OC_callScript']
        self.assertEqual(expected_opcode, function_node.opcode)
        self.assertEqual(2, len(function_node.arguments))
        argument_node = function_node.arguments[0]
        self.assertEqual(ast.ARG_TYPE_IMMEDIATE_VALUE, argument_node.arg_type)
        self.assertEqual(0x01, argument_node.value)
        argument_node = function_node.arguments[1]
        self.assertEqual(ast.ARG_TYPE_GET_VALUE_1, argument_node.arg_type)
        self.assertEqual(1001, argument_node.value)

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

    def testParseMultipleConditionals(self):
        result = grammar.multiple_conditionals.parseString('OC_CurrentCharacterVar0Equals(0x01) and OC_sub17782(0x2B)')
        conditionals = result['conditionals']
        self.assertEqual(2, len(conditionals))
        self.assertEqual(ast.ConditionalNode, type(conditionals[0]))
        self.assertEqual(ast.ConditionalNode, type(conditionals[1]))

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
        self.assertEqual(1, len(rule_node.actions))
        action_node = rule_node.actions[0]
        self.assertEqual('OC_enableCurrentCharacterScript', action_node.opcode.opName)

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
        self.assertEqual(2, len(rule_node.conditions))
        conditional_node = rule_node.conditions[0]
        self.assertEqual('OC_CurrentCharacterVar0Equals', conditional_node.function.opcode.opName)
        conditional_node = rule_node.conditions[1]
        self.assertEqual('OC_sub17782', conditional_node.function.opcode.opName)
        self.assertEqual(1, len(rule_node.actions))
        action_node = rule_node.actions[0]
        self.assertEqual('OC_enableCurrentCharacterScript', action_node.opcode.opName)

    def testParseRuleWithMultipleConditionalsAndMultipleActions(self):
        input = """
            rule "erules_out_gameScript_8-rule-13"
              when
                OC_compWord16EFE(0x6C) and
                OC_IsCurrentCharacterVar0LessEqualThan(0x52) and
                not OC_sub17782(0x2B)
              then
                OC_setCurrentCharacterVar6(0x1B)
                OC_enableCurrentCharacterScript(0x1E)
            end
        """
        result = grammar.rule.parseString(input)
        rule_node = result[0]
        self.assertEqual('erules_out_gameScript_8-rule-13', rule_node.name)
        self.assertEqual(3, len(rule_node.conditions))
        self.assertEqual('OC_compWord16EFE', rule_node.conditions[0].function.opcode.opName)
        self.assertEqual('OC_IsCurrentCharacterVar0LessEqualThan', rule_node.conditions[1].function.opcode.opName)
        self.assertEqual('OC_sub17782', rule_node.conditions[2].function.opcode.opName)
        self.assertEqual(True, rule_node.conditions[2].negated)
        self.assertEqual(2, len(rule_node.actions))
        self.assertEqual('OC_setCurrentCharacterVar6', rule_node.actions[0].opcode.opName)
        self.assertEqual('OC_enableCurrentCharacterScript', rule_node.actions[1].opcode.opName)

    def testParseRuleWithNoConditionals(self):
        input = """
            rule "erules_out_gameScript_8-rule-26"
              always
                OC_callScript(0x01, characterIndex)
            end
        """
        result = grammar.rule.parseString(input)
        self.assertEqual(1, len(result))
        rule_node = result[0]
        self.assertEqual(0, len(rule_node.conditions))
        self.assertEqual(1, len(rule_node.actions))
        self.assertEqual('OC_callScript', rule_node.actions[0].opcode.opName)

    def testParseMultipleRules(self):
        input = """
            rule "erulesout_gameScript_22-rule-06"
              when
                OC_CurrentCharacterVar0Equals(0x01) and
                OC_sub17782(0x2B)
              then
                OC_enableCurrentCharacterScript(0x00)
            end

            rule "erulesout_gameScript_22-rule-07"
              when
                OC_CurrentCharacterVar0Equals(0x02) and
                OC_sub17782(0x2C)
              then
                OC_enableCurrentCharacterScript(0x01)
            end
        """
        result = grammar.root.parseString(input)
        root_node = result[0]
        self.assertEqual(2, len(root_node.rules))
        self.assertEqual(ast.RuleNode, type(root_node.rules[0]))
        self.assertEqual(ast.RuleNode, type(root_node.rules[1]))
