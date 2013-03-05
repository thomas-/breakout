#!/usr/bin/env python2.7

import pygame
from pygame.locals import *
from pygame.sprite import Sprite

class Racket(Sprite):
	def __init__(self, color, position):
		Sprite.__init__(self)
		self.image = pygame.Surface([40, 10])
		self.rect = pygame.Rect(0,0,40,10)
		pygame.draw.rect(self.image, pygame.Color(color), self.rect)
		self.rect.center = position
		self.velocity = 0

	def left(self):
		self.velocity -= 5

	def right(self):
		self.velocity += 5
	
	def update(self):
		self.rect.move_ip(self.velocity, 0)

def breakout(screen):
    clock = pygame.time.Clock()
    racket = Racket('white', (300, 460))

    keymap = {
            pygame.K_LEFT: [racket.left, racket.right],
            pygame.K_RIGHT: [racket.right, racket.left]
            }
   
    isrunning = True

    while isrunning:
        bg = pygame.Surface((640,480))
        bg.fill(pygame.Color("black"))
        screen.blit(bg, (0,0))

        sprites = pygame.sprite.RenderClear([racket])

        sprites.update()
        sprites.draw(screen)
        pygame.display.flip()
        sprites.clear(screen, bg)

        events = pygame.event.get()
        for event in events:
            if (event.type == QUIT) or ((event.type == KEYUP) and (event.key == K_ESCAPE)):
                isrunning = False
            if (event.type == pygame.KEYDOWN) and (event.key in keymap):
                keymap[event.key][0]()
            if (event.type == pygame.KEYUP) and (event.key in keymap):
                keymap[event.key][1]()


        clock.tick(30)


def main():
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    breakout(screen)

if __name__ == '__main__':
    main()
