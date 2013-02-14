import robinpacker.script.ast.elements as ast
import robinpacker.script.opcodes as opcodes
from robinpacker.util import RobinScriptError

def parse_string(toks):
    return toks[0][1:-1] # strip leading/trailing quote marks

def parse_int(toks):
    return int(toks[0])

def parse_hex(toks):
    return int(toks[0], 16)

def parse_immediate_arg(toks):
    arg_node = ast.ArgumentNode()
    arg_node.arg_type = ast.ARG_TYPE_IMMEDIATE_VALUE
    arg_node.value = toks[0]
    return arg_node

def parse_action_function(toks):
    function_name = toks[0]
    args = toks[1]
    return __parse_function_call(function_name, args, is_conditional=False)

def parse_conditional(toks):
    conditional_node = ast.ConditionalNode()
    conditional_node.negated = 'negated' in toks
    function_name = toks['function_name']
    args = toks['arguments']
    function_node = __parse_function_call(function_name, args, is_conditional=True)
    conditional_node.function = function_node
    return conditional_node

def __parse_function_call(function_name, args, is_conditional):
    function_node = ast.FunctionNode()
    opcode_lookup = opcodes.conditionalOpCodesLookup if is_conditional else opcodes.actionOpCodesLookup
    try:
        opcode_value, opcode = opcode_lookup[function_name]
    except KeyError:
        raise RobinScriptError('Unknown function call: {}'.format(function_name)) # TODO: custom exception
    if opcode.numArgs != len(args):
        raise RobinScriptError('Invalid number of arguments passed to function "{}". Expected {}, but was passed {}.'.format(
            function_name, opcode.numArgs, len(args)
        )) # TODO: custom exception
    function_node.opcode = opcode
    function_node.arguments = list(args)
    return function_node

def parse_rule(toks):
    rule_node = ast.RuleNode()
    rule_node.name = toks[0]
    try:
        rule_node.conditions = list(toks['conditionals'])
    except KeyError:
        pass # this is for "always" rules, which have no conditionals
    rule_node.actions = toks['actions']
    return rule_node

def parse_root(toks):
    root_node = ast.RootNode()
    try:
        rules = toks['rules']
        root_node.rules = list(rules)
    except KeyError:
        # Allowed to have no rules.
        pass
    return root_node
