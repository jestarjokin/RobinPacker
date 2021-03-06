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

from robinpacker.util import mkdir

class ProjectExporter(object):
    def __init__(self):
        pass

    def export(self, in_dir, out_dir, options, file_dispatcher):
        logging.info('Unpacking all game files, from {} to {}'.format(in_dir, out_dir))
        accepted_extensions = {
            '.prg' : '.json',
            '.gfx' : '.png',
            '.vga' : '.png',
            '.dta' : '.json'
        }
        file_list = (d for d in os.listdir(in_dir)
            if os.path.isfile(os.path.join(in_dir, d))
            and os.path.splitext(d)[1].lower() in accepted_extensions)
        project_files = []
        mkdir(out_dir)
        for in_fname in file_list:
            base, ext = os.path.splitext(in_fname)
            ext = ext.lower()
            out_ext = accepted_extensions[ext]
            out_fname = base + out_ext
            if ext == '.prg':
                mkdir(os.path.join(out_dir, base.lower()))
                out_fname = os.path.join(base.lower(), out_fname)
            elif ext in {'.gfx', '.vga'}:
                mkdir(os.path.join(out_dir, 'images'))
                out_fname = os.path.join('images', out_fname)
            elif ext == '.dta':
                mkdir(os.path.join(out_dir, 'data'))
                out_fname = os.path.join('data', out_fname)
            file_dispatcher.dispatch_file(os.path.join(in_dir, in_fname), os.path.join(out_dir, out_fname), options)
            project_files.append(
                    {
                    "packedFileName" : in_fname,
                    "unpackedFileName" : out_fname
                }
            )
        json_file_name = os.path.join(out_dir, 'project.json')
        with file(json_file_name, 'w') as json_file:
            json.dump(project_files, json_file, indent=1)
