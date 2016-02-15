# -*- coding: utf-8 -*
# Filename: server.py

__author__ = 'Piratf'

import PodSixNet.Channel
import PodSixNet.Server
from time import sleep

class ClientChannel(PodSixNet.Channel.Channel, object):
    def __init__(self, *args, **kwargs):
        super(ClientChannel, self).__init__(*args, **kwargs)

    def Network(self, data):
        print data

    def Close(self):
        print "connent closed"

    # data: {"action":"openRoom", "level": level, "channelID": channelID}
    def Network_openRoom(self, data):
        print "open room"
        level = data["level"]
        channelID = data["channelID"]
        # 回调 给开启了游戏的链接设置游戏 id
        self._server.openRoom(level, channelID, self)

    # data: {"action": "leaveRoom", "gameID": gameID, "channelID": channelID}
    def Network_leaveRoom(self, data):
        print "leave Room"
        gameID = data["gameID"]
        channelID = data["channelID"]
        print gameID, "leave room"
        self._server.leaveRoom(gameID, channelID)

    # data: {"action": "place", "x": x, "y": y, "h": h, "point": ret["point"], "gameID": gameID, "order": order}
    def Network_place(self, data):
        #x of placed line
        x = data["x"]
        #y of placed line
        y = data["y"]
        #horizontal or vertical?
        h = data["h"]
        #id of game given by server at start of game
        self.gameID = data["gameID"]

        point = data["point"]
        #player number (1 or 0)
        order = data["order"]
        #tells server to place line
        self._server.placeLine(x, y, h, point, self.gameID, order)

    # data: {"action":"joinRoom", "roomID": gameID, "channelID": channelID}
    def Network_joinRoom(self, data):
        print "join room"
        gameID = data["roomID"]
        channelID = data["channelID"]
        self._server.joinRoom(gameID, channelID, self)

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
        print "new room opened"
        gameID = self.currentGameIndex
        listener.gameID = gameID
        listener.channelID = channelID
        channel = self.channelObjs[channelID]
        channel.gameID = gameID
        channel.Send({"action": "openRoom", "gameID": gameID})
        self.waitGames[gameID] = level
        self.games[gameID] = GameJudge(channel, gameID, level)
        self.currentGameIndex += 1
        print self.waitGames
    
    def joinRoom(self, gameID, channelID, listener):
        print "server"
        print "gameID", gameID, "channelID", channelID
        listener.gameID = gameID
        listener.channelID = channelID
        # 获取的是 加入游戏的客户端对象
        if channelID in self.channelObjs.keys():
            awayChannel = self.channelObjs[channelID]
        else:
            print "**error channel"
            awayChannel = None

        currentGame = self.games[gameID]
        # 主场客户端对象
        homeChannel = currentGame.player0
        homeChannel.gameID = gameID

        level = currentGame.level

        # 设置客场玩家
        currentGame.player1 = awayChannel
        awayChannel.gameID = gameID
        homeChannel.Send({"action": "enemy", "turn": currentGame.turn, "gameID": gameID, "level": level})
        awayChannel.Send({"action": "joined", "turn": not currentGame.turn, "gameID": gameID, "level": level})

        # 从等待集合里去除
        del self.waitGames[gameID]

    def deleteRoom(self, gameID):
        if self.waitGames.has_key(gameID):
            del self.waitGames[gameID]
            del self.games[gameID]

    def leaveRoom(self, gameID, channelID):
        print "sever"
        print gameID, channelID

        channel = self.channelObjs[channelID]
        game = self.games[gameID]

        print gameID, channelID
        if (channel == game.player0):
            print "home leaving room"
            self.waitGames[gameID] = game.level
            game.player0.Send({"action": "flee"})
            # 客场玩家成为房主
            if (game.player1 != None):
                game.player0.Send({"action": "flee"})
                game.player0 = game.player1
                game.player1 = None
                game.player0.Send({"action": "restart"})
            else:
                # 如果没有客场玩家则删除房间
                self.deleteRoom(gameID)
        else:
            print "away leaving room"
            # 客场玩家逃跑
            self.waitGames[gameID] = game.level
            game.player1.Send({"action": "flee"})
            game.player0.Send({"action": "restart"})

    def placeLine(self, x, y, h, point, gameID, order):
        print "server"
        game = self.games[gameID]
        if point != None:
            vPos = int(point["y"])
            hPos = int(point["x"])
            print vPos, hPos
            game.owner[vPos][hPos] = True
        home = game.player0
        away = game.player1
        game.turn = not game.turn
        home.Send({"action":"place", "turn": game.turn, "x": x, "y": y, "h": h, "point": point, "order": order})
        if away != None:
            away.Send({"action":"place", "turn": not game.turn, "x": x, "y": y, "h": h, "point": point, "order": order})

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
        # 主场玩家先出手
        self.turn = True
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
        self.level = level


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