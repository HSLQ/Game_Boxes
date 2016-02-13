# -*- coding: utf-8 -*
# Filename: game.py

__author__ = 'Piratf'

from settings import GAME, BOARD
from textButton import TextButton
from centeredImage import CenteredImage
from background import Background
from hud import Hud
from board import Board
import pygame
from pygame.locals import *

class Game:
    """main frame of the game"""
    def __init__(self, level):
        # super(game, self).__init__()
        self.initAttr(level)
        self.initElement()
        self.initContext()

    def initElement(self):
        # 背景
        self.background = Background(self.width, self.height)
        backgroundColor = GAME["GAME_BACKGROUND_COLOR"]
        self.background.setColor(backgroundColor)
        # 返回按钮
        # self.returnButton = CenteredImage(GAME["RETURN_BUTTON_CONTENT"], GAME["RETURN_BUTTON_POSITION"], GAME["RETURN_BUTTON_SIZE"])
        self.returnButton = TextButton(GAME["RETURN_BUTTON_FONTS"], GAME["RETURN_BUTTON_CONTENT"], (30, 30))

    def initAttr(self, level):
        self.level = level
        self.edgeWidth = GAME["EDGE_WIDTH"]
        self.height = BOARD["BOARD_HEIGHT"] + self.edgeWidth * 2
        self.hud = Hud((0, self.height), (0, 0))
        # 根据游戏等级建立棋盘
        self.board = Board(level, (self.hud.width, self.edgeWidth))
        self.width = self.board.width + self.hud.width

    def initContext(self):
        self.screen = pygame.display.set_mode((self.width, self.height), NOFRAME)
        pygame.display.set_caption("Boxes")
        self.clock = pygame.time.Clock();
    
    def draw(self):
        self.screen.set_clip(None)
        self.background.draw(self.screen);
        self.board.draw(self.screen)
        self.hud.draw(self.screen)
        self.returnButton.draw(self.screen)
