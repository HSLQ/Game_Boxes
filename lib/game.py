# -*- coding: utf-8 -*
# Filename: game.py

__author__ = 'Piratf'

from background import Background
from hud import Hud
from board import Board
import pygame

class Game:
    """main frame of the game"""
    def __init__(self, level):
        # super(game, self).__init__()
        self.level = level
        # 根据游戏等级建立棋盘
        self.board = Board(level)
        self.width = self.board.width
        # 有了宽度就可以适应出 HUD
        self.hud = Hud(self.width)
        # 有了 board 和 hud 高度，就可以适应出高度
        self.height = self.board.height + self.hud.height

        self.background = Background(self.width, self.height)

        self.initContext()

    def initContext(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Boxes")
        self.clock = pygame.time.Clock();
    
    def draw(self):

        self.board.draw(self.screen)
        self.hud.draw(self.screen, board.height)