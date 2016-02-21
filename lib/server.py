# -*- coding: utf-8 -*
# Filename: server.py

__author__ = 'Piratf'

import PodSixNet.Channel
import PodSixNet.Server
from sliceable_deque import sliceable_deque
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

    # data: {"action": "getRooms", "page": page, "num": num, "channelID": self.controller.channelID}
    def Network_getRooms(self, data):
        print "get rooms"
        channelID = data["channelID"]
        page = data["page"]
        num = data["num"]
        self._server.getRooms(channelID, page, num)


class BoxesServer(PodSixNet.Server.Server):
    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        self.games = {}
        self.waitGames = {}
        self.waitGamesDeque = sliceable_deque()
        self.channelObjs = {}
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
        # 操作等待集合
        self.addWaitingRoom(gameID, level)
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
        level = currentGame.level


        # 主场玩家
        homeChannel = currentGame.player0

        # 设置客场玩家
        currentGame.player1 = awayChannel
        homeChannel.Send({"action": "enemy", "turn": currentGame.turn, "gameID": gameID, "level": level})
        awayChannel.Send({"action": "joined", "turn": not currentGame.turn, "gameID": gameID, "level": level})

        # 从等待集合里去除
        self.deleteWaitingRoom(gameID, level)

    def addWaitingRoom(self, gameID, level):
        self.waitGames[gameID] = level
        self.waitGamesDeque.append((gameID, level))

    def deleteWaitingRoom(self, gameID, level):
        del self.waitGames[gameID]
        self.waitGamesDeque.remove((gameID, level))

    def deleteRoom(self, gameID):
        if self.waitGames.has_key(gameID):
            # 操作等待集合
            self.deleteWaitingRoom(gameID)
            del self.games[gameID]

    def leaveRoom(self, gameID, channelID):
        print "sever"
        print gameID, channelID

        channel = self.channelObjs[channelID]
        game = self.games[gameID]

        print gameID, channelID
        if (channel == game.player0):
            print "home leaving room"
            self.addWaitingRoom(gameID, game.level)
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
            self.addWaitingRoom(gameID, game.level)
            game.player1.Send({"action": "flee"})
            game.player0.Send({"action": "restart"})
            game.player1 = None

    def getScore(self, game, point, order):
        if point == None: 
            return
        vPos = int(point["y"])
        hPos = int(point["x"])
        print "getScore: ", vPos, hPos
        # 系统棋盘记录得分
        game.owner[vPos][hPos] = True
        # 系统玩家得分 
        if 0 == order:
            game.addScore0()
        else:
            game.addScore1()

    def placeLine(self, x, y, h, point, gameID, order):
        print "server"
        game = self.games[gameID]
        # 出现有玩家得分

        if point[0] != None or point[1] != None:
            self.getScore(game, point[0], order)
            self.getScore(game, point[1], order)
            # 玩家得分时可以再进行一个回合
            game.turn = not game.turn
        home = game.player0
        away = game.player1
        game.turn = not game.turn
        home.Send({"action":"place", "turn": game.turn, "x": x, "y": y, "h": h, "point": point, "order": order})
        if away != None:
            away.Send({"action":"place", "turn": not game.turn, "x": x, "y": y, "h": h, "point": point, "order": order})
        # 判断胜负逻辑
        if game.win():
            if (game.player0Score > game.player1Score):
                print gameID, "player0 win"
                # 主场玩家胜利
                game.player0.Send({"action": "youwin"})
                # 客场玩家胜利
                game.player1.Send({"action": "youlose"})
            elif (game.player1Score > game.player0Score):
                print gameID, "player1 win"
                game.player0.Send({"action": "youlose"})
                game.player1.Send({"action": "youwin"})
            else:
                # 平局
                print gameID, "drawGame"
                game.player0.Send({"action": "drawGame"})
                game.player1.Send({"action": "drawGame"})

    def getRooms(self, channelID, page, num):
        print self.waitGames
        print "server"
        channel = self.channelObjs[channelID]

        startID = page * num
        endID = page * num + num
        quelen = len(self.waitGamesDeque)
        print "startID", startID
        print "endID", endID
        print "queue len", quelen
        rooms = []

        hasLastPage, hasNextPage = True, True

        if startID <= 0:
            hasLastPage = False
        if quelen < endID:
            hasNextPage = False

        if quelen <= startID:
            print "none"
            rooms = []
        elif quelen < endID:
            rooms = self.waitGamesDeque[startID: quelen]
        else:
            rooms = self.waitGamesDeque[startID: endID]
        print "send"
        rooms = list(rooms)
        print rooms
        channel.Send({"action": "setRooms", "rooms": rooms, "l": hasLastPage, "n": hasNextPage})


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
        self.point = 0
        self.player0Score = 0
        self.player1Score = 0

    def win(self):
        return self.point >= self.level * self.level

    def addScore0(self):
        self.point += 1
        self.player0Score += 1
        self.player0.Send({"action":"addScore"})
        self.player1.Send({"action":"enemyAddScore"})

    def addScore1(self):
        self.point += 1
        self.player1Score += 1
        self.player0.Send({"action":"enemyAddScore"})
        self.player1.Send({"action":"addScore"})

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