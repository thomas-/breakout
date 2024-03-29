#!/usr/bin/env python2.7

import argparse, os
from sys import exit
from random import randint, uniform

import time

import pygame
from pygame.locals import *
from sprites import Ball, Racket, Block, Score, Lives, Powerup, NameSprite

def render_text(s, fontsize):
    font = pygame.font.Font(None, fontsize)
    text = font.render(s, True, pygame.Color("white"))
    return text

def screen_message(text, screen, res):
    screen_message = render_text(text, rounder(res[0]*0.1))
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
        pygame.draw.rect(self.surf, pygame.Color("purple"),
            pygame.Rect(0, (self.selected+1)*(self._fontsize),
                self._width, self._fontsize))
        y = 0
        for text in self.text:
            x = self.surf.get_width()/2 - text.get_width()/2
            y += text.get_height()*1.5
            self.surf.blit(text, (x,y))

    def draw(self, screen):
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

        self.bg = pygame.image.load('bg.bmp')
        pygame.transform.scale(self.bg ,(self.res[0], self.res[1]))
        self.linethickness = rounder(self.res[0]/160)

        pygame.draw.line(self.bg, pygame.Color("white"),
            (self.res[0]*0.2375-self.linethickness, self.res[0]/16),
                (self.res[0]*0.2375-self.linethickness,self.res[1]), self.linethickness)

        pygame.draw.line(self.bg, pygame.Color("white"),
            (self.res[0]*0.7625+self.linethickness, self.res[0]/16),
                (self.res[0]*0.7625+self.linethickness, self.res[1]), self.linethickness)

        pygame.draw.line(self.bg, pygame.Color("white"),
            (self.res[0]*0.2375-self.linethickness,
                (self.res[0]/16 + self.linethickness*0.4)),
                    (self.res[0]*0.7625+self.linethickness,
                        (self.res[0]/16 + self.linethickness*0.4)), self.linethickness)

        self.screen.blit(self.bg, (0,0))
        pygame.display.flip()

        self.levelcount = 0

        self.racket = Racket('yellow', (self.res[0]*0.5, self.res[1]-40), self.res)

        self.score = Score(self.res)

        self.lives = Lives(self.res)

        self.currentpowerup = None
        self.powerupdrop = 60 * 15

        self.enteringname = False


    def run(self):

        self.ball = Ball("yellow", (self.res[0]*0.475, self.res[1]-45), self.racket,
                    self.levelLoader(self.levelcount), self.res)

        self.keymap = {
            pygame.K_SPACE: [self.ball.start, nop],
            pygame.K_LEFT: [self.racket.left, self.racket.right],
            pygame.K_RIGHT: [self.racket.right, self.racket.left]
            }

        self.isrunning = True

        self.sprites = pygame.sprite.RenderUpdates([self.score, self.lives, self.ball, self.racket])

        while self.isrunning:

            self.blockimages = pygame.sprite.RenderUpdates(self.blocks)

            self.managePowerups()

            self.blockimages.update()
            self.blockimages.draw(self.screen)

            self.sprites.update()
            self.sprites.draw(self.screen)

            pygame.display.flip()
            self.sprites.clear(self.screen, self.bg)
            self.blockimages.clear(self.screen, self.bg)


            self.events = pygame.event.get()
            for event in self.events:
                if (event.type == QUIT) or ((event.type == KEYUP) and (event.key == K_ESCAPE)):
                    menu(self.screen, self.clock, self.res)

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
                            screen_message("Game Over!", self.screen, self.res)
                            time.sleep(1)
                            self.screen.blit(self.bg, (0,0))
                            pygame.display.flip()
                            self.gameOver()
                    else:
                      print event

            if len(self.blocks) == 0 and self.levelcount < 4:
                screen_message("Level complete", self.screen, self.res)
                self.levelcount += 1
                time.sleep(1)
                self.screen.blit(self.bg, (0,0))
                pygame.display.flip()
                self.ball.reset()
                self.ball.blocks = self.levelLoader(self.levelcount)

            elif len(self.blocks) == 0 and self.levelcount == 4:
                screen_message("You win!!!", self.screen, self.res)
                time.sleep(1)
                self.screen.blit(self.bg, (0,0))
                pygame.display.flip()
                self.gameOver()

            self.clock.tick(60)


    def levelLoader(self, levelcount):

            self.racket.reset()

            screen_message("Level " + str(self.levelcount+1), self.screen, self.res)
            time.sleep(1)
            self.screen.blit(self.bg, (0,0))
            pygame.display.flip()

            levels = [
                [0, 4, 4, 10],
                [2, 5, 3, 11],
                [1, 5, 2, 12],
                [0, 6, 1, 13],
                [0, 6, 0, 14]
                #[0, 1, 0, 1],
                #[0, 1, 0, 1],
                #[0, 1, 0, 1],
                #[0, 1, 0, 1],
                #[0, 1, 0, 1]
            ]

            self.blocks = []
            for i in xrange(levels[self.levelcount][0], levels[self.levelcount][1]):
                for j in xrange(levels[self.levelcount][2], levels[self.levelcount][3]):
                    self.blocks.append(Block(1, (randint(5,240),randint(5,240),randint(5,240)),
                        (i,j), self.res))

            return self.blocks

    def managePowerups(self):

        if self.ball.dead and self.currentpowerup is not None:
            if self.currentpowerup.collected is True:
                self.currentpowerup.countdown = 0

        if self.currentpowerup is None:
            if not self.ball.dead:
                self.powerupdrop -= 1

                if self.powerupdrop <= 0:

                    droppercentages = [
                    (10, '1up'),
                    (0, 'slowball'),
                    (100, 'bigracket')
                    ]

                    choice = uniform(0, 100)
                    for chance, type in droppercentages:
                        if choice <= chance:
                            self.currentpowerup = Powerup(type, self.res)
                            self.sprites.add(self.currentpowerup)
                            break
            return

        if not self.currentpowerup.collected:

            if self.racket.rect.colliderect(self.currentpowerup.rect):
                if self.currentpowerup.type == 'bigracket':
                    self.racket.grow()
                elif self.currentpowerup.type == 'slowball':
                    self.ball.slowDown()
                elif self.currentpowerup.type == '1up':
                    self.lives.addLife()

                self.currentpowerup.collected = True
                self.sprites.remove(self.currentpowerup)

            else:
                alive = self.currentpowerup.update()
                if not alive:
                    self.sprites.remove(self.currentpowerup)
                    self.currentpowerup = None
                    self.powerupdrop = randint(60*5, 60*15)

        elif self.currentpowerup.countdown > 0:
            self.currentpowerup.countdown -= 1

        else:
            if self.currentpowerup is not None:

                if self.currentpowerup.type == 'bigracket':
                    self.racket.shrink()
                elif self.currentpowerup.type == 'slowball':
                    self.ball.speedUp()

                self.currentpowerup = None

                self.powerupdrop = randint(60*15, 60*25)

    def gameOver(self):

        highscores = self.parseHighScores()

        if self.score.score > int(highscores[-1][1]):
            screen_message("Enter Name:", self.screen, self.res)

            self.enteringname = True

            self.name = NameSprite(self.res, (self.res[0]/2, self.res[1]/3), rounder(self.res[0]*0.1))
            self.namesprite = pygame.sprite.RenderUpdates(self.name)

            while self.enteringname:

                for event in pygame.event.get():
                    if event.key == pygame.K_BACKSPACE:
                        self.name.removeLetter()
                    elif event.key == pygame.K_RETURN:
                        self.nameEntered()
                    elif event.type == pygame.KEYDOWN:
                        try:
                            char = chr(event.key)
                            if str(char) in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_':
                                 self.name.addLetter(char)
                        except:
                            pass

                    self.namesprite.update()
                    self.namesprite.draw(self.screen)
                    pygame.display.flip()
                    self.namesprite.clear(self.screen, self.bg)
        else:
            self.showHighScores(highscores)

    def nameEntered(self):
        username = self.name.text

        self.screen.blit(self.bg, (0,0))
        pygame.display.flip

        highscores = self.parseHighScores()

        newscores = []

        for name, score in highscores:
            if self.score.score > int(score):
                newscores.append((username, str(self.score.score)))
                self.score.score = 0
            newscores.append((name, score))
        newscores = newscores[0:10]

        highscorefile = 'highscores.txt'
        f = open(highscorefile, 'w')
        for name, score in newscores:
            f.write("%s: %s\n" % (name, score))
        f.close()

        self.showHighScores(newscores)

    def parseHighScores(self):
        highscorefile = 'highscores.txt'
        if os.path.isfile(highscorefile):
            f = open(highscorefile, 'r')
            lines = f.readlines()
            scores = []

            for line in lines:
                scores.append( line.strip().split(':') )
            return scores
        else:
            f = open (highscorefile, 'w')
            f.write("""JJJ:0000
III:0000
HHH:0000
GGG:0000
FFF:0000
EEE:0000
DDD:0000
CCC:0000
BBB:0000
AAA:0000""")
            f.close()
            return self.parseHighScores()

    def showHighScores(self, scores):

        font = pygame.font.Font(None, rounder(self.res[0]*0.05))
        color = pygame.Color("white")

        for i in range(len(scores)):
            name, score = scores[i]
            nameimage = font.render(name, True, color)
            namerect = nameimage.get_rect()
            namerect.left = rounder(self.res[0]*0.3)
            namerect.centery = rounder(self.res[0]/8)+(i*(namerect.height + rounder(self.res[0]/40)))
            self.screen.blit(nameimage, namerect)

            scoreimage = font.render(score, True, color)
            scorerect = scoreimage.get_rect()
            scorerect.right = rounder(self.res[0]*0.7)
            scorerect.centery = namerect.centery
            self.screen.blit(scoreimage, scorerect)

        pygame.display.flip()
        time.sleep(3)
        menu(self.screen, self.clock, self.res)


