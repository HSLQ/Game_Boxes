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
        self.exitFlag = False

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
        # print "leave server", gameID
        self.Send({"action": "leaveRoom", "gameID": gameID, "channelID": self.controller.channelID})

    # 开启新的游戏房间
    def openRoom(self, level):
        print "open room"
        self.Send({"action": "openRoom", "level": level, "channelID": self.controller.channelID})

    # data: {"action": "place", "x": x, "y": y, "h": h, "point": ret["point"], "gameID": gameID, "order": order}
    def placeLine(self, data, gameID, order):
        data["action"] = "place"
        data["gameID"] = gameID
        data["order"] = order
        print "place line"
        self.Send(data)

    def getRooms(self, matching):
        print "refresh room"
        print self.controller.channelID
        self.rooms = None
        self.Send({"action": "getRooms", "channelID": self.controller.channelID})
        rec = 0
        startTime = time.time()
        while (self.rooms == None):
            self.pump()
            if (time.time() - startTime > 1) and rec < 3:
                print "Network error, trying reconnecting"
                self.connectToServer()
                return self.getRooms(matching)
            if (rec > 3):
                matching.rooms = []
                return False
        matching.rooms = self.rooms
        return True

    def joinRoom(self, roomID):
        channelID = self.controller.channelID
        print "join room", channelID
        self.Send({"action": "joinRoom", "roomID": roomID, "channelID": channelID})

    def Network_setChannelID(self, data):
        channelID = data["channelID"]
        self.controller.channelID = channelID
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

    # data: {"action": "enemy","turn": True, "gameID": gameID, "level": level}
    def Network_enemy(self, data):
        turn = data["turn"]
        self.controller.enemyComming(turn)

    # data: {"action": "joined","turn": False, "gameID": gameID, "level": level}
    def Network_joined(self, data):
        turn = data["turn"]
        level = data["level"]
        gameID = data["gameID"]
        self.controller.joinGame(level, gameID, turn)

    # data: {"action": "flee"}
    def Network_flee(self, data):
        self.exit() if self.exitFlag else self.controller.enterMenu()

    def Network_place(self, data):
        x = data["x"]
        y = data["y"]
        h = data["h"]
        turn = data["turn"]
        point = data["point"]
        order = data["order"]
        self.controller.game.placeLineAnswer(turn, x, y, h, point, order)

    def exit(self):
        self.controller.exit()

    def Network_restart(self, data):
        self.controller.game.restart()
