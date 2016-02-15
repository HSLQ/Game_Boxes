# -*- coding: utf-8 -*
# Filename: gameNet.py

__author__ = 'Piratf'

from settings import NETWORK
from PodSixNet.Connection import ConnectionListener, connection
import time

class GameNet(ConnectionListener):
    """network part of the game"""
    def __init__(self, controller):
        # super(GameNet, self).__init__()
        self.controller = controller
        self.linked = False

    def connectToServer(self):
        if not self.linked:
            host, port = NETWORK["HOST"], NETWORK["PORT"]
            self.Connect((host, int(port)))
            self.linked = True

    def pump(self):
        if self.linked:
            connection.Pump()
            self.Pump()

    def leaveServer(self, gameID):
        print "leave server"
        self.Send({"action": "leaveRoom", "gameID": gameID})

    # 开启新的游戏房间
    def openRoom(self, level):
        print "open room"
        self.Send({"action": "openRoom", "level": level})

    def placeLine(self, x, y, h, gameID, order):
        print "place line"
        self.Send({"action": "place", "x": x, "y": y, "h": h, "gameID": gameID, "order": order})

    def getRooms(self, matching):
        print "refresh room"
        self.rooms = None
        self.Send({"action": "getRooms"})
        rec = 0
        startTime = time.time()
        while (self.rooms == None):
            self.pump()
            print self.rooms
            if (time.time() - startTime > 1) and rec < 3:
                print "Network error, trying reconnecting"
                self.connectToServer()
                return self.getRooms(matching)
            if (rec > 3):
                matching.rooms = []
                return False
        matching.rooms = self.rooms
        return True

    def Network_setClientID(self, data):
        clientID = data["clientID"]
        self.controller.clientID = clientID
        self.controller.linkSuccess()

    def Network_openRoom(self, data):
        print "server opened"
        self.controller.game.gameID = data["gameID"]

    # data: {"action": "startgame","player":0, "gameID": gameID}
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

    # data: {"action": "setRooms", "rooms": waitGames}
    def Network_setRooms(self, data):
        print "set rooms"
        roomsDict = data["rooms"]
        roomsList = [[k, v] for (k, v) in roomsDict.items()]
        self.rooms = sorted(roomsList)
        print self.rooms