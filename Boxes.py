# -*- coding: utf-8 -*
# Filename: Boxes.py

__author__ = 'Piratf'

from PodSixNet.Connection import ConnectionListener, connection
from time import sleep
import pygame
import math
import PodSixNet

IMAGE_PATH = "Resource/Image/"
MEDIA_PATH = "Resource/Media/"
SIDE_LENGTH = 3
EDGE_LENGTH = SIDE_LENGTH + 1
STICK_LENGTH = 59
GAP_SIZE = 5
INDICATOR_GAP = 130
PART_LENGTH = STICK_LENGTH + GAP_SIZE

BOARD_LENGTH = PART_LENGTH * SIDE_LENGTH + GAP_SIZE
HUD_HEIGHT = 110

# 记分板各元素的位置
SCORE_TEXT_BOTTOM = 59
SCORE_NUM_BOTTOM = 45
SCORE_TEXT_LEFT = 10
SCORE_NUM_LEFT = 12
SCORE_TEXT_RIGHT = 89
SCORE_NUM_RIGHT = 89

# 放置一条线 10 帧后才能进行下一个动作
JUST_PLACED = 10

WIDTH, HEIGHT = BOARD_LENGTH, BOARD_LENGTH + HUD_HEIGHT

TOTAL_SQUARE = SIDE_LENGTH * SIDE_LENGTH

