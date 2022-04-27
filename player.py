from multiprocessing.connection import Client
import traceback
import pygame
import sys, os


SIDES = ["one", "two"]
SIDESSTR = ["one", "two"]

FPS = 60

WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 5
WIN_LINE_WIDTH = 3
BOARD_ROWS = 20
BOARD_COLS = 20
SQUARE_SIZE = 30
CIRCLE_RADIUS = 10
CIRCLE_WIDTH = 3
CROSS_WIDTH = 5
SPACE = 25

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BG_COLOR = (20, 200, 160)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

BOARD_SIZE=20


class Player():
	def __init__(self, turn):
		self.turn = turn

class Board():
	def __init__(self):
		self.grid=[]
		self.scr = pygame.display.set_mode((WIDTH, HEIGHT))

	def draw_lines(self):
		for i in range(1,BOARD_ROWS):
			pygame.draw.line( self.scr, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH )
			pygame.draw.line( self.scr, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH )

	def draw_vertical_winning_line(self,col, i, player):
		posX = col * SQUARE_SIZE + SQUARE_SIZE//2
		if player == 1:
			color = CIRCLE_COLOR
		elif player == 2:
			color = CROSS_COLOR
		pygame.draw.line( self.scr, color, (posX, 15+i*SQUARE_SIZE), (posX, HEIGHT//4 - 15+i*SQUARE_SIZE), WIN_LINE_WIDTH )

	def draw_horizontal_winning_line(self,row, i, player):
		posY = row * SQUARE_SIZE + SQUARE_SIZE//2
		if player == 1:
			color = CIRCLE_COLOR
		elif player == 2:
			color = CROSS_COLOR
		pygame.draw.line( self.scr, color, (15+i*SQUARE_SIZE, posY), (WIDTH//4 - 15+i*SQUARE_SIZE, posY), WIN_LINE_WIDTH )

	def draw_asc_diagonal(self,player, i, j):
		if player == 1:
			color = CIRCLE_COLOR
		elif player == 2:
			color = CROSS_COLOR
		pygame.draw.line( self.scr, color, (15+j*SQUARE_SIZE, 15+i*SQUARE_SIZE), (WIDTH//4 - 15+j*SQUARE_SIZE, -HEIGHT//4 +45+i*SQUARE_SIZE), WIN_LINE_WIDTH )

	def draw_desc_diagonal(self, player, i, j):
		if player == 1:
			color = CIRCLE_COLOR
		elif player == 2:
			color = CROSS_COLOR
		pygame.draw.line( self.scr, color, (15+j*SQUARE_SIZE, 15+i*SQUARE_SIZE), (WIDTH//4 - 15+j*SQUARE_SIZE, HEIGHT//4 - 15+i*SQUARE_SIZE), WIN_LINE_WIDTH )

	def initialize(self):
		for row in range(BOARD_ROWS):
			self.grid.append([])
			for column in range(BOARD_ROWS):
				self.grid[row].append(0)
		self.scr.fill( BG_COLOR )
		self.draw_lines()
		pygame.display.flip()
		self.clock =  pygame.time.Clock()
		pygame.init()

	def available_square(self, row, column):
		return self.grid[row][column]==0

	def draw_figures(self):
		for row in range(20):
			for col in range(20):
				if self.grid[row][col]==1:
					pygame.draw.circle( self.scr, CIRCLE_COLOR, (int( col * SQUARE_SIZE + SQUARE_SIZE//2 ), int( row * SQUARE_SIZE + SQUARE_SIZE//2 )), CIRCLE_RADIUS, CIRCLE_WIDTH )
				elif self.grid[row][col]==2:
					pygame.draw.line( self.scr, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH )
					pygame.draw.line( self.scr, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH )

	def refresh_board(self):
		pygame.display.update()

	def tick(self):
		self.clock.tick(FPS)

	def print_winner(self, turn):
		font = pygame.font.Font(None, 74)
		text = font.render(f"Player {turn + 1} wins!", 1, WHITE)
		self.scr.blit(text, (130, 230))
		font = pygame.font.Font(None, 40)
		text = font.render(f"Press R for restart", 1, WHITE)
		self.scr.blit(text, (170, 360))
		text = font.render(f"Press ESC for quit", 1, WHITE)
		self.scr.blit(text, (170, 330))

	@staticmethod
	def quit():
		pygame.quit()


class Game():
	def __init__(self):
		self.running = True
		self.board = Board()
		self.winner = False

	def initialize(self):
		self.board.initialize()
	
	def get_player(self, turn):
		return self.players[turn]

	def get_board(self):
		return self.board

	def check_winner(self):
		for turn in range(0,2):
			for col in range(BOARD_SIZE):
				for i in range(BOARD_SIZE):
					if self.board.grid[i][col] == turn + 1 and self.board.grid[i + 1][col] == turn + 1 and \
						self.board.grid[i + 2][col] == turn + 1 and self.board.grid[i + 3][col] == turn + 1 and \
						self.board.grid[i + 4][col] == turn + 1:
						self.board.draw_vertical_winning_line(col, i, turn+1)
						self.board.print_winner(turn)
						return True

		for turn in range(0,2):
			for row in range(BOARD_SIZE):
				for i in range(BOARD_SIZE):
					if self.board.grid[row][i] == turn + 1 and self.board.grid[row][i + 1] == turn + 1 and \
						self.board.grid[row][i + 2] == turn + 1 and self.board.grid[row][i + 3] == turn + 1 and \
						self.board.grid[row][i + 4] == turn + 1:
						self.board.draw_horizontal_winning_line(row, i, turn+1)
						self.board.print_winner(turn)

						return True

		for turn in range(0,2):
			for i in range(BOARD_SIZE):
				for j in range(BOARD_SIZE):
					if self.board.grid[i][j] == turn + 1 and self.board.grid[i + 1][j + 1] == turn + 1 and \
						self.board.grid[i + 2][j + 2] == turn + 1 and self.board.grid[i + 3][j + 3] == turn + 1 and \
						self.board.grid[i + 4][j + 4] == turn + 1:
						self.board.draw_desc_diagonal(turn+1, i, j)
						self.board.print_winner(turn)
						return True

		for turn in range(0,2):
			for i in range (4,BOARD_SIZE):
				for j in range(BOARD_SIZE):
					if self.board.grid[i][j] == turn + 1 and self.board.grid[i - 1][j + 1] == turn + 1 and \
						self.board.grid[i - 2][j + 2] == turn + 1 and self.board.grid[i - 3][j + 3] == turn + 1 and \
						self.board.grid[i - 4][j + 4] == turn + 1:
						self.board.draw_asc_diagonal(turn+1, i, j)
						self.board.print_winner(turn)
						return True
		return False

	def update(self, gameinfo):
		self.running = gameinfo['is_running']
		self.up_board(gameinfo['board'])
		self.winner = self.check_winner()
		if gameinfo['restart']==True:
			self.initialize()

	def up_board(self,info):
		self.board.grid=info
		self.board.draw_figures()

	def is_running(self):
		return self.running

	def analyze_events(self, turn):   #vi ska inte ändra planen i player utan endast skicka info till room
		events = []
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN and not self.winner:
				mouseX = event.pos[0]
				mouseY = event.pos[1]
				row = int(mouseY // SQUARE_SIZE)
				column = int(mouseX // SQUARE_SIZE)
				if self.board.available_square(row, column):
					events.append(["color", row, column])
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					events.append("restart")
				elif event.key == pygame.K_ESCAPE:
					events.append("quit")
			elif event.type == pygame.QUIT:
				events.append("quit")
		return events

	def stop(self):
		self.running = False



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
					#print(gameinfo)
					if ev == 'quit':
						game.stop()
				conn.send("next")
				turn, gameinfo = conn.recv()
				game.update(gameinfo)
				game.board.refresh_board()
				game.board.tick()

	except:
		traceback.print_exc()
	finally:
		pygame.quit()


if __name__=="__main__":
	port = 24657
	ip_address = "147.96.81.245"
	if len(sys.argv)>1:
		ip_address = sys.argv[1]
	if len(sys.argv) > 2:
		port = int(sys.argv[2])

	main(ip_address, port)