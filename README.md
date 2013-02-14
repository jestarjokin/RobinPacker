RobinPacker
===========

Packs and unpacks game resources for the old DOS game, The Adventures of Robin Hood, by Millenium.

Usage
=====

To unpack rules files:

    robinpacker.py -u ERULES.prg erules_out.json

To convert graphics files to PNG:

    robinpacker.py -u AUTUMN.GFX autumn_out.gfx

To pack rules files:

    robinpacker.py -p erules_out.json erules_packed.prg
  
To convert PNG files back to games graphics:

    robinpacker.py -p autumn_out.png autumn_packed.gfx
