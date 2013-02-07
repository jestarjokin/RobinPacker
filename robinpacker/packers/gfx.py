import array
import struct

def paletteRGB2VGA(val):
    return val >> 2 # VGA palette only uses the lower six bits (64 possible colours)

class GfxRleEncoder(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.repeating_length = 0
        self.repeating_value = None
        self.discrete_values = array.array('B')
        self.output = array.array('B')

    def encodeGfx(self, gfx_data):
        self.reset()
        for i in xrange(len(gfx_data.data)):
            val = gfx_data.data[i]
            next_val = gfx_data.data[i + 1] if i + 1 < len(gfx_data.data) else None

            if next_val != val:
                if self._isRepeatingRun():
                    if (next_val is not None) or self.repeating_value != 0:
                        self.repeating_length += 1
                        self._endRun()
                else:
                    self.discrete_values.append(val)
            else:
                if not self._isRepeatingRun():
                    self._endRun()
                    self.repeating_value = val
                self.repeating_length += 1
        if len(self.discrete_values):
            if self.discrete_values[-1] == 0:
                del self.discrete_values[-1]
            self._endRun()
        self.output.append(0xFF)
        self.output.append(0xFF)
        return self.output

    def _isRepeatingRun(self):
        return self.repeating_length > 0

    def _endRun(self):
        if self._isRepeatingRun():
            self._writeRepeatingRun()
            self.repeating_value = None
            self.repeating_length = 0
        else:
            self._writeDiscreteRun()
            self.discrete_values = array.array('B')

    def _writeRepeatingRun(self):
        while self.repeating_length:
            min_length = min(self.repeating_length, 0x7E)
            self.output.append(min_length | 0x80)
            self.output.append(self.repeating_value)
            self.repeating_length -= min_length

    def _writeDiscreteRun(self):
        length = len(self.discrete_values)
        slice_start = 0
        while length:
            min_length = min(length, 0x7F)
            self.output.append(min_length)
            self.output.extend(self.discrete_values[slice_start:slice_start + min_length])
            length -= min_length
            slice_start += min_length


class GfxBinaryPacker(object):
    def pack(self, gfx_data, output_file_name):
        with file(output_file_name, 'wb') as output_file:
            if gfx_data.metadata.has_palette:
                assert len(gfx_data.palette) == 768
                for i in xrange(len(gfx_data.palette)):
                    val = paletteRGB2VGA(gfx_data.palette[i])
                    output_file.write(struct.pack('B', val))
            rle_encoder = GfxRleEncoder()
            packed_data = rle_encoder.encodeGfx(gfx_data)
            packed_data.tofile(output_file)
