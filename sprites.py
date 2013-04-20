import pygame
from pygame.sprite import Sprite

class Block(Sprite):
    blockwidth = 30
    blockheight = 15
    def __init__(self, color, position):
        Sprite.__init__(self)
        self.image = pygame.Surface((self.blockwidth-1,self.blockheight-1))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.top = 120 + (position[0]*self.blockheight)
        self.rect.left = 190 + (position[1]*self.blockwidth)

    def hit(self):
        pass


class Ball(Sprite):
    def __init__(self, color, position, racket, blocks):
        Sprite.__init__(self)
        self.image = pygame.Surface((6,6))
        pygame.draw.circle(self.image, pygame.Color(color), (3,3), 3)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.velocity = [0,0]
        self.racket = racket
        self.blocks = blocks

    def start(self):
        self.velocity = [3, -3]

    def collider(self, block):
        # left
        if self.rect.colliderect(
            pygame.Rect(block.rect.left, block.rect.top, 1, block.rect.height)):
            self.velocity[0] *= -1
            self.rect.right = block.rect.left - 1
            return

        # right
        if self.rect.colliderect(
            pygame.Rect(block.rect.right, block.rect.top, 1, block.rect.width)):
            self.velocity[0] *= -1
            self.rect.left = block.rect.right + 1
            return

        # top
        if self.rect.colliderect(
            pygame.Rect(block.rect.left, block.rect.top, block.rect.width, 1)):
            self.velocity[1] *= -1
            self.rect.bottom = block.rect.top - 1
            return

        # bot
        if self.rect.colliderect(
            pygame.Rect(block.rect.left, block.rect.bottom, block.rect.width, 1)):
            self.velocity[1] *= -1
            self.rect.top = block.rect.bottom + 1
            return


    def update(self):
        self.rect.move_ip(*self.velocity)
        if self.rect.colliderect(self.racket.rect):
            self.collider(self.racket)

        hits = pygame.sprite.spritecollide(self, self.blocks, False)

        if len(hits)>0:
            self.collider(hits[0])
            self.blocks.remove(hits[0])

        if self.rect.top < 50:
            self.velocity[1] *= -1
            self.rect.top = 51
        if self.rect.left < 190:
            self.velocity[0] *= -1
            self.rect.left = 191
        if self.rect.right > 610:
            self.velocity[0] *= -1
            self.rect.right = 609
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
        if self.rect.left < 200 and self.velocity < 0:
            pass
        elif self.rect.right > 600 and self.velocity > 0:
            pass
        else:
            self.rect.move_ip(self.velocity, 0)


