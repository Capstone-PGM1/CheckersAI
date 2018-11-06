from PodSixNet.Connection import connection, ConnectionListener

from gamestate import *
from time import sleep, time
from datetime import datetime
import sys

class PendingChallenge:
    def __init__(self, challengeTo, challengeFrom, startTime):
        self.challengeTo = challengeTo
        self.challengeFrom = challengeFrom
        self.startTime = startTime

class Client(ConnectionListener):
    def __init__(self, host, port):
        self.Connect((host, port))
        self.pendingChallenge = None
        self.rejectedChallenge = None
        self.hasCurrentGame = False
        self.possibleMoves = None
        self.board = None

    def Network(self, data):
        print
        'network data:', data

    def Network_connected(self, data):
        print
        "connected to the server"

    def Network_error(self, data):
        print
        "error:", data['error'][1]

    def Network_disconnect(self):
        print
        "disconnected from the server"

    def closeConnection(self):
        connection.Send({"action": "disconnect"})

    def Network_receiveId(self, data):
        self.id = data['id']
        print("hello, you have joined the game. You are player " + str(self.id))

    def Loop(self):
        connection.Pump()
        self.Pump()

    def printGame(self, gameDict):
        firstRow = '  '
        for i in range(8):
            firstRow += str(i) + ' '
        print(firstRow)

        for row in range(8):
            rowString = str(row) + ' '
            for column in range(8):
                rowString += gameDict[(row, column)] + " "
            print(rowString)


    # These methods deal with connecting to a multiplayer game

    # When the server sends the list of players, display possible
    # players on the screen
    def Network_getPlayers(self, data):
        self.otherPlayers = list(filter(lambda x: x != str(self.id), data['players']))

    def sendChallenge(self, otherPlayerId):
        self.pendingChallenge = PendingChallenge(otherPlayerId, self.id, datetime.now())
        connection.Send({"action": "getChallenge", "id": self.id, "otherPlayer": int(otherPlayerId)})

    # When receiving a challenge from another player, display the challenger on the screen
    def Network_getChallenge(self, data):
        if not self.pendingChallenge:
            self.pendingChallenge = PendingChallenge(self.id, data['otherPlayerId'], datetime.now())
            print(str(data['otherPlayerId']) + " has invited you to a challenge\n")

    def respondToChallenge(self, response):
        print("in client's respond to challenge")
        print(str(self.id))
        print(str(self.pendingChallenge.challengeFrom))
        print(type(self.pendingChallenge.challengeFrom))
        connection.Send({"action": "getResponseToChallenge", "id": self.id, "response": response, "otherPlayer": self.pendingChallenge.challengeFrom})

    def Network_rejectChallenge(self, data):
        self.pendingChallenge = None
        self.rejectedChallenge = data['playerId']

    def Network_acceptChallenge(self, data):
        self.pendingChallenge = None
        self.hasCurrentGame = True

    def acknowledge_rejected_challenge(self):
        self.rejectedChallenge = None
        print("rejected challenge is now none.")

    # These methods deal with the checkers game.
    # print the game on the screen and highlight possible moves.
    def Network_getPossibleMoves(self, data):
        print("got the game")
        # data['game'] is a {(rowIndex, columnIndex): 'char'} for each item.
        # Characters: x is black, o is red, K is a red king, Q is a black king, and R/B are pieces.
        self.board = data['game']
        if "possibleMoves" in data:
            print("got the possible moves")
            self.possibleMoves = data['possibleMoves']
        else:
            self.possibleMoves = None

    def Network_gameEnd(self, data):
        self.gameOver = True
        self.winner = data['winner']
        self.hasCurrentGame = False

    def sendResponse(self, move):
        print("going to send a response")
        print(move)
        connection.Send({"action": "updateBoard", "move": move, "id": self.id})
        # self.pump()

    # This method deals with the chat room.
    def Network_message(self, data):
        self.latestMessage = {data['playerName']: data['message']}

    def sendMessage(self, message):
        connection.Send({"action": "message", "id": self.id, "message": message})

    def pump(self):
        # Clear pending challenge if the challenge has timed out.
        if self.pendingChallenge and (datetime.now() - self.pendingChallenge.startTime).seconds >= 60:
            self.pendingChallenge = None
        self.Loop()

def startClient():
    #  TODO: make this a real server one day.
    return Client('localhost', 12345)

if __name__ == '__main__':
    c = startClient()

    while 1:
        c.Loop()
        sleep(0.001)