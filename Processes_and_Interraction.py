import pygame, sys, Space_ships_Classes, random

def Game_Process(player, menu, FPS, total_frames_game, SCREENWIDTH, SCREENHEIGHT):

    # paused = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                Space_ships_Classes.Laser_Bullet.Blue_Laser = not Space_ships_Classes.Laser_Bullet.Blue_Laser
                gun_change = pygame.mixer.Sound("Audio/Gun_change.ogg")
                gun_change.play()

        # ------------ MENU PAGE CONTROLS ------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            Mx, My = pygame.mouse.get_pos()
            button_click = pygame.mixer.Sound("Audio/Blue_Laser.ogg")
            # Start button
            if Mx >= 404 and Mx <= 622 and My >= 407 and My <= 498 and menu.home_page \
                    or Mx >= 568 and Mx <= 873 and My >= 517 and My <= 593 and menu.instruction_page and menu.inst_page_no == 3:
                button_click.play()
                menu.menu_display = False
                menu.home_page = False
                menu.instruction_page = False
                total_frames_game = 0
            # Instructions button
            if Mx >= 317 and Mx <= 698 and My >= 516 and My <= 606 and menu.menu_display and menu.home_page:
                button_click.play()
                menu.home_page = False
                menu.instruction_page = True
            # Start_War Button
            if Mx >= 802 and Mx <= 991 and My >= 539 and My <= 619 and menu.menu_display and menu.instruction_page:
                button_click.play()
                if menu.inst_page_no <= 3:
                    menu.inst_page_no += 1

    keys = pygame.key.get_pressed()

#------------ VERTICAL MOVEMENT -------------
    if player.pos.y > 0 and player.pos.y + player.rect.height < SCREENHEIGHT:
        if keys[pygame.K_UP]:
            player.acc.y= -5
        elif keys[pygame.K_DOWN]:
            player.acc.y = 5
        else:
            player.acc.y = 0
    else:
        if player.pos.y < 0:
            player.pos.y = 1
        elif player.pos.y + player.rect.height > SCREENHEIGHT:
            player.pos.y = SCREENHEIGHT - player.rect.height - 1
        player.vel.y = 0
        player.acc.y = 0
# ----------- HORIZONTAL MOVEMENT-------------
    if player.pos.x > 0 and player.pos.x + player.rect.width < SCREENWIDTH:
        if keys[pygame.K_RIGHT]:
            player.acc.x = 5
        elif keys[pygame.K_LEFT]:
            player.acc.x = -5
        else:
            player.acc.x = 0
    else:
        if player.pos.x < 0:
            player.pos.x = 1
        elif player.pos.x + player.rect.width > SCREENWIDTH:
            player.pos.x = SCREENWIDTH - player.rect.width - 1
        player.vel.x = 0
        player.acc.x = 0

#----------- LASER BULLETS ------------------
    if keys[pygame.K_SPACE]:

        def play_bullet_sound():
            if Space_ships_Classes.Laser_Bullet.Blue_Laser:
                Laser = pygame.mixer.Sound("Audio/Blue_Laser.ogg")
            else:
                Laser = pygame.mixer.Sound("Audio/Red_Laser.ogg")
            Laser.play()

        def activate_bullet():
            bullet.velx = 30


        if Space_ships_Classes.Laser_Bullet.Blue_Laser:
            bullet = Space_ships_Classes.Laser_Bullet(player.rect.x + 5,
                                                      player.rect.y + 25,
                                                      True, "images/Blue_Laser.png")
            activate_bullet()
            play_bullet_sound()

        else:
            bullet = Space_ships_Classes.Laser_Bullet(player.rect.x + 5,
                                                      player.rect.y + 25,
                                                      True, "images/Red_Laser.png")
            activate_bullet()
            play_bullet_sound()

    if not menu.menu_display:
        spawn(FPS, total_frames_game, player, SCREENWIDTH, SCREENHEIGHT)
        collision(player)


def spawn(FPS, total_frames_game, player, SCREENWIDTH, SCREENHEIGHT):
    one_third_second_gap = FPS / 3

    if total_frames_game % one_third_second_gap == 0 and player.score <= player.win_score - player.m_ship_appear:
        y = random.randint(0, SCREENHEIGHT - 151)
        x = 1000

        Space_ships_Classes.Enemy(x, y, "images/enemy.png")

def mother_ship_spawn(SCREENWIDTH, SCREENHEIGHT):
    y = SCREENHEIGHT / 6
    x = SCREENWIDTH

    Space_ships_Classes.Mother_ship(x, y, "images/mother_ship.png")


def collision(player):
    for enemy in Space_ships_Classes.Enemy.List:

        bullets = pygame.sprite.spritecollide(enemy, Space_ships_Classes.Laser_Bullet.List, True)

        for collided_bullet in bullets:
            if not Space_ships_Classes.Laser_Bullet.Blue_Laser:
                enemy.health -= enemy.half_health
                player.score += 10
            elif Space_ships_Classes.Laser_Bullet.Blue_Laser:
                enemy.health -= enemy.quarter_health
                player.score += 5
            collided_bullet.destroy()

    try:
        for m_ship in Space_ships_Classes.Mother_ship.List:

            bullets = pygame.sprite.spritecollide(m_ship, Space_ships_Classes.Laser_Bullet.List, True)

            for collided_bullet in bullets:
                if not Space_ships_Classes.Laser_Bullet.Blue_Laser:
                    m_ship.mother_health -= m_ship.mother_dmg
                    player.score += 10
                elif Space_ships_Classes.Laser_Bullet.Blue_Laser:
                    m_ship.mother_health -= m_ship.mother_dmg
                    player.score += 5
                collided_bullet.destroy()

            if m_ship.mother_health <= 0:
                player.score = player.win_score
                
    except Exception:
        pass


    player_enemy_collide = pygame.sprite.spritecollide(player, Space_ships_Classes.Enemy.List, False)
    for collide in player_enemy_collide:
        player.health -= 5

    player_mother_ship_collide = pygame.sprite.spritecollide(player, Space_ships_Classes.Mother_ship.List, False)
    for collide in player_mother_ship_collide:
        player.health = 0


def text_to_screen(screen, text, x, y, size=15, color=(255, 255, 255), font_type='monospace'):

    try:
        text = str(text)
        font = pygame.font.SysFont(font_type, size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))
    except Exception:
        print('Font Error')


def init_all(menu, player, Enemy, Laser_Bullet, Mother_ship, SCREENHEIGHT):
    menu.menu_display = True
    menu.home_page = True
    menu.instruction_page = False
    player.__init__(0, SCREENHEIGHT/2, "images/player.png", SCREENHEIGHT)
    Laser_Bullet.Blue_Laser = True
    for enemy in Enemy.List:
        Enemy.List.remove(enemy)
        enemy.kill()
    for bullet in Laser_Bullet.List:
        Laser_Bullet.List.remove(bullet)
        bullet.kill()
    for m_ship in Mother_ship.List:
        Mother_ship.List.remove(m_ship)
        m_ship.kill()
