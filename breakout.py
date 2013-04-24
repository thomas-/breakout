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
    
def screen_message(text, screen, res):
    screen_message = render_text(text, int(round(res[0]*0.1)))
    screen_message_rect  = screen_message.get_rect()
    screen_message_rect.center = (res[0]/2, res[1]/4)
    screen.blit(screen_message, screen_message_rect)
    pygame.display.flip()

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


class Breakout(object):

    def __init__(self, screen, clock, res):
        
        self.res = res
        self.screen = screen
        self.clock = clock
        
        self.levelcount = 0
        
        self.racket = Racket('yellow', (self.res[0]*0.5, self.res[1]-40), self.res)
             
        self.score = Score(self.res)

        self.lives = Lives(self.res)
    
        self.levelLoader(self.levelcount)

    def run(self):
        
        isrunning = True

        while isrunning:
            
            self.bg = pygame.Surface((self.res[0],self.res[1]))
            self.bg.fill(pygame.Color("black"))
            
            self.linethickness = rounder(self.res[0]/160)
            pygame.draw.line(self.bg, pygame.Color("white"), (self.res[0]*0.2375-self.linethickness, self.res[0]/16), (self.res[0]*0.2375-self.linethickness,self.res[1]), self.linethickness)
            pygame.draw.line(self.bg, pygame.Color("white"), (self.res[0]*0.7625+self.linethickness, self.res[0]/16), (self.res[0]*0.7625+self.linethickness, self.res[1]), self.linethickness)
            pygame.draw.line(self.bg, pygame.Color("white"), (self.res[0]*0.2375-self.linethickness, (self.res[0]/16 + self.linethickness*0.4)), (self.res[0]*0.7625+self.linethickness, (self.res[0]/16 + self.linethickness*0.4)), self.linethickness)
            self.screen.blit(self.bg, (0,0))
            
            self.sprites = pygame.sprite.Group([self.racket, self.ball, self.blocks, self.score, self.lives])

            self.sprites.update()
            self.sprites.draw(self.screen)
            pygame.display.flip()
            self.sprites.clear(self.screen, self.bg)

            self.events = pygame.event.get()
            for event in self.events:
                if (event.type == QUIT) or ((event.type == KEYUP) and (event.key == K_ESCAPE)):
                    isrunning = False
                if (event.type == pygame.KEYDOWN) and (event.key in self.keymap):
                    self.keymap[event.key][0]()
                if (event.type == pygame.KEYUP) and (event.key in self.keymap):
                    self.keymap[event.key][1]()
                if (event.type == pygame.USEREVENT):
                    if event.event == 'score':
                        self.score.update(event.score)
                    elif event.event == 'lives':
                        self.lives.update(event.lives)
                        if self.lives.lives == 0:
                            screen_message("Game over!!!", self.screen, self.res)
                            time.sleep(2)
                            menu(self.screen, self.clock, self.res)
                    else:
                      print event
            
            if self.ball.blockcount == 0 and self.levelcount < 4:
                screen_message("Level complete", self.screen, self.res)
                self.levelcount += 1
                self.levelLoader(self.levelcount)
                
            elif self.ball.blockcount == 0 and self.levelcount == 4:
                screen_message("You win!!!", self.screen, self.res)
                time.sleep(2)
                menu(self.screen, self.clock, self.res)
                              
            self.clock.tick(60)


    def levelLoader(self, levelcount):
            
            self.racket.reset()
            self.racket.update()
            self.blockcount = 0
            self.bg = pygame.Surface((self.res[0], self.res[1]))
            self.bg.fill(pygame.Color("black"))
            self.screen.blit(self.bg, (0,0))
            pygame.display.flip()
            
            screen_message("Level " + str(self.levelcount+1), self.screen, self.res)
            time.sleep(1)
  
            levels = [
                # [0, 4, 4, 10],
                # [2, 5, 3, 11],
                # [1, 5, 2, 12],
                # [0, 6, 1, 13],
                # [0, 6, 0, 14]
                [0, 1, 0, 1],
                [0, 1, 0, 1],
                [0, 1, 0, 1],
                [0, 1, 0, 1],
                [0, 1, 0, 1]
            ]
            
            self.blocks = []
            for i in xrange(levels[self.levelcount][0], levels[self.levelcount][1]):
                for j in xrange(levels[self.levelcount][2], levels[self.levelcount][3]):            
                    self.blocks.append(Block(1, (randint(5,240),randint(5,240),randint(5,240)), (i,j), self.res))
                    self.blockcount += 1
            
            self.ball = Ball("yellow", (self.res[0]*0.475, self.res[1]-45), self.racket, self.blocks, self.blockcount, self.res)
            
            self.keymap = {
                pygame.K_SPACE: [self.ball.start, nop],
                pygame.K_LEFT: [self.racket.left, self.racket.right],
                pygame.K_RIGHT: [self.racket.right, self.racket.left]
                }
            
            self.ball.combo = 0
            
   
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
                    breakout = Breakout(screen, clock, res)
                    breakout.run()
                else:
                    selected()
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
    
    pygame.display.set_caption('Breakout - g51fse_cw')
    if fs:
        screen = pygame.display.set_mode((0,0), FULLSCREEN, 16)
        info = pygame.display.Info()
        res = info.current_w, info.current_h
    else:
        screen = pygame.display.set_mode((res))
    print "Using display driver:", pygame.display.get_driver()
    print pygame.display.Info()

    pygame.init()
    clock = pygame.time.Clock()

    menu(screen, clock, res)

if __name__ == '__main__':
    main()
