try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

import robinpacker.script.opcodes as opcodes
from robinpacker.util import pack

class RobinRulesCompiler(object):
    def __init__(self):
        pass

    def _compile_argument(self, argument_node, output):
        pack(output, argument_node.value, '<H')

    def _compile_function(self, function_node, output, is_negated=False):
        opcode = function_node.opcode
        value = opcode.value + 1000 if is_negated else opcode.value
        pack(output, value, '<H')
        assert len(function_node.arguments) == len(opcode.arguments) # should already be validated by the parser.
        for argument_node in function_node.arguments:
            # assume the arguments are the right type; parse should already handle this validation.
            self._compile_argument(argument_node, output)

    def _compile_conditional(self, conditional_node, output):
        self._compile_function(conditional_node.function,
            output,
            is_negated=conditional_node.negated)

    def _compile_rule(self, rule_node, output):
        for conditional_node in rule_node.conditions:
            self._compile_conditional(conditional_node, output)
        pack(output, 0xFFF8, '<H')
        for function_node in rule_node.actions:
            self._compile_function(function_node, output)
        pack(output, 0xFFF7, '<H')

    def compile(self, root_node, output):
        for rule_node in root_node.rules:
            self._compile_rule(rule_node, output)

    def compile_to_string(self, root_node):
        output = StringIO.StringIO()
        self.compile(root_node, output)
        return output.getvalue()


def compile_to_string(root_node):
    compiler = RobinRulesCompiler()
    return compiler.compile_to_string(root_node)
