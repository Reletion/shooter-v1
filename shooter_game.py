#Створи власний Шутер!
from models import *
from random import random
FPS = 60
font.init()

mixer.init()
clock = time.Clock()
mixer.music.load("space.ogg")
mixer.music.set_volume(0.1)
mixer.music.play()
enemies = sprite.Group()
asteroids = sprite.Group()

for i in range(5):
    enemies.add(Enemy(ufo_img,randint(0,WINDOW_SIZE[0]-SPRITE_SIZE[0]),-SPRITE_SIZE[1],randint(1,3),1,(75,50)))
for i in range(5):
    asteroids.add(Enemy(asteroid_img,randint(0-SPRITE_SIZE[0]*4,0-SPRITE_SIZE[0]),randint(0,(WINDOW_SIZE[1]/2)),1,2,(75,50)))

player = Player(player_img,WINDOW_SIZE[0]/2-SPRITE_SIZE[0]/2,WINDOW_SIZE[1]-SPRITE_SIZE[1]-WINDOW_SIZE[1]/100*10,10)

finish = False
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if not finish:
        
        window.blit(background,(0,0))

        bullets.update()
        bullets.draw(window)
        player.move()
        player.fire()
        enemies.draw(window)
        enemies.update()
        asteroids.draw(window)
        asteroids.update()

        for bullet in bullets:
            for enemy in enemies:
                if sprite.collide_rect(enemy,bullet):
                    enemy.change_coor()
                    bullet.kill()
                    counter.kill_enemy += 1
            for asteroid in asteroids:
                if sprite.collide_rect(asteroid,bullet):
                    bullet.kill()
        if counter.lost_enemy >= 10 or sprite.spritecollide(player,enemies,False):
            window.blit(lost,(WINDOW_SIZE[0]/2,WINDOW_SIZE[1]/2))
            finish = True
        if counter.kill_enemy >= 10:
            window.blit(background,(0,0))
            window.blit(win,(WINDOW_SIZE[0]/2-25,WINDOW_SIZE[1]/2))
            finish = True
        counter.show()
        display.update()
        clock.tick(FPS)