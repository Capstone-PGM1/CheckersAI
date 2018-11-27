from PodSixNet.Connection import connection, ConnectionListener

from time import sleep

class PendingChallenge:
    def __init__(self, challengeTo, challengeFrom, playerName):
        self.challenge_to = challengeTo
        self.challenge_from = challengeFrom
        self.playerName = playerName

class Client(ConnectionListener):
    def __init__(self, host, port):
        self.Connect((host, port))
        self.pending_challenge = None
        self.rejected_challenge = None
        self.has_current_game = False
        self.possible_moves = None
        self.board = None
        self.messages = []
        self.error = False
        self.game_message = ""
        self.winner = -1
        self.winner_name = ""
        self.color = 0

    def Network(self, data):
        print
        'network data:', data

    def Network_connected(self, data):
        print
        "connected to the server"

    def close(self):
        connection.Close()

    def Network_error(self, data):
        self.error = True
        if ("error_message" in data):
            self.game_message = data['error_message']

    def Network_disconnected(self, data):
        self.error = True
        self.game_message = "The server has disconnected."

    def Network_receiveId(self, data):
        self.id = data['id']
        print("hello, you have joined the game. You are player " + str(self.id))

    def update_username(self, username):
        connection.Send({"action": "updateUsername", "username": username})

    def Loop(self):
        connection.Pump()
        self.Pump()

    # These methods deal with connecting to a multiplayer game

    # When the server sends the list of players, display possible
    # players on the screen
    def Network_getPlayers(self, data):
        self_index = data['players'].index(str(self.id))
        data['players'].pop(self_index)
        self.other_players = data['players']
        data['usernames'].pop(self_index)
        self.other_players_usernames = data['usernames']

    def send_challenge(self, otherPlayerId, playerName):
        if not self.pending_challenge:
            self.game_message = "Waiting for a response from {}".format(playerName)
            self.pending_challenge = PendingChallenge(otherPlayerId, self.id, playerName)
            connection.Send({"action": "getChallenge", "id": self.id, "otherPlayer": int(otherPlayerId)})

    # When receiving a challenge from another player, display the challenger on the screen
    def Network_getChallenge(self, data):
        if not self.pending_challenge:
            self.game_message = "You have received a challenge from {}".format(data['otherPlayerName'])
            self.pending_challenge = PendingChallenge(self.id, data['otherPlayerId'], data['otherPlayerName'])

    def respond_to_challenge(self, response):
        connection.Send({"action": "getResponseToChallenge", "id": self.id, "response": response, "otherPlayer": self.pending_challenge.challenge_from})
        self.pending_challenge = None
        self.game_message = ""

    def Network_rejectChallenge(self, data):
        self.pending_challenge = None
        self.game_message = "{} has rejected your challenge.".format(data['playerName'])

    def Network_acceptChallenge(self, data):
        self.pending_challenge = None
        self.game_message = ""
        self.has_current_game = True

    def Network_closeGame(self, data):
        self.clear_game_info(data['message'])

    def clear_game_info(self, message = ""):
        self.has_current_game = False
        self.possible_moves = None
        self.board = None
        self.messages = []
        self.winner = -1
        self.winner_name = ""
        self.game_message = message
        self.color = 0

    # These methods deal with the checkers game.
    def Network_getPossibleMoves(self, data):
        # data['game'] is a {(rowIndex, columnIndex): 'char'} for each item.
        # Characters: x is black, o is red, K is a red king, Q is a black king, and R/B are pieces.
        self.board = data['game']
        if "possibleMoves" in data:
            self.possible_moves = data['possibleMoves']
        else:
            self.possible_moves = None
        self.color = data['color']

    def Network_gameEnd(self, data):
        self.winner = data['winner']
        self.winner_name = str(data['winner_name'])

    def update_game_state_with_move(self, start_row, start_column, end_row, end_column):
        connection.Send({"action": "updateBoard", "move": {"startRow": start_row, "startColumn": start_column, "endRow": end_row, "endCol": end_column}, "id": self.id})

    def resign_game(self):
        connection.Send({"action": "endGame", 'id': self.id})

    # This method deals with the chat room.
    def Network_message(self, data):
        self.messages.append("{}: {}".format(data['playerName'], data['message']))

    def sendMessage(self, message):
        connection.Send({"action": "message", "id": self.id, "message": message})

    def pump(self):
        self.Loop()


def startClient(username):
    client = Client('45.33.41.181', 12345)
    # client = Client('localhost', 12345)
    client.update_username(username)
    return client

if __name__ == '__main__':
    c = startClient()

    while 1:
        c.Loop()
        sleep(0.01)