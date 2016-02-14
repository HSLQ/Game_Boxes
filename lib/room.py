# -*- coding: utf-8 -*
# Filename: room.py

__author__ = 'Piratf'

from centeredText import CenteredText
from text import Text
from div import Div
import math
import pygame

class Room(Div):
    """room div in matching"""
    def __init__(self, (width, height), (x, y)):
        super(Room, self).__init__((width, height), (x, y))

    def setID(self, roomID):
        self.roomID = roomID
        self.roomIDLabel = Text(
            ROOM["ROOM_ID_FONTS"], 
            ROOM["ROOM_ID_LABEL_CONTENT"], 
            (self.x + ROOM["ROOM_ID_OFFSET_LEFT"], self.y + ROOM["ROOM_ID_OFFSET_TOP"]))
        offsetIDLeft = math.ceil(pygame.font.Font.size(str(self.roomID)) / 2.) + math.ceil(pygame.font.Font.size(str(ROOM["ROOM_ID_LABEL_CONTENT"]) / 2.))
        self.roomIDText = CenteredText(
            ROOM["ROOM_ID_FONTS"],
            self.roomID,
            self.x + ROOM["ROOM_ID_OFFSET_LEFT"] + offsetIDLeft + )

    def draw(self):
        self.roomID.draw()
        self.level.draw()