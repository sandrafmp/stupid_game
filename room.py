from multiprocessing.connection import Listener
from multiprocessing import Process, Manager, Value, Lock
import traceback
import sys

PLAYER_ONE = 0
PLAYER_TWO = 1
SIDESSTR = ["one", "two"]
SIZE = (505, 505)

WIDTH = 20
HEIGHT = 20
MARGIN = 5
BOARD_SIZE = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)


class Board():
    def __init__(self):
        self.grid = [[0]*BOARD_SIZE for _ in range(BOARD_SIZE)]

    def update(self, player, row, column):
        self.grid[row][column] = player+1

class Game():
    def __init__(self, manager):
        self.players = manager.list([Player(PLAYER_ONE), Player(PLAYER_TWO)])
        self.running = Value('i', 1)  # 1 equals running
        self.board = manager.list([Board()])
        self.lock = Lock()

    def get_player(self, turn):
        return self.players[turn]

    def stop(self):
        self.running.value = 0

    def get_info(self):
        info = {
            'is_running': self.running.value == 1,
            'board': self.board[0].grid
        }
        return info

    def is_running(self):
        return self.running.value == 1
        
    def change_color(self, player, row, column):
        self.lock.acquire()
        board = self.board[0]
        board.update(player, row, column)
        self.board[0] = board
        self.lock.release()


class Player():
    def __init__(self, turn):
        self.turn = turn

def player(turn, conn, game):
    try:
        print(f"starting player {SIDESSTR[turn]}:{game.get_info()}")
        conn.send((turn, game.get_info()))
        while game.is_running():
            command = ""
            while command != "next":
                command = conn.recv()
                if command[0] == "color":
                    game.change_color(turn, command[1], command[2])
                elif command == "quit":
                    game.stop()
            conn.send(game.get_info())
    except:
        traceback.print_exc()
        conn.close()
    finally:
        print(f"Game ended {game}")


def main(ip_address, port):
    manager = Manager()
    try:
        with Listener((ip_address, port),
                      authkey=b'secret password') as listener:
            n_player = 0
            players = [None, None]
            game = Game(manager)
            while True:
                print(f"accepting connection {n_player}")
                conn = listener.accept()
                players[n_player] = Process(target=player,
                                            args=(n_player, conn, game))
                n_player += 1
                if n_player == 2:
                    players[0].start()
                    players[1].start()
                    n_player = 0
                    players = [None, None]
                    game = Game(manager)

    except Exception as e:
        traceback.print_exc()


if __name__ == '__main__':
    port = 24655
    ip_address = "127.0.0.1"
    if len(sys.argv) > 1:
        ip_address = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])

    main(ip_address, port)