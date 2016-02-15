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

class Game(object):
    """main frame of the game"""
    def __init__(self, level, controller):
        # super(game, self).__init__()
        self.controller = controller
        self.initAttr(level)
        self.initElement()
        self.initContext()

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

        self.gameID = 0
        self.order = None

    def initElement(self):
        # 背景
        self.background = Background((self.width, self.height))
        backgroundColor = GAME["GAME_BACKGROUND_COLOR"]
        self.background.setColor(backgroundColor)
        # 返回按钮
        self.returnButton = TextButton(GAME["RETURN_BUTTON_FONTS"], GAME["RETURN_BUTTON_CONTENT"], (30, 30))

    def initContext(self):
        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF)
        pygame.display.set_caption("Boxes")
        self.clock = pygame.time.Clock();

    def openRoom(self):
        print "open room"
        self.controller.gameNet.openRoom(self.level)

    def leaveServer(self, *args):
        self.controller.gameNet.leaveServer(self.gameID)
        return STATE.menu

    def placeLine(self, data):
        self.controller.gameNet.placeLine(data, self.gameID, self.order)

    def setTurn(self, turn):
        self.hud.setMark(turn)
        self.board.setTurn(turn)

    # 对手玩家进入游戏
    def enemyComming(self, turn):
        self.setTurn(turn)
        self.hud.startGame()

    def newHost(self):
        self.hud.restart()

    # 数据清零，重新开始游戏
    def restart(self):
        self.board.restart()
        self.hud.restart()

    def placeLineAnswer(self, turn, x, y, h, point, order):
        self.setTurn(turn)
        if order == self.order:
            self.board.placeLine(x, y, h, point, True)
        else:
            self.board.placeLine(x, y, h, point, False)

    def draw(self):
        self.screen.set_clip(None)
        self.background.draw(self.screen)
        ret = self.board.draw(self.screen)
        if ret != None:
            self.placeLine(ret)
        self.hud.draw(self.screen)
        self.returnButton.draw(self.screen)
        var = self.returnButton.click(self.leaveServer)
        if var != None:
            return var
        return STATE.game
