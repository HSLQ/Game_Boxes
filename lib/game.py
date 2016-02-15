# -*- coding: utf-8 -*
# Filename: game.py

__author__ = 'Piratf'

from settings import GAME, BOARD, STATE
from textButton import TextButton
from centeredImage import CenteredImage
from background import Background
from hud import Hud
from board import Board
import pygame
from pygame.locals import *
from PodSixNet.Connection import ConnectionListener, connection

class Game(ConnectionListener):
    """main frame of the game"""
    def __init__(self, level):
        # super(game, self).__init__()
        self.initAttr(level)
        self.initElement()
        self.connectToServer()
        self.initContext()

    def initAttr(self, level):
        self.level = level
        self.edgeWidth = GAME["EDGE_WIDTH"]
        self.height = BOARD["BOARD_HEIGHT"] + self.edgeWidth * 2
        self.hud = Hud((0, self.height), (0, 0))
        # 根据游戏等级建立棋盘
        self.board = Board(level, (self.hud.width, self.edgeWidth))
        self.width = self.board.width + self.hud.width

    def initElement(self):
        # 背景
        self.background = Background((self.width, self.height))
        backgroundColor = GAME["GAME_BACKGROUND_COLOR"]
        self.background.setColor(backgroundColor)
        # 返回按钮
        self.returnButton = TextButton(GAME["RETURN_BUTTON_FONTS"], GAME["RETURN_BUTTON_CONTENT"], (30, 30))

    def connectToServer(self):
        host, port="localhost", 8000
        self.Connect((host, int(port)))
        # address = raw_input("Address of Server: ")
        # try:
        #     if not address:
        #         host, port="localhost", 8000
        #     else:
        #         host,port=address.split(":")
        #     self.Connect((host, int(port)))
        # except:
        #     print "Error Connecting to Server"
        #     print "Usage:", "host:port"
        #     print "e.g.", "localhost:31425"
        #     exit()
        print "Boxes client started"

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
        var = self.returnButton.click(lambda : STATE.menu)
        return var if var else STATE.game
