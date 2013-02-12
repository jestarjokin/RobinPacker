import unittest

import robinpacker.script.ast.elements as ast
import robinpacker.script.parser.grammar as grammar
import robinpacker.script.opcodes as opcodes

class GrammarTest(unittest.TestCase):
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

    def testParseFunctionWithImmediateHexArgument(self):
        result = grammar.function_call.parseString('OC_sub18213(0xA5)')
        function_node = result[0]
        opcode_val, expected_opcode = opcodes.actionOpCodesLookup['OC_sub18213']
        self.assertEqual(expected_opcode, function_node.opcode)
        self.assertEqual(1, len(function_node.arguments))
        argument_node = function_node.arguments[0]
        self.assertEqual(ast.ARG_TYPE_IMMEDIATE_VALUE, argument_node.arg_type)
        self.assertEqual(0xA5, argument_node.value)

#    def testParseFunctionWithImmediateHexArgument(self):
#        result = grammar.function_call.parseString('OC_sub18213(0xA5)')
#        print result