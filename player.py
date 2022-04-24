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
BOARD_SIZE = 20

PLAYER_ONE = 0
PLAYER_TWO = 1
PLAYER_COLOR = [GREEN, BLUE]

FPS = 60

WIDTH = 20
HEIGHT = 20
MARGIN = 5

SIDES = ["one", "two"]
SIDESSTR = ["one", "two"]



class Player():
	def __init__(self, turn):
		self.turn = turn

class Board():
	def __init__(self):
		self.grid = []
		self.scr = pygame.display.set_mode(SIZE)

	def initialize(self):
		for row in range(BOARD_SIZE):
			self.grid.append([])
			for column in range(BOARD_SIZE):
				self.grid[row].append(0)
				color = WHITE
				pygame.draw.rect(self.scr,
								 color,
								 [(MARGIN + WIDTH) * column + MARGIN,
								  (MARGIN + HEIGHT) * row + MARGIN,
								  WIDTH,
								  HEIGHT])
		pygame.display.flip()
		self.clock =  pygame.time.Clock()
		pygame.init()
	
		
	def analyze_events(self, turn):
		events = []
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				column = pos[0] // (WIDTH + MARGIN)
				row = pos[1] // (HEIGHT + MARGIN)
				#self.grid[row][column]=turn
				events.append(["color", row, column])
				#print(row,column)
		return events


	def change_color(self):
		for i in range(20):
			for j in range(20):
				if self.grid[i][j]==1:
					color=BLUE
					pygame.draw.rect(self.scr,color,[(MARGIN + WIDTH) * j + MARGIN,(MARGIN + HEIGHT) * i + MARGIN,WIDTH,HEIGHT])
				elif self.grid[i][j]==2:
					color=GREEN
					pygame.draw.rect(self.scr,color,
						 [(MARGIN + WIDTH) * j + MARGIN,
						  (MARGIN + HEIGHT) * i + MARGIN,
						  WIDTH,
						  HEIGHT])
		pygame.display.flip()

	def refresh_board(self):
		pygame.display.update() #is it flip instead of update?

	def tick(self):
		self.clock.tick(FPS)


class Game():
	def __init__(self):
		self.running = True
		self.board = Board()

	def initialize(self):
		self.board.initialize()
	
	def get_player(self, turn):
		return self.players[turn]

	def get_board(self):
		return self.board

	def analyze_events(self, turn):
		return self.board.analyze_events(turn)

	def update(self, gameinfo):
		self.running = gameinfo['is_running']
		#print(gameinfo['board'])
		self.up_board(gameinfo['board'])

	def up_board(self,info):
		for i in range(BOARD_SIZE):
			for j in range(BOARD_SIZE):
				self.board.grid[i][j]=info[i][j]
		self.board.change_color()

	def is_running(self):
		return self.running





def main (ip_address, port):
	try:
		with Client((ip_address, port), authkey=b'secret password') as conn:
			game = Game()
			game.initialize()
			turn, gameinfo = conn.recv()
			print(f"I am playing {SIDESSTR[turn]}")
			game.update(gameinfo)
			while game.is_running():
				events = game.analyze_events(turn)
				for ev in events:
					conn.send(ev)
					#game.board.change_color()
					if ev[0] == 'quit':
						game.stop()
				conn.send("next")
				gameinfo = conn.recv()
				game.update(gameinfo)
				game.board.refresh_board()
				game.board.tick()

	except:
		traceback.print_exc()
	finally:
		pygame.quit()

if __name__=="__main__":
	port = 24655
	ip_address = "147.96.81.245"
	if len(sys.argv)>1:
		ip_address = sys.argv[1]
	if len(sys.argv) > 2:
		port = int(sys.argv[2])

	main(ip_address, port)