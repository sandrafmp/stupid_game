from multiprocessing.connection import Client
import traceback
import pygame
import sys, os

print<("bla")

class Display():
    def __init__(self, game):
        pygame.init()

    def analyze_events(self, side):
        events = []
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
					
		return events
					

    def refresh(self):

    def tick(self):
        self.clock.tick(FPS)

    @staticmethod
    def quit():
        pygame.quit()


def main(ip_address, port):
    try:
        with Client((ip_address, port), authkey=b'secret password') as conn:
            game = Game()
            side,gameinfo = conn.recv()
            print(f"I am playing {SIDESSTR[side]}")
            game.update(gameinfo)
            display = Display(game)
            while game.is_running():
                events = display.analyze_events(side)
                for ev in events:
                    conn.send(ev)
                    if ev == 'quit':
                        game.stop()
                conn.send("next")
                gameinfo = conn.recv()
                game.update(gameinfo)
                display.refresh()
                display.tick()
    except:
        traceback.print_exc()
    finally:
        pygame.quit()


if __name__=="__main__":
    port = 24654
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])

    main(ip_address, port)

    print('test')