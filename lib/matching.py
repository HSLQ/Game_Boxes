# -*- coding: utf-8 -*
# Filename: matching.py

__author__ = 'Piratf'

import pygame
from textButton import TextButton
from div import Div


# 游戏匹配界面
# 可以刷新，获得游戏所有空闲房间的编号
# 获得标号后使用 setRooms 刷新房间对象
# 使用 setCurrentRooms 构造当前页面的房间对象
# ---
class Matching:
    """matching frame, show rooms which could be linked"""
    def __init__(self):
        # super(Matching, self).__init__()
        self.initAttr()
        self.getRooms()

    def initAttr(self):
        self.beginIndex = 0;
        self.roomsInOnePage = MATCHING["ROOMS_IN_ONE_PAGE"]

    def setCurrentRooms(self):

        # for x in range(self.roomsInOnePage):
        #     if (beginIndex + x) < self.roomCount:
        #         self.currentRooms.append(rooms[beginIndex + x])
        self.currentRooms = [rooms[beginIndex + x] for x in range(self.roomsInOnePage) if (beginIndex + x) < self.roomCount]
        print "currentRooms: "
        print self.currentRooms

    # 设置房间个数
    def getRooms(self):
        self.rooms = set([1, 2])
        self.roomCount = len(self.rooms)

        self.setCurrentRooms()

    def draw(screen):
        [div.draw(screen) for div in self.currentRooms]

