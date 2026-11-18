import sys
import pygame
from pygame.locals import *
import time

from Game import Playground, Pos

class Graphic:
    def __init__(self, playground:Playground, player_num:int):
        pygame.init()

        self.fps = 60
        self.fpsClock = pygame.time.Clock()

        self.play = playground

        self.width, self.height = playground.pixels
        self.size = self.play.size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(str(player_num))
        self.my_font = pygame.font.SysFont('Comic Sans MS', round(self.play.yField * 0.5))

    def grid(self):
        for y in range(self.size[1]):
            pygame.draw.line(self.screen, (0, 0, 0), (0, y * self.play.yField), (self.width, y * self.play.yField))

        for x in range(self.size[0]):
            pygame.draw.line(self.screen, (0, 0, 0), (x * self.play.xField, 0), (x * self.play.xField, self.height))

    def draw(self)->None:
        self.screen.fill((210, 210, 210))
        self.grid()

        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if self.play.state[(x, y)] is not None:

                    match self.play.state[(x, y)]:
                        case 0:
                            pygame.draw.circle(self.screen, (255,0,0), self.play.mid_pos[x, y], self.play.xField * 0.4)
                        case 1:
                            # draw x
                            os = self.play.xField * 0.35
                            mid = Pos(*self.play.mid_pos[x, y])
                            pygame.draw.line(self.screen, color="Blue",
                                             start_pos=(mid.x - os, mid.y + os),
                                             end_pos=(mid.x + os, mid.y - os),
                                             width=5)
                            pygame.draw.line(self.screen, color="Blue",
                                             start_pos=(mid.x + os, mid.y + os),
                                             end_pos=(mid.x - os, mid.y - os),
                                             width=5)

    def click(self) -> None | Pos:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                pos = Pos(int(x // self.play.xField), int(y // self.play.yField))
                if self.play.state.get(pos.xy) is None and pos.xy in self.play.state:
                    return pos
        return None

    def move(self)->Pos:
        mov = self.click()
        while mov is None:
            mov = self.click()
        return mov

    def handle_win(self, start_end)-> None:
        print("s-------------------------")
        print(start_end)
        pygame.draw.line(self.screen, (70,70,70),self.play.mid_pos[start_end[0]], self.play.mid_pos[start_end[1]], width=10)

    def update(self):
        self.draw()
        pygame.display.flip()
        self.fpsClock.tick(self.fps)

if __name__ == "__main__":
    play = Playground((16,16), (800,800))

    game = Graphic(play, 0)
    play.add_move(Pos(5,5), 0)
    play.add_move(Pos(6,5), 1)
    while True:
        game.click()
        game.update()