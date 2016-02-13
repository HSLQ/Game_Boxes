# -*- coding: utf-8 -*
# Filename: settings.py

__author__ = 'Piratf'

from util import getFilePath
import pygame

UNDEFINED = -1
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

# 主菜单
pygame.font.init()
MENU_TEXTS = [u"发起新游戏", u"匹配", u"游戏规则", u"退出"]
MENU_FONTS = pygame.font.Font(getFilePath("CindyAfternoonTea.ttf"), 25)

# set 实现的 枚举类型
class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

STATE = Enum(['menu', 'game', 'setLevel', 'rules', 'matching', 'exit'])

# 游戏规则
RULES_CONTENT = [
u"两人轮流采取行动", 
u"绿灯行动，红灯等待对方行动",
u"鼠标点击, 点亮格子边的线", 
u"圈成完整格子的玩家即占领该格子并得分", 
u"得分玩家可以再进行一个回合", 
u"返回"]
RULES_CONTENT_FONTS = pygame.font.SysFont("yaheiconsolashybrid", 18)
RULES_EXIT_FONTS = MENU_FONTS
# RULES_EXIT_FONTS = pygame.font.Font(getFilePath("CindyAfternoonTea.ttf"), 25)

# 设置等级

SETLEVEL = {
"TITLE_CONTENT" : u"游戏设置",
"TITLE_FONTS" : MENU_FONTS,

"EXIT_CONTENT" : u"返回", 
"EXIT_FONTS" : MENU_FONTS, 

"BEGIN_CONTENT" : u"开始", 
"BEGIN_FONTS" : MENU_FONTS,

"DEFAULT_LEVEL" : 6,
"MAX_LEVEL" : 9,
"MIN_LEVEL" : 5,
"LEVEL_FONTS" : pygame.font.Font(getFilePath("Mf_Kings_Queens.ttf"), 80),
"ARROW_SIZE" : 60,

"JUST_CLICKED" : 3
}

# 棋盘
BOARD = {
    "STICK_LENGTH": 59,
    "SEPARATOR_LENGTH": 5,
    "STICK_NOR_IMAGE": pygame.image.load(getFilePath("normalline.png")),
    "STICK_DONE_IMAGE": pygame.image.load(getFilePath("bar_done.png")),
    "SEPARATOR_IMAGE": pygame.image.load(getFilePath("separators.png"))
}
        
# HUD
HUD = {
    "HUD_HEIGHT": 110,
    "HUD_BACKGROUND_IMAGE": pygame.image.load(getFilePath("panel.png"))
}