from multiprocessing import Process, Manager, Value, Lock
from multiprocessing.connection import Listener
import traceback
import sys
import pygame

WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 10
WIN_LINE_WIDTH = 5
BOARD_ROWS = 10
BOARD_COLS = 10
SQUARE_SIZE = 60
CIRCLE_RADIUS = 20
CIRCLE_WIDTH = 5
CROSS_WIDTH = 5
SPACE = 55

RED = (255, 0, 0)
BG_COLOR = (20, 200, 160)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)



def grid():
    grid = []
    for row in range(20):
        grid.append([])
        for column in range(20):
            grid[row].append(0)
    grid[1][5] = 0
    window_size = [505, 505]

class Board():
    def __init__(self, velocity):
        self.squares=[ SIZE[X]//2, SIZE[Y]//2 ]
        self.velocity = velocity

    def get_pos(self):
        return self.pos

    def update(self):
        self.pos[X] += self.velocity[X]
        self.pos[Y] += self.velocity[Y]

    def bounce(self, AXIS):
        self.velocity[AXIS] = -self.velocity[AXIS]

    def collide_player(self, side):
        self.bounce(X)
        self.pos[X] += 3*self.velocity[X]
        self.pos[Y] += 3*self.velocity[Y]


class Game():
    def __init__(self):
        self.grid = grid()
        self.score = [0, 0]
        self.running = True
        self.players = [Player(i) for i in range(2)]



class Display():
    def __init__(self, window_size):
        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock() #frames per second
        pygame.init()

    def analyze_events(self, player):

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            grid[row][column] = 1

        events = []
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
            if event.key == pygame.K_ESCAPE:
                events.append("quit")
                
        if pygame.sprite.collide_rect(self.ball, self.paddles[side]):
            events.append("collide")
        return events


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
            command = ""
            while command != "next":
                command, square = conn.recv()
                if command == "click":
                    update
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
