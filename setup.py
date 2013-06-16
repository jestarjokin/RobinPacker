#! /usr/bin/python
# Use, distribution, and modification of the RobinPacker binaries, source code,
# or documentation, is subject to the terms of the MIT license.
#
# Copyright (c) 2013 Laurence Dougal Myers
#
# http://opensource.org/licenses/MIT

from distutils.core import setup
from glob import glob
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

MANIFEST = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1"
manifestVersion="1.0">
<assemblyIdentity
    version="{}.1.0"
    processorArchitecture="x86"
    name="{}"
    type="win32"
/>
<description>{}</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.VC90.CRT"
            version="9.0.21022.8"
            processorArchitecture="X86"
            publicKeyToken="1fc8b3b9a1e18e3b"
            language="*"
        />
    </dependentAssembly>
</dependency>
""".format(
    APP_VERSION,
    APP_NAME,
    APP_DESCRIPTION,
)

def find_packages(path, prefix):
    yield prefix
    prefix += "."
    for _, name, ispkg in walk_packages(path, prefix):
        if ispkg:
            yield name

class BuildInstaller(py2exe.build_exe.py2exe, object):
    def run(self):
        global APP_NAME
        global APP_VERSION
        # Make sure you have this version of "Microsoft Visual C++ 2008 Redistributable Package" installed:
        # http://www.microsoft.com/downloads/details.aspx?FamilyID=9b2da534-3e03-4391-8a4d-074b9f2bc1bf&displaylang=en
        # (also check that you have the legal ability to redistribute these files)
        data_files.extend([
            ("VC90", glob(r'C:\Windows\winsxs\x86_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.21022.8_none_bcb86ed6ac711f91\*.*')),
            ("VC90", glob(r'C:\Windows\winsxs\Manifests\x86_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.21022.8_none_bcb86ed6ac711f91.manifest'))
        ])

        super(BuildInstaller, self).run()

        logging.info('Performing post-build actions.')
        try:
            shutil.rmtree('build')
        except Exception:
            logging.exception('Could not delete "build" directory.')

        return_code = subprocess.call(os.path.join(os.getcwd(), 'compress.bat'), cwd='dist')
        if return_code != 0:
            logging.error("Extra compression returned an error, check if the packaged files are okay.")

        app_prefix = '-'.join((APP_NAME, APP_VERSION))
        os.renames('dist', os.path.join('_temp', app_prefix)) # requires py2exe to be run before sdist!
        shutil.make_archive('dist/{}.win32'.format(app_prefix),
            'zip',
            root_dir='_temp',
            base_dir=app_prefix)
        try:
            shutil.rmtree('_temp')
        except Exception:
            logging.exception('Could not delete "_temp" directory.')

logging.info('Building distribution.')

opts = {
    'py2exe': {
        'includes': [],
        "dll_excludes" : [],
        'bundle_files': 1,
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
            "other_resources": [(24, 1, MANIFEST)]
        },
    ],
    options=opts,
    cmdclass={
        "py2exe": BuildInstaller
    },
    data_files=data_files
)

