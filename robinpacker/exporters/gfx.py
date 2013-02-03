#! /usr/bin/python

from collections import OrderedDict
import json
import os.path

try:
    import Image
except ImportError:
    Image = None

class GfxJsonExporter(object):
    def export(self, gfx_data, output_file_name):
        output = OrderedDict()
        output['originalFileName'] = gfx_data.originalFileName
        output['metadata'] = gfx_data.metadata
        with file(output_file_name, 'w') as json_file:
            json.dump(output, json_file, indent=1)


class GfxRawExporter(object):
    def export(self, gfx_data, output_file_name):
        with file(output_file_name + '.act', 'wb') as palette_file:
            gfx_data.palette.tofile(palette_file)
        with file(output_file_name, 'wb') as output_file:
            gfx_data.data.tofile(output_file)


class GfxPngExporter(object):
    def export(self, gfx_data, output_file_name):
        if not Image:
            raise Exception('The Python Imaging Library (PIL) must be installed to save PNG files.') # TODO: use a custom exception
        output = Image.new('P', (gfx_data.metadata.width, gfx_data.metadata.height))
        output.putpalette(gfx_data.palette)
        output.putdata(gfx_data.data)
        if os.path.splitext(output_file_name)[1].lower() != '.png':
            output_file_name += '.png'
        output.save(output_file_name, 'png')
