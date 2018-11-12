from PodSixNet.Connection import connection, ConnectionListener

from gamestate import *
from time import sleep, time
from datetime import datetime
import sys

class PendingChallenge:
    def __init__(self, challengeTo, challengeFrom, startTime):
        self.challenge_to = challengeTo
        self.challenge_from = challengeFrom
        self.start_time = startTime

class Client(ConnectionListener):
    def __init__(self, host, port):
        self.Connect((host, port))
        self.pending_challenge = None
        self.rejected_challenge = None
        self.has_current_game = False
        self.possible_moves = None
        self.board = None
        self.messages = []

    def Network(self, data):
        print
        'network data:', data

    def Network_connected(self, data):
        print
        "connected to the server"

    def Network_error(self, data):
        print
        "error:", data['error'][1]
        raise ConnectionError

    def Network_disconnect(self):
        print
        "disconnected from the server"

    def __del__(self):
        connection.Send({"action": "disconnect"})

    def Network_receiveId(self, data):
        self.id = data['id']
        print("hello, you have joined the game. You are player " + str(self.id))

    def Loop(self):
        connection.Pump()
        self.Pump()

    # These methods deal with connecting to a multiplayer game

    # When the server sends the list of players, display possible
    # players on the screen
    def Network_getPlayers(self, data):
        self.other_players = list(filter(lambda x: x != str(self.id), data['players']))

    def send_challenge(self, otherPlayerId):
        self.pending_challenge = PendingChallenge(otherPlayerId, self.id, datetime.now())
        connection.Send({"action": "getChallenge", "id": self.id, "otherPlayer": int(otherPlayerId)})

    # When receiving a challenge from another player, display the challenger on the screen
    def Network_getChallenge(self, data):
        if not self.pending_challenge:
            self.pending_challenge = PendingChallenge(self.id, data['otherPlayerId'], datetime.now())

    def respond_to_challenge(self, response):
        connection.Send({"action": "getResponseToChallenge", "id": self.id, "response": response, "otherPlayer": self.pending_challenge.challenge_from})
        self.pending_challenge = None

    def Network_rejectChallenge(self, data):
        self.pending_challenge = None
        self.rejected_challenge = data['playerId']

    def Network_acceptChallenge(self, data):
        self.pending_challenge = None
        self.has_current_game = True

    def acknowledge_rejected_challenge(self):
        self.rejected_challenge = None

    def Network_closeGame(self, data):
        self.messages.append("{}: {}".format(data['playerName'], data['message']))
        self.has_current_game = False
        self.possible_moves = None
        self.board = None
        self.messages = []

    # These methods deal with the checkers game.
    def Network_getPossibleMoves(self, data):
        # data['game'] is a {(rowIndex, columnIndex): 'char'} for each item.
        # Characters: x is black, o is red, K is a red king, Q is a black king, and R/B are pieces.
        self.board = data['game']
        if "possibleMoves" in data:
            self.possible_moves = data['possibleMoves']
        else:
            self.possible_moves = None

    def Network_gameEnd(self, data):
        self.gameOver = True
        self.winner = data['winner']
        self.has_current_game = False

    def update_game_state_with_move(self, start_row, start_column, end_row, end_column):
        connection.Send({"action": "updateBoard", "move": {"startRow": start_row, "startColumn": start_column, "endRow": end_row, "endCol": end_column}, "id": self.id})

    # This method deals with the chat room.
    def Network_message(self, data):
        self.messages.append("{}: {}".format(data['playerName'], data['message']))

    def sendMessage(self, message):
        connection.Send({"action": "message", "id": self.id, "message": message})

    def pump(self):
        # Clear pending challenge if the challenge has timed out.
        if self.pending_challenge and (datetime.now() - self.pending_challenge.start_time).seconds >= 60:
            self.pending_challenge = None
        self.Loop()

def startClient():
    #  TODO: make this a real server one day.
    return Client('localhost', 12345)

if __name__ == '__main__':
    c = startClient()

    while 1:
        c.Loop()
        sleep(0.001)