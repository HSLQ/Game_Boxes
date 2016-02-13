# -*- coding: utf-8 -*
# Filename: main.py

__author__ = 'Piratf'

from settings import WINDOW_WIDTH, WINDOW_HEIGHT, STATE, Enum
from menu import Menu
from setLevel import SetLevel
from settings import SETLEVEL
from rules import Rules
from game import Game
import pygame
from pygame.locals import *

class Main():
    """main loop of the game"""
    def __init__(self):
        pygame.init()
        # 包括读取设置文件，设置游戏基本属性
        self.initAttr()
        # 传递所需的参数，实例化所包含的各个类
        self.initObj()
        self.loadResouce()
        self.initContext()

    def initObj(self):
        # 设置大小，用于背景图片的缩放
        self.menu = Menu(self.width, self.height)
        self.rules = Rules(self.width, self.height)
        self.setLevel = SetLevel(self.width, self.height)
        # self.game = Game(self.level)

    def loadResouce(self):
        pass

    def initContext(self):
        self.screen = pygame.display.set_mode((self.width, self.height), NOFRAME)
        pygame.display.set_caption("Boxes")

        self.clock = pygame.time.Clock();

    def initAttr(self):
        self.width, self.height = WINDOW_WIDTH, WINDOW_HEIGHT
        self.state = STATE.menu
        self.running = True
        self.level = SETLEVEL["DEFAULT_LEVEL"]

    def update(self):
        self.clock.tick(60)
        self.screen.fill(0)

        if STATE.exit == self.state:
            exit()

        elif STATE.setLevel == self.state:
            self.setLevel.draw(self.screen)

            var = self.setLevel.clickListener()
            if isinstance(var, str):
                self.state = var
            elif isinstance(var, Game):
                self.game = var
                self.state = STATE.game
            else:
                raise TypeError, var

        elif STATE.game == self.state:
            self.state = self.game.draw()
            if (self.state != STATE.game):
                self.initContext()

        elif STATE.menu == self.state:
            self.menu.draw(self.screen)
            self.state = self.menu.clickListener()

        elif STATE.rules == self.state:
            self.rules.draw(self.screen)
            self.state = self.rules.clickListener()

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                exit()
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    exit()
                    pygame.quit()
        pygame.display.flip()

    def run(self):
        while self.running:
            self.update()