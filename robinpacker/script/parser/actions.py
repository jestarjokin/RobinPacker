import robinpacker.script.ast.elements as ast
import robinpacker.script.opcodes as opcodes

def parse_int(s, loc, toks):
    return int(toks[0])

def parse_hex(s, loc, toks):
    return int(toks[0], 16)

def parse_immediate_arg(s, loc, toks):
    arg_node = ast.ArgumentNode()
    arg_node.arg_type = ast.ARG_TYPE_IMMEDIATE_VALUE
    arg_node.value = toks[0]
    return arg_node

def parse_function_call(s, loc, toks, is_conditional=False):
    function_node = ast.FunctionNode()
    function_name = toks[0]
    args = toks[1]
    opcode_lookup = opcodes.conditionalOpCodesLookup if is_conditional else opcodes.actionOpCodesLookup
    try:
        opcode_value, opcode = opcode_lookup[function_name]
    except KeyError:
        raise NameError('Unknown function call: {}'.format(function_name)) # TODO: custom exception
    if opcode.numArgs != len(args):
        raise TypeError('Invalid number of arguments passed to function "{}". Expected {}, but was passed {}.'.format(
            function_name, opcode.numArgs, len(args)
        )) # TODO: custom exception
    function_node.opcode = opcode
    function_node.arguments = list(args)
    return function_node
