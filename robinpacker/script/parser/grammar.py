#! /usr/bin/python
# Use, distribution, and modification of the RobinPacker binaries, source code,
# or documentation, is subject to the terms of the MIT license.
#
# Copyright (c) 2013 Laurence Dougal Myers
#
# http://opensource.org/licenses/MIT

from pyparsing import *

class RobinScriptGrammar(object):
    def __init__(self):
        self.initialize_grammar()

    def _define_get_value_arg(self):
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
                          self.number +
                          Suppress(Literal(')'))
                         )
                        )
        return get_value_arg

    def _define_point_arg(self):
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
            self.number +
            Suppress(Literal(']')) +
            Suppress(Literal(',')) +
            Literal('_vm->_rulesBuffer2_14') +
            Suppress(Literal('[')) +
            self.number +
            Suppress(Literal(']')) +
            Suppress(Literal(')'))
        )
        character_pos_arg = (
            Suppress(Literal('(')) +
            Literal('characterPositionTileX') +
            Suppress(Literal('[')) +
            self.number +
            Suppress(Literal(']')) +
            Suppress(Literal(',')) +
            Literal('characterPositionTileY') +
            Suppress(Literal('[')) +
            self.number +
            Suppress(Literal(']')) +
            Suppress(Literal(')'))
        )
        rules_buffer_12_arg = (
            Literal('_vm->_rulesBuffer12Pos3') +
            Suppress(Literal('[')) +
            self.number +
            Suppress(Literal(']'))
            )
        normal_point_arg = (
            Suppress(Literal('(')) +
            self.number +
            Suppress(Literal(',')) +
            self.number +
            Suppress(Literal(')'))
        )
        point_arg = oneOf(funky_values) | rules_buffer_2_arg | character_pos_arg | rules_buffer_12_arg | normal_point_arg
        return point_arg

    def initialize_grammar(self):
        self.comment = pythonStyleComment.copy()
        self.string_value = dblQuotedString.copy()

        self.integer = Word(nums)
        self.hex_number = Suppress(Literal('0x')) + Word(nums + srange('[a-fA-F]'), max=4)
        self.number = self.hex_number | self.integer
        self.compare_operator = oneOf(['<', '>', '=='])
        self.compute_operator = oneOf(['-', '+', '*', '/', '%', '='])

        self.immediate_arg = self.hex_number | self.integer
        self.get_value_arg = self._define_get_value_arg()
        self.compare_arg = self.compare_operator
        self.compute_arg = self.compute_operator
        self.point_arg = self._define_point_arg()
        self.string_ref = self.string_value.copy()

        self.argument = (self.immediate_arg |
                         self.get_value_arg |
                         self.compare_arg |
                         self.compute_arg |
                         self.point_arg |
                         self.string_ref
        )

        self.arguments = delimitedList(self.argument)

        self.function_call = Word(alphas, alphanums + '_')('function_name') + Suppress(Literal('(')) + Group(Optional(self.arguments))('arguments') + Suppress(Literal(')'))
        self.action_function = self.function_call.copy() # be careful with copy(), looks like copying an expression also recursively copies all sub-expressions. Doesn't apply for elements, though.
        self.conditional = Optional(Keyword('not'))('negated') + self.function_call

        self.multiple_conditionals = Group(self.conditional + ZeroOrMore(Suppress(Keyword('and')) + self.conditional))('conditionals')

        self.rule = (Suppress(Keyword('rule')) + self.string_value +
                (Suppress(Keyword('always')) |
                 (Suppress(Keyword('when')) +
                  self.multiple_conditionals +
                  Suppress(Keyword('then'))
                 )
                ) + Group(OneOrMore(self.action_function))('actions') +
                Suppress(Keyword('end'))
        )

        self.root = ZeroOrMore(self.rule)('rules')
        self.root.ignore(self.comment)
