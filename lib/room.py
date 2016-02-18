# -*- coding: utf-8 -*
# Filename: room.py

__author__ = 'Piratf'

from settings import ROOM
from centeredText import CenteredText
from text import Text
from div import Div
from button import Button
from background import Background
import math
import pygame

class Room(Div, Button):
    """room div in matching"""
    def __init__(self, roomID, roomLevel, (width, height), (x, y)):
        Div.__init__(self, (width, height), (x, y))
        Button.__init__(self, self.rect)
        self.background = Background((width, height), (x, y))
        self.background.setColor((200, 200, 200))
        self.initAttr()
        self.setID(roomID)
        self.setLevel(roomLevel)

    def initAttr(self):
        self.idFont = ROOM["ROOM_ID_FONTS"]

    def setID(self, roomID):
        self.roomID = roomID
        self.roomIDLabel = Text(
            self.idFont, 
            ROOM["ROOM_ID_LABEL_CONTENT"], 
            (self.x + ROOM["ROOM_ID_LABEL_OFFSET_LEFT"], 
                self.y + ROOM["ROOM_ID_OFFSET_TOP"])
            )
        offsetIDNumLeft = math.ceil(
            (self.idFont.size(str(self.roomID))[0] / 2.) + 
            math.ceil(
                (self.idFont.size(ROOM["ROOM_ID_LABEL_CONTENT"])[0])
                )
            ) + ROOM["ROOM_ID_LABEL_OFFSET_LEFT"] + ROOM["ROOM_LEVEL_DISTANCE_NUM_LABEL"]
        self.roomIDText = CenteredText(
            self.idFont,
            str(self.roomID),
            (self.x + offsetIDNumLeft,
                self.y + ROOM["ROOM_ID_OFFSET_TOP"] * 2)
            )

    def setLevel(self, roomLevel):
        self.roomLevel = roomLevel
        offsetLevelLabelLeft = math.ceil(
            (self.idFont.size(str(self.roomLevel))[0]) + 
            math.ceil(
                (self.idFont.size(ROOM["ROOM_LEVEL_CONTENT"])[0] / 2.)
                )) + ROOM["ROOM_LEVEL_NUM_OFFSET_RIGHT"]
        self.roomLevelLabel = CenteredText(
            self.idFont, 
            ROOM["ROOM_LEVEL_CONTENT"], 
            (self.x + self.width - offsetLevelLabelLeft,
                self.y + self.height - ROOM["ROOM_LEVEL_OFFSET_BOTTOM"])
            )
        self.roomLevelText = CenteredText(
            self.idFont,
            str(self.roomLevel),
            (self.x + self.width - ROOM["ROOM_LEVEL_NUM_OFFSET_RIGHT"],
                self.y + self.height - (ROOM["ROOM_LEVEL_OFFSET_BOTTOM"]))
            )
    
    def draw(self, screen):
        self.background.draw(screen)
        Button.draw(self, screen)
        self.roomIDLabel.draw(screen)
        self.roomIDText.draw(screen)
        self.roomLevelText.draw(screen)
        self.roomLevelLabel.draw(screen)