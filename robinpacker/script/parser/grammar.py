from pyparsing import *

import robinpacker.script.parser.actions as actions

string_value = dblQuotedString.copy()

integer = Word(nums)
hex_number = Suppress(Literal('0x')) + Word(nums + srange('[a-fA-F]'), max=4)
number = hex_number | integer

immediate_arg = number
get_value_arg = None
compare_arg = None
compute_arg = None
point_arg = None

argument = (immediate_arg #|
#    get_value_arg |
#    compare_arg |
#    compute_arg |
#    point_arg
) # TODO

arguments = delimitedList(argument)

function_call = Word(alphas, alphanums + '_')('function_name') + Suppress(Literal('(')) + Group(Optional(arguments))('arguments') + Suppress(Literal(')'))
action_function = function_call.copy()
conditional = Optional(Keyword('not'))('negated') + function_call

multiple_conditionals = Group(conditional + ZeroOrMore(Suppress(Keyword('and')) + conditional))('conditionals')

rule = (Suppress(Keyword('rule')) + string_value +
        Suppress(Keyword('when')) + multiple_conditionals +
        Suppress(Keyword('then')) + Group(OneOrMore(action_function))('actions') +
        Suppress(Keyword('end'))
)

root = ZeroOrMore(rule)('rules')


# Assign some parse actions
string_value.setParseAction(actions.parse_string)
integer.setParseAction(actions.parse_int)
hex_number.setParseAction(actions.parse_hex)
immediate_arg.setParseAction(actions.parse_immediate_arg)
action_function.setParseAction(actions.parse_action_function)
conditional.setParseAction(actions.parse_conditional)
rule.setParseAction(actions.parse_rule)
root.setParseAction(actions.parse_root)
