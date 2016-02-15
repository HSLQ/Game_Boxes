# -*- coding: utf-8 -*
# Filename: game.py

__author__ = 'Piratf'

from settings import GAME, BOARD, STATE, NETWORK
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
        self.initContext()
        self.connectToServer()

    def initAttr(self, level):
        self.turn = True
        self.level = level
        self.edgeWidth = GAME["EDGE_WIDTH"]
        self.height = BOARD["BOARD_HEIGHT"] + self.edgeWidth * 2
        # 根据窗口高度设置 HUD 高度
        self.hud = Hud((0, self.height), (0, 0))
        self.hud.setMark(self.turn)
        # 根据游戏等级建立棋盘
        self.board = Board(level, (self.hud.width, self.edgeWidth))
        self.board.setTurn(self.turn)

        self.width = self.board.width + self.hud.width

        self.gameID = None
        self.order = None

    def initElement(self):
        # 背景
        self.background = Background((self.width, self.height))
        backgroundColor = GAME["GAME_BACKGROUND_COLOR"]
        self.background.setColor(backgroundColor)
        # 返回按钮
        self.returnButton = TextButton(GAME["RETURN_BUTTON_FONTS"], GAME["RETURN_BUTTON_CONTENT"], (30, 30))

    def connectToServer(self):
        host, port = NETWORK["HOST"], NETWORK["PORT"]
        self.Connect((host, int(port)))
        print "linked to server"
        self.Send({"action":"startGame", "level": self.level})

    def initContext(self):
        self.screen = pygame.display.set_mode((self.width, self.height), NOFRAME)
        pygame.display.set_caption("Boxes")
        self.clock = pygame.time.Clock();
    
    def Network_startgame(self, data):
        # 获取服务器的数据
        self.order = data["player"]
        self.gameID = data["gameID"]
        # 分配游戏顺序
        if self.order == 0:
            self.turn = True
            self.board.setTurn(self.turn)
        else:
            self.turn = False
            self.board.setTurn(self.turn)
        self.hud.setMark(self.turn)
        self.hud.startGame()

    def leaveGame(self):
        self.Send({"action": "leaveGame", "gameID": self.gameID})
        return STATE.menu

    def draw(self):
        connection.Pump()
        self.Pump()
        self.screen.set_clip(None)
        self.background.draw(self.screen)
        ret = self.board.draw(self.screen)
        if ret != None:
            self.Send({"action": "place", "x":ret["x"], "y":ret["y"], "is_horizontal": ret["h"], "gameID": self.gameID, "order": self.order})
        self.hud.draw(self.screen)
        self.returnButton.draw(self.screen)
        var = self.returnButton.click(self.leaveGame)
        return var if var else STATE.game
