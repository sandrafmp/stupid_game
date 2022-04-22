from multiprocessing import Process, Manager, Value, Lock
from multiprocessing.connection import Listener
import traceback
import sys

FIRST_PLAYER = 0
SECOND_PLAYER = 1
RED= (255, 0, 0)
BLUE = (0, 0, 255)
WIDTH = 20
HEIGHT = 20
MARGIN = 5
grid = []

class Player():
    def __init__(self, number):
        self.number = number
        if number == FIRST_PLAYER:
            self.color = RED
        else:
            self.color = BLUE
        self.counter = Value('i',0)

    def get_color(self):
        return self.color

    def get_number(self):
        return self.number

class Game():
    def __init__(self, manager):
        self.players = manager.list( [Player(FIRST_PLAYER), Player(SECOND_PLAYER)] )
        self.score = manager.list( [] )
        self.running = Value('i', 1) # 1 running
        self.lock = Lock()

    def get_player(self, number):
        return self.players[number]
        
    def get_score(self):
        return list(self.score)

    def is_running(self):
        return self.running.value == 1

    def stop(self):
        self.running.value = 0

    def get_info(self):
        info = {
            'score_first_player': self.players[LEFT_PLAYER].get_pos(),
            'score_second_player': self.players[RIGHT_PLAYER].get_pos(),
            'pos_ball': self.ball[0].get_pos(),
            'score': list(self.score),
            'is_running': self.running.value == 1
        }
        return info


def player(number, conn, game):
    try:
        print(f"starting player {SIDESSTR[number]}:{game.get_info()}")
        conn.send( (number, game.get_info()) )
        while game.is_running():
            square = [None , None]
            while command != "next":
                square = conn.recv()
                if command == "up":
                    game.moveUp(side)
                elif command == "down":
                    game.moveDown(side)
                elif command == "collide":
                    game.ball_collide(side)
                elif command == "quit":
                    game.stop()
            if side == 1:
                game.move_ball()
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
