#! /usr/bin/python

import logging
import os.path

from exporters.rules import RulesJsonExporter
from importers.rules import RulesJsonImporter
from packers.rules import RulesBinaryPacker
from unpackers.rules import RulesBinaryUnpacker
from unpackers.gfx import GfxBinaryUnpacker

DEFAULT_GFX_METADATA = (0xFA00, True)
GFX_METADATA_LOOKUP = {
    "AERIAL.GFX" : (0xFA00, True),
    "AUTUMN.GFX" : (0xFA00, True),
    "CREDITS.GFX" : (0xFA00, True),
    "CUBES0.GFX" : (0xF000, False),
    "CUBES1.GFX" : (0xF000, False),
    "CUBES2.GFX" : (0xF000, False),
    "CUBES3.GFX" : (0xF000, False),
    "DYING.GFX" : (0xFA00, True),
    "FIRE.GFX" : (0xFA00, True),
    "GALLOWS.GFX" : (0xFA00, True),
    "IDEOGRAM.VGA" : (0x6400, False),
    "ISOCHARS.VGA" : (0x1000, False),
    "MEN.VGA" : (0xF000, False),
    "MEN2.VGA" : (0xF000, False),
    "PAUSE.GFX" : (0xFA00, True),
    "SCREEN.GFX" : (0xFA00, True),
    "SOUL.GFX" : (0xFA00, True),
    "SPRING.GFX" : (0xFA00, True),
    "SUMMER.GFX" : (0xFA00, True),
    "TITLE.GFX" : (0xFA00, True),
    "WINTER.GFX" : (0xFA00, True),
    "WIZARD.GFX" : (0xFA00, True),
    "WON1.GFX" : (0xFA00, True),
    "WON2.GFX" : (0xFA00, True)
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
        elif ext == '.gfx':
            self.process_gfx(input_fname, output_fname, options)
#        elif ext == '.vga':
#            self.process_vga(input_fname, output_fname, options)
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
        unpacker = GfxBinaryUnpacker()
        try:
            image_metadata = GFX_METADATA_LOOKUP[os.path.basename(in_fname).upper()]
        except KeyError:
            logging.error('Unrecognised input image; using default metadata.')
            image_metadata = DEFAULT_GFX_METADATA

        gfx_data = unpacker.unpack(in_fname, image_metadata)


    def process_directory(self, in_fname, out_fname, options):
        for x, y, z in os.path.walk(in_fname):
            # TODO
            pass
