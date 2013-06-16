#! /usr/bin/python
# Use, distribution, and modification of the RobinPacker binaries, source code,
# or documentation, is subject to the terms of the MIT license.
#
# Copyright (c) 2013 Laurence Dougal Myers
#
# http://opensource.org/licenses/MIT

from distutils.core import setup
import logging
import os
from pkgutil import walk_packages
import shutil
import subprocess
import py2exe

import robinpacker

directories_to_remove = [
    'dist',
    'build',
    '_temp'
]
for dir in directories_to_remove:
    try:
        shutil.rmtree(dir)
    except Exception:
        pass

APP_NAME = 'RobinPacker'
APP_VERSION = '1.0'
APP_DESCRIPTION = 'Packs/unpacks game resources for "The Adventures of Robin Hood" by Millenium Interactive.'

data_files = [
    ('', ['README.md']),
    ('docs', ['docs/LICENSE.txt'])
]

def find_packages(path, prefix):
    yield prefix
    prefix += "."
    for _, name, ispkg in walk_packages(path, prefix):
        if ispkg:
            yield name

def emptydir(top, ignored_files=[]):
    ignored_files = set(ignored_files)
    if top == '/' or top == "\\":
        return
    else:
        for root, dirs, files in os.walk(top, topdown=False):
            for name in files:
                if not name in ignored_files:
                    os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

class BuildInstaller(py2exe.build_exe.py2exe, object):
    def run(self):
        global APP_NAME
        global APP_VERSION
        APP_PREFIX = '-'.join((APP_NAME, APP_VERSION))
        SDIST_ZIP_NAME = '{}.zip'.format(APP_PREFIX)
        BIN_NAME = '{}.win32'.format(APP_PREFIX)

        super(BuildInstaller, self).run()

        logging.info('Performing post-build actions.')
        # Remove build dir
        try:
            shutil.rmtree('build')
        except Exception:
            logging.exception('Could not delete "build" directory.')

        # Re-compress the library.zip
        return_code = subprocess.call([os.path.join(os.getcwd(), 'compress.bat'), 'library'], cwd='dist')
        if return_code != 0:
            logging.error("Extra compression returned an error, check if the packaged files are okay.")

        # Move the files to a temp directory
        ignores = shutil.ignore_patterns(SDIST_ZIP_NAME)
        shutil.copytree(  # requires py2exe to be run before sdist!
            'dist',
            os.path.join('_temp', APP_PREFIX),
            ignore=ignores
        )
        emptydir('dist', [SDIST_ZIP_NAME])

        # Archive the binary distribution
        shutil.make_archive('dist/{}'.format(BIN_NAME),
            'zip',
            root_dir='_temp',
            base_dir=APP_PREFIX)

        # Delete the temp dir
        try:
            shutil.rmtree('_temp')
        except Exception:
            logging.exception('Could not delete "_temp" directory.')

        # Re-compress the binary distribution archive (to minimise the file size of Python DLLs)
        # Commented out because the gains are minimal.
        #return_code = subprocess.call([os.path.join(os.getcwd(), 'compress.bat'), BIN_NAME], cwd='dist')
        #if return_code != 0:
        #    logging.error("Extra compression returned an error, check if the packaged files are okay.")

logging.info('Building distribution.')

opts = {
    'py2exe': {
        'includes': [],
        "dll_excludes" : [],
        'bundle_files': 2,
        'compressed' : False,
        'optimize' : 2,
    }
}

setup(
    name=APP_NAME,
    version=APP_VERSION,
    url='http://www.jestarjokin.net/apps/robinpacker',
    license='MIT',
    author='Laurence Dougal Myers',
    author_email='jestarjokin@jestarjokin.net',
    description=APP_DESCRIPTION,
    packages=list(find_packages(robinpacker.__path__, robinpacker.__name__)),
    console=[
        {
            "script": "robinpacker.py",
        },
    ],
    options=opts,
    cmdclass={
        "py2exe": BuildInstaller
    },
    data_files=data_files
)

