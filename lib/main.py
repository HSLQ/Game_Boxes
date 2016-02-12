# -*- coding: utf-8 -*
# Filename: main.py

__author__ = 'Piratf'

from settings import WINDOW_WIDTH, WINDOW_HEIGHT
import pygame
from menu import Menu 

# set 实现的 枚举类型
class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

STATE = Enum(['menu', 'game', 'setLevel', 'rules', 'matching'])

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

    def loadResouce(self):
        pass

    def initContext(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Boxes")

        self.clock = pygame.time.Clock();

    def initAttr(self):
        self.width, self.height = WINDOW_WIDTH, WINDOW_HEIGHT
        self.state = STATE.menu
        self.running = True

    def update(self):
        self.clock.tick(60)
        self.screen.fill(0)

        if STATE.menu == self.state:
            self.menu.draw(self.screen)
            self.menu.clickListener()
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                exit()
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    exit()
                    pygame.quit()

    def run(self):
        while self.running:
            self.update()