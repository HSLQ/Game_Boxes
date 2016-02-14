# -*- coding: utf-8 -*
# Filename: div.py

__author__ = 'Piratf'

class Div:
    """small panel in the frame"""
    def __init__(self, (width, height), (x, y)):
        # super(Div, self).__init__()
        self.initAttr((width, height), (x, y))
        self.initElem()

    def initAttr(self, (width, height), (x, y)):
        self.width = width
        self.height = height
        self.x = x;
        self.y = y;
        
    def initElem(self):
        self.background = Background(self.width, self.height, self.x, self,y)
        self.background.setColor(255, 255, 255)

    def draw(screen):
        self.background.draw(screen)
