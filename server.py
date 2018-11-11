from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

from gamestate import *

from time import sleep
import sys

class RoomInfo:
    def __init__(self, player0, player1, game):
        self.player0 = player0
        self.player1 = player1
        self.game = game

    def __repr__(self):
        return "player0: " + str(self.player0) + "\nplayer1: " + str(self.player0)

class ClientChannel(Channel):
    def __init__(self, *args, **kwargs):
        self.nickname = "anonymous"
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        print("closing channel")
        if self.id in self._server.playerIdToRoom:
            self._server.deleteGame(self._server.playerIdToRoom[self.id], str(self.id) + " has left the game.")
        self._server.playerIdToPlayerChannel.pop(self.id)
        self._server.sendPlayers()

    def Network_getChallenge(self, data):
        print('received a challenge')
        self._server.sendChallenge(data['id'], data['otherPlayer'])

    def Network_getResponseToChallenge(self, data):
        if data['response']:
            self._server.startGame(data['otherPlayer'], data['id'])
        else:
            self._server.rejectChallenge(data['id'], data['otherPlayer'])

    def Network_updateBoard(self, data):
        # print('received a move')
        self._server.updateBoard(data['id'], data['move'])

    def Network_message(self, data):
        self._server.sendToPlayersInGame(data['playerId'], {"action": 'message', "message": data['message'], "playerName": str(data['playerId'])})

    def Network_disconnect(self):
        self.Close()

class CheckersServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.playerIdToPlayerChannel = dict()
        self.playerIdToRoom = dict()
        self.counter = 0
        self.nextId = 0

    def Connected(self, channel, addr):
        playerId = self.nextId
        self.nextId += 1
        self.playerIdToPlayerChannel[playerId] = channel
        channel.id = playerId

        channel.Send({"action": "receiveId", "id": playerId})
        self.sendPlayers()

    # These methods have to do with connecting the game for many players.
    def sendPlayers(self):
        # send something to both players in the game.
        for playerId, channel in self.playerIdToPlayerChannel.items():
            if playerId not in self.playerIdToRoom:
                x = list(map(lambda y: str(y), filter(lambda x: x not in self.playerIdToRoom, self.playerIdToPlayerChannel.keys())))
                channel.Send({"action": "getPlayers", "players": x})

    def sendChallenge(self, playerId, otherPlayerId):
        # make sure the other player is not already in a game and that the other player exists.
        if otherPlayerId not in self.playerIdToRoom and otherPlayerId in self.playerIdToPlayerChannel:
            self.playerIdToPlayerChannel[otherPlayerId].Send({"action": "getChallenge", "otherPlayerId": playerId})

    def rejectChallenge(self, playerId, otherPlayerId):
        self.playerIdToPlayerChannel[otherPlayerId].Send({"action": "rejectChallenge", "playerId": playerId})

    # These methods have to do with playing the game
    def startGame(self, player0, player1):
        room = RoomInfo(player0, player1, GameState())
        self.playerIdToRoom[player0] = room
        self.playerIdToRoom[player1] = room

        self.sendBoardToPlayers(player0)

        self.sendToPlayersInGame(player0, {"action": "acceptChallenge"})

    def sendBoardToPlayers(self, player):
        print("sending the board to the players")
        room = self.playerIdToRoom[player]

        if room.game.activePlayer == 0:
            self.playerIdToPlayerChannel[room.player0].Send(
                {"action": "getPossibleMoves", "game": room.game.get_board_for_network(), "possibleMoves": room.game.send_possible_moves_for_network()})
            self.playerIdToPlayerChannel[room.player1].Send(
                {"action": "getPossibleMoves", "game": room.game.get_board_for_network()})
        else:
            self.playerIdToPlayerChannel[room.player1].Send(
                {"action": "getPossibleMoves", "game": room.game.get_board_for_network(), "possibleMoves": room.game.send_possible_moves_for_network()})
            self.playerIdToPlayerChannel[room.player0].Send(
                {"action": "getPossibleMoves", "game": room.game.get_board_for_network()})
        # self.Pump()

    def deleteGame(self, game, message):
        print("received delete game request")
        self.sendToPlayersInGame(game.player0, {"action": "message", "playerName": "game", "message": message})

        self.playerIdToRoom.pop(game.player0)
        self.playerIdToRoom.pop(game.player1)

    def updateBoard(self, player, move):
        print("in server's update board")
        room = self.playerIdToRoom[player]

        if move['startRow'] < 0 or move['startRow'] > 7 or move['startColumn'] < 0 or move['startColumn'] > 7:
            self.sendBoardToPlayers(player)
            return

        room.game.update_game_state_with_move(move['startRow'], move['startColumn'], move['endRow'], move['endCol'])
        self.sendBoardToPlayers(player)

        # If the game is over, notify participants and delete the game.
        is_over, winner = room.game.is_game_over(room.game.get_all_legal_moves())
        if is_over:
            print('game is over')
            message = "The game has ended in a draw." if winner == 2 else "Player " + str(winner) + " has won the game."
            self.deleteGame(self.playerIdToRoom[player], message)
        #     Otherwise, continue sending the board to the players.
        else:

            self.sendBoardToPlayers(player)

    def sendToPlayersInGame(self, player, toSend):
        room = self.playerIdToRoom[player]
        print(room)

        self.playerIdToPlayerChannel[room.player0].Send(toSend)
        print('sent to player 1: ' + str(room.player0))
        self.playerIdToPlayerChannel[room.player1].Send(toSend)
        print('sent to player 2: ' + str(room.player1))


    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)

if __name__ == '__main__':
    # get command line argument of server, port
    # if len(sys.argv) != 2:
    #     print("Usage:", sys.argv[0], "host:port")
    #     print("e.g.", sys.argv[0], "localhost:31425")
    # else:
    #     host, port = sys.argv[1].split(":")
    host = "localhost"
    port = "12345"
    s = CheckersServer(localaddr=(host, int(port)))
    s.Launch()