from multiprocessing.connection import Client
import traceback
import pygame
import sys, os


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
GREEN = (0,255,0)
X = 0
Y = 1
SIZE = (505, 505)
grid = []

LEFT_PLAYER = 0
RIGHT_PLAYER = 1
PLAYER_COLOR = [GREEN, YELLOW]
PLAYER_HEIGHT = 60
PLAYER_WIDTH = 10

BALL_COLOR = WHITE
BALL_SIZE = 10
FPS = 60

WIDTH = 20
HEIGHT = 20
MARGIN = 5

SIDES = ["one", "two"]
SIDESSTR = ["one", "two"]



class Player():
    def __init__(self, turn): #turn är side
        self.turn = turn


class Board():
    def __init__(self, game):
        self.grid = []
        self.scr = pygame.display.set_mode(SIZE)

        for row in range(20):
            self.grid.append([])
            for column in range(20):
                self.grid[row].append(0)
                color = WHITE
                pygame.draw.rect(self.scr,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])
        pygame.display.flip()
        self.clock =  pygame.time.Clock()  #FPS
        pygame.init()

    def analyze_events(self, turn):   #vi ska inte ändra planen i player utan endast skicka info till room
        events = []
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                events.append(["color", row, column])
        return events


    def change_color(self): #
    	for i in range(20):
    		for j in range(20):
    			if self.grid[i][j]==1:
    				color=BLUE
    				pygame.draw.rect(self.scr,
                         color,
                         [(MARGIN + WIDTH) * column + MARGIN,
                          (MARGIN + HEIGHT) * row + MARGIN,
                          WIDTH,
                          HEIGHT])
                if self.grid[i][j]==2:
    				color=BLUE
    				pygame.draw.rect(self.scr,
                         color,
                         [(MARGIN + WIDTH) * column + MARGIN,
                          (MARGIN + HEIGHT) * row + MARGIN,
                          WIDTH,
                          HEIGHT])
                          
        # clock.tick(50)
        pygame.display.flip()

    def update(self):
        self.change_color()

    def refresh_board(self):
        pygame.display.update()

    def tick(self):
        self.clock.tick(FPS)


class Game():
    def __init__(self):
        self.running = True
        self.board = Board()

    def get_player(self, turn):
        return self.players[turn]

    def update(self, gameinfo):
        self.running = gameinfo['is_running']
        self.board = self.up_board(gameinfo['board'])

	def up_board(self,info):
		for i in range(20):
			for j in range(20):
				self.board.grid[i][j]=sala[i][j]
		self.board.change_color()
		
    def is_running(self):
        return self.running





def main (ip_address, port):
    try:
        with Client((ip_address, port), authkey=b'secret password') as conn:
            display = Board()
            game = Game(display)
            turn, gameinfo = conn.recv()
            print(f"I am playing {SIDESSTR[turn]}")
            game.update(gameinfo)
            while game.is_running():
                events = display.analyze_events(turn)
                for ev in events:
                    print(turn)
                    display.change_color(turn,ev[1],ev[2]) #DETTA SKA GÖRAS FÖR BÅDA, SÅ I RUM KANSKE? HAR PROVAT
                    conn.send(ev)
                    if ev[0] == 'quit':
                        game.stop()
                conn.send("next")
                gameinfo = conn.recv()
                game.update(gameinfo)
                display.refresh_board()
                display.tick()

    except:
        traceback.print_exc()
    finally:
        pygame.quit()

if __name__=="__main__":
    port = 24654
    ip_address = "147.96.81.245"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])

    main(ip_address, port)