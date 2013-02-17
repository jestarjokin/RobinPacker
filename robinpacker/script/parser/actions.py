import robinpacker.script.ast.elements as ast
import robinpacker.script.argtypes as argtypes
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
    arg_node.arg_type = argtypes.IMMEDIATE_VALUE
    arg_node.value = toks[0]
    return arg_node

def parse_get_value_arg(toks):
    funky_values = {
        '_word10804' : 1004,
        '_currentCharacterVariables[6]' : 1003,
        '_word16F00_characterId' : 1002,
        'characterIndex' : 1001,
        '_selectedCharacterId' : 1000,
    }
    try:
        value = funky_values[toks[0]]
    except KeyError:
        value = toks[1]
    arg_node = ast.ArgumentNode()
    arg_node.arg_type = argtypes.GET_VALUE_1
    arg_node.value = value
    return arg_node

def parse_compare_arg(toks):
    value = toks[0]
    if value == '==':
        value = '='
    value = ord(value)
    arg_node = ast.ArgumentNode()
    arg_node.arg_type = argtypes.COMPARE_OPERATION
    arg_node.value = value
    return arg_node

def parse_compute_arg(toks):
    value = ord(toks[0])
    arg_node = ast.ArgumentNode()
    arg_node.arg_type = argtypes.COMPUTE_OPERATION
    arg_node.value = value
    return arg_node

def parse_point_arg(toks):
    funky_values = {
        '(_rulesBuffer2_13[currentCharacter], _rulesBuffer2_14[currentCharacter])' : 0xFF00,
        '_currentScriptCharacterPosition' : 0xFD00,
        '(characterPositionTileX[_word16F00_characterId], characterPositionTileY[_word16F00_characterId])' : 0xFB00,
        '(_array10999PosX[currentCharacter], _array109C1PosY[currentCharacter])' : 0xFA00,
        '(_currentCharacterVariables[4], _currentCharacterVariables[5])' : 0xF900,
        '(_characterPositionTileX[_currentCharacterVariables[6]], _characterPositionTileY[_currentCharacterVariables[6]])' : 0xF700,
        '_savedMousePosDivided' : 0xF600,
    }
    if len(toks) == 1:
        value = funky_values[toks[0]]
    elif len(toks) == 4:
        if toks[0] == '_vm->_rulesBuffer2_13' and toks[2] == '_vm->_rulesBuffer2_14':
            assert toks[1] == toks[3] # TODO: real exception/validation
            value = 0xFE00 | toks[1]
        elif toks[0] == 'characterPositionTileX' and toks[2] == 'characterPositionTileY':
            assert toks[1] == toks[3]
            value = 0xFC00 | toks[1]
        else:
            raise RobinScriptError('Unrecognised point argument: {}',format(toks))
    elif len(toks) == 2:
        if toks[0] == '_vm->_rulesBuffer12Pos3':
            value = 0xF800 | toks[1]
        else:
            value = ((toks[0] << 8) & 0xFF00) | (toks[1] & 0xFF)
    else:
        raise RobinScriptError('Unrecognised point argument: {}'.format(toks))
    arg_node = ast.ArgumentNode()
    arg_node.arg_type = argtypes.GET_POS_FROM_SCRIPT
    arg_node.value = value
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
    opcode_lookup = opcodes.conditionalOpcodesLookup if is_conditional else opcodes.actionOpcodesLookup
    try:
        opcode = opcode_lookup[function_name]
    except KeyError:
        raise RobinScriptError('Unknown function call: {}'.format(function_name))
    if len(opcode.arguments) != len(args):
        raise RobinScriptError('Invalid number of arguments passed to function "{}". Expected {}, but was passed {}.'.format(
            function_name, len(opcode.arguments), len(args)
        ))
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
