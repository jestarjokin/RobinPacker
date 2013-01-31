#! /usr/bin/python

from collections import OrderedDict
import json


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
    pass
