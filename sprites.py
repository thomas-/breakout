import math
import pygame
from pygame.sprite import Sprite

def rounder(number):
    result = int(round(number))
    return result

class Block(Sprite):
    
    def __init__(self, life, color, position, res):
        Sprite.__init__(self)
        self.blockwidth = res[0]*0.0375
        self.blockheight = self.blockwidth/2
        self.image = pygame.Surface((self.blockwidth-(self.blockwidth/30),self.blockheight-(self.blockheight/15)))
        self.image.fill(color)
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.top = res[0]*0.15 + (position[0]*self.blockheight)
        self.rect.left = (res[0]+(res[0]/160))*0.2375 + (position[1]*self.blockwidth)
        self.life = life
    def hit(self):
        return True


class Ball(Sprite):
    def __init__(self, color, position, racket, blocks, res):
        Sprite.__init__(self)
        self.res = res
        self.position = position
        self.size = self.res[1]/100
        self.image = pygame.Surface((self.size, self.size))
        pygame.draw.circle(self.image, pygame.Color(color), ((self.size/2), (self.size/2)), (self.size/2))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.velocity = [0,0]
        self.racket = racket
        self.blocks = blocks
        self.dead = True
        self.combo = 0
        if self.res[1] > 700:
            self.speed = self.res[1]/100
            self.maxspeed = self.res[1]/50
        else:
            self.speed = self.res[1]/200
            self.maxspeed = self.res[1]/100       

    def start(self):
        if self.dead:
            self.velocity = [self.speed, -self.speed]
            self.dead = False

    def collider(self, block):
        if hasattr(block, 'velocity'):
            self.velocity[0] += block.velocity * 0.25
            
            if math.fabs(self.velocity[0]) > self.maxspeed:
                if self.velocity[0] > 0:
                    self.velocity[0] = self.maxspeed
                if self.velocity[0] < 0:
                    self.velocity[0] = -self.maxspeed
    
        cornervalue = rounder(self.res[1]/160)
        
        #top left corner
        if self.rect.colliderect(
            pygame.Rect(block.rect.left, block.rect.top, cornervalue, cornervalue)):
                speed = math.hypot(self.velocity[0], self.velocity[1])
                if self.velocity[0] >= 0:
                    self.velocity[0] = -speed * .7071
                if self.velocity[1] >= 0:
                    self.velocity[1] = -speed * .7071
                self.rect.bottom = block.rect.top -1
                return
        
         #top right corner
        if self.rect.colliderect(
            pygame.Rect(block.rect.right, block.rect.top, cornervalue, cornervalue)):
                speed = math.hypot(self.velocity[0], self.velocity[1])
                if self.velocity[0] <= 0:
                    self.velocity[0] = speed * .7071
                if self.velocity[1] >= 0:
                    self.velocity[1] = -speed * .7071
                self.rect.bottom = block.rect.top -1
                return       

        #bottom left corner
        if self.rect.colliderect(
            pygame.Rect(block.rect.left, block.rect.bottom, cornervalue, cornervalue)):
                speed = math.hypot(self.velocity[0], self.velocity[1])
                if self.velocity[0] >= 0:
                    self.velocity[0] = -speed * .7071
                if self.velocity[1] <= 0:
                    self.velocity[1] = speed * .7071
                self.rect.top = block.rect.bottom -1
                return                

        #bottom right corner
        if self.rect.colliderect(
            pygame.Rect(block.rect.right, block.rect.bottom, cornervalue, cornervalue)):
                speed = math.hypot(self.velocity[0], self.velocity[1])
                if self.velocity[0] <= 0:
                    self.velocity[0] = speed * .7071
                if self.velocity[1] <= 0:
                    self.velocity[1] = speed * .7071
                self.rect.top = block.rect.bottom -1
                return 
                
        sidevalue = rounder(self.res[1]/400)
        
        # top
        if self.rect.colliderect(
            pygame.Rect(block.rect.left, block.rect.top, block.rect.width, sidevalue)):
                self.velocity[1] *= -1
                self.rect.bottom = block.rect.top - 1
                return

        # bot
        elif self.rect.colliderect(
            pygame.Rect(block.rect.left, block.rect.bottom - sidevalue, block.rect.width, sidevalue)):
                self.velocity[1] *= -1
                self.rect.top = block.rect.bottom + 1
                return

            
        # left
        if self.rect.collidepoint((block.rect.left, block.position[1])):
                self.velocity[0] *= -1
                self.rect.right = block.rect.left - 1
                return

        # right
        elif self.rect.collidepoint((block.rect.right, block.position[1])):
                self.velocity[0] *= -1
                self.rect.left = block.rect.right + 1
                return

    def update(self):
        if self.dead:
            self.rect.center = (self.racket.rect.center[0], self.racket.rect.top - 10)

        self.rect.move_ip(*self.velocity)
        if self.rect.colliderect(self.racket.rect):
            self.combo = 0
            self.collider(self.racket)

        hits = pygame.sprite.spritecollide(self, self.blocks, False)
                
        if len(hits) >=2:
            if hits[0].rect.y == hits[1].rect.y:
                self.velocity[1] *= -1
                self.rect.top = hits[0].rect.bottom + 1
            
            else:
                if self.velocity[0] > 0:
                    self.rect.right = hits[0].rect.left - 1
                else:
                    self.rect.left = hits[0].rect.right + 1
                self.velocity[0] *= -1
              
            for block in hits:
                pygame.event.post(pygame.event.Event(pygame.USEREVENT,
                                                     {'event': 'score',
                                                      'score': len(hits)*10
                                                      }))
                self.blocks.remove(block)
            
        
        if len(hits) == 1:
            self.collider(hits[0])
            if hits[0].hit():
                self.combo += 1
                pygame.event.post(pygame.event.Event(pygame.USEREVENT,
                                                     {'event': 'score',
                                                      'score': self.combo*10
                                                      }))
                self.blocks.remove(hits[0])
                

        if self.rect.top <= ((self.res[0]/16) + (self.res[0]/160)):
            self.velocity[1] *= -1
            self.rect.top = ((self.res[0]/16) + (self.res[0]/160))+1
        if self.rect.left <= self.res[0]*0.2375:
            self.velocity[0] *= -1
            self.rect.left = (self.res[0]*0.2375)+1
        elif self.rect.right > self.res[0]*0.7625:
            self.velocity[0] *= -1
            self.rect.right = (self.res[0]*0.7625)-1
        if self.rect.bottom > self.res[1]:
            if self.velocity[1] > 0:
                self.velocity[0] = 0
                self.velocity[1] = 0
                self.killed()

    def killed(self):
        self.combo = 0
        self.dead = True
        pygame.event.post(pygame.event.Event(pygame.USEREVENT,
                                                {'event': 'lives',
                                                'lives': -1
                                                }))
        self.reset()
        self.racket.reset()
                                                       
    def reset(self):
        self.rect.center = self.position

