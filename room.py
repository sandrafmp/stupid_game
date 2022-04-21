from multiprocessing import Process, Manager, Value, Lock
from multiprocessing.connection import Listener
import traceback
import sys
import pygame


black = (0, 0, 0)
white = (255, 255, 255)

green = (0, 255, 0)
blue = (0, 0, 255)
WIDTH = 20
HEIGHT = 20
MARGIN = 5


def grid():
    grid = []
    for row in range(20):
        grid.append([])
        for column in range(20):
            grid[row].append(0)
    grid[1][5] = 0
    window_size = [505, 505]

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
