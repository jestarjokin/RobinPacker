# RobinPacker

Packs and unpacks game resources for the old DOS game, The Adventures of Robin Hood, by Millenium.

RobinPacker is based on work by the ScummVM team to re-implement the Robin Hood engine.

# Installation

* Install Python 2.7. Other versions of Python are not supported!
* Install the following Python packages (I suggest using PIP to do so):
** PyParsing >= 1.5.6
** PIL (Python Imaging Library) >= 1.1.6
* Download the source code and put it somewhere
* Run "robinpacker.py" from the command line (see the "Usage" section for more info)

# Usage

To unpack all game files, pass the game directory as the first argument, and the output directory as the second argument.

    robinpacker.py -u C:\Games\Robin C:\temp\unpacked
    
To re-pack the game files, do the following. Note that a "project.json" file must exist.

    robinpacker.py -p C:\temp\unpacked C:\temp\repacked

To unpack rules files:

    robinpacker.py -u ERULES.prg erules_out.json

To pack rules files:

    robinpacker.py -p erules_out.json erules_packed.prg
    
To convert graphics files to PNG:

    robinpacker.py -u AUTUMN.GFX autumn_out.gfx
  
To convert PNG files back to games graphics:

    robinpacker.py -p autumn_out.png autumn_packed.gfx
    
# Rules Script Format

Scripts are comprised of one or more rules. Each rule looks like the following:

    rule "rule-name"
      when
        <conditionals>
      then
        <actions>
    end

Conditionals are one or more function calls. Each call is separated by the keyword "and". You can negate each conditional by putting "not" at the start.

Actions are also function calls.

Here is an example rule.

    rule "erules_out_gameScript_11-rule-01"
      when
        CurrentCharacterVar0Equals(0x00)
      then
        callScriptAndReturn(0x3A, characterIndex)
    end

There is a special case for rules with no conditionals. Omit the "when" section, and instead of writing the keyword "then", write "always".

    rule "rule-name"
      always
        <actions>
    end

Refer to the section _Function reference_ for a list of functions you can use in conditionals or actions.

Comments are written using the hash symbol, `#`, and will apply to any text after the hash until the end of the line.
This is similar to comments used in the Python programming language.

    # This rule is totally awesome
    rule "erules_out_gameScript_11-rule-01"
      when # when? WHEN? How about NOW!
        CurrentCharacterVar0Equals(0x00) #and
        #sub17782(0x2B)
      then
        callScriptAndReturn(0x3A, characterIndex)
    end

# TODO

* Support for ROBIN.MUS. There's definitely some standard MIDI data in there, but I'm not sure about the structure of the file.
* Separate the rules JSON into more files, maybe one for each logical section extracted.
* Better names for many of the functions in the rules scripts.
* Support for Rome: Pathway to Power (aka Rome: AD 92)

# Support

RobinPacker is available from:

