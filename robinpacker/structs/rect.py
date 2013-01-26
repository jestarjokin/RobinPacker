#! /usr/bin/python

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
