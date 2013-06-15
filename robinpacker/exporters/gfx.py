#! /usr/bin/python

from collections import OrderedDict
import json
import os.path

try:
    from PIL import Image
except ImportError:
    try:
        import Image
    except ImportError:
        Image = None

from robinpacker.util import RobinPackerException

class GfxJsonExporter(object):
    def export(self, gfx_data, output_file_name):
        output = OrderedDict()
        output['__json_type__'] = 'gfx' # a bit gross, might need to put it in a wrapper dict
        output['__type__'] = 'GfxData'
        output['original_file_name'] = gfx_data.original_file_name
        metadata = OrderedDict()
        metadata['__type__'] = 'GfxMetadata'
        metadata['max_size'] = gfx_data.metadata.max_size
        metadata['has_palette'] = gfx_data.metadata.has_palette
        metadata['width'] = gfx_data.metadata.width
        metadata['height'] = gfx_data.metadata.height
        output['metadata'] = metadata
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
            raise RobinPackerException('The Python Imaging Library (PIL) must be installed to save PNG files.')
        output = Image.new('P', (gfx_data.metadata.width, gfx_data.metadata.height))
        output.putpalette(gfx_data.palette)
        output.putdata(gfx_data.data)
        if os.path.splitext(output_file_name)[1].lower() != '.png':
            output_file_name += '.png'
        output.save(output_file_name, 'png')