[https://github.com/jestarjokin/RobinPacker/](https://github.com/jestarjokin/RobinPacker/)

Issues/bugs/feature requests can be lodged there.

Feel free to e-mail the author, Laurence Dougal Myers, at jestarjokin@jestarjokin.net

# Function reference

## Argument types

### Immediate
IMMEDIATE_VALUE

This is just an immediate value. Like 43 or 0x23.

### Get Value
GET_VALUE

Possibly a reference, rather than an immediate value. Can be one of the following:

* `val(IMMEDIATE_VALUE)`
* `getValue1(IMMEDIATE_VALUE)`
* `_word10804`
* `_currentCharacterVariables[6]`
* `_word16F00_characterId`
* `characterIndex`
* `_selectedCharacterId`

Values are limited to 16 bits.

### Point
POINT_VALUE

A 2-dimensional point, in the format (x, y). Also a few special values available.

* `(IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `(_rulesBuffer2_13[currentCharacter], _rulesBuffer2_14[currentCharacter])`
* `(_vm->_rulesBuffer2_13[IMMEDIATE_VALUE], _vm->_rulesBuffer2_14[IMMEDIATE_VALUE])`
* `_currentScriptCharacterPosition`
* `(characterPositionTileX[IMMEDIATE_VALUE], characterPositionTileY[IMMEDIATE_VALUE])`
* `(characterPositionTileX[_word16F00_characterId], characterPositionTileY[_word16F00_characterId])`
* `(_array10999PosX[currentCharacter], _array109C1PosY[currentCharacter])`
* `(_currentCharacterVariables[4], _currentCharacterVariables[5])`
* `_vm->_rulesBuffer12Pos3[IMMEDIATE_VALUE]`
* `(_characterPositionTileX[_currentCharacterVariables[6]], _characterPositionTileY[_currentCharacterVariables[6]])`
* `_savedMousePosDivided`

### Compare
COMPARE_OPERATION

One of:

* `<`
* `>`
* `==`

### Compute
COMPUTE_OPERATION

One of:

* `-`
* `+`
* `*`
* `/`
* `%`
* `=`

### String Reference
STRING_REF

This is a reference to a string value.

The string value will appear in the script file; however, in the bytecode this gets
translated to an index, to the "strings" array stored in the rules file.

This means strings in the script must exactly match a string in the strings array
in the rules file. You cannot define new strings in the script alone.

## Conditionals
* `checkCharacterGoalPos(POINT_VALUE)`
* `comparePos(GET_VALUE, POINT_VALUE)`
* `checkIsoMap3(IMMEDIATE_VALUE)`
* `compareCharacterVariable(GET_VALUE, IMMEDIATE_VALUE, COMPARE_OPERATION, IMMEDIATE_VALUE)`
* `CompareLastRandomValue(COMPARE_OPERATION, IMMEDIATE_VALUE)`
* `getRandom(IMMEDIATE_VALUE)`
* `for(IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `compCurrentSpeechId(STRING_REF)`
* `checkSaveFlag()`
* `compScriptForVal(COMPARE_OPERATION, IMMEDIATE_VALUE)`
* `sub174D8(GET_VALUE, GET_VALUE)`
* `CompareCharacterVariables(GET_VALUE, IMMEDIATE_VALUE, COMPARE_OPERATION, GET_VALUE, IMMEDIATE_VALUE)`
* `compareCoords_1(IMMEDIATE_VALUE)`
* `compareCoords_2(GET_VALUE, IMMEDIATE_VALUE)`
* `CompareDistanceFromCharacterToPositionWith(POINT_VALUE, COMPARE_OPERATION, IMMEDIATE_VALUE)`
* `compareRandomCharacterId(GET_VALUE, COMPARE_OPERATION, IMMEDIATE_VALUE)`
* `IsCurrentCharacterIndex(GET_VALUE)`
* `sub175C8(IMMEDIATE_VALUE, GET_VALUE)`
* `sub17640(IMMEDIATE_VALUE, GET_VALUE)`
* `sub176C4(IMMEDIATE_VALUE, GET_VALUE)`
* `compWord10804(GET_VALUE)`
* `sub17766(IMMEDIATE_VALUE)`
* `sub17782(IMMEDIATE_VALUE)`
* `CompareMapValueWith(POINT_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, COMPARE_OPERATION)`
* `IsCharacterValid(GET_VALUE)`
* `compWord16EFE(IMMEDIATE_VALUE)`
* `AreCurrentCharacterVar0AndVar1EqualsTo(IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `CurrentCharacterVar0Equals(IMMEDIATE_VALUE)`
* `checkLastInterfaceHotspotIndexMenu13(IMMEDIATE_VALUE)`
* `checkLastInterfaceHotspotIndexMenu2(IMMEDIATE_VALUE)`
* `CompareNumberOfCharacterWithVar0Equals(IMMEDIATE_VALUE, COMPARE_OPERATION, IMMEDIATE_VALUE)`
* `IsPositionInViewport(POINT_VALUE)`
* `CompareGameVariables(GET_VALUE, GET_VALUE)`
* `skipNextOpcode(IMMEDIATE_VALUE)`
* `CurrentCharacterVar2Equals1()`
* `sub178D2(GET_VALUE, IMMEDIATE_VALUE)`
* `CharacterVariableAnd(GET_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `IsCurrentCharacterVar0LessEqualThan(IMMEDIATE_VALUE)`
* `sub1790F(GET_VALUE)`
* `CurrentCharacterVar1Equals(IMMEDIATE_VALUE)`
* `isCurrentCharacterActive()`
* `CurrentCharacterVar3Equals1()`
* `sub1796E(GET_VALUE, IMMEDIATE_VALUE)`
* `checkLastInterfaceHotspotIndex(IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `checkSelectedCharacter()`
* `checkDelayedReactivation()`
* `sub179C2(POINT_VALUE)`
* `checkFunctionKeyPressed(IMMEDIATE_VALUE)`
* `checkCodeEntered(IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `checkViewPortCharacterTarget(GET_VALUE)`

## Actions
* `setWord18821(GET_VALUE)`
* `ChangeIsoMap(POINT_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `startSpeech(STRING_REF)`
* `getComputedVariantSpeech(GET_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, STRING_REF)`
* `getRotatingVariantSpeech(STRING_REF, IMMEDIATE_VALUE)`
* `startSpeechIfMute(STRING_REF)`
* `getComputedVariantSpeechIfMute(GET_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, STRING_REF)`
* `startSpeechIfSilent(STRING_REF, IMMEDIATE_VALUE)`
* `ComputeCharacterVariable(GET_VALUE, IMMEDIATE_VALUE, COMPUTE_OPERATION, IMMEDIATE_VALUE)`
* `getRandom_type2(GET_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `setCharacterPosition(GET_VALUE, POINT_VALUE)`
* `DisableCharacter(GET_VALUE)`
* `saveAndQuit()`
* `sub17B93(IMMEDIATE_VALUE)`
* `startSpeech5()`
* `resetByte1714E()`
* `deleteSavegameAndQuit()`
* `incScriptForVal()`
* `sub17BA5(GET_VALUE, IMMEDIATE_VALUE, COMPUTE_OPERATION, GET_VALUE, IMMEDIATE_VALUE)`
* `setByte18823(GET_VALUE, IMMEDIATE_VALUE)`
* `callScript(IMMEDIATE_VALUE, GET_VALUE)`
* `callScriptAndReturn(IMMEDIATE_VALUE, GET_VALUE)`
* `setCurrentScriptCharacterPos(POINT_VALUE)`
* `initScriptFor()`
* `sub17AE1(IMMEDIATE_VALUE)`
* `sub17AEE(IMMEDIATE_VALUE)`
* `setWord10804(GET_VALUE)`
* `sub17C0E()`
* `sub17C55(GET_VALUE, GET_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `sub17C76(GET_VALUE)`
* `setCurrentCharacter(GET_VALUE)`
* `sub17C8B(IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `sub17CA2(IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `sub17CB9(IMMEDIATE_VALUE, GET_VALUE, IMMEDIATE_VALUE)`
* `sub17CD1(IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `resetWord16EFE()`
* `enableCurrentCharacterScript(IMMEDIATE_VALUE)`
* `IncCurrentCharacterVar1()`
* `sub17D23(IMMEDIATE_VALUE, POINT_VALUE)`
* `sub17E6D(IMMEDIATE_VALUE)`
* `changeCurrentCharacterSprite(IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `sub17E99(IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `sub17EC5(IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `setCharacterDirectionTowardsPos(POINT_VALUE)`
* `turnCharacterTowardsAnother(GET_VALUE)`
* `sub17F4F(GET_VALUE)`
* `scrollAwayFromCharacter()`
* `skipNextVal(IMMEDIATE_VALUE)`
* `setCurrentCharacterVar6(GET_VALUE)`
* `sub17FDD(IMMEDIATE_VALUE)`
* `setCharacterScriptEnabled(GET_VALUE)`
* `setCurrentCharacterVar2(IMMEDIATE_VALUE)`
* `SetCurrentCharacterVar2ToZero()`
* `setCharacterProperties(GET_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `sub1805D(GET_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `sub18074(IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `setCurrentCharacterDirection(IMMEDIATE_VALUE)`
* `setInterfaceHotspot(IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `scrollViewPort(IMMEDIATE_VALUE)`
* `setViewPortPos(POINT_VALUE)`
* `setCurrentCharacterAltitude(IMMEDIATE_VALUE)`
* `sub1817F(IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `sub181BB(IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `sub18213(IMMEDIATE_VALUE)`
* `sub18252(GET_VALUE)`
* `sub18260(GET_VALUE, POINT_VALUE)`
* `CharacterVariableAddOrRemoveFlag(GET_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `PaletteFadeOut()`
* `PaletteFadeIn()`
* `loadAndDisplayCUBESx_GFX(IMMEDIATE_VALUE)`
* `setCurrentCharacterVar3(IMMEDIATE_VALUE)`
* `setArray122C1(IMMEDIATE_VALUE)`
* `sub18367()`
* `enableCharacterScript(GET_VALUE, IMMEDIATE_VALUE)`
* `setRulesBuffer2Element(GET_VALUE, IMMEDIATE_VALUE)`
* `setDebugFlag()`
* `setByte14837()`
* `waitForEvent()`
* `disableInterfaceHotspot(IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `loadFileAerial()`
* `startSpeechIfSoundOff(STRING_REF)`
* `sub1844A(GET_VALUE, IMMEDIATE_VALUE)`
* `displayNumericCharacterVariable(GET_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `displayVGAFile(STRING_REF)`
* `startSpeechWithoutSpeaker(STRING_REF)`
* `displayTitleScreen(IMMEDIATE_VALUE)`
* `initGameAreaDisplay()`
* `displayCharacterStatBar(GET_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `initSmallAnim(IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `setCharacterHeroismBar(GET_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `sub18690(GET_VALUE, POINT_VALUE)`
* `setViewPortCharacterTarget(GET_VALUE)`
* `sub186A1(GET_VALUE, IMMEDIATE_VALUE, IMMEDIATE_VALUE)`
* `sub186E5_snd(GET_VALUE, IMMEDIATE_VALUE)`
* `sub1870A_snd(POINT_VALUE, IMMEDIATE_VALUE)`
* `sub18725_snd(GET_VALUE)`
* `sub18733_snd(GET_VALUE)`
* `sub1873F_snd(POINT_VALUE)`
* `sub18746_snd(IMMEDIATE_VALUE)`
* `sub1875D_snd()`
* `setCharacterMapColor(GET_VALUE, IMMEDIATE_VALUE)`
* `initGameAreaDisplay2()`