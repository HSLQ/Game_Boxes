# -*- coding: utf-8 -*
# Filename: matching.py

__author__ = 'Piratf'

from settings import MATCHING, STATE
from textButton import TextButton
from background import Background
from div import Div
from panel import Panel
from room import Room
import pygame
import random


# 游戏匹配界面
# 可以刷新，获得游戏所有空闲房间的编号
# 获得标号后使用 setRooms 刷新房间对象
# 使用 setCurrentRooms 构造当前页面的房间对象
# 
# 
# 新建 panel，返回方块的大小
# 根据大小实例化方块
# 实例化完成后传递到 panel 中，
# panel 负责绘制 panel 内部的内容
# ---
class Matching(object):
    """matching frame, show rooms which could be linked"""
    def __init__(self, (width, height)):
        # super(Matching, self).__init__()
        self.initAttr((width, height))
        self.initElem()
        self.getRooms()

    def initAttr(self, (width, height)):
        self.width = width
        self.height = height

        self.beginIndex = 0;
        self.roomsInOnePage = MATCHING["ROOMS_ROW"] * MATCHING["ROOMS_COL"]

        self.buttonFont = MATCHING["BUTTON_FONT"]

    def initElem(self):
        # panel 部分
        self.background = Background((self.width, self.height))
        self.background.setColor((50, 50, 50))
        self.setRoomLayout()
        # button 部分
        self.returnButton = TextButton(self.buttonFont, MATCHING["RETURN_BUTTON_CONTENT"], (MATCHING["RETURN_BUTTON_OFFSET_LEFT"], self.height - MATCHING["RETURN_BUTTON_OFFSET_BOTTOM"]))
        self.refreshButton = TextButton(self.buttonFont, MATCHING["REFRESH_BUTTON_CONTENT"], (self.width - MATCHING["REFRESH_BUTTON_OFFSET_RIGHT"], self.height - MATCHING["REFRESH_BUTTON_OFFSET_BOTTOM"]))


    def setRoomLayout(self, (row, col) = (MATCHING["ROOMS_ROW"], MATCHING["ROOMS_COL"])):
        panelWidth = self.width - MATCHING["PANEL_OFFSET_LEFT"] * 2
        panelHeight = self.height - MATCHING["PANEL_OFFSET_TOP"] - MATCHING["PANEL_OFFSET_BOTTOM"]
        self.panel = Panel((panelWidth, panelHeight), (MATCHING["PANEL_OFFSET_LEFT"], MATCHING["PANEL_OFFSET_TOP"]), (row, col))
        self.currentRoomLocation = self.panel.getLocationList()
        self.roomSize = self.panel.getChildSize()

    def setCurrentRoom(self):
        self.currentRoomID = [self.rooms[self.beginIndex + x][0] for x in range(self.roomsInOnePage) if (self.beginIndex + x) < self.roomCount]
        self.currentRoomLevel = [self.rooms[self.beginIndex + x][1] for x in range(self.roomsInOnePage) if (self.beginIndex + x) < self.roomCount]
        self.currentRoom = [Room(roomID, roomLevel, self.roomSize, location) for roomID, roomLevel, location in zip(self.currentRoomID, self.currentRoomLevel, self.currentRoomLocation)]
        self.panel.setChildren(self.currentRoom)

    # 设置房间个数
    def getRooms(self):
        # 从服务器获取房间
        
        self.rooms = [(random.randint(1, 100), random.randint(5, 9)) for x in range(random.randint(0, 4))]
        self.roomCount = len(self.rooms)
        self.setCurrentRoom()
        return None

    def draw(self, screen):
        self.background.draw(screen)
        self.panel.draw(screen)
        self.returnButton.draw(screen)
        var = self.returnButton.click(lambda : STATE.menu)
        self.refreshButton.draw(screen)
        self.refreshButton.click(self.getRooms)
        return var if var else STATE.matching
