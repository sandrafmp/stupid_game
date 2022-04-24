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
        self.grid = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

    def update(self, player, row, column):
        self.grid[row][column] = player + 1
        
    def initialize(self):
        self.grid = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]


class Game():
    def __init__(self, manager):
        self.players = manager.list([Player(PLAYER_ONE), Player(PLAYER_TWO)])
        self.running = Value('i', 1)  # 1 equals running
        self.board = manager.list([Board()])
        self.lock = Lock()
        self.winner = False
        self.restart = False

    def initialize(self):
        board=self.board[0]
        winner=self.winner
        board.initialize()
        winner=False
        self.board[0]=board
        self.winner=winner

    def get_player(self, turn):
        return self.players[turn]

    def stop(self):
        self.running.value = 0

    def get_info(self):
        info = {
            'is_running': self.running.value == 1,
            'board': self.board[0].grid,
            'winner': self.winner,
            'restart': self.restart
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

    def check_winner(self, turn):
        for col in range(BOARD_SIZE):
            for i in range(BOARD_SIZE):
                if self.board[0].grid[i][col] == turn + 1 and self.board[0].grid[i + 1][col] == turn + 1 and \
                        self.board[0].grid[i + 2][col] == turn + 1 and self.board[0].grid[i + 3][col] == turn + 1 and \
                        self.board[0].grid[i + 4][col] == turn + 1:
                    # draw_vertical_winning_line(col, i, turn)
                    print("wins in column")
                    return True

        for row in range(BOARD_SIZE):
            for i in range(BOARD_SIZE):
                if self.board[0].grid[row][i] == turn + 1 and self.board[0].grid[row][i + 1] == turn + 1 and \
                        self.board[0].grid[row][i + 2] == turn + 1 and self.board[0].grid[row][i + 3] == turn + 1 and \
                        self.board[0].grid[row][i + 4] == turn + 1:
                    # draw_horizontal_winning_line(row, i, player)
                    print("wins in row")
                    return True

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[0].grid[i][j] == turn + 1 and self.board[0].grid[i + 1][j + 1] == turn + 1 and \
                        self.board[0].grid[i + 2][j + 2] == turn + 1 and self.board[0].grid[i + 3][
                    j + 3] == turn + 1 and \
                        self.board[0].grid[i + 4][j + 4] == turn + 1:
                    # draw_desc_diagonal(player, i, j)
                    print("wins in diag desc")
                    return True

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[0].grid[i][j] == turn + 1 and self.board[0].grid[i - 1][j + 1] == turn + 1 and \
                        self.board[0].grid[i - 2][j + 2] == turn + 1 and self.board[0].grid[i - 3][
                    j + 3] == turn + 1 and \
                        self.board[0].grid[i - 4][j + 4] == turn + 1:
                    # draw_asc_diagonal(player, i, j)
                    print("wins in diag asc")
                    return True

        return False


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
                elif command[0] == "quit":
                    game.stop()
                elif command == "restart":
                    game.initialize()
                    restart=game.restart
                    restart=True
                    
            conn.send((turn, game.get_info()))
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
    port = 24656
    ip_address = "147.96.81.245"
    if len(sys.argv) > 1:
        ip_address = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    print(ip_address, port)

    main(ip_address, port)