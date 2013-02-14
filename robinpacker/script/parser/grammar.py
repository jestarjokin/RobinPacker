from pyparsing import *

import robinpacker.script.parser.actions as actions

def define_get_value_arg():
    global number
    funky_values = [
        '_word10804',
        '_currentCharacterVariables[6]',
        '_word16F00_characterId',
        'characterIndex',
        '_selectedCharacterId'
    ]
    get_value_arg = (oneOf(funky_values) |
                     (oneOf(['getValue1', 'val']) +
                      Suppress(Literal('(')) +
                      number +
                      Suppress(Literal(')'))
                     )
                    )
    return get_value_arg

def define_point_arg():
    global number
    funky_values = [
        '(_rulesBuffer2_13[currentCharacter], _rulesBuffer2_14[currentCharacter])',
        #'(_vm->_rulesBuffer2_13[{0}], _vm->_rulesBuffer2_14[{0}])',
        '_currentScriptCharacterPosition',
        #'(characterPositionTileX[{0}], characterPositionTileY[{0}])',
        '(characterPositionTileX[_word16F00_characterId], characterPositionTileY[_word16F00_characterId])',
        '(_array10999PosX[currentCharacter], _array109C1PosY[currentCharacter])',
        '(_currentCharacterVariables[4], _currentCharacterVariables[5])',
        #'_vm->_rulesBuffer12Pos3[{0}]',
        '(_characterPositionTileX[_currentCharacterVariables[6]], _characterPositionTileY[_currentCharacterVariables[6]])',
        '_savedMousePosDivided',
        #'(0x{0:02X}, 0x{0:02X})'
    ]
    rules_buffer_2_arg = (
        Suppress(Literal('(')) +
        Literal('_vm->_rulesBuffer2_13') +
        Suppress(Literal('[')) +
        number +
        Suppress(Literal(']')) +
        Suppress(Literal(',')) +
        Literal('_vm->_rulesBuffer2_14') +
        Suppress(Literal('[')) +
        number +
        Suppress(Literal(']')) +
        Suppress(Literal(')'))
    )
    character_pos_arg = (
        Suppress(Literal('(')) +
        Literal('characterPositionTileX') +
        Suppress(Literal('[')) +
        number +
        Suppress(Literal(']')) +
        Suppress(Literal(',')) +
        Literal('characterPositionTileY') +
        Suppress(Literal('[')) +
        number +
        Suppress(Literal(']')) +
        Suppress(Literal(')'))
    )
    rules_buffer_12_arg = (
        Literal('_vm->_rulesBuffer12Pos3') +
        Suppress(Literal('[')) +
        number +
        Suppress(Literal(']'))
        )
    normal_point_arg = (
        Suppress(Literal('(')) +
        number +
        Suppress(Literal(',')) +
        number +
        Suppress(Literal(')'))
    )
    point_arg = oneOf(funky_values) | rules_buffer_2_arg | character_pos_arg | rules_buffer_12_arg | normal_point_arg
    return point_arg


string_value = dblQuotedString.copy()

integer = Word(nums)
hex_number = Suppress(Literal('0x')) + Word(nums + srange('[a-fA-F]'), max=4)
number = hex_number | integer
compare_operator = oneOf(['<', '>', '=='])
compute_operator = oneOf(['-', '+', '*', '/', '%', '='])

immediate_arg = hex_number | integer
get_value_arg = define_get_value_arg()
compare_arg = compare_operator
compute_arg = compute_operator
point_arg = define_point_arg()

argument = (immediate_arg |
    get_value_arg |
    compare_arg |
    compute_arg |
    point_arg
)

arguments = delimitedList(argument)

function_call = Word(alphas, alphanums + '_')('function_name') + Suppress(Literal('(')) + Group(Optional(arguments))('arguments') + Suppress(Literal(')'))
action_function = function_call.copy() # be careful with copy(), looks like copying an expression also recursively copies all sub-expressions. Doesn't apply for elements, though.
conditional = Optional(Keyword('not'))('negated') + function_call

multiple_conditionals = Group(conditional + ZeroOrMore(Suppress(Keyword('and')) + conditional))('conditionals')

rule = (Suppress(Keyword('rule')) + string_value +
        (Suppress(Keyword('always')) |
         (Suppress(Keyword('when')) +
          multiple_conditionals +
          Suppress(Keyword('then'))
         )
        ) + Group(OneOrMore(action_function))('actions') +
        Suppress(Keyword('end'))
)

root = ZeroOrMore(rule)('rules')


# Assign some parse actions
string_value.setParseAction(actions.parse_string)
integer.setParseAction(actions.parse_int)
hex_number.setParseAction(actions.parse_hex)
immediate_arg.setParseAction(actions.parse_immediate_arg)
get_value_arg.setParseAction(actions.parse_get_value_arg)
compare_arg.setParseAction(actions.parse_compare_arg)
compute_arg.setParseAction(actions.parse_compute_arg)
point_arg.setParseAction(actions.parse_point_arg)
action_function.setParseAction(actions.parse_action_function)
conditional.setParseAction(actions.parse_conditional)
rule.setParseAction(actions.parse_rule)
root.setParseAction(actions.parse_root)
