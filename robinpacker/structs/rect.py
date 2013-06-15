#! /usr/bin/python
# Use, distribution, and modification of the RobinPacker binaries, source code,
# or documentation, is subject to the terms of the MIT license.
#
# Copyright (c) 2013 Laurence Dougal Myers
#
# http://opensource.org/licenses/MIT

class RectData(object):
    def __init__(self,
                maxX=None,
                minX=None,
                maxY=None,
                minY=None,
                topLeftPosY=None,
                topLeftPosX=None,
                bottomRightPosY=None,
                bottomRightPosX=None
        ):
        self.maxX = maxX
        self.minX = minX
        self.maxY = maxY
        self.minY = minY
        self.topLeftPosY = topLeftPosY
        self.topLeftPosX = topLeftPosX
        self.bottomRightPosY = bottomRightPosY
        self.bottomRightPosX = bottomRightPosX
