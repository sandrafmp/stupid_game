from multiprocessing.connection import Client
import traceback
import pygame
import sys, os

class Display():
    def __init__(self, game):
        pygame.init()

    def analyze_events(self, side):
        events = []
        for event in pygame.event.get():
        	if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
        		events.append("square clicked")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    events.append("restart")
            elif event.type == pygame.QUIT:
                events.append("quit")
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