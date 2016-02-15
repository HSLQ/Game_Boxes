# -*- coding: utf-8 -*
# Filename: settings.py

__author__ = 'Piratf'

from util import getFilePath
import pygame

UNDEFINED = -1
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

# 字体
pygame.font.init()
FONT_CINDY_AFTERNOON25 = pygame.font.Font(getFilePath("CindyAfternoonTea.ttf"), 25)
FONT_SYS_NONE = pygame.font.SysFont("simhei", 25)
FONT_CHILD30 = pygame.font.Font(getFilePath("Child.ttf"), 30)
FONT_CHILD20 = pygame.font.Font(getFilePath("Child.ttf"), 20)

# 主菜单
MENU_TEXTS = [u"发起新游戏", u"匹配", u"游戏规则", u"退出"]
MENU_FONTS = FONT_CINDY_AFTERNOON25

# set 实现的 枚举类型
class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

STATE = Enum(['menu', 'game', 'setLevel', 'rules', 'matching', 'exit'])

# 游戏规则 rules
RULES_CONTENT = [
u"两人轮流采取行动", 
u"绿灯行动，红灯等待对方行动",
u"鼠标点击, 点亮格子边的线", 
u"圈成完整格子的玩家即占领该格子并得分", 
u"得分玩家可以再进行一个回合", 
u"返回"]
RULES_CONTENT_FONTS = pygame.font.SysFont("yaheiconsolashybrid", 18)
RULES_EXIT_FONTS = FONT_CINDY_AFTERNOON25
# RULES_EXIT_FONTS = pygame.font.Font(getFilePath("CindyAfternoonTea.ttf"), 25)

# 设置等级 set level
SETLEVEL = {
    "TITLE_CONTENT" : u"游戏设置",
    "TITLE_FONTS" : FONT_CINDY_AFTERNOON25,
    
    "EXIT_CONTENT" : u"返回", 
    "EXIT_FONTS" : FONT_CINDY_AFTERNOON25, 
    
    "BEGIN_CONTENT" : u"开始", 
    "BEGIN_FONTS" : FONT_CINDY_AFTERNOON25,
    
    "DEFAULT_LEVEL" : 6,
    "MAX_LEVEL" : 9,
    "MIN_LEVEL" : 5,
    "LEVEL_FONTS" : pygame.font.Font(getFilePath("Mf_Kings_Queens.ttf"), 80),
    "ARROW_SIZE" : 60,
    
    "JUST_CLICKED" : 3
}

# 房间 div

ROOM = {
    "ROOM_ID_FONTS": FONT_CHILD20,
    "ROOM_ID_LABEL_CONTENT": u"房间编号:",
    "ROOM_ID_LABEL_OFFSET_LEFT": 10,
    "ROOM_ID_DISTANCE_LABEL_NUM": 10,
    "ROOM_ID_OFFSET_TOP": 10,

    "ROOM_LEVEL_FONTS": FONT_CHILD20,
    "ROOM_LEVEL_CONTENT": u"等级:",
    "ROOM_LEVEL_OFFSET_BOTTOM": 20,
    "ROOM_LEVEL_NUM_OFFSET_RIGHT": 15,
    "ROOM_LEVEL_DISTANCE_NUM_LABEL": 10,
}

# 房间匹配
MATCHING = {
    "ROOMS_ROW": 2,
    "ROOMS_COL": 2,
    "PANEL_OFFSET_LEFT": 30,
    "PANEL_OFFSET_TOP": 30,
    "PANEL_OFFSET_BOTTOM": 100,
    "BUTTON_FONT": FONT_CINDY_AFTERNOON25,
    "RETURN_BUTTON_CONTENT": u"返回",
    "RETURN_BUTTON_OFFSET_LEFT": 40,
    "RETURN_BUTTON_OFFSET_BOTTOM": 30,
    "REFRESH_BUTTON_CONTENT": u"刷新",
    "REFRESH_BUTTON_OFFSET_RIGHT": 50,
    "REFRESH_BUTTON_OFFSET_BOTTOM": 30
}

# panel 设置
PANEL = {
    "GAP_WIDTH": 30,
    "GAP_HEIGHT": 20
}

# 主游戏 game frame
GAME = {
    "EDGE_WIDTH": 40,
    "GAME_BACKGROUND_COLOR": (112, 242, 181),
    # "RETURN_BUTTON_CONTENT": pygame.transform.flip(pygame.image.load(getFilePath("return.png")), True, False),
    "RETURN_BUTTON_FONTS": FONT_CINDY_AFTERNOON25,
    "RETURN_BUTTON_CONTENT": u"逃跑",
    "RETURN_BUTTON_OFFSET_LEFT": 30,
    "RETURN_BUTTON_SIZE": (40, 40),

}

# 棋盘 board
BOARD = {
    "BOARD_WIDTH": 64 * 7 + 5,
    "BOARD_HEIGHT": 64 * 7 + 5,
    "STICK_LENGTH": 59,
    "SEPARATOR_LENGTH": 5,
    "STICK_NOR_IMAGE": pygame.image.load(getFilePath("normalline.png")),
    "STICK_DONE_IMAGE": pygame.image.load(getFilePath("bar_done.png")),
    "SEPARATOR_IMAGE": pygame.image.load(getFilePath("separators.png")),

    "GREEN_SQUARE": pygame.image.load(getFilePath("greenplayer.png")),
    "YELLOW_SQUARE": pygame.image.load(getFilePath("yellowplayer.png")),

    "JUST_PLACED": 10
}
        
# HUD
HUD = {
    "HUD_HEIGHT": 180,
    "HUD_WIDTH": 140,
    "HUD_BACKGROUND_IMAGE": pygame.image.load(getFilePath("panel_V.png")),

    "LAMP_WIDTH": 35,
    "LAMP_HEIGHT": 37,
    "GREEN_PILOT_LAMP": pygame.image.load(getFilePath("greenindicator.png")),
    "RED_PILOT_LAMP": pygame.image.load(getFilePath("redindicator.png")),

    "MARK_TEXT_FONTS": FONT_CHILD30,
    "MARK_TEXT_CONTENT": u"行动",

    "SCORE_TEXT_FONTS": FONT_CHILD30,

    "LABEL_FONTS": FONT_CHILD20,
    "MY_SCORE_LABEL_CONTENT": u"我的分数",
    "MY_SCORE_LABEL_OFFSET_TOP": 70,
    "MY_SCORE_LABEL_OFFSET_LEFT": 10,
    "OTHER_SCORE_LABEL_CONTENT": u"对手分数",
    "OTHER_SCORE_LABEL_OFFSET_BOTTOM": 67,
    "OTHER_SCORE_LABEL_OFFSET_LEFT": 10,

    "MY_SCORE_TEXT_OFFSET_TOP": 100,
    "MY_SCORE_TEXT_OFFSET_LEFT": 10,

    "OTHER_SCORE_TEXT_OFFSET_BOTTOM": 30,
    "OTHER_SCORE_TEXT_OFFSET_LEFT": 10,

}

# 按钮

BUTTON = {
    "BUTTON_JUST_CLICKED": 3,
}
 
TEXTBUTTON = {
    "BUTTON_TEXT_PADDING": 5,
}