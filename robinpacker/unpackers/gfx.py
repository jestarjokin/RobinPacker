#! /usr/bin/python

import array

from structs.gfx import GfxData

def paletteVGA2RGB(val):
    return val << 2 # VGA palette only uses the lower six bits (64 possible colours)

def readPalette(input_file):
    """ Returns an array of 768 bytes.
    """
    output = array.array('B')
    for i in xrange(768):
        val = paletteVGA2RGB(ord(input_file.read(1)))
        output.append(val)
    return output

def decodeGfx(input_file, max_pos):
    output = array.array('B')
    while True:
        runLength = ord(input_file.read(1))
        if runLength == 0xFF:
            break
        useRLE = runLength & 0x80
        runLength &= 0x7F
        endpos = len(output) + runLength
        if endpos >= max_pos:
            runLength -= endpos
            if not runLength:
                break
        if useRLE:
            val = input_file.read(1)
            for i in xrange(runLength):
                output.append(val)
        else:
            for i in xrange(runLength):
                val = input_file.read(1)
                output.append(val)
    # Fill in pixels until we get to the maximum position.
    while output.tell() < max_pos:
        output.append(0x00)
    return output


class GfxBinaryUnpacker(object):
    def unpack(self, fname, metadata):
        output = GfxData()
        with file(fname, 'rb') as input_file:
            max_pos, has_palette = metadata
            if has_palette:
                output.palette = readPalette(input_file)
            else:
                output.palette = None # TODO: use the default palette
            output.data = decodeGfx(input_file, max_pos)
        return output

