import pygame
import sys
import traceback
from myplane import MyPlane
from enemy import SmallEnemy,MidEnemy,GiantEnemy
from bullet import Bullet1




pygame.init() #pygame module initialize
pygame.mixer.init()  #music initialize

bg_size = width,height = 480,700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("Plane Fight")
background = pygame.image.load("images/background1.png").convert()

#difine the RGB color (the RGB ways)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)

pygame.mixer.music.load('sound/game_music.ogg')
pygame.mixer.music.set_volume(0.1)
bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
bullet_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound('sound/supply.wav')
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound('sound/get_bomb.wav')
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound('sound/get_bullet.wav')
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound('sound/upgrade.wav')
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound('sound/enemy3_flying.wav')
enemy3_fly_sound.set_volume(0.1)
enemy1_down_sound = pygame.mixer.Sound('sound/enemy1_down.wav')
enemy1_down_sound.set_volume(0.1)
enemy2_down_sound = pygame.mixer.Sound('sound/enemy2_down.wav')
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound('sound/enemy3_down.wav')
enemy3_down_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound('sound/me_down.wav')
me_down_sound.set_volume(0.2)

def add_small_enemies(group1,group2,number):
    for i in range(number):
        e1 = SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1,group2,number):
    for i in range(number):
        e2 = MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)

def add_giant_enemies(group1,group2,number):
    for i in range(number):
        e3 = GiantEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)

def main():
    pygame.mixer.music.play(-1) #play music circulatory
    clock = pygame.time.Clock() #creat an object of clock(to set fps)

    running = True
    switch_image = True #to exchange pics(creat a dynamic effects)
    delay = 100
    #the index of indicating dynamic pics
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    plane_destroy_index = 0

    score = 0
    score_font = pygame.font.Font('font/font.ttf',36)

    paused = False
    pause_nor_image = pygame.image.load('images/pause_nor.png').convert_alpha()
    pause_pressed_image = pygame.image.load('images/pause_pressed.png').convert_alpha()
    resume_nor_image = pygame.image.load('images/resume_nor.png').convert_alpha()
    resume_pressed_image = pygame.image.load('images/resume_pressed.png').convert_alpha()
    pause_rect = pause_nor_image.get_rect()
    pause_rect.left,pause_rect.top = width - pause_rect.width - 10,10
    pause_image = pause_nor_image


    plane = MyPlane(bg_size)
    enemies = pygame.sprite.Group()

    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies,enemies,15)

    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies,enemies,6)

    giant_enemies = pygame.sprite.Group()
    add_giant_enemies(giant_enemies,enemies,2)

    #add common bullets
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4
    for i in range(BULLET1_NUM):
        bullet1.append(Bullet1(plane.rect.midtop)) #midtop is attribution of Rect


#mian running programme
    while running:
        for event in pygame.event.get(): #get event consecutively
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and pause_rect.collidepoint(event.pos):
                    paused = not paused
            elif event.type == pygame.MOUSEMOTION:
                if pause_rect.collidepoint(event.pos):#check whether the mouse in the range of pause_rect
                    if paused:
                        pause_image = resume_pressed_image
                    else:
                        pause_image = pause_pressed_image
                else:
                    if paused:
                        pause_image = resume_nor_image
                    else:
                        pause_image = pause_nor_image

        #draw background
        screen.blit(background,(0,0))  #draw one pic onto anther.(0,0): represent the relative location

        if not paused:
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
                plane.moveUp()
            if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
                plane.moveLeft()
            if key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
                plane.moveDown()
            if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
                plane.moveRight()


            #the plane fires
            if not(delay % 10):
                bullet1[bullet1_index].reset(plane.rect.midtop)
                bullet1_index = (bullet1_index + 1) % BULLET1_NUM
            #check whether bullets hit enemies
            for bullet in bullet1:
                if bullet.active:
                    bullet.move()
                    screen.blit(bullet.image,bullet.rect)
                    collapse = pygame.sprite.spritecollide(bullet,enemies,False,pygame.sprite.collide_mask)
                    if collapse:
                        bullet.active = False
                        for e in collapse:
                            if e in mid_enemies or e in giant_enemies:
                                e.energy -= 1
                                e.hit = True
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False

            #draw giant enemies
            for each in giant_enemies:
                if each.active: #survive
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit,each.rect)
                        each.hit = False
                    else:
                        if switch_image: #creat a dynamic effect
                            screen.blit(each.image1,each.rect)
                        else:
                            screen.blit(each.image2,each.rect)
                    #draw giant enemies's blood
                    pygame.draw.line(screen,BLACK,(each.rect.left,each.rect.top - 5),(each.rect.right,each.rect.top - 5),2)
                    energy_remain = each.energy / GiantEnemy.ENERGY
                    if energy_remain > 0.3:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen,energy_color,(each.rect.left,each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain,each.rect.top - 5),2)

                    if each.rect.bottom > -50: #when the giant enemies appear play music
                        enemy3_fly_sound.play(-1)
                else: #destroy
                    if not(delay % 3): #generate dynamic effect
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index],each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            enemy3_fly_sound.stop()
                            score += 20
                            each.reset()

            #draw mid enemies
            for each in mid_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit,each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image,each.rect)
                    #draw giant enemies's blood
                    pygame.draw.line(screen,BLACK,(each.rect.left,each.rect.top - 5),(each.rect.right,each.rect.top - 5),2)
                    energy_remain = each.energy / MidEnemy.ENERGY
                    if energy_remain > 0.3:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen,energy_color,(each.rect.left,each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain,each.rect.top - 5),2)
                else:
                    if not(delay % 3):
                        if e2_destroy_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index],each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 10
                            each.reset()

            #draw small enemies
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image,each.rect)
                else:
                    if not(delay % 3):
                        if e1_destroy_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index],each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 1
                            each.reset()

            #check whether occurs collapse between plane and enemies
            collapse = pygame.sprite.spritecollide(plane,enemies,False,pygame.sprite.collide_mask)
            #the statement returns two types(one is a list,anther is bool)
            if collapse:
                plane.active = False
                for e in collapse:
                    e.active = False

            #draw plane and creat a dynamic effect
            if plane.active:
                if switch_image:
                    screen.blit(plane.image1,plane.rect)
                else:
                    screen.blit(plane.image2,plane.rect)
            else:
                me_down_sound.play()
                if not(delay % 3):
                    screen.blit(plane.destroy_images[plane_destroy_index],plane.rect)
                    plane_destroy_index = (plane_destroy_index + 1) % 4

        score_text = score_font.render('Score : %s'%str(score),True,WHITE)
        screen.blit(score_text,(10,5))

        screen.blit(pause_image,pause_rect)

        if not (delay % 5):
            switch_image = not switch_image

        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip() #update the full display Surface(temporary stored in buffer) to the screen
        clock.tick(60) #fps is 60 per second

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()  #print the exception
        pygame.quit()

