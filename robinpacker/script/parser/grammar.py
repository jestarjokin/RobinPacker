from pyparsing import *

import robinpacker.script.parser.actions as actions

def define_get_value_arg():
    global number
    funky_values = [
        '_word10804',
        '_currentCharacterVariables[6]',
        '_word16F00_characterId',
        'characterIndex',
        '_selectedCharacterId',
        #'getValue1(0x{0:02X})',
        #'val(0x{0:02X})'
    ]
    get_value_arg = (oneOf(funky_values) |
                     (oneOf(['getValue1', 'val']) +
                      Suppress(Literal('(')) +
                      number +
                      Suppress(Literal(')'))
                     )
                    )
    return get_value_arg

string_value = dblQuotedString.copy()

integer = Word(nums)
hex_number = Suppress(Literal('0x')) + Word(nums + srange('[a-fA-F]'), max=4)
number = hex_number | integer

immediate_arg = hex_number | integer
get_value_arg = define_get_value_arg()
compare_arg = None
compute_arg = None
point_arg = None

argument = (immediate_arg |
    get_value_arg #|
#    compare_arg |
#    compute_arg |
#    point_arg
) # TODO

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
action_function.setParseAction(actions.parse_action_function)
conditional.setParseAction(actions.parse_conditional)
rule.setParseAction(actions.parse_rule)
root.setParseAction(actions.parse_root)
