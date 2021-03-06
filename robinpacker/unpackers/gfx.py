#! /usr/bin/python
# Use, distribution, and modification of the RobinPacker binaries, source code,
# or documentation, is subject to the terms of the MIT license.
#
# Copyright (c) 2013 Laurence Dougal Myers
#
# http://opensource.org/licenses/MIT

import array
import os.path

from robinpacker.structs.gfx import GfxData

DEFAULT_PALETTE = array.array('B', [0, 0, 0, 0, 0, 168, 0, 168, 0, 0, 168, 168, 168, 0, 0, 168, 0, 168, 168, 84, 0, 168, 168, 168, 84, 84, 84, 84, 84, 252, 84, 252, 84, 84, 252, 252, 252, 84, 84, 252, 84, 252, 252, 252, 84, 252, 252, 252, 252, 252, 252, 236, 236, 236, 216, 216, 216, 200, 200, 200, 184, 184, 184, 168, 168, 168, 152, 152, 152, 132, 132, 132, 116, 116, 116, 100, 100, 100, 84, 84, 84, 68, 68, 68, 52, 52, 52, 32, 32, 32, 16, 16, 16, 0, 0, 0, 252, 216, 216, 252, 184, 184, 252, 156, 156, 252, 124, 124, 252, 92, 92, 252, 64, 64, 252, 32, 32, 252, 0, 0, 228, 0, 0, 204, 0, 0, 180, 0, 0, 156, 0, 0, 132, 0, 0, 112, 0, 0, 88, 0, 0, 64, 0, 0, 252, 232, 216, 252, 216, 184, 252, 200, 156, 252, 184, 124, 252, 168, 92, 252, 152, 64, 252, 136, 32, 252, 120, 0, 228, 108, 0, 204, 96, 0, 180, 84, 0, 156, 76, 0, 132, 64, 0, 112, 56, 0, 88, 44, 0, 64, 32, 0, 252, 252, 216, 252, 252, 184, 252, 252, 156, 252, 252, 124, 252, 248, 92, 252, 244, 64, 252, 244, 32, 252, 244, 0, 228, 216, 0, 204, 196, 0, 180, 172, 0, 156, 156, 0, 132, 132, 0, 112, 108, 0, 88, 84, 0, 64, 64, 0, 248, 252, 216, 236, 244, 188, 224, 236, 168, 212, 232, 144, 200, 224, 128, 188, 216, 104, 176, 208, 88, 164, 200, 68, 144, 184, 56, 128, 168, 44, 112, 148, 32, 96, 132, 24, 80, 116, 16, 64, 100, 8, 52, 80, 4, 40, 64, 0, 216, 252, 216, 192, 244, 192, 172, 236, 172, 152, 232, 152, 132, 224, 132, 116, 216, 116, 100, 208, 96, 84, 200, 80, 64, 184, 64, 56, 168, 52, 40, 148, 36, 32, 132, 28, 24, 116, 16, 16, 100, 8, 8, 80, 4, 4, 64, 0, 236, 252, 252, 212, 252, 252, 188, 248, 252, 164, 244, 248, 140, 240, 248, 120, 236, 248, 96, 228, 248, 72, 220, 248, 80, 208, 224, 60, 188, 200, 44, 168, 180, 32, 148, 156, 20, 128, 132, 12, 108, 108, 4, 88, 88, 0, 64, 64, 216, 236, 252, 184, 224, 252, 156, 212, 252, 124, 200, 252, 92, 188, 252, 64, 176, 252, 32, 168, 252, 0, 156, 252, 0, 140, 228, 0, 124, 204, 0, 108, 180, 0, 92, 156, 0, 76, 132, 0, 64, 112, 0, 48, 88, 0, 36, 64, 216, 216, 252, 184, 188, 252, 156, 156, 252, 124, 128, 252, 92, 96, 252, 64, 64, 252, 32, 36, 252, 0, 4, 252, 0, 4, 228, 0, 4, 204, 0, 0, 180, 0, 0, 156, 0, 0, 132, 0, 0, 112, 0, 0, 88, 0, 0, 64, 216, 252, 216, 188, 252, 184, 156, 252, 156, 128, 252, 124, 96, 252, 92, 64, 252, 64, 32, 252, 32, 0, 252, 0, 0, 224, 0, 0, 196, 0, 0, 172, 0, 0, 144, 0, 0, 120, 0, 0, 92, 0, 0, 64, 0, 0, 40, 0, 252, 216, 252, 252, 184, 252, 252, 156, 252, 252, 124, 252, 252, 92, 252, 252, 64, 252, 252, 32, 252, 252, 0, 252, 224, 0, 228, 200, 0, 204, 180, 0, 180, 156, 0, 156, 132, 0, 132, 108, 0, 112, 88, 0, 88, 64, 0, 64, 252, 232, 220, 252, 224, 208, 252, 216, 196, 252, 212, 188, 252, 204, 176, 252, 196, 164, 252, 188, 156, 252, 184, 144, 252, 176, 128, 252, 164, 112, 252, 156, 96, 240, 148, 92, 232, 140, 88, 220, 136, 84, 208, 128, 80, 200, 124, 76, 188, 120, 72, 180, 112, 68, 168, 104, 64, 160, 100, 60, 156, 96, 56, 144, 92, 52, 136, 88, 48, 128, 80, 44, 116, 76, 40, 108, 72, 36, 92, 64, 32, 84, 60, 28, 72, 56, 24, 64, 48, 24, 56, 44, 20, 40, 32, 12, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252])

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

def decodeGfx(input_file, max_size):
    output = array.array('B')
    while True:
        runLength = ord(input_file.read(1))
        if runLength == 0xFF:
            break
        useRLE = runLength & 0x80
        runLength &= 0x7F
        endpos = len(output) + runLength
        if endpos >= max_size:
            runLength -= endpos
            if not runLength:
                break
        if useRLE:
            val = ord(input_file.read(1))
            for i in xrange(runLength):
                output.append(val)
        else:
            for i in xrange(runLength):
                val = ord(input_file.read(1))
                output.append(val)
    # Fill in pixels until we get to the maximum position.
    while len(output) < max_size:
        output.append(0x00)
    return output


class GfxBinaryUnpacker(object):
    def unpack(self, fname, metadata):
        output = GfxData()
        with file(fname, 'rb') as input_file:
            if metadata.has_palette:
                output.palette = readPalette(input_file)
            else:
                output.palette = DEFAULT_PALETTE
            output.data = decodeGfx(input_file, metadata.max_size)
        output.metadata = metadata
        output.original_file_name = os.path.basename(fname)
        return output
