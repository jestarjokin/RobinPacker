#! /usr/bin/python
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import struct

from opcodes import *

def unpack(rfile, format):
    result = struct.unpack(format, rfile.read(struct.calcsize(format)))
    return result[0] if len(result) == 1 else result


class ScriptDisassembler(object):
    """Adapted/translated from ScummVM."""
    SCUMMVM_COMPATIBLE, RULES = range(2)

    def __init__(self, output_mode=RULES):
        self.output_mode = output_mode

    def _generate_method_call(self, opCode, script):
        out_str = opCode.opName
        out_str += "("
        for i in xrange(2, 2 + opCode.numArgs):
            opArgType = opCode[min(i, 2 + 4)] # only 5 arg types allowed
            out_str += self._getArgumentString(opArgType, script)
            if i != 2 + opCode.numArgs - 1:
                out_str += ", "
        out_str += ")"
        return out_str

    def _getArgumentString(self, argType, script):
        out_str = ""
        if argType == kImmediateValue:
            out_str = "0x{0:02X}".format(unpack(script, '<H'))
        elif argType == kGetValue1:
            val = unpack(script, '<H')
            if val < 1000:
                out_str = "0x{0:02X}".format(val)
            elif val > 1004:
                out_str = "getValue1(0x{0:02X})".format(val)
            elif val == 1000:
                out_str = "_selectedCharacterId"
            elif val == 1001:
                out_str = "characterIndex"
            elif val == 1002:
                out_str = "_word16F00_characterId"
            elif val == 1003:
                out_str = "_currentCharacterVariables[6]"
            elif val == 1004:
                out_str = "_word10804"
        elif argType == kgetPosFromScript:
            curWord = unpack(script, '<H')
            tmpVal = curWord >> 8
            # switch statement
            if tmpVal == 0xFF:
                out_str = "(_rulesBuffer2_13[currentCharacter],_rulesBuffer2_14[currentCharacter])"
            elif tmpVal == 0xFE:
                index = curWord & 0xFF
                assert 0 <= index < 40
                out_str = "_vm->_rulesBuffer2_13[{0}],_vm->_rulesBuffer2_14[{0}]".format(index)
            elif tmpVal == 0xFD:
                out_str = "_currentScriptCharacterPosition"
            elif tmpVal == 0xFC:
                index = curWord & 0xFF
                assert index < 40
                out_str = "(characterPositionTileX[{0}], characterPositionTileY[{0}])".format(index)
            elif tmpVal == 0xFB:
                out_str = "(characterPositionTileX[_word16F00_characterId], characterPositionTileY[_word16F00_characterId])"
            elif tmpVal == 0xFA:
                out_str = "(_array10999PosX[currentCharacter], _array109C1PosY[currentCharacter])"
            elif tmpVal == 0xF9:
                out_str = "(_currentCharacterVariables[4], _currentCharacterVariables[5])"
            elif tmpVal == 0xF8:
                index = curWord & 0xFF
                assert 0 <= index < 40
                out_str = "_vm->_rulesBuffer12Pos3[{0}]".format(index)
            elif tmpVal == 0xF7:
                out_str = "(_characterPositionTileX[_currentCharacterVariables[6]], _characterPositionTileY[_currentCharacterVariables[6]])"
            elif tmpVal == 0xF6:
                out_str = "_savedMousePosDivided"
            else:
                out_str = "(0x{0:02X},0x{0:02X})".format(curWord >> 8, curWord & 0xFF)
        elif argType == kCompareOperation:
            comp = unpack(script, '<H')
            if comp != ord('<') and comp != ord('>'):
                comp = ord('=')
            out_str = "{0:c}".format(comp)
        elif argType == kComputeOperation:
            comp = unpack(script, '<H')
            out_str = "{0:c}".format(comp)
        return out_str

    def disassemble_scummvm_compatible(self, script, output_file, script_base_name):
        eof = False
        while not eof:
            val = unpack(script, '<H')
            if val == 0xFFF6: # end of script
                return
            hasIf = False
            if val != 0xFFF8:
                hasIf = True
            firstIf = True

            # check the conditions.
            while val != 0xFFF8:
                neg = False
                if val >= 1000:
                    val -= 1000
                    # negative condition
                    neg = True

                # op code type 1
                assert val < len(opCodes1)
                opCode = opCodes1[val]

                if firstIf:
                    out_str = "if ("
                    firstIf = False
                else:
                    out_str = "    and "
                if neg:
                    out_str += "not "

                out_str += self._generate_method_call(opCode, script)

                val = unpack(script, '<H')
                if val == 0xFFF8:
                    out_str += ")"

                output_file.write("{0}\n".format(out_str))

            output_file.write("{ \n")
            val = unpack(script, '<H')
            while val != 0xFFF7:
                # op code type 2
                assert val < len(opCodes2)
                opCode = opCodes2[val]
                out_str = "    "
                out_str += self._generate_method_call(opCode, script)
                out_str += ";"
                output_file.write("{0}\n".format(out_str))
                val = unpack(script, '<H')

            output_file.write("} \n")
            output_file.write(" \n")
        script.close()

    def disassemble_rules(self, script, output_file, script_base_name):
        eof = False
        rule_counter = 0
        while not eof:
            val = unpack(script, '<H')
            if val == 0xFFF6: # end of script
                return

            rule_counter += 1
            output_file.write("rule \"{0}-rule-{1:02d}\"\n".format(script_base_name, rule_counter))
            has_conditions = val != 0xFFF8
            if has_conditions:
                output_file.write("  when\n")

            # check the conditions.
            while val != 0xFFF8:
                out_str = "    "
                is_negative_condition = val >= 1000
                if is_negative_condition:
                    val -= 1000
                    out_str += "not "

                # op code type 1
                assert val < len(opCodes1)
                opCode = opCodes1[val]

                out_str += self._generate_method_call(opCode, script)

                val = unpack(script, '<H')
                if val != 0xFFF8:
                    out_str += " and"

                output_file.write("{0}\n".format(out_str))

            if has_conditions:
                output_file.write("  then\n")
            else:
                output_file.write("  always\n")
            val = unpack(script, '<H')
            while val != 0xFFF7:
                # op code type 2
                assert val < len(opCodes2)
                opCode = opCodes2[val]
                out_str = "    "
                out_str += self._generate_method_call(opCode, script)

                output_file.write("{0}\n".format(out_str))
                val = unpack(script, '<H')

            output_file.write("end\n")
            output_file.write("\n")
        script.close()

    def disassemble(self, script_byte_string, output_file, script_base_name):
        """
        script should be a string of bytes.
        """
        script = StringIO.StringIO(script_byte_string)
        if self.output_mode == self.SCUMMVM_COMPATIBLE:
            return self.disassemble_scummvm_compatible(script, output_file, script_base_name)
        else:
            return self.disassemble_rules(script, output_file, script_base_name)

