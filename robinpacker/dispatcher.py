#! /usr/bin/python
# Use, distribution, and modification of the RobinPacker binaries, source code,
# or documentation, is subject to the terms of the MIT license.
#
# Copyright (c) 2013 Laurence Dougal Myers
#
# http://opensource.org/licenses/MIT

import json
import logging
import os

from exporters.project import ProjectExporter
from importers.project import ProjectImporter
from exporters.rules import RulesJsonExporter
from importers.rules import RulesJsonImporter
from packers.rules import RulesBinaryPacker
from unpackers.rules import RulesBinaryUnpacker
from exporters.gfx import GfxPngExporter, GfxJsonExporter
from importers.gfx import GfxPngImporter, GfxJsonImporter
from packers.gfx import GfxBinaryPacker
from unpackers.gfx import GfxBinaryUnpacker
from structs.gfx import GfxMetadata
from unpackers.simple import ArrayBinaryUnpacker
from exporters.simple import ArrayJsonExporter
from packers.simple import ArrayBinaryPacker
from importers.simple import ArrayJsonImporter
from util import RobinPackerException, RobinPackerJsonIdentified

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
    def __init__(self):
        self.json_type_dispatch = {
            'rules' : self.process_prg,
            'gfx' : self.process_gfx,
            #'dta' : self.process_dta,
            'array' : self.process_dta # hmm
            #'project' : self.process_project
        }

    def dispatch_args(self, args, options):
        input_fname = args[0]
        output_fname = args[1]
        self.dispatch_file(input_fname, output_fname, options)

    def dispatch_file(self, input_fname, output_fname, options):
        if os.path.isdir(input_fname):
            self.process_directory(input_fname, output_fname, options)
        else:
            ext = os.path.splitext(input_fname)[1].lower()
            if ext in ('.json'):
                self.dispatch_json(input_fname, output_fname, options)
            elif ext in ('.prg'):
                self.process_prg(input_fname, output_fname, options)
            elif ext in ('.gfx', '.vga', '.png', '.raw'):
                self.process_gfx(input_fname, output_fname, options)
            # TODO: support for isomap.dta
            elif ext in ('.dta'):
                self.process_dta(input_fname, output_fname, options)
            # TODO: support for sound data
            else:
                logging.error('Unrecognised extension: %s' % ext)
                raise NotImplementedError()

    def process_prg(self, input_fname, output_fname, options):
        if options.unpack:
            logging.info('Unpacking %s to %s...' % (input_fname, output_fname))
            unpacker = RulesBinaryUnpacker()
            rules = unpacker.unpack(input_fname)
            exporter = RulesJsonExporter(options.dump_scripts)
            exporter.export(rules, output_fname)
        elif options.pack:
            logging.info('Packing %s to %s...' % (input_fname, output_fname))
            importer = RulesJsonImporter()
            rules = importer.import_file(input_fname)
            packer = RulesBinaryPacker()
            packer.pack(rules, output_fname)
        else:
            raise NotImplementedError()

    def process_gfx(self, in_fname, out_fname, options):
        if options.unpack:
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
        else:
            logging.info('Packing %s to %s...' % (in_fname, out_fname))
            json_importer = GfxJsonImporter()
            gfx_data = json_importer.import_file(in_fname + '.json')
            importer = GfxPngImporter()
            gfx_data = importer.import_file(in_fname, gfx_data)
            packer = GfxBinaryPacker()
            packer.pack(gfx_data, out_fname)

    def process_directory(self, in_dir, out_dir, options):
        if options.unpack:
            exporter = ProjectExporter()
            exporter.export(in_dir, out_dir, options, self)
        else:
            importer = ProjectImporter()
            importer.import_directory(in_dir, out_dir, options, self)

    def process_dta(self, input_fname, output_fname, options):
        if options.unpack:
            logging.info('Unpacking %s to %s...' % (input_fname, output_fname))
            unpacker = ArrayBinaryUnpacker()
            array_data = unpacker.unpack(input_fname)
            exporter = ArrayJsonExporter()
            exporter.export(array_data, output_fname)
        else:
            logging.info('Packing %s to %s...' % (input_fname, output_fname))
            importer = ArrayJsonImporter()
            array_data = importer.import_file(input_fname)
            packer = ArrayBinaryPacker()
            packer.pack(array_data, output_fname)

    def dispatch_json(self, input_fname, output_fname, options):
        if options.unpack:
            raise RobinPackerException('Tried to dispatch a JSON file when unpacking! HOW?! "{}"'.format(
                input_fname
            ))
        else:
            detector = JsonTypeDetector()
            json_type = detector.detect_json_type(input_fname)
            self.json_type_dispatch[json_type](input_fname, output_fname, options)


class JsonTypeDetector(object):
    def __init__(self):
        pass

    def detect_json_type(self, json_file_name):
        with file(json_file_name, 'r') as json_file:
            try:
                # TODO: I believe this still loads the entire file into memory first.
                # Need some way of quickly "peeking" into the JSON file, probably involves
                # writing a custom decoder and/or scanner.
                json.load(json_file, object_hook=self._decode_objects)
            except RobinPackerJsonIdentified, e:
                return e.json_type_string
        raise RobinPackerException('Could not identify the type of JSON in file "{}".'.format(
            json_file_name
        ))

    def _decode_objects(self, dct):
        try:
            json_type = dct['__json_type__']
            raise RobinPackerJsonIdentified(json_type)
        except KeyError:
            return dct
