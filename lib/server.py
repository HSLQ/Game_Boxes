# -*- coding: utf-8 -*
# Filename: server.py

__author__ = 'Piratf'

import PodSixNet.Channel
import PodSixNet.Server
from time import sleep

class ClientChannel(PodSixNet.Channel.Channel):
    def Network(self, data):
        print data

    def Close(self):
        print "connent colsed"
        # self._server.leaveRoom(self.gameID)
        # self._server.close(self.gameid)

    # data: {"action":"openRoom", "level": level, "channelID": channelID}
    def Network_openRoom(self, data):
        print "open room"
        level = data["level"]
        channelID = data["channelID"]
        # 回调 给开启了游戏的链接设置游戏 id
        self._server.openRoom(level, channelID, self)

    # data: {"action": "leaveRoom", "gameID": self.gameID}
    def Network_leaveRoom(self, data):
        gameID = data["gameID"]
        print gameID, "leave game"
        self._server.leaveRoom(gameID)

    def Network_place(self, data):
        #x of placed line
        x = data["x"]
        #y of placed line
        y = data["y"]
        #horizontal or vertical?
        h = data["h"]
        #id of game given by server at start of game
        self.gameID = data["gameID"]
        #player number (1 or 0)
        order = data["order"]
        #tells server to place line
        self._server.placeLine(x, y, h, self.gameID, order)

    # data: {"action":"joinRoom", "gameID": gameID}
    def Network_joinRoom(self, data):
        print "join game"
        self._server.joinRoom(gameID)

    # data: {"action": "getRooms", "channelID", channelID}
    def Network_getRooms(self, data):
        print "get rooms"
        channelID = data["channelID"]
        self._server.getRooms(channelID)


class BoxesServer(PodSixNet.Server.Server):
    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        self.games = {}
        self.waitGames = {}
        self.channelObjs = {}
        self.queue = None
        self.currentGameIndex=0
        self.currentChannelIndex = 0

    channelClass = ClientChannel
 
    def Connected(self, channel, addr):
        print 'new connection:', channel
        self.currentChannelIndex += 1
        self.channelObjs[self.currentChannelIndex] = channel
        self.setChannelID(self.currentChannelIndex)
        print self.currentChannelIndex

    def setChannelID(self, channelID):
        self.channelObjs[channelID].Send({"action": "setChannelID", "channelID": channelID})
        
    def openRoom(self, level, channelID, listener):
        print "start game"
        gameID = self.currentGameIndex
        listener.gameID = gameID
        self.channelObjs[channelID].Send({"action": "openRoom", "gameID": gameID})
        self.waitGames[gameID] = level
        self.games[gameID] = GameJudge(self.channelObjs[channelID], self.currentGameIndex, level)
        self.currentGameIndex += 1
        print self.waitGames
    
    def joinRoom(self, gameID):
        print "join game"
        level = 0
        try:
            level = self.waitGames[gameID]
        except Exception as e:
            raise
        else:
            return
        finally:
            pass

        self.games[gameID].player1 = channel
        self.queue.player0.Send({"action": "startgame","player":0, "gameID": gameID})
        self.queue.player1.Send({"action": "startgame","player":1, "gameID": gameID})
        # 从等待集合里去除
        del self.waitGames[gameID]

    def leaveRoom(self, gameID):
        if self.waitGames.has_key(gameID):
            del self.waitGames[gameID]

    def placeLine(self, x, y, h, gameID, order):
        print x, y

    def getRooms(self, channelID):
        print channelID
        print self.channelObjs
        print self.waitGames
        channel = self.channelObjs[channelID]
        print channel
        channel.Send({"action": "setRooms", "rooms": self.waitGames})

class GameJudge:
    def __init__(self, player0, currentGameIndex, level):
        
# whose turn (1 or 0)
        self.turn = 0
#owner map
        self.owner = [[False for x in range(level)] for y in range(level)]
        
# Seven lines in each direction to make a six by six grid.
        # self.boardh = [[False for x in range(6)] for y in range(7)]
        # self.boardv = [[False for x in range(7)] for y in range(6)]
        
#initialize the players including the one who started the game
        self.player0 = player0
        self.player1 = None
        
#gameID of game
        self.gameID = currentGameIndex

print ("STARTING SERVER ON LOCALHOST")
# boxesServe = BoxesServer()
# try:
host, port="localhost", 8000
# address=raw_input("Host:Port (localhost:8000): ")
# if not address:
#     host, port="localhost", 8000
# else:
#     host,port=address.split(":")
boxesServe = BoxesServer(localaddr=(host, int(port)))

while True:
    boxesServe.Pump();
    sleep(0.01)