def nop():
    pass


def menu(screen, clock, res):

    menu_position = 1

    mainmenu = [
            ["START GAME", 'play'],
            ["SCREEN SETTINGS", 'settings'],
            ["HIGH SCORES", 'highscores'],
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
            if (event.type == KEYDOWN) and (event.key == K_UP) and menu_position > 1:
                o.up()
                menu_position -= 1
            if (event.type == KEYDOWN) and (event.key == K_DOWN) and menu_position < 4:
                o.down()
                menu_position += 1
            if (event.type == KEYDOWN) and (event.key == K_RETURN):
                selected = o.select()
                if selected == 'play':
                    breakout = Breakout(screen, clock, res)
                    breakout.run()
                if selected == 'highscores':
                    breakout = Breakout(screen, clock, res)
                    breakout.showHighScores(breakout.parseHighScores())
                if selected == 'settings':
                    settings(screen, clock, res)
                else:
                    selected()
        clock.tick(30)

def settings(screen, clock, res):

    settings_position = 1

    settings = [
        ["640x480", 'menu_1'],
        ["800x600", 'menu_2'],
        ["1024x768", 'menu_3'],
        ["1280x800", 'menu_4'],
        ["FULLSCREEN", 'menu_5']
        ]

    s = Options((res[0], res[1]), settings)

    issettings = True

    while issettings:
        s.update()
        s.draw(screen)
        pygame.display.flip()
        events = pygame.event.get()
        for event in events:
            if (event.type == QUIT):
                issettings = False
            if (event.type == KEYUP) and (event.key == K_ESCAPE):
                issettings = False
            if (event.type == KEYDOWN) and (event.key == K_UP) and settings_position > 1:
                s.up()
                settings_position -= 1
            if (event.type == KEYDOWN) and (event.key == K_DOWN) and settings_position < 5:
                s.down()
                settings_position += 1
            if (event.type == KEYDOWN) and (event.key == K_RETURN):
                selected = s.select()
                if selected == 'menu_1':
                    res = (640,480)
                    createScreen(screen, clock, res)
                elif selected == 'menu_2':
                    res = (800,600)
                    createScreen(screen, clock, res)
                elif selected == 'menu_3':
                    res = (1024,768)
                    createScreen(screen, clock, res)
                elif selected == 'menu_4':
                    res = (1280,800)
                    createScreen(screen, clock, res)
                elif selected == 'menu_5':
                    screen = pygame.display.set_mode((0,0), FULLSCREEN, 16)
                    info = pygame.display.Info()
                    res = info.current_w, info.current_h
                else:
                    selected()
        clock.tick(30)

def createScreen(screen, clock, res):
    pygame.display.set_caption('Breakout - g51fse_cw')
    screen = pygame.display.set_mode(res)
    print "Using display driver:", pygame.display.get_driver()
    print pygame.display.Info()
    menu(screen, clock, res)

def main():

    res = (800,600)
    screen = pygame.display.set_mode(res)
    pygame.init()
    clock = pygame.time.Clock()

    createScreen(screen, clock, res)

if __name__ == '__main__':
    main()
