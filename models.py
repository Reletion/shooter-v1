from pygame import *
from random import randint
from time import time as t

bullet_img = image.load("bullet.png")
player_img = image.load("rocket.png")
asteroid_img = image.load("asteroid.png")
ufo_img = image.load("ufo.png")
WINDOW_SIZE = (700,500)
SPRITE_SIZE = (75,75)
WHITE = (255,255,255)

window = display.set_mode(WINDOW_SIZE)
display.set_caption("Шутер")

background = transform.scale(image.load("galaxy.jpg"),WINDOW_SIZE)

bullets = sprite.Group()

timer = t()

DOWN = 1
LEFT = 2

font.init()
font1 = font.Font(None,30)
font2 = font.SysFont('Times New Roman',70,True)

win = font1.render("WIN!!!",1,WHITE)
lost = font1.render("LOST!!!",1, WHITE)

class Lichilnik:
    def __init__(self):
        self.lost_enemy = 0
        self.kill_enemy = 0
    def show(self):
        self.lost_enemy_label = font1.render("Пропущено: "+str(self.lost_enemy),1,WHITE)
        self.kill_enemy_label = font1.render("Вбито: "+str(self.kill_enemy),1, WHITE)
        window.blit(self.lost_enemy_label,(0,0))
        window.blit(self.kill_enemy_label,(0,35))

counter = Lichilnik()

class GameSprite(sprite.Sprite):
    def __init__(self,image_name,x_pos,y_pos,speed,sprite_size = SPRITE_SIZE):
        super().__init__()
        self.spritesize = sprite_size
        self.image = transform.scale(image_name,self.spritesize)
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

class Player(GameSprite):
    def move(self):
        keys = key.get_pressed()
        if keys[K_a]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
        elif keys[K_d]:
            if self.rect.x < WINDOW_SIZE[0] - SPRITE_SIZE[0]:
                self.rect.x += self.speed
        elif keys[K_LEFT]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
        elif keys[K_RIGHT]:
            if self.rect.x < WINDOW_SIZE[0] - SPRITE_SIZE[0]:
                self.rect.x += self.speed
        self.reset()
    def fire(self):
        keys = key.get_pressed()
        global timer
        if t() - timer > 0.5:
            charge_label = font1.render("Заряджено",1,WHITE)
            if keys[K_SPACE]:
                fire = mixer.Sound('fire.ogg')
                fire.set_volume(0.5)
                fire.play()
                bullets.add(Bullet((bullet_img),self.rect.x+self.spritesize[0]/2-10,self.rect.y+self.spritesize[1]/2,10,(30,30)))

                timer = t()
        else:
            charge_label = font1.render("Перезарядка",1,WHITE)

class Enemy(GameSprite):
    def __init__(self, image_name, x_pos, y_pos, speed,direction ,sprite_size=SPRITE_SIZE):
        super().__init__(image_name, x_pos, y_pos, speed, sprite_size)
        self.direction = direction
    def change_coor(self):
        if self.direction == DOWN:
            self.rect.y=-self.spritesize[1]
            self.rect.x = randint(0,WINDOW_SIZE[0]-self.spritesize[0])
            self.speed = randint(1,2)
        elif self.direction == LEFT:
            self.rect.x=randint(0-SPRITE_SIZE[0]*4,0-SPRITE_SIZE[0])
            self.rect.y = randint(0,WINDOW_SIZE[1]/2)
    def update(self):
        if self.direction == DOWN:
            if self.rect.y < WINDOW_SIZE[1]:
                self.rect.y +=self.speed
            else:
                self.change_coor()
                counter.lost_enemy += 1
        elif self.direction == LEFT:
            if self.rect.x < WINDOW_SIZE[0]:
                self.rect.x +=self.speed
            else:
                self.change_coor()
                counter.lost_enemy += 1