class BoxesGame(ConnectionListener):
    """drawing lines, make boxes to earn points"""
    def __init__(self):
        pygame.init()

        # 初始化格子数据
        # ---
        self.initBoard()

        self.width, self.height = self.board_length, self.board_length + HUD_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Boxes")

        self.clock = pygame.time.Clock();

        # ---
        
        self.boardH = [[False for x in range(self.level)] for y in range(self.edge_length)]
        self.boardV = [[False for x in range(self.edge_length)] for y in range(self.level)]

        # ---
        # load resources
        self.initGraphics()
        self.initSound()
        pygame.font.init()

        # ---
        # set hud
        # 当前玩家信息
        self.turn = True
        self.myScore = 0
        self.otherScore = 0
        self.pWin = False
        
        self.gameID = None
        self.num = None

        self.justPlaced = 10

        # ---
        # 记录了占领和失去的格子
        self.owner = [[0 for x in range(self.level)] for y in range(self.level)]

        # ---
        self.Connect()
        
        # address=raw_input("Address of Server: ")
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
        # print "Boxes client started"

        # self.waitingToStart()

    def initBoard(self):
        self.level = int(raw_input("input level:"))
        self.edge_length = self.level + 1
        self.board_length = PART_LENGTH * self.level + GAP_SIZE
        self.total_square = self.level * self.level

    def waitingToStart(self):
        self.running=False
        while not self.running:
            self.Pump()
            connection.Pump()
            sleep(0.01)
        # determine attributes from player #
        if self.num == 0:
            self.turn = True
            self.marker = self.greenplayer
            self.othermarker = self.blueplayer
        else:
            self.turn = False
            self.marker = self.blueplayer
            self.othermarker = self.greenplayer

    def HeartBeat(self):
        connection.Pump()
        self.Pump()

    def update(self):
        if (self.myScore + self.otherScore == self.total_square):
            self.pWin = True if self.myScore > self.otherScore else False
            return 1
        self.justPlaced -= 1

        # ---
        self.HeartBeat()

        # ---
        self.clock.tick(60)

        self.screen.fill(0)
        self.drawBoard()
        self.drawHUD()
        self.drawOwnerMap();

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                exit()
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    exit()
                    pygame.quit()

        self.flowLines()
        pygame.display.flip()

    def initGraphics(self):
        self.normalLiveV = pygame.image.load(IMAGE_PATH + "normalline.png")
        self.normallineH = pygame.transform.rotate(pygame.image.load(IMAGE_PATH + "normalline.png"), -90)
        self.bar_doneV = pygame.image.load(IMAGE_PATH +"bar_done.png")
        self.bar_doneH = pygame.transform.rotate(pygame.image.load(IMAGE_PATH +"bar_done.png"), -90)
        self.hoverlineV = pygame.image.load(IMAGE_PATH +"hoverline.png")
        self.hoverlineH = pygame.transform.rotate(pygame.image.load(IMAGE_PATH +"hoverline.png"), -90)
        self.separators = pygame.image.load(IMAGE_PATH + "separators.png")
        self.redindicator = pygame.image.load(IMAGE_PATH + "redindicator.png")
        self.greenindicator = pygame.image.load(IMAGE_PATH + "greenindicator.png")
        self.greenplayer = pygame.image.load(IMAGE_PATH + "greenplayer.png")
        self.blueplayer = pygame.image.load(IMAGE_PATH + "blueplayer.png")
        self.winningscreen = pygame.image.load(IMAGE_PATH + "youwin.png")
        self.gameover = pygame.image.load(IMAGE_PATH + "gameover.png")
        self.score_panel = pygame.image.load(IMAGE_PATH + "score_panel.png")
        self.score_panel = pygame.transform.scale(self.score_panel, (self.board_length, HUD_HEIGHT))

    def initSound(self):
        pygame.mixer.music.load(MEDIA_PATH + "music.wav")
        self.winSound = pygame.mixer.Sound(MEDIA_PATH + 'win.wav')
        self.loseSound = pygame.mixer.Sound(MEDIA_PATH + 'lose.wav')
        self.placeSound = pygame.mixer.Sound(MEDIA_PATH + 'place.wav')
        pygame.mixer.music.play()

    def drawBoard(self):
        for y in range(self.edge_length):
            for x in range(self.level):
                if not self.boardH[y][x]:
                    self.screen.blit(self.normallineH, [x * PART_LENGTH + GAP_SIZE, y * PART_LENGTH])
                else:
                    self.screen.blit(self.bar_doneH, [x * PART_LENGTH + GAP_SIZE, y * PART_LENGTH])
        for y in range(self.level):
            for x in range(self.edge_length):
                if not self.boardV[y][x]:
                    self.screen.blit(self.normalLiveV, [x * PART_LENGTH, y * PART_LENGTH + GAP_SIZE])
                else:
                    self.screen.blit(self.bar_doneV, [x * PART_LENGTH, y * PART_LENGTH + GAP_SIZE])
        #draw separators
        for x in range(self.edge_length):
            for y in range(self.edge_length):
                self.screen.blit(self.separators, [x * PART_LENGTH, y * PART_LENGTH])

    def flowLines(self):
        mouse = pygame.mouse.get_pos()
        xpos = int(math.ceil( (mouse[0] - 32) / float(PART_LENGTH)) )
        ypos = int(math.ceil( (mouse[1] - 32) / float(PART_LENGTH)) )

        is_horizontal = abs(mouse[1] - ypos * PART_LENGTH) < abs(mouse[0] - xpos * PART_LENGTH)

        ypos = ypos - 1 if mouse[1] - ypos * PART_LENGTH < 0 and not is_horizontal else ypos
        xpos = xpos - 1 if mouse[0] - xpos * PART_LENGTH < 0 and is_horizontal else xpos

        board = self.boardH if is_horizontal else self.boardV
        isOutOfBounds = False

        try:
            if not board[ypos][xpos]: self.screen.blit(self.hoverlineH if is_horizontal else self.hoverlineV, [xpos * PART_LENGTH + GAP_SIZE if is_horizontal else xpos * PART_LENGTH, ypos * PART_LENGTH if is_horizontal else ypos * PART_LENGTH + GAP_SIZE])
        except:
            isOutOfBounds = True
            pass
        if not isOutOfBounds:
            alreadyPlaced = board[ypos][xpos]
        else:
            alreadyPlaced = False

        if (pygame.mouse.get_pressed()[0] and not alreadyPlaced and not isOutOfBounds and self.turn == True and self.justPlaced <= 0):
            self.justPlaced = 10
            if (is_horizontal):
                self.boardH[ypos][xpos] = True
                self.Send({"action": "place", "x":xpos, "y":ypos, "is_horizontal": is_horizontal, "gameID": self.gameID, "num": self.num})
            else:
                self.boardV[ypos][xpos] = True
                self.Send({"action": "place", "x":xpos, "y":ypos, "is_horizontal": is_horizontal, "gameID": self.gameID, "num": self.num})

    def drawHUD(self):
        self.screen.blit(self.score_panel, [0, self.board_length])

        # label
        myFont = pygame.font.SysFont(None, 32)
        label = myFont.render("Your Turn:", 1, (255, 255, 255))
        self.screen.blit(label, (10, self.board_length + 15))
        self.screen.blit(self.greenindicator if self.turn else self.redindicator, (INDICATOR_GAP, self.board_length + 10))

        # score
        myFont64 = pygame.font.SysFont(None, 64)
        myFont20 = pygame.font.SysFont(None, 20)

        myScore = myFont64.render(str(self.myScore), 1, (255, 255, 255))        
        otherScore = myFont64.render(str(self.otherScore), 1, (255, 255, 255))
        scoreTextMe = myFont20.render("Your Point", 1, (255, 255, 255))
        scoreTextOther = myFont20.render("Other Player", 1, (255, 255, 255))

        self.screen.blit(scoreTextMe, (SCORE_TEXT_LEFT, self.height - SCORE_TEXT_BOTTOM))
        self.screen.blit(myScore, (SCORE_NUM_LEFT, self.height - SCORE_NUM_BOTTOM))
        self.screen.blit(scoreTextOther, (self.board_length - SCORE_TEXT_RIGHT, self.height - SCORE_TEXT_BOTTOM))
        self.screen.blit(otherScore, (self.board_length - SCORE_TEXT_RIGHT, self.height - SCORE_NUM_BOTTOM))

    def drawOwnerMap(self):
        for x in range(self.level):
            for y in range(self.level):
                if self.owner[x][y] != 0:
                    if self.owner[x][y] == "win":
                        self.screen.blit(self.marker, (x * PART_LENGTH + GAP_SIZE, y * PART_LENGTH + GAP_SIZE))
                    if self.owner[x][y] == "lose":
                        self.screen.blit(self.othermarker, (x * PART_LENGTH + GAP_SIZE, y * PART_LENGTH + GAP_SIZE))

    def Network_startGame(self, data):
        self.running = True
        self.num = data["player"]
        self.gameID = data["gameID"]

    def Network_place(self, data):
        self.placeSound.play()
        #get attributes
        x = data["x"]
        y = data["y"]
        is_horizontal = data["is_horizontal"]
    
        #horizontal or vertical
        if is_horizontal:
            self.boardH[y][x] = True
        else:
            self.boardV[y][x] = True

    def Network_yourTurn(self, data):
        self.turn = data["torf"]

    def Network_win(self, data):
        self.winSound.play()
        self.owner[data["x"]][data["y"]] = "win"
        self.boardH[data["y"]][data["x"]] = True
        self.boardV[data["y"]][data["x"]] = True
        self.boardH[data["y"] + 1][data["x"]] = True
        self.boardV[data["y"]][data["x"] + 1] = True
        self.myScore +=  1

    def Network_lose(self, data):
        self.loseSound.play()
        self.owner[data["x"]][data["y"]] = "lose"
        self.boardH[data["y"]][data["x"]] = True
        self.boardV[data["y"]][data["x"]] = True
        self.boardH[data["y"] + 1][data["x"]] = True
        self.boardV[data["y"]][data["x"] + 1] = True
        self.otherScore += 1

    def Network_close(self, data):
        exit()

    def finished(self):
        self.screen.blit(self.gameover if not self.pWin else self.winningscreen, (0, 0))

        while (1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            pygame.display.flip()
# ---
bg = BoxesGame()
running = True
while (running):
    if bg.update()==1:
        break
bg.finished()