class Racket(Sprite):
    def __init__(self, color, position, res):
        Sprite.__init__(self)
        self.position = position
        self.res = res
        self.image = pygame.Surface([(self.res[0]/16), (self.res[0]/80)])
        self.rect = pygame.Rect(0, 0, (self.res[0]/16), (self.res[0]/80))
        pygame.draw.rect(self.image, pygame.Color(color), self.rect)
        self.rect.center = position
        self.velocity = 0

    def left(self):
        self.velocity -= self.res[0]/100

    def right(self):
        self.velocity += self.res[0]/100

    def update(self):
        if self.velocity != 0:
            if self.rect.left + self.velocity < (self.res[0] + (self.res[0]/160)) * 0.2375:
                self.rect.left = (self.res[0] + (self.res[0]/160)) * 0.2375
            elif self.rect.right + self.velocity > self.res[0] * 0.7625:
                self.rect.right = self.res[0] * 0.7625
            else:
                self.rect.move_ip(self.velocity, 0)
                
    def reset(self):
        self.rect.center = self.position

class Score(Sprite):
    def __init__(self, res, score=0):
        Sprite.__init__(self)
        self.res = res
        self.image = pygame.Surface([(self.res[0]*0.225), (self.res[0]/16)])
        self.rect = self.image.get_rect()
        self.rect.bottom = self.res[1]
        self.score = score
        self.font = pygame.font.Font(None, int(round(self.res[0]*0.06)))
        self.update()

    def update(self, score=0):
        self.image.fill(pygame.Color("black"))
        self.score += score
        text = self.font.render(str(self.score), True, pygame.Color("white"))
        rect = text.get_rect()
        rect.right = self.res[0]*0.225
        self.image.blit(text, rect)

class Lives(Sprite):
    def __init__(self, res, lives=3):
        Sprite.__init__(self)
        self.res = res
        self.image = pygame.Surface([(self.res[0]*0.225), (self.res[0]/16)])
        self.rect = self.image.get_rect()
        self.rect.bottom = self.res[1]
        self.rect.right = self.res[0]
        self.lives = lives
        self.font = pygame.font.Font(None, int(round(self.res[0]*0.06)))
        self.update()
        
    def update(self, lives=0):
        self.image.fill(pygame.Color("black"))
        self.lives += lives
        text = self.font.render("Lives: "+str(self.lives), True, pygame.Color("white"))
        rect = text.get_rect()
        self.image.blit(text, rect)        
            


