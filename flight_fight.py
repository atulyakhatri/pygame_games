# show score on the screen -- done
# create an entry and out screen -- needs another day 
# database of player name and high score -- after next game

#use with_alpha for transparent and any geometrical shape not just rectangle

import time
# from tracemalloc import reset_peak
import pygame
import random
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_p,
    K_s,
    K_r,
    K_o,
    QUIT,
)
from sqlalchemy import false

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 720
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
BLUE = [41, 170, 227]
GREEN = [0, 120, 0]


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(
            r"D:\All_code\srk_pyt\all_pygame\flight_fight\SeekPng.com_airplane-png_2044225.png").convert()
        self.surf = pygame.transform.scale(self.surf, (90, 80))
        self.surf.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -7)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 7)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-7, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(7, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(
            r"D:\All_code\srk_pyt\all_pygame\flight_fight\missile.png").convert()
        self.surf = pygame.transform.scale(self.surf, (50, 40))
        self.surf.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 15)
        # self.score = 0
        # self.speed = random.randint(3, 5)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            global score
            score += 1


class Cloud(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super(Cloud, self).__init__()
        self.surf = pygame.image.load(
            r"D:\All_code\srk_pyt\all_pygame\flight_fight\CLOUD4.png").convert()
        self.surf = pygame.transform.scale(self.surf, (120, 80))
        self.surf.set_colorkey(BLACK, RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-8, 0)
        if self.rect.right < 0:
            self.kill()


pygame.mixer.init(channels=4)
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.load(r"D:\All_code\srk_pyt\all_pygame\flight_fight\music.mp3")
pygame.mixer.music.play(-1)
# pygame.mixer.music.pause()

# backgrounMusc = pygame.mixer.Sound(r"D:\All_code\srk_pyt\all_pygame\flight_fight\music.mp3")
# backgrounMusc.set_volume(0.4)
# backgrounMusc.play(-1)

pygame.font.init()
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
score = 0

ENEMY_OCUURING_SPEED = 500
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, ENEMY_OCUURING_SPEED)

CLOUD_OCUURING_SPEED = 1000
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, CLOUD_OCUURING_SPEED)

player = Player()

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(clouds)
myfont = pygame.font.SysFont("monospace", 16)

# score_board = pygame.font.Font.render(str(score),True,GREEN)
# star_display = score.get_rect()

clock = pygame.time.Clock()

move_up_sound = pygame.mixer.Sound(
    r"D:\All_code\srk_pyt\all_pygame\flight_fight\die2.mp3")
move_up_sound.set_volume(0.1)
move_down_sound = pygame.mixer.Sound(
    r"D:\All_code\srk_pyt\all_pygame\flight_fight\score.mp3")
move_down_sound.set_volume(0.1)
collision_sound = pygame.mixer.Sound(
    r"D:\All_code\srk_pyt\all_pygame\flight_fight\die1.mp3")
move_down_sound.set_volume(0.1)


