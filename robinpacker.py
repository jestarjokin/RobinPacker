#! /usr/bin/python
# Use, distribution, and modification of the RobinPacker binaries, source code,
# or documentation, is subject to the terms of the MIT license.
#
# Copyright (c) 2013 Laurence Dougal Myers
#
# http://opensource.org/licenses/MIT

import sys

import robinpacker

if __name__ == "__main__":
    sys.exit(robinpacker.main.main(sys.argv[1:]))
