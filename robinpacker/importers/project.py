import json
import logging
import os.path

from robinpacker.util import mkdir, RobinPackerException

class ProjectImporter(object):
    def __init__(self):
        pass

    def importDirectory(self, in_dir, out_dir, options, file_dispatcher):
        logging.info('Packing all game files, from {} to {}'.format(in_dir, out_dir))
        project_fname = os.path.join(in_dir, 'project.json')
        if not os.path.isfile(project_fname):
            raise RobinPackerException('Could not find a "project.json" file in {}.'.format(in_dir))
        mkdir(out_dir)
        with file(os.path.join(in_dir, 'project.json')) as json_file:
            project_info = json.load(json_file)
        for entry in project_info:
            in_fname = os.path.join(in_dir, entry['unpackedFileName'])
            out_fname = os.path.join(out_dir, entry['packedFileName'])
            file_dispatcher.dispatch_file(in_fname, out_fname, options)
