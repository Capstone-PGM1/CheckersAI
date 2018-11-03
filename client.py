from PodSixNet.Connection import connection, ConnectionListener

from gamestate import *
from time import sleep
import sys

class Client(ConnectionListener):
    def __init__(self, host, port):
        self.Connect((host, port))
        self.hasChallenge = False

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

    def Loop(self):
        connection.Pump()
        self.Pump()

    # These methods deal with connecting to a multiplayer game

    # When the server sends the list of players, display possible
    # players on the screen
    def Network_getPlayers(self, data):
        self.otherPlayers = list(filter(lambda x: x != str(self.id), data['players']))

    def sendChallenge(self, otherPlayerId):
        self.hasChallenge = True
        self.challenger = otherPlayerId
        connection.Send({"action": "getChallenge", "id": self.id, "otherPlayer": int(otherPlayerId)})

    # When receiving a challenge from another player, display the challenger on the screen
    def Network_getChallenge(self, data):
        if not self.hasChallenge:
            self.hasChallenge = True
            self.challengeFrom = (data['playerName'])
            print(str(data['playerName']) + " has invited you to a challenge\n")

    def respondToChallenge(self, otherPlayer, response):
        self.hasChallenge = False
        connection.Send({"action": "getResponseToChallenge", "otherPlayer": otherPlayer, "id": self.id, "accept": response})

    def Network_rejectChallenge(self, data):
        self.hasChallenge = False
        self.rejectedChallenge = data['playerId']

    # These methods deal with the checkers game.
    # print the game on the screen and highlight possible moves.
    def Network_getPossibleMoves(self, data):
        # data['game'] is a {(rowIndex, columnIndex): 'char'} for each item.
        # Characters: x is black, o is red, K is a red king, Q is a black king, and R/B are pieces.
        self.game = data['game']
        if "possibleMoves" in data:
            self.possibleMoves = data['possibleMoves']

    def Network_gameEnd(self, data):
        self.gameOver = True
        self.winner = data['winner']

    def sendResponse(self, move):
        connection.Send({"action": "updateBoard", "move": move, "id": self.id})

    # This method deals with the chat room.
    def Network_message(self, data):
        self.latestMessage = {data['playerName']: data['message']}

    def sendMessage(self, message):
        connection.Send({"action": "message", "id": self.id, "message": message})

    def pump(self):
        self.Loop()

def startClient():
    #  TODO: make this a real server one day.
    return Client('localhost', 12345)

if __name__ == '__main__':
    c = startClient()

    while 1:
        c.Loop()
        sleep(0.001)