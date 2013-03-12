#!/usr/bin/env python2.7

import argparse
from sys import exit

import pygame
from pygame.locals import *
from pygame.sprite import Sprite

def render_text(s, fontsize):
    font = pygame.font.Font(None, fontsize)
    text = font.render(s, True, pygame.Color("white"))
    return text

def exit_game():
    exit()

class Ball(Sprite):
    def __init__(self, color, position, racket):
        Sprite.__init__(self)
        self.image = pygame.Surface((6,6))
        pygame.draw.circle(self.image, pygame.Color(color), (3,3), 3)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.velocity = [0,0]
        self.racket = racket

    def start(self):
        self.velocity = [10, -10]

    def update(self):
        self.rect.move_ip(*self.velocity)
        if self.rect.colliderect(self.racket.rect):
            print "collide"
            self.velocity[1] *= -1.2
            self.rect.x += self.velocity[0]


        if self.rect.top < 0:
            self.velocity[1] *= -1
            self.rect.top = 1
        if self.rect.left < 100:
            self.velocity[0] *= -1
            self.rect.left = 101
        if self.rect.right > 700:
            self.velocity[0] *= -1
            self.rect.right = 699
        if self.rect.bottom > 600:
            if self.velocity[1] > 0:
                self.velocity[0] = 0
                self.velocity[1] = 0
                print "game over"

class Racket(Sprite):
    def __init__(self, color, position):
        Sprite.__init__(self)
        self.image = pygame.Surface([40, 10])
        self.rect = pygame.Rect(0,0,40,10)
        pygame.draw.rect(self.image, pygame.Color(color), self.rect)
        self.rect.center = position
        self.velocity = 0

    def left(self):
        self.velocity -= 15

    def right(self):
        self.velocity += 15
            
    def update(self):
        if self.rect.left < 100 and self.velocity < 0:
            pass
        elif self.rect.right > 700 and self.velocity > 0:
            pass
        else:
            self.rect.move_ip(self.velocity, 0)

class Options():
    def __init__(self, res, opts):
        self._width = res[0]
        self._fontsize = 50
        self.selected = 0
        self.surf = pygame.Surface(res)
        self.text = []
        self.opts = opts

        for opt in opts:
            self.text.append(render_text(opt[0], 50))

    def run(self):
        self.running = True

        while self.running:
            for text in self.text:
                x = self.surf.get_width()/2 - text.get_width()/2
                y += text.get_height()*1.5 
                self.surf.blit(text, (x,y))

    def update(self):
        self.surf.fill(pygame.Color("black"))
        pygame.draw.rect(self.surf, pygame.Color("purple"), pygame.Rect(0, (self.selected+1)*(self._fontsize), self._width, self._fontsize))
        y = 0
        for text in self.text:
            x = self.surf.get_width()/2 - text.get_width()/2
            y += text.get_height()*1.5 
            self.surf.blit(text, (x,y))

    def draw(self, screen):
#        screen.blit(self.select, (0, self.selected*1.5))
        screen.blit(self.surf, (0,0))

    def up(self):
        self.selected -= 1

    def down(self):
        self.selected += 1

    def select(self):
        return self.opts[self.selected][1]




def nop():
    pass


def menu(screen, clock):
    mainmenu = [
            ["START GAME", 'play'],
            ["SELECT LEVEL", nop],
            ["OPTIONS", nop],
            ["QUIT", exit_game]
            ]
    o = Options((600,400), mainmenu)

    ismenu = True
    while ismenu:
        o.update()
        o.draw(screen)
        pygame.display.flip()
        events = pygame.event.get()
        for event in events:
            if (event.type == QUIT):
                exit_game()
            if (event.type == KEYUP) and (event.key == K_ESCAPE):
                exit_game()
            if (event.type == KEYDOWN) and (event.key == K_UP):
                o.up()
            if (event.type == KEYDOWN) and (event.key == K_DOWN):
                o.down()
            if (event.type == KEYDOWN) and (event.key == K_RETURN):
                selected = o.select()
                if selected == 'play':
                    breakout(screen, clock)
                else:
                    selected()
        clock.tick(30)


def breakout(screen, clock):
    game = pygame.Surface((600,600))
    racket = Racket('white', (380, 560))
    ball = Ball("yellow", (380, 550), racket)

    keymap = {
            pygame.K_SPACE: [ball.start, nop],
            pygame.K_LEFT: [racket.left, racket.right],
            pygame.K_RIGHT: [racket.right, racket.left]
            }
   
    isrunning = True

    while isrunning:
        bg = pygame.Surface((800,600))
        bg.fill(pygame.Color("black"))
        screen.blit(bg, (0,0))

        sprites = pygame.sprite.RenderClear([racket, ball])

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
    parser = argparse.ArgumentParser(description=
            "A pygame implementation of Breakout")
    parser.add_argument('-r', '--resolution',
            help="Resolution", default='800x600')
    parser.add_argument('-f', '--fullscreen',
            help="Fullscreen", action='store_true')
    args = vars(parser.parse_args())
    res = tuple(int(x) for x in args['resolution'].split('x'))
    fs = args['fullscreen']

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(res)
    
    menu(screen, clock)

if __name__ == '__main__':
    main()
