#! /usr/bin/python
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import os.path
import unittest

import robinpacker.script.disasm as disasm
from robinpacker.structs.parser import StringTable

class ScriptDisassemblerTest(unittest.TestCase):
    def testMenuScripts(self):
        string_map = {
            "PAUSE.GFX" : 354,
            "GALLOWS.GFX" : 79,
            "[[This poor devil is beyond even Robin Hood's help!]It is too late to help this poor creature!]A brave attempt, but once they're dead, there's little you can do!" :355,
            "Um..... No, I am too shy to do that!" : 356,
            "If it's a fight you want, then a fight you shall have!" : 357,
            "Nay sir, I see no reason to fight thee." : 108,
            "Who is this that dares to stare at Robin Hood?!" : 358,
            "Here Sir, have this money as a token that I mean thee no harm." : 359,
            "[Help me someone!!!!!] Down with the Norman pigs!" : 360,
            "Toot! Toot!" : 144,
            "[You're not taking me anywhere!]Get your hands off me, pig!" : 361,
            "[I think I will follow him for a while.]I wonder where he is going." : 362,
            "[The sight of a pretty maid would cheer me greatly. I shall follow her.]I wonder where she is going." : 363,
            "I think I'll follow that animal." : 364,
            "Where is that animal going?" : 365,
            "[Go forth, my merry fellow, and find a wealthy man, that ye might relieve him of his riches for our cause!]Go ye forth sir, and find a man to rob. Bring the spoils back to me, that we might profit from them!" : 366,
            "['Tis time you earned your keep, Sir. Go ye forth and spill the blood of our enemy!]Methinks 'tis time for heads to roll! Go forth and rid this land of another filthy Norman swine!" : 367,
            "SOUL.GFX" : 368,
            "[[Take this!]Have at ye knave!]Have a taste of my knuckles!" : 369,
        }
        string_table = StringTable(string_map)

        with file(os.path.join('data', 'erules_out_menuScripts.dmp'), 'rb') as bytecode_file:
            script = bytecode_file.read()
        output = StringIO.StringIO()
        disasm.disassemble(script, output, 'erules_out_menuScripts', string_table)
        output.seek(0)
        with file(os.path.join('data', 'erules_out_menuScripts.rrs'), 'r') as rules_file:
            while True:
                val1 = rules_file.readline()
                val2 = output.readline()
                self.assertEqual(val1, val2)
                if val1 == '':
                    break
