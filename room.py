from multiprocessing.connection import Listener
from multiprocessing import Process, Manager, Value, Lock
import traceback
import sys

LEFT_PLAYER = 0
RIGHT_PLAYER = 1
SIDESSTR = ["one", "two"]
SIZE = (505, 505)
X=0
Y=1
DELTA = 30

WIDTH = 20
HEIGHT = 20
MARGIN = 5


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
GREEN = (0,255,0)


class Game():
    def __init__(self, manager):
        self.players = manager.list([Player(LEFT_PLAYER), Player(RIGHT_PLAYER)])
        self.running = Value('i', 1)  # 1 running
        self.lock = Lock()


    def get_player(self, turn):
        return self.players[turn]

    def stop(self):
        self.running.value = 0

    def get_info(self):
        info = { #info who board looks now
            'is_running': self.running.value == 1
        }
        return info

    def color_board(self): #needed?
        print('')

    def is_running(self):
        return self.running.value == 1



class Player():
    def __init__(self, turn):
        self.turn = turn





def player(turn, conn, game):
    try:
        print(f"starting player {SIDESSTR[turn]}:{game.get_info()}")
        conn.send( (turn, game.get_info()) )
        while game.is_running():
            command = ""
            while command != "next":
                command = conn.recv()
                if command[0] == "color":
                    print('change color on board')
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


if __name__=='__main__':
    port = 24654
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])

    main(ip_address, port)