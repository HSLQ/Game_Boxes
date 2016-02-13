# -*- coding: utf-8 -*
# Filename: game.py

__author__ = 'Piratf'

from settings import GAME
from background import Background
from hud import Hud
from board import Board
import pygame

class Game:
    """main frame of the game"""
    def __init__(self, level):
        # super(game, self).__init__()
        self.initAttr(level)
        self.initContext()

    def initAttr(self, level):
        self.level = level
        # 根据游戏等级建立棋盘
        self.edgeWidth = GAME["EDGE_WIDTH"]
        self.board = Board(level, (self.edgeWidth, 0))
        self.width = self.board.width + self.edgeWidth * 2
        # 有了宽度就可以适应出 HUD
        self.hud = Hud(self.width, self.board.height)
        # 有了 board 和 hud 高度，就可以适应出高度
        self.height = self.board.height + self.hud.height

        self.background = Background(self.width, self.height)
        backgroundColor = GAME["GAME_BACKGROUND_COLOR"]
        self.background.setColor(backgroundColor)

    def initContext(self):
        self.screen = pygame.display.set_mode((self.width, self.height), NOFRAME)
        pygame.display.set_caption("Boxes")
        self.clock = pygame.time.Clock();
    
    def draw(self):
        self.background.draw(self.screen);
        self.board.draw(self.screen)
        self.hud.draw(self.screen)