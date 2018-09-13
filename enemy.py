import pygame
from random import randint


class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/enemy1.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load('images/enemy1_down1.png').convert_alpha(),
                                    pygame.image.load('images/enemy1_down2.png').convert_alpha(),
                                    pygame.image.load('images/enemy1_down3.png').convert_alpha(),
                                    pygame.image.load('images/enemy1_down4.png').convert_alpha()])
        self.rect = self.image.get_rect()
        self.limit_width,self.limit_height = bg_size[0],bg_size[1]
        self.speed = 2
        self.active = True
        self.rect.left,self.rect.top = randint(0,self.limit_width - self.rect.width),randint(-5*self.limit_height,0)

    def move(self):
        if self.rect.top < self.limit_height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.rect.left,self.rect.top = randint(0,self.limit_width - self.rect.width),randint(-5*self.limit_height,0)

class MidEnemy(pygame.sprite.Sprite):
    ENERGY = 8
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/enemy2.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.image_hit = pygame.image.load('images/enemy2_hit.png').convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load('images/enemy2_down1.png').convert_alpha(),
                                    pygame.image.load('images/enemy2_down2.png').convert_alpha(),
                                    pygame.image.load('images/enemy2_down3.png').convert_alpha(),
                                    pygame.image.load('images/enemy2_down4.png').convert_alpha()])
        self.rect = self.image.get_rect()
        self.limit_width,self.limit_height = bg_size[0],bg_size[1]
        self.speed = 1
        self.active = True
        self.hit = False
        self.energy = MidEnemy.ENERGY
        self.rect.left,self.rect.top = randint(0,self.limit_width - self.rect.width),randint(-10*self.limit_height,
                                                                                             -self.limit_height)

    def move(self):
        if self.rect.top < self.limit_height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy = MidEnemy.ENERGY
        self.rect.left,self.rect.top = randint(0,self.limit_width - self.rect.width),randint(-10*self.limit_height,
                                                                                             -self.limit_height)

class GiantEnemy(pygame.sprite.Sprite):
    ENERGY = 20
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load('images/enemy3_n1.png').convert_alpha()
        self.image2 = pygame.image.load('images/enemy3_n2.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image1)
        self.image_hit = pygame.image.load('images/enemy2_hit.png').convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load('images/enemy3_down1.png').convert_alpha(),
                                    pygame.image.load('images/enemy3_down2.png').convert_alpha(),
                                    pygame.image.load('images/enemy3_down3.png').convert_alpha(),
                                    pygame.image.load('images/enemy3_down4.png').convert_alpha(),
                                    pygame.image.load('images/enemy3_down5.png').convert_alpha(),
                                    pygame.image.load('images/enemy3_down6.png').convert_alpha()])
        self.rect = self.image1.get_rect()
        self.limit_width,self.limit_height = bg_size[0],bg_size[1]
        self.speed = 0.5
        self.active = True
        self.hit = False
        self.energy = GiantEnemy.ENERGY
        self.rect.left,self.rect.top = randint(0,self.limit_width - self.rect.width),randint(-15*self.limit_height,
                                                                                             -5 * self.limit_height)

    def move(self):
        if self.rect.top < self.limit_height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy = GiantEnemy.ENERGY
        self.rect.left,self.rect.top = randint(0,self.limit_width - self.rect.width),randint(-15*self.limit_height,
                                                                                             -5 * self.limit_height)