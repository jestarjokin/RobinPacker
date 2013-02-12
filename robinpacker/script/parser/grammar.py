from pyparsing import *

import robinpacker.script.parser.actions as actions

string = dblQuotedString

integer = Word(nums)
hex_number = Suppress(Literal('0x')) + Word(nums + '[a-fA-F]', max=4)
number = hex_number | integer

immediate_arg = number
get_value_arg = None
compare_arg = None
compute_arg = None
point_arg = None

arguments = ZeroOrMore(
    immediate_arg #|
#    get_value_arg |
#    compare_arg |
#    compute_arg |
#    point_arg
) # TODO
function_call = Word(alphas, alphanums + '_')('function_name') + Suppress(Literal('(')) + Group(arguments)('arguments') + Suppress(Literal(')'))
action = function_call
conditional = Optional(Keyword('not'))('negated') + function_call

rule = (Suppress(Keyword('rule')) + string +
        Suppress(Keyword('when')) + conditional +
            ZeroOrMore(Suppress(Keyword('and')) + conditional) +
        Suppress(Keyword('then')) + OneOrMore(action) +
        Suppress(Keyword('end'))
)

expr = ZeroOrMore(rule)
bnf = expr

# Assign some parse actions
integer.setParseAction(actions.parse_int)
hex_number.setParseAction(actions.parse_hex)
immediate_arg.setParseAction(actions.parse_immediate_arg)
function_call.setParseAction(actions.parse_function_call)
