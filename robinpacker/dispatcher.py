#! /usr/bin/python

import collections
import logging
import os.path

from exporters.rules import RulesJsonExporter
from importers.rules import RulesJsonImporter
from packers.rules import RulesBinaryPacker
from unpackers.rules import RulesBinaryUnpacker

from exporters.gfx import GfxPngExporter, GfxJsonExporter
from unpackers.gfx import GfxBinaryUnpacker

GfxMetadata = collections.namedtuple('GfxMetadata', 'max_size, has_palette, width, height')

DEFAULT_GFX_METADATA = GfxMetadata(0xFA00, True, 320, 200)
GFX_METADATA_LOOKUP = {
    "AERIAL.GFX" : GfxMetadata(0xFA00, True, 320, 200),
    "AUTUMN.GFX" : GfxMetadata(0xFA00, True, 320, 200),
    "CREDITS.GFX" : GfxMetadata(0xFA00, True, 320, 200),
    "CUBES0.GFX" : GfxMetadata(0xF000, False, 32, 1920),
    "CUBES1.GFX" : GfxMetadata(0xF000, False, 32, 1920),
    "CUBES2.GFX" : GfxMetadata(0xF000, False, 32, 1920),
    "CUBES3.GFX" : GfxMetadata(0xF000, False, 32, 1920),
    "DYING.GFX" : GfxMetadata(0xFA00, True, 320, 200),
    "FIRE.GFX" : GfxMetadata(0xFA00, True, 320, 200),
    "GALLOWS.GFX" : GfxMetadata(0xFA00, True, 320, 200),
    "IDEOGRAM.VGA" : GfxMetadata(0x6400, False, 16, 1600),
    "ISOCHARS.VGA" : GfxMetadata(0x1000, False, 4, 1024),
    "MEN.VGA" : GfxMetadata(0xF000, False, 16, 3840),
    "MEN2.VGA" : GfxMetadata(0xF000, False, 16, 3840),
    "PAUSE.GFX" : GfxMetadata(0xFA00, True, 320, 200),
    "SCREEN.GFX" : GfxMetadata(0xFA00, True, 320, 200),
    "SOUL.GFX" : GfxMetadata(0xFA00, True, 320, 200),
    "SPRING.GFX" : GfxMetadata(0xFA00, True, 320, 200),
    "SUMMER.GFX" : GfxMetadata(0xFA00, True, 320, 200),
    "TITLE.GFX" : GfxMetadata(0xFA00, True, 320, 200),
    "WINTER.GFX" : GfxMetadata(0xFA00, True, 320, 200),
    "WIZARD.GFX" : GfxMetadata(0xFA00, True, 320, 200),
    "WON1.GFX" : GfxMetadata(0xFA00, True, 320, 200),
    "WON2.GFX" : GfxMetadata(0xFA00, True, 320, 200)
}

class FileDispatcher(object):
    def dispatch_args(self, args, options):
        input_fname = args[0]
        output_fname = args[1]
        if os.path.isdir(input_fname):
            return self.process_directory(input_fname, output_fname,options)
        ext = os.path.splitext(input_fname)[1].lower()
        if ext == '.prg':
            self.process_prg(input_fname, output_fname, options)
        elif ext in ('.gfx', '.vga'):
            self.process_gfx(input_fname, output_fname, options)
#        elif ext == '.vga':
#            self.process_vga(input_fname, output_fname, options)
        # TODO: support for isomap.dta
        else:
            logging.error('Unrecognised extension: %s' % ext)
            raise NotImplementedError()

    def process_prg(self, input_fname, output_fname, options):
        if options.unpack:
            logging.info('Unpacking %s to %s...' % (input_fname, output_fname))
            unpacker = RulesBinaryUnpacker()
            rules = unpacker.unpack(input_fname)
            #exporter = RulesXmlExporter()
            exporter = RulesJsonExporter()
            exporter.export(rules, output_fname)
        elif options.pack:
            logging.info('Packing %s to %s...' % (input_fname, output_fname))
            importer = RulesJsonImporter()
            rules = importer.importFile(input_fname)
            #exporter = RulesJsonExporter()
            #exporter.export(rules, output_fname)
            packer = RulesBinaryPacker()
            packer.pack(rules, output_fname)
        else:
            raise NotImplementedError()

    def process_gfx(self, in_fname, out_fname, options):
        logging.info('Unpacking %s to %s...' % (in_fname, out_fname))
        try:
            image_metadata = GFX_METADATA_LOOKUP[os.path.basename(in_fname).upper()]
        except KeyError:
            logging.error('Unrecognised input image; using default metadata.')
            image_metadata = DEFAULT_GFX_METADATA

        unpacker = GfxBinaryUnpacker()
        gfx_data = unpacker.unpack(in_fname, image_metadata)
        exporter = GfxPngExporter()
        exporter.export(gfx_data, out_fname)
        json_exporter = GfxJsonExporter()
        json_exporter.export(gfx_data, out_fname + '.json')

    def process_directory(self, in_fname, out_fname, options):
        for x, y, z in os.path.walk(in_fname):
            # TODO
            pass
