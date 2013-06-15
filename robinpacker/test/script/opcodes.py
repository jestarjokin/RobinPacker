#! /usr/bin/python
# Use, distribution, and modification of the RobinPacker binaries, source code,
# or documentation, is subject to the terms of the MIT license.
#
# Copyright (c) 2013 Laurence Dougal Myers
#
# http://opensource.org/licenses/MIT

import unittest

import robinpacker.script.argtypes as argtypes
import robinpacker.script.opcodes as opcodes

class OpcodeDocumentationGenerator(unittest.TestCase):
    """This is not what unit tests are for."""
    def testGenerateDocumentation(self):
        print "# Function reference"
        print ""
        print "## Argument types"
        print ""
        print "### Immediate"
        print "{}\n".format(argtypes.ARG_TYPE_LOOKUP[argtypes.IMMEDIATE_VALUE])
        print "This is just an immediate value. Like 43 or 0x23."
        print ""
        print "### Get Value"
        print "{}\n".format(argtypes.ARG_TYPE_LOOKUP[argtypes.GET_VALUE])
        print """Possibly a reference, rather than an immediate value. Can be one of the following:

* `val({0})`
* `getValue1({0})`
* `_word10804`
* `_currentCharacterVariables[6]`
* `_word16F00_characterId`
* `characterIndex`
* `_selectedCharacterId`

Values are limited to 16 bits.
""".format(argtypes.ARG_TYPE_LOOKUP[argtypes.IMMEDIATE_VALUE])
        print "### Point"
        print "{}\n".format(argtypes.ARG_TYPE_LOOKUP[argtypes.POINT_VALUE])
        print """A 2-dimensional point, in the format (x, y). Also a few special values available.

* `({0}, {0})`
* `(_rulesBuffer2_13[currentCharacter], _rulesBuffer2_14[currentCharacter])`
* `(_vm->_rulesBuffer2_13[{0}], _vm->_rulesBuffer2_14[{0}])`
* `_currentScriptCharacterPosition`
* `(characterPositionTileX[{0}], characterPositionTileY[{0}])`
* `(characterPositionTileX[_word16F00_characterId], characterPositionTileY[_word16F00_characterId])`
* `(_array10999PosX[currentCharacter], _array109C1PosY[currentCharacter])`
* `(_currentCharacterVariables[4], _currentCharacterVariables[5])`
* `_vm->_rulesBuffer12Pos3[{0}]`
* `(_characterPositionTileX[_currentCharacterVariables[6]], _characterPositionTileY[_currentCharacterVariables[6]])`
* `_savedMousePosDivided`
""".format(argtypes.ARG_TYPE_LOOKUP[argtypes.IMMEDIATE_VALUE])
        print "### Compare"
        print "{}\n".format(argtypes.ARG_TYPE_LOOKUP[argtypes.COMPARE_OPERATION])
        print """One of:

* `<`
* `>`
* `==`
"""
        print "### Compute"
        print "{}\n".format(argtypes.ARG_TYPE_LOOKUP[argtypes.COMPUTE_OPERATION])
        print """One of:

* `-`
* `+`
* `*`
* `/`
* `%`
* `=`
"""
        print "### String Reference"
        print "{}\n".format(argtypes.ARG_TYPE_LOOKUP[argtypes.STRING_REF])
        print """This is a reference to a string value.

The string value will appear in the script file; however, in the bytecode this gets
translated to an index, to the "strings" array stored in the rules file.

This means strings in the script must exactly match a string in the strings array
in the rules file. You cannot define new strings in the script alone.
"""
        print "## Conditionals"
        for function in opcodes.conditionalOpcodes:
            argument_string = ', '.join(
                map(lambda x: argtypes.ARG_TYPE_LOOKUP[x], function.arguments)
            )
            print "* `{}({})`".format(function.name, argument_string)
        print ""
        print "## Actions"
        for function in opcodes.actionOpcodes:
            argument_string = ', '.join(
                map(lambda x: argtypes.ARG_TYPE_LOOKUP[x], function.arguments)
            )
            print "* `{}({})`".format(function.name, argument_string)
