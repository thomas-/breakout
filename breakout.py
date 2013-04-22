#!/usr/bin/env python2.7

import argparse
from sys import exit
from random import randint

import time

import pygame
from pygame.locals import *
from sprites import Ball, Racket, Block, Score, Lives

def render_text(s, fontsize):
    font = pygame.font.Font(None, fontsize)
    text = font.render(s, True, pygame.Color("white"))
    return text

def exit_game():
    exit()
    
def rounder(number):
    result = int(round(number))
    return result

class Options():
    def __init__(self, res, opts):
        self.res = res
        self._width = res[0]
        self._fontsize = rounder(self.res[0]/20)
        self.selected = 0
        self.surf = pygame.Surface(self.res)
        self.text = []
        self.opts = opts

        for opt in opts:
            self.text.append(render_text(opt[0], rounder(self.res[0]/20)))

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


def menu(screen, clock, res):
    mainmenu = [
            ["START GAME", 'play'],
            ["SELECT LEVEL", nop],
            ["OPTIONS", nop],
            ["QUIT", exit_game]
            ]
    o = Options((res[0], res[1]), mainmenu)

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
                    breakout(screen, clock, res)
                else:
                    selected()
        clock.tick(30)


def breakout(screen, clock, res):
    #game = pygame.Surface((res[0]*0.75,res[1]))
    racket = Racket('yellow', (res[0]*0.475, res[1]-40), res)

    blocks = []
    for i in xrange(0, 6):
        for j in xrange(0, 14):
            blocks.append(Block(1, (randint(5,250),randint(5,250),randint(5,250)), (i,j), res))

    score = Score(res)

    lives = Lives(res)

    ball = Ball("yellow", (res[0]*0.475, res[1]-45), racket, blocks, res)

    keymap = {
            pygame.K_SPACE: [ball.start, nop],
            pygame.K_LEFT: [racket.left, racket.right],
            pygame.K_RIGHT: [racket.right, racket.left]
            }

    isrunning = True

    while isrunning:
        bg = pygame.Surface((res[0],res[1]))
        bg.fill(pygame.Color("black"))
        linethickness = rounder(res[0]/160)
        pygame.draw.line(bg, pygame.Color("white"), (res[0]*0.2375-linethickness, res[0]/16), (res[0]*0.2375-linethickness,res[1]), linethickness)
        pygame.draw.line(bg, pygame.Color("white"), (res[0]*0.7625+linethickness, res[0]/16), (res[0]*0.7625+linethickness, res[1]), linethickness)
        pygame.draw.line(bg, pygame.Color("white"), (res[0]*0.2375-linethickness, (res[0]/16 + linethickness*0.4)), (res[0]*0.7625+linethickness, (res[0]/16 + linethickness*0.4)), linethickness)
        screen.blit(bg, (0,0))

        sprites = pygame.sprite.Group([racket, ball, blocks, score, lives])

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
            if (event.type == pygame.USEREVENT):
                if event.event == 'score':
                    score.update(event.score)
                elif event.event == 'lives':
                    lives.update(event.lives)
                    if lives.lives == 0:
                        gameover = render_text("Game Over!!!", int(round(res[0]*0.1)))
                        gameover_rect  = gameover.get_rect()
                        gameover_rect.center = (res[0]/2, res[1]/4)
                        screen.blit(gameover, gameover_rect)
                        pygame.display.flip()
                        time.sleep(3)
                        menu(screen, clock, res)
                else:
                  print event
                
        clock.tick(60)


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

    menu(screen, clock, res)

if __name__ == '__main__':
    main()