reset_start = 2
def run_game():
    global reset_start
    paused_music = 0
    # time_end = 0
    RUN = True
    IN,OUT,RUNNING, PAUSE = -2, -1, 0, 1
    state = IN
    while RUN:
        for event in pygame.event.get():
            if event.type == QUIT:
                # pygame.mixer.music.stop()
                # pygame.mixer.quit()
                # move_up_sound.stop()
                # move_down_sound.stop()
                collision_sound.play()
                RUN = False

            elif event.type == KEYDOWN:
                if state == RUNNING:
                    if event.key == K_p:
                        state = PAUSE
                if state == PAUSE:
                    if event.key == K_s:
                        state = RUNNING
                elif state == IN:
                    if event.key == K_r:
                        state = RUNNING
                        
                elif state == OUT:
                    if event.key == pygame.K_c:
                        # pygame.mixer.music.stop()
                        # pygame.mixer.quit()
                        # new_enemy.kill()
                        reset_start = 2
                        RUN = False
            


            elif state == RUNNING:
                if event.type == ADDENEMY:
                    new_enemy = Enemy()

                    enemies.add(new_enemy)
                    all_sprites.add(new_enemy)

                elif event.type == ADDCLOUD:
                    new_cloud = Cloud()
                    clouds.add(new_cloud)
                    all_sprites.add(new_cloud)

        if state == IN:
            introText1 = myfont.render("WELCOME", 1, (0, 0, 0))
            introtext2 = myfont.render("TO FLYING FLIGHT", 1, (0, 0, 0))
            introtext3 = myfont.render("GAME", 1, (0, 0, 0))
            introtext4 = myfont.render("Enter r to play", 1, (0, 0, 0))
            screen.fill(BLUE)
            screen.blit(introText1, ((SCREEN_WIDTH/3)-20, (SCREEN_HEIGHT/3) - 20))
            screen.blit(introtext2, ((SCREEN_WIDTH/3)-50, SCREEN_HEIGHT/3))
            screen.blit(introtext3, ((SCREEN_WIDTH/3)-10, (SCREEN_HEIGHT/3) + 20))
            screen.blit(introtext4, ((SCREEN_WIDTH/3)-40, (SCREEN_HEIGHT/3) + 40))
            # for event in pygame.event.get():
            # if pygame.event. == KEYDOWN:
            #     if pygame.event.key == K_r:
            #         state = RUNNING
                        # break
                    # if event.key == K_o:
                    #     RUN = False
                # state = RUNNING
            
        if state == OUT:
            # RUN = False
            outroText1 = myfont.render("OHHHH!", 1, BLACK)
            outrotext2 = myfont.render("BAD LUCK", 1, BLACK)
            outrotext3 = myfont.render("GAME OVERR!", 1, BLACK)
            outrotext4 = myfont.render("Enter c to quit", 1, BLACK)
            scoretext = myfont.render(f"You Scored {score}", 1, (0, 0, 0))
            screen.fill(BLUE)
            # pygame.time.delay(10000)

            # pygame.time.delay(10000)
            
            # collision_sound.stop()
            
            # pygame.mixer.music.stop()
            # pygame.mixer.quit()
            screen.blit(outroText1, ((SCREEN_WIDTH/3)-20, (SCREEN_HEIGHT/3) - 20))
            screen.blit(outrotext2, ((SCREEN_WIDTH/3)-50, SCREEN_HEIGHT/3))
            screen.blit(outrotext3, ((SCREEN_WIDTH/3)-10, (SCREEN_HEIGHT/3) + 20))
            screen.blit(outrotext4, ((SCREEN_WIDTH/3)-40, (SCREEN_HEIGHT/3) + 40))
            screen.blit(scoretext, ((SCREEN_WIDTH/4),(SCREEN_HEIGHT/4)))
            


            # print(time_end)
            # for i in range(2):
            #     if time_end == 1:
            #         Run = False
            #     time_end = 1
            # print(time_end)

            # pygame.time.delay(10000)
            
            # pygame.quit()
            # RUN = false
            # 

        if state == RUNNING:
            
            if paused_music != 0:
                pygame.mixer.music.unpause()
                paused_music = 0
                # backgrounMusc.play()

            # ENEMY_OCUURING_SPEED = 600
            # CLOUD_OCUURING_SPEED = 1000

            pressed_keys = pygame.key.get_pressed()
            player.update(pressed_keys)
            # pygame.event.pump()

            enemies.update()
            clouds.update()

            screen.fill(BLUE)
            # print(score)

            # screen.blit(pygame.font.Font.render(str(score),True,GREEN))

            scoretext = myfont.render(f"Score {score}", 1, (0, 0, 0))
            screen.blit(scoretext, (5, 10))
            for entity in all_sprites:
                screen.blit(entity.surf, entity.rect)

            if pygame.sprite.spritecollideany(player, enemies):
                state = OUT
                player.kill()


                
                
                # RUN = False
                # pass

        if state == PAUSE:
            ENEMY_OCUURING_SPEED = 0
            CLOUD_OCUURING_SPEED = 0

            pauseText = myfont.render("GAME PAUSED", 1, (0, 0, 0))
            screen.blit(pauseText, (350, 300))
            # backgrounMusc.stop()
            pygame.mixer.music.pause()
            paused_music = 1

        

        pygame.display.flip()

        clock.tick(45)
    
    return 0
run_game()
# while (reset_start == 2):
#     reset_start = 3
#     run_game()
    
pygame.quit()
