# -*- coding: utf-8 -*
# Filename: hud.py

__author__ = 'Piratf'

from settings import HUD
from background import Background
from centeredImage import CenteredImage
from centeredText import CenteredText
import pygame

class Hud(object):
    """hud panel"""
    def __init__(self, (width, height), (x, y)):
        # super(Hud, self).__init__()
        self.initAttr((width, height), (x, y))
        self.initElement()
    
    def initAttr(self, (width, height), (x, y)):
        self.width = HUD["HUD_WIDTH"]
        self.height = height
        self.x, self.y = x, y
        self.started = False
        self.myScore = 0
        self.otherScore = 0

    def initElement(self):
        # 背景
        backgroundImg = pygame.transform.scale(HUD["HUD_BACKGROUND_IMAGE"], (self.width, self.height))
        self.background = Background((self.width, self.height), (self.x, self.y))
        self.background.setColor(backgroundImg)

        # 回合指示
        self.setMark(False)
        offSetLeft = HUD["MARK_TEXT_FONTS"].size(HUD["MARK_TEXT_CONTENT"])[0] / 2
        self.markText = CenteredText(HUD["MARK_TEXT_FONTS"], HUD["MARK_TEXT_CONTENT"], (offSetLeft + 10, self.height / 2 - 3))

        # 得分，默认 0 分开始
        self.setScore()

        # 两块 label
        [myLabelOffSetLeft, myLabelOffSetTop] = [var / 2 for var in HUD["LABEL_FONTS"].size(HUD["MY_SCORE_LABEL_CONTENT"])]
        self.myScoreLabel = CenteredText(HUD["LABEL_FONTS"], 
            HUD["MY_SCORE_LABEL_CONTENT"], 
            (myLabelOffSetLeft + HUD["MY_SCORE_LABEL_OFFSET_LEFT"], 
                myLabelOffSetTop + HUD["MY_SCORE_LABEL_OFFSET_TOP"]))
        self.initWaitingLabel()

    def setMark(self, Turn):
        if Turn:
             self.mark = CenteredImage(HUD["GREEN_PILOT_LAMP"], (HUD["LAMP_WIDTH"], HUD["LAMP_HEIGHT"]), (self.width - 20, self.height / 2))
        else:
             self.mark = CenteredImage(HUD["RED_PILOT_LAMP"], (HUD["LAMP_WIDTH"], HUD["LAMP_HEIGHT"]), (self.width - 20, self.height / 2))

    def setScore(self, myScore = 0, otherScore = 0):
        self.myScore, self.otherScore = myScore, otherScore
        # 根据分数内容即时计算位置
        [myScoreOffSetLeft, myScoreOffSetTop] = [var / 2 for var in HUD["MARK_TEXT_FONTS"].size(str(myScore))]
        self.myScoreText = CenteredText(HUD["SCORE_TEXT_FONTS"], str(self.myScore), (myScoreOffSetLeft + HUD["MY_SCORE_TEXT_OFFSET_LEFT"], myScoreOffSetTop + HUD["MY_SCORE_TEXT_OFFSET_TOP"]))
        [otherScoreOffSetLeft, otherScoreOffSetTop] = [var / 2 for var in HUD["MARK_TEXT_FONTS"].size(str(otherScore))]
        self.otherScoreText = CenteredText(HUD["SCORE_TEXT_FONTS"], str(self.otherScore), (otherScoreOffSetLeft + HUD["OTHER_SCORE_TEXT_OFFSET_LEFT"], self.height - otherScoreOffSetTop - HUD["OTHER_SCORE_TEXT_OFFSET_BOTTOM"]))

    def addScore(self):
        self.setScore(self.myScore + 1, self.otherScore)
        print self.myScore, self.otherScore

    def enemyAddScore(self):
        self.setScore(self.myScore, self.otherScore + 1)
        print self.myScore, self.otherScore

    def initWaitingLabel(self):
        otherLabelOffSet = HUD["WAIT_BATTLE_LABEL_FONT"].size(HUD["WAIT_BATTLE_LABEL_CONTENT"])
        [otherLabelOffSetLeft, otherLabelOffSetBottom] = [
        self.x + otherLabelOffSet[0] / 2. + 
            HUD["WAIT_BATTLE_LABEL_OFFSET_LEFT"],
        self.y + otherLabelOffSet[1] / 2. + 
            HUD["WAIT_BATTLE_LABEL_OFFSET_BOTTOM"]
        ]
        self.waitingLabel = CenteredText(HUD["WAIT_BATTLE_LABEL_FONT"], 
            HUD["WAIT_BATTLE_LABEL_CONTENT"], 
            (otherLabelOffSetLeft, self.height - otherLabelOffSetBottom))

    def startGame(self):
        self.started = True
        [otherLabelOffSetLeft, otherLabelOffSetTop] = [var / 2 for var in HUD["LABEL_FONTS"].size(HUD["OTHER_SCORE_LABEL_CONTENT"])]
        self.otherScoreLabel = CenteredText(HUD["LABEL_FONTS"], 
            HUD["OTHER_SCORE_LABEL_CONTENT"], 
            (otherLabelOffSetLeft + HUD["OTHER_SCORE_LABEL_OFFSET_LEFT"], 
                self.height - otherLabelOffSetTop - HUD["OTHER_SCORE_LABEL_OFFSET_BOTTOM"]))

    def drawScore(self, screen):
        self.myScoreText.draw(screen)
        if self.started:
            self.otherScoreText.draw(screen)
            self.otherScoreLabel.draw(screen)
        else:
            self.waitingLabel.draw(screen)
        self.myScoreLabel.draw(screen)

    def restart(self):
        self.started = False
        self.setScore(0, 0)

    def draw(self, screen):
        # screen.set_clip(self.x, self.y, self.width, self.height)
        self.background.draw(screen)
        self.mark.draw(screen)
        self.markText.draw(screen)

        self.drawScore(screen)

        