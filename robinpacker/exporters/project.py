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
            '.vga' : '.png'
        }
        file_list = [d for d in os.listdir(in_dir)
            if os.path.isfile(os.path.join(in_dir, d))
            and os.path.splitext(d)[1].lower() in accepted_extensions]
        logging.info('Found the following files to unpack: {}'.format(', '.join(file_list)))
        project_files = []
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
            file_dispatcher.dispatch_args((os.path.join(in_dir, in_fname), os.path.join(out_dir, out_fname)), options)
            project_files.append(
                    {
                    "packedFileName" : in_fname,
                    "unpackedFileName" : out_fname
                }
            )
        json_file_name = os.path.join(out_dir, 'project.json')
        with file(json_file_name, 'w') as json_file:
            json.dump(project_files, json_file, indent=1)
