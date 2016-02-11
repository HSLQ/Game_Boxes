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
SIDE_LENGTH = 6
TOTAL_SQUARE = SIDE_LENGTH * SIDE_LENGTH

class BoxesGame(ConnectionListener):
    """drawing lines, make boxes to earn points"""
    def __init__(self):
        pygame.init()
        width, height = 389, 489
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Boxes")

        self.clock = pygame.time.Clock();

        # ---
        
        self.boardH = [[False for x in range(6)] for y in range(7)]
        self.boardV = [[False for x in range(7)] for y in range(6)]

        # ---
        # load resources
        self.initGraphics()
        self.initSound()
        pygame.font.init();

        # ---
        # set hud
        self.turn = True

        self.myScore = 0
        self.otherScore = 0
        self.pWin = False
        self.gameID = None
        self.num = None
        self.justPlaced = 10

        # ---
        self.owner = [[0 for x in range(6)] for y in range(6)]

        # ---
        self.Connect()
        # self.finished();
        self.waitingToStart()

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

    def update(self):
        # self.myScore += 1
        if (self.myScore + self.otherScore == TOTAL_SQUARE):
            self.pWin = True if self.myScore > self.otherScore else False
            return 1
        self.justPlaced -= 1

        # ---
        connection.Pump()
        self.Pump()

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

    def initSound(self):
        pygame.mixer.music.load(MEDIA_PATH + "music.wav")
        self.winSound = pygame.mixer.Sound(MEDIA_PATH + 'win.wav')
        self.loseSound = pygame.mixer.Sound(MEDIA_PATH + 'lose.wav')
        self.placeSound = pygame.mixer.Sound(MEDIA_PATH + 'place.wav')
        pygame.mixer.music.play()

    def drawBoard(self):
        for y in range(7):
            for x in range(6):
                if not self.boardH[y][x]:
                    self.screen.blit(self.normallineH, [x * 64 + 5, y * 64])
                else:
                    self.screen.blit(self.bar_doneH, [x * 64 + 5, y * 64])
        for y in range(6):
            for x in range(7):
                if not self.boardV[y][x]:
                    self.screen.blit(self.normalLiveV, [x * 64, y * 64 + 5])
                else:
                    self.screen.blit(self.bar_doneV, [x * 64, y * 64 + 5])
        #draw separators
        for x in range(7):
            for y in range(7):
                self.screen.blit(self.separators, [x * 64, y * 64])

    def flowLines(self):
        mouse = pygame.mouse.get_pos()
        xpos = int(math.ceil( (mouse[0] - 32) / 64.0) )
        ypos = int(math.ceil( (mouse[1] - 32) / 64.0) )

        is_horizontal = abs(mouse[1] - ypos * 64) < abs(mouse[0] - xpos * 64)

        ypos = ypos - 1 if mouse[1] - ypos * 64 < 0 and not is_horizontal else ypos
        xpos = xpos - 1 if mouse[0] - xpos * 64 < 0 and is_horizontal else xpos

        board = self.boardH if is_horizontal else self.boardV
        isOutOfBounds = False

        try:
            if not board[ypos][xpos]: self.screen.blit(self.hoverlineH if is_horizontal else self.hoverlineV, [xpos * 64 + 5 if is_horizontal else xpos * 64, ypos * 64 if is_horizontal else ypos * 64 + 5])
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
        self.screen.blit(self.score_panel, [0, 389])

        # label
        myFont = pygame.font.SysFont(None, 32)
        label = myFont.render("Your Turn:", 1, (255, 255, 255))
        self.screen.blit(label, (10, 400))
        self.screen.blit(self.greenindicator if self.turn else self.redindicator, (130, 395))

        # score
        myFont64 = pygame.font.SysFont(None, 64)
        myFont20 = pygame.font.SysFont(None, 20)

        myScore = myFont64.render(str(self.myScore), 1, (255, 255, 255))        
        otherScore = myFont64.render(str(self.otherScore), 1, (255, 255, 255))
        scoreTextMe = myFont20.render("You", 1, (255, 255, 255))
        scoreTextOther = myFont20.render("Other Player", 1, (255, 255, 255))

        self.screen.blit(scoreTextMe, (10, 428))
        self.screen.blit(myScore, (12, 443))
        self.screen.blit(scoreTextOther, (300, 428))
        self.screen.blit(otherScore, (300, 443))

    def drawOwnerMap(self):
        for x in range(6):
            for y in range(6):
                if self.owner[x][y] != 0:
                    if self.owner[x][y] == "win":
                        self.screen.blit(self.marker, (x * 64 + 5, y * 64 + 5))
                    if self.owner[x][y] == "lose":
                        self.screen.blit(self.othermarker, (x * 64 + 5, y * 64 + 5))

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
