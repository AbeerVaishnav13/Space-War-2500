import pygame, sys
from Space_ships_Classes import *
from Processes_and_Interraction import *
from time import sleep

pygame.init()
pygame.font.init()
pygame.mixer.init()

Theme_sound = pygame.mixer.Sound("Audio/Star Wars_edit.ogg")
Theme_sound.play(-1)

SCREENWIDTH, SCREENHEIGHT = 1000, 625
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32)
clock = pygame.time.Clock()
FPS = 24
total_frames_game = 0

menu = Menu()
background = pygame.image.load("images/Background.png")
home_img = pygame.image.load("images/Home_Page.png")
inst_img_1 = pygame.image.load("images/Inst_Page_1.png")
inst_img_2 = pygame.image.load("images/Inst_Page_2.png")
inst_img_3 = pygame.image.load("images/Inst_Page_3.png")
player = Player(0, SCREENHEIGHT/2, "images/player.png", SCREENHEIGHT)
mother_ship = False

while True:

    Game_Process(player, menu, FPS, total_frames_game, SCREENWIDTH, SCREENHEIGHT)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused

    if menu.menu_display:
        if menu.home_page:
            screen.blit(home_img, (0, 0))
        if menu.instruction_page:
            if menu.inst_page_no == 1:
                screen.blit(inst_img_1, (0, 0))
            elif menu.inst_page_no == 2:
                screen.blit(inst_img_2, (0, 0))
            elif menu.inst_page_no == 3:
                screen.blit(inst_img_3, (0, 0))


    else:
        player.motion(SCREENWIDTH, SCREENHEIGHT)
        Enemy.update_all(SCREENWIDTH, SCREENHEIGHT)
        Laser_Bullet.update_all(SCREENWIDTH)
        if mother_ship:
            Mother_ship.update_all(SCREENWIDTH, SCREENHEIGHT)

        screen.blit(background, (0, 0))

        if player.health >= -20:
            text_to_screen(screen, 'Health:{0}'.format(player.health), 0, 0, size=30, color=[75, 255, 30])
            text_to_screen(screen, 'Score:{0}'.format(player.score), 0, 30, size=30, color=[240, 75, 30])
            text_to_screen(screen, 'Win Score:{0}'.format(player.win_score), 0, 60, size=30, color=[240, 75, 30])

        if player.score >= player.win_score - player.m_ship_appear and player.score <= player.win_score and not mother_ship:
            mother_ship_spawn(SCREENWIDTH, SCREENHEIGHT)
            mother_ship = True

        SpaceShip.all_sprites.draw(screen)
        Laser_Bullet.List.draw(screen)

        if player.score >= player.win_score:
            mother_ship = False
            sleep(1)
            screen.fill([0, 0, 0])
            text_to_screen(screen, 'YOU WIN!!', 150, 100, size=100, color=[0, 255, 0])
            text_to_screen(screen, "YOU SAVED PLANET EARTH", 150, 300, size=50, color=[0, 255, 0])
            text_to_screen(screen, "FROM ALIENS!!", 250, 350, size=50, color=[0, 255, 0])
            text_to_screen(screen, 'YOUR SCORE:{0}'.format(player.score), 50, 500, size=100, color=[0, 255, 0])
            pygame.display.update()
            sleep(4)
            init_all(menu, player, Enemy, Laser_Bullet, Mother_ship, SCREENHEIGHT)

        if player.health <= 0:
            mother_ship = False
            sleep(1)
            screen.fill([0, 0, 0])
            text_to_screen(screen, 'GAME OVER!!', 150, 100, size=100, color=[240, 75, 30])
            text_to_screen(screen, "YOU LOSE!!", 150, 200, size=100, color=[240, 75, 30])
            text_to_screen(screen, "ALIENS CONQUERED THE EARTH!!", 60, 400, size=50, color=[240, 75, 30])
            text_to_screen(screen, 'YOUR SCORE:{0}'.format(player.score), 100, 500, size=100, color=[240, 75, 30])
            pygame.display.update()
            sleep(4)
            init_all(menu, player, Enemy, Laser_Bullet, Mother_ship, SCREENHEIGHT)


    total_frames_game += 1
    pygame.display.flip()
    clock.tick(FPS)