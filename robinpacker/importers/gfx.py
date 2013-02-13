#! /usr/bin/python
import array
import json

try:
    import Image
except ImportError:
    Image = None

import robinpacker.structs.gfx

class GfxJsonImporter(object):
    def importFile(self, json_file_name, gfx_data=None):
        def decode_objects(dct):
            try:
                type_val = dct['__type__']
            except KeyError:
                return dct
            if type_val == 'GfxData':
                gfx_data = robinpacker.structs.gfx.GfxData()
                gfx_data.original_file_name = dct['original_file_name']
                gfx_data.metadata = dct['metadata']
                return gfx_data
            elif type_val == 'GfxMetadata':
                metadata = robinpacker.structs.gfx.GfxMetadata(
                    dct['max_size'], dct['has_palette'], dct['width'], dct['height'])
                return metadata
        with file(json_file_name, 'r') as json_file:
            gfx_data = json.load(json_file, object_hook=decode_objects)
        return gfx_data


class GfxRawImporter(object):
    def importFile(self, input_file_name, gfx_data=None):
        if gfx_data is None:
            gfx_data = robinpacker.structs.gfx.GfxData()
        with file(input_file_name, 'rb') as raw_file:
            gfx_data.data = array.array('B')
            gfx_data.fromfile(raw_file)
        # Always import the palette file, even if the output GFX/VGA
        #  file doesn't include the palette.
        with file(input_file_name + '.act', 'rb') as palette_file:
            gfx_data.palette = array.array('B')
            gfx_data.fromfile(palette_file)


class GfxPngImporter(object):
    def importFile(self, input_file_name, gfx_data=None):
        if Image is None:
            raise Exception('The Python Imaging Library (PIL) must be installed to load PNG files.') # TODO: use a custom exception
        png_data = Image.open(input_file_name)
        if png_data.palette is None or png_data.mode != 'P':
            raise Exception('Input images must have a 256-colour palette. 16/24/32-bit images are not supported.')
        if gfx_data is None:
            gfx_data = robinpacker.structs.gfx.GfxData()
        gfx_data.palette = array.array('B', png_data.palette.palette)
        gfx_data.data = array.array('B', png_data.getdata())

        del png_data
        return gfx_data
