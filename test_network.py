import unittest
from client import Client
from server import CheckersServer

class TestNetwork(unittest.TestCase):
    def test_client_server(self):
        s = CheckersServer(localaddr=("localhost", int(8000)))
        # s.launch()
        c1 = Client("localhost", int(8000))
        c2 = Client("localhost", int(8000))

        # c1.


if __name__ == '__main__':
    unittest.main()
