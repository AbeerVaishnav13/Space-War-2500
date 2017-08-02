import pygame
from random import randint

Vector = pygame.math.Vector2

class SpaceShip(pygame.sprite.Sprite):

    all_sprites = pygame.sprite.Group()

    def __init__(self, x, y, image_string):

        pygame.sprite.Sprite.__init__(self)
        SpaceShip.all_sprites.add(self)

        self.image = pygame.image.load(image_string)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def destroy(self, class_name):
        class_name.List.remove(self)
        SpaceShip.all_sprites.remove(self)
        del self


class Player(SpaceShip):
    List = pygame.sprite.Group()
    active = True

    def __init__(self, x, y, image_string, SCREENHEIGHT):
        SpaceShip.__init__(self, x, y, image_string)
        Player.List.add(self)
        self.pos = Vector(10, SCREENHEIGHT // 2)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)
        self.friction = -0.2
        self.health = 1000
        self.score, self.win_score = 0, randint(3, 5) * 1000
        self.m_ship_appear = 1000

    def motion(self, SCREENWIDTH, SCREENHEIGHT):

        self.acc += self.vel * self.friction
        self.vel += self.acc
        self.pos += self.vel + (self.acc / 2)

        if self.pos.x < 0:
            self.vel.x = 0
            self.acc.x = 0
        elif self.pos.x + self.rect.width > SCREENWIDTH:
            self.vel.x = 0
            self.acc.x = 0

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y


class Enemy(SpaceShip):
    List = pygame.sprite.Group()

    def __init__(self, x, y, image_string):
        SpaceShip.__init__(self, x, y, image_string)
        Enemy.List.add(self)
        self.health = 100
        self.half_health = self.health / 2.0
        self.quarter_health = self.health / 4.0
        self.velx = randint(5, 10)

    @staticmethod
    def update_all(SCREENWIDTH, SCREENHEIGHT):
        for enemy in Enemy.List:
            if enemy.health <= 0 or enemy.rect.x + enemy.rect.width < 0:
                enemy.destroy(Enemy)

            else:
                enemy.fly()

    def fly(self):
        self.rect.x -= self.velx


class Mother_ship(SpaceShip):
    List = pygame.sprite.Group()

    def __init__(self, x, y, image_string):#, SCREENWIDTH, SCREENHEIGHT):
        SpaceShip.__init__(self, x, y, image_string)
        Mother_ship.List.add(self)
        self.mother_health = 1000
        self.mother_dmg = 12
        self.mother_velx = 3
        # self.mother_ship = False
        # self.amplitude, self.period = SCREENHEIGHT / 2
        
    def mother_fly(self):
        self.rect.x -= self.mother_velx

    @staticmethod
    def update_all(SCREENWIDTH, SCREENHEIGHT):
        for m_ship in Mother_ship.List:
            if m_ship.mother_health <= 0 or m_ship.rect.x + m_ship.rect.width < 0:
                m_ship.destroy(Mother_ship)

            else:
                m_ship.mother_fly()

class Laser_Bullet(pygame.sprite.Sprite):
    List = pygame.sprite.Group()
    normal_list = []
    Blue_Laser = True

    def __init__(self, x, y, fire_var, image_string):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_string)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.fire_var = fire_var
        self.rect.width

        try:
            last_element = Laser_Bullet.normal_list[-1]
            difference = abs(self.rect.x - last_element.rect.x)

            if difference < self.rect.width + 10:
                return

        except Exception:
            pass

        Laser_Bullet.normal_list.append(self)
        Laser_Bullet.List.add(self)
        self.velx = None

    def destroy(self):
        Laser_Bullet.List.remove(self)
        Laser_Bullet.normal_list.remove(self)
        del self

    @staticmethod
    def update_all(SCREENWIDTH):
        for bullet in Laser_Bullet.List:
            bullet.rect.x += bullet.velx
            if bullet.rect.x > SCREENWIDTH:
                bullet.destroy()


class Menu():

    def __init__(self):
        self.menu_display = True
        self.home_page = True
        self.instruction_page = False
        self.inst_page_no = 1
