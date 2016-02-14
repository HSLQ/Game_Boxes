# -*- coding: utf-8 -*
# Filename: panel.py

__author__ = 'Piratf'

from settings import PANEL
from background import Background
from math import ceil
import pygame

class Panel(object):
    """a div container"""
    def __init__(self, (width, height), (x, y), (rows, cols)):
        # super(Panel(object), self).__init__()
        self.initAttr((width, height), (x, y), (rows, cols))
        self.initElem()

    def initAttr(self, (width, height), (x, y), (rows, cols)):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.rows = rows
        self.cols = cols
        self.gapWidth = PANEL["GAP_WIDTH"]
        self.gapHeight = PANEL["GAP_HEIGHT"]

    def initElem(self):
        self.background = Background((self.width, self.height), (self.x, self.y))

    def getChildWidth(self):
        return ceil((self.width - (self.rows - 1) * self.gapWidth) / self.rows)

    def getChildHeight(self):
        return ceil((self.height - (self.cols - 1) * self.gapHeight) / self.cols)

    def getLocationList(self):
        self.childWidth = self.getChildWidth()
        self.chileHeight = self.getChildHeight()
        locationList = []
        for c in range(self.cols):
            for r in range(self.rows):
                locationList.append((self.x + r * (self.childWidth + self.gapWidth), self.y + c * (self.chileHeight + self.gapHeight)))
        return locationList

    def getChildSize(self):
        return (self.childWidth, self.chileHeight)

    def setChildren(self, children):
        self.children = children

    def draw(self, screen):
        self.background.draw(screen)
        [child.draw(screen) for child in self.children]
