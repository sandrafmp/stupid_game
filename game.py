import pygame, sys
import numpy as np
pygame.init()

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

screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption( 'TIC TAC TOE' )
screen.fill( BG_COLOR )

board = np.zeros( (BOARD_ROWS, BOARD_COLS) )

def draw_lines():
	
	for i in range(1,BOARD_ROWS):
		pygame.draw.line( screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH )
		pygame.draw.line( screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH )

def draw_figures():
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == 1:
				pygame.draw.circle( screen, CIRCLE_COLOR, (int( col * SQUARE_SIZE + SQUARE_SIZE//2 ), int( row * SQUARE_SIZE + SQUARE_SIZE//2 )), CIRCLE_RADIUS, CIRCLE_WIDTH )
			elif board[row][col] == 2:
				pygame.draw.line( screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH )	
				pygame.draw.line( screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH )

def mark_square(row, col, player):
	board[row][col] = player

def available_square(row, col):
	return board[row][col] == 0

def is_board_full():
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == 0:
				return False
	return True

def check_win(player):
	for col in range(BOARD_COLS):
		for i in range(0,5):
			if board[i][col] == player and board[i+1][col] == player and board[i+2][col] == player and board[i+3][col] == player and board[i+4][col] == player:
				draw_vertical_winning_line(col, i, player)
				return True

	for row in range(BOARD_ROWS):
		for i in range(0,5):
			if board[row][i] == player and board[row][i+1] == player and board[row][i+2] == player and board[row][i+3] == player and board[row][i+4] == player:
				draw_horizontal_winning_line(row, i, player)
				return True
	for i in range(0,6):
		for j in range(0,6):
			if board[i,j]==player and board[i+1][j+1] == player and board[i+2][j+2] == player and board[i+3][j+3] == player and board[i+4][j+4] == player:
				draw_desc_diagonal(player, i, j)
				return True
	
	for i in range(4,10):
		for j in range(0,6):
			if board[i,j]==player and board[i-1,j+1]==player and board[i-2,j+2]==player and board[i-3,j+3]==player and board[i-4,j+4]==player:
				draw_asc_diagonal(player, i, j)
				return True
	
	return False
	
def draw_vertical_winning_line(col, i, player):
	posX = col * SQUARE_SIZE + SQUARE_SIZE//2

	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( screen, color, (posX, 15+i*SQUARE_SIZE), (posX, HEIGHT//2 - 15+i*SQUARE_SIZE), WIN_LINE_WIDTH )

def draw_horizontal_winning_line(row, i, player):
	posY = row * SQUARE_SIZE + SQUARE_SIZE//2

	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( screen, color, (15+i*SQUARE_SIZE, posY), (WIDTH//2 - 15+i*SQUARE_SIZE, posY), WIN_LINE_WIDTH )

def draw_asc_diagonal(player, i, j):
	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( screen, color, (15+j*SQUARE_SIZE, 45+i*SQUARE_SIZE), (WIDTH//2 - 15+j*SQUARE_SIZE, -HEIGHT//2 +75+i*SQUARE_SIZE), WIN_LINE_WIDTH )

def draw_desc_diagonal(player, i, j):
	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( screen, color, (15+j*SQUARE_SIZE, 15+i*SQUARE_SIZE), (WIDTH//2 - 15+j*SQUARE_SIZE, HEIGHT//2 - 15+i*SQUARE_SIZE), WIN_LINE_WIDTH )

def restart():
	screen.fill( BG_COLOR )
	draw_lines()
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			board[row][col] = 0

draw_lines()

player = 1
game_over = False

while True:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

			mouseX = event.pos[0] 
			mouseY = event.pos[1] 

			clicked_row = int(mouseY // SQUARE_SIZE)
			clicked_col = int(mouseX // SQUARE_SIZE)

			if available_square( clicked_row, clicked_col ):

				mark_square( clicked_row, clicked_col, player )
				if check_win( player ):
					game_over = True
				player = player % 2 + 1

				draw_figures()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				restart()
				player = 1
				game_over = False

	pygame.display.update()
	


        
        
        