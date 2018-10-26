from PodSixNet.Connection import connection, ConnectionListener

from gamestate import *
from time import sleep
import sys

class Client(ConnectionListener):
    def __init__(self, host, port):
        self.Connect((host, port))

    def Network(self, data):
        print
        'network data:', data

    def Network_connected(self, data):
        print
        "connected to the server"

    def Network_error(self, data):
        print
        "error:", data['error'][1]

    def Network_disconnected(self, data):
        print
        "disconnected from the server"

    def Network_receiveId(self, data):
        self.id = data['id']

    def Loop(self):
        connection.Pump()
        self.Pump()

    # These methods deal with connecting to a multiplayer game

    # When the server sends the list of players, display possible
    # players on the screen
    def Network_getPlayers(self, data):
        print("Available Players: " + ', '.join(data['players']))

    # When receiving a challenge from another player, display the challenger on the screen
    def Network_getChallenge(self, data):
        print(data['playerName'] + " has invited you to a challenge")

    # These methods deal with the checkers game.
    # print the game on the screen and highlight possible moves.
    def Network_getPossibleMoves(self, data):
        # data['game'] is a {(rowIndex, columnIndex): 'char'} for each item.
        # Characters: x is black, o is red, K is a red king, Q is a black king, and R/B are pieces.
        self.printGame(data['game'])
        if "possibleMoves" in data:
            # data['possibleMoves'] = {(startRow, startColumn): [{endRow, endColumn, piecesNumber}]}.
            # It doesn't include pieces that have no possible moves.
            move = get_move_from_player_for_network(data['possibleMoves'])
            # move here expects a {"startRow": row, "startColumn": column, "endRow": row1, "endColumn": column1}
            self.sendResponse(move)

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

    def Network_gameEnd(self, data):
        print(data['endMessage'])

    def sendResponse(self, move):
        connection.Send({"action": "updateBoard", "move": move, "id": self.id})

    # This method deals with the chat room.
    def Network_message(self, data):
        print(data['playerName'] + ": " + data['message'])

    def sendMessage(self, message):
        connection.Send({"action": "message", "id": self.id, "message": message})


if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "host:port")
    print("e.g.", sys.argv[0], "localhost:31425")
else:
    host, port = sys.argv[1].split(":")
    c = Client(host, int(port))
    while 1:
        c.Loop()
        sleep(0.001)