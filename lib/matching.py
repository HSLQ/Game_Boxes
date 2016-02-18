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
from time import sleep
from math import ceil

# 游戏匹配界面
# 可以刷新，获得游戏所有空闲房间的编号
# 获得标号后使用 setRooms 刷新房间对象
# 使用 setCurrentRooms 构造当前页面的房间对象
# 
# 新建 panel，返回方块的大小
# 根据大小实例化方块
# 实例化完成后传递到 panel 中，
# panel 负责绘制 panel 内部的内容
# ---
class Matching(object):
    """matching frame, show rooms which could be linked"""
    def __init__(self, (width, height), controller):
        # super(Matching, self).__init__()
        self.controller = controller
        self.initAttr((width, height))
        self.initElem()

    def initAttr(self, (width, height)):
        self.width = width
        self.height = height

        self.beginIndex = 0;
        self.roomsInOnePage = MATCHING["ROOMS_ROW"] * MATCHING["ROOMS_COL"]

        self.buttonFont = MATCHING["BUTTON_FONT"]
        self.pageButtonFont = MATCHING["PAGE_BUTTON_FONT"]
        self.currentRoom = []

        self.hasLastPage = False
        self.hasNextPage = True

    def initElem(self):
        # panel 部分
        self.background = Background((self.width, self.height))
        self.background.setColor((50, 50, 50))
        self.setRoomLayout()

        # 房间翻页
        self.pageButtonOffsetBottom = MATCHING["PAGE_BUTTON_OFFSET_BOTTOM"]
        self.pageButtonOffsetMiddleLine = MATCHING["PAGE_BUTTON_OFFSET_MIDDLE_LINE"]
        lastPageCoord = int(ceil(self.width / 2.) - self.pageButtonOffsetMiddleLine), int(ceil(self.height - self.pageButtonOffsetBottom))
        nextPageCoord = int(ceil(self.width / 2.) + self.pageButtonOffsetMiddleLine), int(ceil(self.height - self.pageButtonOffsetBottom))
        self.lastPageButton = TextButton(self.pageButtonFont, MATCHING["LAST_PAGE_BUTTON_CONTENT"], lastPageCoord)
        self.nextPageButton = TextButton(self.pageButtonFont, MATCHING["NEXT_PAGE_BUTTON_CONTENT"], nextPageCoord)

        # button 部分
        self.returnButton = TextButton(self.buttonFont, MATCHING["RETURN_BUTTON_CONTENT"], (MATCHING["RETURN_BUTTON_OFFSET_LEFT"], self.height - MATCHING["RETURN_BUTTON_OFFSET_BOTTOM"]))
        self.refreshButton = TextButton(self.buttonFont, MATCHING["REFRESH_BUTTON_CONTENT"], (self.width - MATCHING["REFRESH_BUTTON_OFFSET_RIGHT"], self.height - MATCHING["REFRESH_BUTTON_OFFSET_BOTTOM"]))

    def setRoomLayout(self, (row, col) = (MATCHING["ROOMS_ROW"], MATCHING["ROOMS_COL"])):
        panelWidth = self.width - MATCHING["PANEL_OFFSET_LEFT"] * 2
        panelHeight = self.height - MATCHING["PANEL_OFFSET_TOP"] - MATCHING["PANEL_OFFSET_BOTTOM"]
        self.panel = Panel((panelWidth, panelHeight), (MATCHING["PANEL_OFFSET_LEFT"], MATCHING["PANEL_OFFSET_TOP"]), (row, col))
        self.currentRoomLocation = self.panel.getLocationList()
        self.roomSize = self.panel.getChildSize()

    # 更新当前房间对象，放入panel 中，为绘制做准备
    def setCurrentRoom(self):
        roomCount = len(self.rooms)
        print "roomCount", roomCount

        if roomCount < 1 or self.rooms == None: 
            self.currentRoom = []
        else:
            self.currentRoomID = [self.rooms[x][0] for x in range(roomCount)]
            self.currentRoomLevel = [self.rooms[x][1] for x in range(roomCount)]
            self.currentRoom = [Room(roomID, roomLevel, self.roomSize, location) for roomID, roomLevel, location in zip(self.currentRoomID, self.currentRoomLevel, self.currentRoomLocation)]
        self.panel.setChildren(self.currentRoom)

    # 设置房间个数
    def getRooms(self, *args):
        print "get rooms"
        # 从服务器获取房间
        if len(args) > 0:
            index = args[0]
            print index
            self.beginIndex += index
            if self.beginIndex < 0:
                self.beginIndex = 0
        ret = self.controller.getRooms(self, self.beginIndex, self.roomsInOnePage)
        self.roomCount = len(self.rooms)
        self.setCurrentRoom()
        if False == ret:
            return STATE.menu
        else:
            return None

    def joinRoom(self, roomID):
        roomID = roomID
        print "roomID", roomID
        self.controller.gameNet.joinRoom(roomID)

    def backToMenu(self, *args):
        self.beginIndex = 0
        return STATE.menu

    def draw(self, screen):
        self.background.draw(screen)
        self.panel.draw(screen)

        if self.hasLastPage:
            self.lastPageButton.draw(screen)
            self.lastPageButton.click(self.getRooms, -1)

        if self.hasNextPage:
            self.nextPageButton.draw(screen)
            self.nextPageButton.click(self.getRooms, 1)

        self.returnButton.draw(screen)
        self.refreshButton.draw(screen)

        ret = self.returnButton.click(self.backToMenu)
        if ret != None:
            return ret

        ret = self.refreshButton.click(self.getRooms)
        if ret != None:
            return ret

        for room in self.currentRoom:
            room.click(self.joinRoom, room.roomID)

        return STATE.matching
