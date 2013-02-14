import collections

kNone, kImmediateValue, kCompareOperation, kComputeOperation, kGetValue1, kgetPosFromScript = range(6)

OpCode = collections.namedtuple('OpCode', 'opName, numArgs, arg1, arg2, arg3, arg4, arg5')

conditionalOpCodes = (
    OpCode( "OC_checkCharacterGoalPos", 1, kgetPosFromScript, kNone, kNone, kNone, kNone ),
    OpCode( "OC_comparePos", 2, kGetValue1, kgetPosFromScript, kNone, kNone, kNone ),
    OpCode( "OC_checkIsoMap3", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_compareCharacterVariable", 4, kGetValue1, kImmediateValue, kCompareOperation, kImmediateValue, kNone ),
    OpCode( "OC_CompareLastRandomValue", 2, kCompareOperation, kImmediateValue, kNone, kNone, kNone ),
    OpCode( "OC_getRandom", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_for", 2, kImmediateValue, kImmediateValue, kNone, kNone, kNone ),
    OpCode( "OC_compCurrentSpeechId", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_checkSaveFlag", 0, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_compScriptForVal", 2, kCompareOperation, kImmediateValue, kNone, kNone, kNone ),
    OpCode( "OC_sub174D8", 2, kGetValue1, kGetValue1, kNone, kNone, kNone ),
    OpCode( "OC_CompareCharacterVariables", 5, kGetValue1, kImmediateValue, kCompareOperation, kGetValue1, kImmediateValue ),
    OpCode( "OC_compareCoords_1", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_compareCoords_2", 2, kGetValue1, kImmediateValue, kNone, kNone, kNone ),
    OpCode( "OC_CompareDistanceFromCharacterToPositionWith", 3, kgetPosFromScript, kCompareOperation, kImmediateValue, kNone, kNone ),
    OpCode( "OC_compareRandomCharacterId", 3, kGetValue1, kCompareOperation, kImmediateValue, kNone, kNone ),
    OpCode( "OC_IsCurrentCharacterIndex", 1, kGetValue1, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub175C8", 2, kImmediateValue, kGetValue1, kNone, kNone, kNone ),
    OpCode( "OC_sub17640", 2, kImmediateValue, kGetValue1, kNone, kNone, kNone ),
    OpCode( "OC_sub176C4", 2, kImmediateValue, kGetValue1, kNone, kNone, kNone ),
    OpCode( "OC_compWord10804", 1, kGetValue1, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub17766", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub17782", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_CompareMapValueWith", 4, kgetPosFromScript, kImmediateValue, kImmediateValue, kCompareOperation, kNone ),
    OpCode( "OC_IsCharacterValid", 1, kGetValue1, kNone, kNone, kNone, kNone ),
    OpCode( "OC_compWord16EFE", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_AreCurrentCharacterVar0AndVar1EqualsTo", 2, kImmediateValue, kImmediateValue, kNone, kNone, kNone ),
    OpCode( "OC_CurrentCharacterVar0Equals", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_checkLastInterfaceHotspotIndexMenu13", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_checkLastInterfaceHotspotIndexMenu2", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_CompareNumberOfCharacterWithVar0Equals", 3, kImmediateValue, kCompareOperation, kImmediateValue, kNone, kNone ),
    OpCode( "OC_IsPositionInViewport", 1, kgetPosFromScript, kNone, kNone, kNone, kNone ),
    OpCode( "OC_CompareGameVariables", 2, kGetValue1, kGetValue1, kNone, kNone, kNone ),
    OpCode( "OC_skipNextOpcode", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_CurrentCharacterVar2Equals1", 0, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub178D2", 2, kGetValue1, kImmediateValue, kNone, kNone, kNone ),
    OpCode( "OC_CharacterVariableAnd", 3, kGetValue1, kImmediateValue, kImmediateValue, kNone, kNone ),
    OpCode( "OC_IsCurrentCharacterVar0LessEqualThan", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub1790F", 1, kGetValue1, kNone, kNone, kNone, kNone ),
    OpCode( "OC_CurrentCharacterVar1Equals", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_isCurrentCharacterActive", 0, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_CurrentCharacterVar3Equals1", 0, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub1796E", 2, kGetValue1, kImmediateValue, kNone, kNone, kNone ),
    OpCode( "OC_checkLastInterfaceHotspotIndex", 2, kImmediateValue, kImmediateValue, kNone, kNone, kNone ),
    OpCode( "OC_checkSelectedCharacter", 0, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_checkDelayedReactivation", 0, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub179C2", 1, kgetPosFromScript, kNone, kNone, kNone, kNone ),
    OpCode( "OC_checkFunctionKeyPressed", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_checkCodeEntered", 3, kImmediateValue, kImmediateValue, kImmediateValue, kNone, kNone ),
    OpCode( "OC_checkViewPortCharacterTarget", 1, kGetValue1, kNone, kNone, kNone, kNone ),
)
conditionalOpCodesLookup = {opcode.opName : (i, opcode) for i, opcode in enumerate(conditionalOpCodes)}

actionOpCodes = (
    OpCode( "OC_setWord18821", 1, kGetValue1, kNone, kNone, kNone, kNone ),
    OpCode( "OC_ChangeIsoMap", 3, kgetPosFromScript, kImmediateValue, kImmediateValue, kNone, kNone ),
    OpCode( "OC_startSpeech", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_getComputedVariantSpeech", 4, kGetValue1, kImmediateValue, kImmediateValue, kImmediateValue, kNone ),
    OpCode( "OC_getRotatingVariantSpeech", 2, kImmediateValue, kImmediateValue, kNone, kNone, kNone ), # todo
    OpCode( "OC_startSpeechIfMute", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_getComputedVariantSpeechIfMute", 4, kGetValue1, kImmediateValue, kImmediateValue, kImmediateValue, kNone ), # pb
    OpCode( "OC_startSpeechIfSilent", 2, kImmediateValue, kImmediateValue, kNone, kNone, kNone ),
    OpCode( "OC_ComputeCharacterVariable", 4, kGetValue1, kImmediateValue, kComputeOperation, kImmediateValue, kNone ),
    OpCode( "OC_getRandom_type2", 3, kGetValue1, kImmediateValue, kImmediateValue, kNone, kNone ),
    OpCode( "OC_setCharacterPosition", 2, kGetValue1, kgetPosFromScript, kNone, kNone, kNone ),
    OpCode( "OC_DisableCharacter", 1, kGetValue1, kNone, kNone, kNone, kNone ),
    OpCode( "OC_saveAndQuit", 0, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub17B93", 1, kImmediateValue, kNone, kNone, kNone, kNone ), # todo : jump to other opcode
    OpCode( "OC_startSpeech5", 0, kNone, kNone, kNone, kNone, kNone ),  # todo
    OpCode( "OC_resetByte1714E", 0, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_deleteSavegameAndQuit", 0, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_incScriptForVal", 0, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub17BA5", 5, kGetValue1, kImmediateValue,kComputeOperation, kGetValue1, kImmediateValue ),
    OpCode( "OC_setByte18823", 2, kGetValue1, kImmediateValue, kNone, kNone, kNone ),
    OpCode( "OC_callScript", 2, kImmediateValue, kGetValue1, kNone, kNone, kNone ),  # run script
    OpCode( "OC_callScriptAndReturn", 2, kImmediateValue, kGetValue1, kNone, kNone, kNone ),  # run script then stop
    OpCode( "OC_setCurrentScriptCharacterPos", 1, kgetPosFromScript, kNone, kNone, kNone, kNone ),
    OpCode( "OC_initScriptFor", 0, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub17AE1", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub17AEE", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_setWord10804", 1, kGetValue1, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub17C0E", 0, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub17C55", 4, kGetValue1, kGetValue1, kImmediateValue, kImmediateValue, kNone ),
    OpCode( "OC_sub17C76", 1, kGetValue1, kNone, kNone, kNone, kNone ),
    OpCode( "OC_setCurrentCharacter", 1, kGetValue1, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub17C8B", 2, kImmediateValue, kImmediateValue, kNone, kNone, kNone ),
    OpCode( "OC_sub17CA2", 2, kImmediateValue, kImmediateValue, kNone, kNone, kNone ),
    OpCode( "OC_sub17CB9", 3, kImmediateValue, kGetValue1, kImmediateValue, kNone, kNone ),
    OpCode( "OC_sub17CD1", 2, kImmediateValue, kImmediateValue, kNone, kNone, kNone ),
    OpCode( "OC_resetWord16EFE", 0, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_enableCurrentCharacterScript", 1, kImmediateValue, kNone, kNone, kNone, kNone ),   # stop script
    OpCode( "OC_IncCurrentCharacterVar1", 0, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub17D23", 2, kImmediateValue, kgetPosFromScript, kNone, kNone, kNone ),
    OpCode( "OC_sub17E6D", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_changeCurrentCharacterSprite", 2, kImmediateValue, kImmediateValue, kNone, kNone, kNone ),
    OpCode( "OC_sub17E99", 4, kImmediateValue, kImmediateValue, kImmediateValue, kImmediateValue, kNone ),
    OpCode( "OC_sub17EC5", 4, kImmediateValue, kImmediateValue, kImmediateValue, kImmediateValue, kNone ),
    OpCode( "OC_setCharacterDirectionTowardsPos", 1, kgetPosFromScript, kNone, kNone, kNone, kNone ),
    OpCode( "OC_turnCharacterTowardsAnother", 1, kGetValue1, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub17F4F", 1, kGetValue1, kNone, kNone, kNone, kNone ),
    OpCode( "OC_scrollAwayFromCharacter", 0, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_skipNextVal", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_setCurrentCharacterVar6", 1, kGetValue1, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub17FDD", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_setCharacterScriptEnabled", 1, kGetValue1, kNone, kNone, kNone, kNone ),
    OpCode( "OC_setCurrentCharacterVar2", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_SetCurrentCharacterVar2ToZero", 0, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_setCharacterProperties", 5, kGetValue1, kImmediateValue, kImmediateValue, kImmediateValue, kImmediateValue ),
    OpCode( "OC_sub1805D", 5, kGetValue1, kImmediateValue, kImmediateValue, kImmediateValue, kImmediateValue ),
    OpCode( "OC_sub18074", 2, kImmediateValue, kImmediateValue, kNone, kNone, kNone ),
    OpCode( "OC_setCurrentCharacterDirection", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_setInterfaceHotspot", 2, kImmediateValue, kImmediateValue, kNone, kNone, kNone ),
    OpCode( "OC_scrollViewPort", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_setViewPortPos", 1, kgetPosFromScript, kNone, kNone, kNone, kNone ),
    OpCode( "OC_setCurrentCharacterAltitude", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub1817F", 2, kImmediateValue, kImmediateValue, kNone, kNone, kNone ),
    OpCode( "OC_sub181BB", 4, kImmediateValue, kImmediateValue, kImmediateValue, kImmediateValue, kNone ),
    OpCode( "OC_sub18213", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub18252", 1, kGetValue1, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub18260", 2, kGetValue1, kgetPosFromScript, kNone, kNone, kNone ), # TODO
    OpCode( "OC_CharacterVariableAddOrRemoveFlag", 4, kGetValue1, kImmediateValue, kImmediateValue, kImmediateValue, kNone ),
    OpCode( "OC_PaletteFadeOut", 0, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_PaletteFadeIn", 0, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_loadAndDisplayCUBESx_GFX", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_setCurrentCharacterVar3", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_setArray122C1", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub18367", 0, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_enableCharacterScript", 2, kGetValue1, kImmediateValue, kNone, kNone, kNone ),
    OpCode( "OC_setRulesBuffer2Element", 2, kGetValue1, kImmediateValue, kNone, kNone, kNone ),
    OpCode( "OC_setDebugFlag", 0, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_setByte14837", 0, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_waitForEvent", 0, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_disableInterfaceHotspot", 2, kImmediateValue, kImmediateValue, kNone, kNone, kNone ),  # TODO
    OpCode( "OC_loadFileAerial", 1, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_startSpeechIfSoundOff", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub1844A", 2, kGetValue1, kImmediateValue, kNone, kNone, kNone ),
    OpCode( "OC_displayNumericCharacterVariable", 5, kGetValue1, kImmediateValue, kImmediateValue, kImmediateValue, kImmediateValue ),
    OpCode( "OC_displayVGAFile", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_startSpeechWithoutSpeeker", 1, kImmediateValue, kNone, kNone, kNone, kNone ),   # TODO
    OpCode( "OC_displayTitleScreen", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_initGameAreaDisplay", 0, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_displayCharacterStatBar", 6, kGetValue1, kImmediateValue, kImmediateValue, kImmediateValue, kImmediateValue),
    OpCode( "OC_initSmallAnim", 11, kImmediateValue, kImmediateValue, kImmediateValue, kImmediateValue, kImmediateValue ),
    OpCode( "OC_setCharacterHeroismBar", 4, kGetValue1, kImmediateValue, kImmediateValue, kImmediateValue, kNone ),
    OpCode( "OC_sub18690", 2, kGetValue1, kgetPosFromScript, kNone, kNone, kNone ),  #TODO
    OpCode( "OC_setViewPortCharacterTarget", 1, kGetValue1, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub186A1", 3, kGetValue1, kImmediateValue, kImmediateValue, kNone, kNone ),  #TODO
    OpCode( "OC_sub186E5_snd", 2, kGetValue1, kImmediateValue, kNone, kNone, kNone ),
    OpCode( "OC_sub1870A_snd", 2, kgetPosFromScript, kImmediateValue, kNone, kNone, kNone ),
    OpCode( "OC_sub18725_snd", 1, kGetValue1, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub18733_snd", 1, kGetValue1, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub1873F_snd", 1, kgetPosFromScript, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub18746_snd", 1, kImmediateValue, kNone, kNone, kNone, kNone ),
    OpCode( "OC_sub1875D_snd", 0, kNone, kNone, kNone, kNone, kNone ),
    OpCode( "OC_setCharacterMapColor", 2, kGetValue1, kImmediateValue, kNone, kNone, kNone ),
    OpCode( "OC_initGameAreaDisplay", 0, kNone, kNone, kNone, kNone, kNone )
)
actionOpCodesLookup = {opcode.opName : (i, opcode) for i, opcode in enumerate(actionOpCodes)}