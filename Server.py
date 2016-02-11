# -*- coding: utf-8 -*
# Filename: Server.py

__author__ = 'Piratf'

import PodSixNet
import PodSixNet.Channel
import PodSixNet.Server
from time import sleep
class ClientChannel(PodSixNet.Channel.Channel):
    def Network(self, data):
        print (data)

    def Network_place(self, data):
    #deconsolidate all of the data from the dictionary
    #horizontal or vertical?
        is_horizontal = data["is_horizontal"]
    #x of placed line
        x = data["x"]
    #y of placed line
        y = data["y"]
    #player number (1 or 0)
        num = data["num"]
    #id of game given by server at start of game
        self.gameID = data["gameID"]
    #tells server to place line
        self._server.placeLine(is_horizontal, x, y, data, self.gameID, num)
     
    def Close(self):
        self._server.close(self.gameID)

class BoxesServer(PodSixNet.Server.Server):
    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        self.games = []
        self.queue = None
        self.currentIndex = 0
 
    channelClass = ClientChannel

    def placeLine(self, is_horizontal, x, y, data, gameID, num):
        game = [a for a in self.games if a.gameID==gameID]
        if len(game)==1:
            game[0].placeLine(is_horizontal, x, y, data, num)
 
    def Connected(self, channel, addr):
        print ('new connection:', channel)
        if (self.queue == None):
            print ("Left")
            self.currentIndex += 1
            channel.gameID = self.currentIndex
            self.queue = Game(channel, self.currentIndex)
        else:
            channel.gameID = self.currentIndex
            print ("Right")
            self.queue.playerR = channel
            self.queue.playerL.Send({"action":"startGame", "player":0, "gameID": self.queue.gameID})
            self.queue.playerR.Send({"action":"startGame", "player":1, "gameID": self.queue.gameID})
            self.games.append(self.queue)
            self.queue = None

    def close(self, gameID):
        try:
            print "close " + str(gameID)
            game = [a for a in self.games if a.gameID == gameID][0]
            game.playerL.Send({"action":"close"})
            game.playerR.Send({"action":"close"})
        except:
            pass

    def tick(self):
        index = 0
        change = 3
        for game in self.games:
            change = 3
            for time in range(2):
                for y in range(6):
                    for x in range(6):
                        if (game.boardH[y][x] and game.boardV[y][x] and game.boardH[y + 1][x] and game.boardV[y][x + 1] and not game.owner[x][y]):
                            if (self.games[index].turn == 1):
                                self.games[index].owner[x][y] = 2;
                                game.playerL.Send({"action":"win", "x":x, "y":y})
                                game.playerR.Send({"action":"lose", "x":x, "y":y})
                                change = 0
                            else:
                                self.games[index].owner[x][y] = 1;
                                game.playerL.Send({"action":"lose", "x":x, "y":y})
                                game.playerR.Send({"action":"win", "x":x, "y":y})
                                change = 1
            self.games[index].turn = change if change != 3 else self.games[index].turn
            self.games[index].playerL.Send({"action":"yourTurn", "torf":True if self.games[index].turn == 0 else False})
            self.games[index].playerR.Send({"action":"yourTurn", "torf":True if self.games[index].turn == 1 else False})
            index += 1
        self.Pump();

class Game():
    """judge obj of each game"""
    def __init__(self, playerL, currentIndex):
        self.turn = 0
        self.owner = [[False for x in range(6)] for y in range(6)]
        self.boardH = [[False for x in range(6)] for y in range(7)]
        self.boardV = [[False for x in range(7)] for y in range(6)]

        self.playerL = playerL
        self.playerR = None

        self.gameID = currentIndex

    def placeLine(self, is_horizontal, x, y, data, num):
        if (num == self.turn):
            self.turn = 0 if self.turn else 1
            print self.turn

            if (is_horizontal):
                self.boardH[y][x] = True
            else:
                self.boardV[y][x] = True

            self.playerL.Send(data)
            self.playerR.Send(data)
            self.playerL.Send({"action":"yourTurn", "torf":True if self.turn == 0 else False})
            self.playerR.Send({"action":"yourTurn", "torf":True if self.turn == 1 else False})

    def sendTurn(self):
        self.playerL.Send({"action":"yourTurn", "torf":True if self.turn == 0 else False})
        self.playerR.Send({"action":"yourTurn", "torf":True if self.turn == 1 else False})

    def sendSquare(self):
        playerL.Send({"action":"win", "x":x, "y":y})
        playerR.Send({"action":"win", "x":x, "y":y})

 
print ("STARTING SERVER ON LOCALHOST")
boxesServe = BoxesServer()
while True:
    boxesServe.tick()
    sleep(0.01)