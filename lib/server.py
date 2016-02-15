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
        print "leaving"
        # self._server.close(self.gameid)

    # data: {"action": "leaveGame", "gameID": self.gameID}
    # 玩家在匹配之前离开游戏
    def Network_leaveGame(self, data):
        print "leave game"
        gameID = data["gameID"]
        self._server.leaveGame(gameID)

    # data: {"action":"startGame", "level": level}
    def Network_startGame(self, data):
        level = data["level"]
        self._server.startGame(level)

    # data: {"action":"joinGame", "gameID": gameID}
    def Network_joinGame(self, data):
        print "join game"
        self._server.joinGame(gameID)

    def Network_getRooms(self, data):
        print "get rooms"
        self._server.getRooms()
 
class BoxesServer(PodSixNet.Server.Server):
    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        self.games = {}
        self.waitGames = {}
        self.queue = None
        self.currentIndex=0

    channelClass = ClientChannel
 
    def Connected(self, channel, addr):
        print 'new connection:', channel
        self.currentChannel = channel
        
    def startGame(self, level):
        print "start game"
        gameID = self.currentIndex
        self.currentChannel.gameID = gameID
        self.waitGames[gameID] = level
        self.games[gameID] = Game(self.currentChannel, self.currentIndex, level)
    
    def joinGame(self, gameID):
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

    def leaveGame(self, gameID):
        if self.waitGames.has_key(gameID):
            del self.waitGames[gameID]

    def getRooms(self):
        print self.waitGames
        self.currentChannel.Send({"action": "setRooms", "rooms": self.waitGames})

class Game:
    def __init__(self, player0, currentIndex, level):
        
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
        self.gameID = currentIndex

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