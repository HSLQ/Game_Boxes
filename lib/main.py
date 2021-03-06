# -*- coding: utf-8 -*
# Filename: main.py

__author__ = 'Piratf'

from settings import WINDOW_WIDTH, WINDOW_HEIGHT, STATE, Enum
from menu import Menu
from setLevel import SetLevel
from settings import SETLEVEL
from rules import Rules
from game import Game
from matching import Matching
from gameNet import GameNet
from finish import Finish
import pygame
from pygame.locals import *
from time import sleep

class Main(object):
    """main loop of the game"""
    def __init__(self):
        pygame.init()
        # 包括读取设置文件，设置游戏基本属性
        self.initAttr()
        # 传递所需的参数，实例化所包含的各个类
        self.initObj()
        self.initContext()

    def initAttr(self):
        self.width, self.height = WINDOW_WIDTH, WINDOW_HEIGHT
        self.state = STATE.menu
        self.running = True
        self.level = SETLEVEL["DEFAULT_LEVEL"]
        self.channelID = None

    def initObj(self):
        # 设置大小，用于背景图片的缩放
        self.gameNet = GameNet(self)
        self.gameNet.connectToServer()
        self.menu = Menu((self.width, self.height), self)
        self.rules = Rules(self.width, self.height)
        self.setLevel = SetLevel(self.width, self.height)
        self.matching = Matching((self.width, self.height), self)
        self.game = Game(self)
        # finish 界面的大小和游戏界面一样
        self.finish = Finish((self.game.width, self.game.height))

    # 绘制游戏主窗体
    def initContext(self):
        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF)
        pygame.display.set_caption("Boxes")

        self.clock = pygame.time.Clock();

    def linkSuccess(self):
        print "link success"
        print self.channelID

    def enterMatching(self):
        self.matching.getRooms()

    def enemyComming(self, turn, gameID):
        self.gameID = gameID
        self.game.enemyComming(turn)
        self.game.setHome()

    def joinGame(self, level, gameID, turn):
        self.game = Game(self)
        self.game.gameID = gameID
        self.state = STATE.game
        self.game.setLevel(level)
        self.game.enemyComming(turn)
        self.game.setAway()

    def enterMenu(self):
        self.state = STATE.menu

    # 进入游戏界面事件
    def enterGame(self, level):
        self.game.setLevel(level)
        self.game.initContext()
        self.state = STATE.game

    def startedNewGame(self, level):
        print "open room", level
        self.gameNet.openRoom(level)

    def leaveServer(self, gameID):
        self.gameNet.leaveServer(self.gameID)
        self.state = STATE.menu

    def backToMenu(self):
        self.initContext()
        self.state = STATE.menu

    def addScore(self):
        self.game.addScore()

    def enemyAddScore(self):
        self.game.enemyAddScore()

    def getRooms(self, matching, page, num):
        self.gameNet.getRooms(matching, page, num)

    def update(self):
        self.clock.tick(60)
        self.screen.fill(0)
        self.gameNet.pump()

        if STATE.exit == self.state:
            exit()

        elif STATE.setLevel == self.state:
            var = self.setLevel.draw(self.screen)
            if (var in STATE):
                self.state = var
            else:
                self.startedNewGame(var)
                self.enterGame(var)

        elif STATE.game == self.state:
            self.state = self.game.draw()
            if (self.state != STATE.game):
                self.initContext()

        elif STATE.matching == self.state:
            self.state = self.matching.draw(self.screen)

        elif STATE.menu == self.state:
            self.menu.draw(self.screen)
            self.state = self.menu.clickListener()

        elif STATE.rules == self.state:
            self.rules.draw(self.screen)
            self.state = self.rules.clickListener()

        elif STATE.finish == self.state:
            var = self.finish.draw(self.screen)
            if (var != STATE.finish):
                self.backToMenu()

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                if STATE.game == self.state:
                    self.gameNet.exitFlag = True
                    self.gameNet.leaveServer(self.game.gameID)
                    sleep(0.5)
                    pygame.quit()
                    exit()
                else:
                    pygame.quit()
                    exit()
                # exit()
            # if (event.type == pygame.KEYDOWN):
            #     if (event.key == pygame.K_ESCAPE):
            #         exit() 
            #         pygame.quit()
        pygame.display.flip()

    def winning(self):
        self.finish.setWin(self.game.gameID)
        self.enterFinish()

    def lost(self):
        self.finish.setLost(self.game.gameID)
        self.enterFinish()

    def drawGame(self):
        self.finish.setDraw(self.game.gameID)
        self.enterFinish()

    def enterFinish(self):
        self.state = STATE.finish

    def run(self):
        while self.running:
            self.update()

    def exit(self):
        pygame.quit()
        exit()