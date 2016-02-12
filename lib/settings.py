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