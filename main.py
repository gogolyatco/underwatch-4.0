from random import randint

from pygame import *

win_width = 700
win_height = 500
display.set_caption("Underwatch")
window = display.set_mode((win_width, win_height))

img_back = "hanamura.jpg"
img_hero = "tracer.jpg"
img_hero2 = "genji.jpg"
img_bullet = "bullet (1).png"
img_enemy = "genji.jng"
score = 0
lost = 0
max_lost = 3


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_X, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_X, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_width - 80:
            self.rect.y += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.centery, 15, 10, -15)
        bullets.add(bullet)

class Player2(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_width - 80:
            self.rect.y += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 10, 15)
        bullets2.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

ship = Player(img_hero, 455, win_height - 80, 80, 100, 10)
ship2 = Player2(img_hero2, 455, 80, 80, 100, 10)
bullets = sprite.Group()
bullets2 = sprite.Group()
mixer.init()
# mixer.music.load("fantastika-atmosfera-kosmosa-29355.mp3")
# mixer.music.play()
# fire_sound = mixer.Sound("fire.ogg")
background = transform.scale(image.load(img_back), (win_width, win_height))
finish = False
run = True
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -50
            lost += 1
# monsters = sprite.Group()
# for i in range(1, 6):
#     monster = Enemy(img_enemy, randint(50, win_height - 80), -60, 80, 50, randint(1, 5))
#     monsters.add(monster)
font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)
win = font1.render('VICTORY!', True, (255, 255, 255))
lose = font1.render('DEFEATE!', True, (255, 0, 0))
goal = 15
life = 3
max_fire = 5
rel_time = False
num_fire = 0
from time import time as timer

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < max_fire and rel_time == False:
                    num_fire += 1
                    # fire_sound.play()
                    ship.fire()
                if num_fire >= max_fire and rel_time == False:
                    last_time = timer()
                    rel_time = True
        elif e.type == MOUSEBUTTONDOWN:
            ship2.fire()
    if not finish:
        window.blit(background, (0, 0))
        ship.update()
        ship2.update()
        bullets.update()
        bullets2.update()
        # monsters.update()
        text = font2.render('Рахунок:' + str(score), True, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render('Пропущено:' + str(lost), True, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        ship.reset()
        ship2.reset()
        bullets.draw(window)
        bullets2.draw(window)
        # monsters.draw(window)
        # collides = sprite.groupcollide(monsters, bullets, True, True)
        # for c in collides:
        #     score= score+ 1
        #     monster = Enemy(img_enemy, randint(50, win_width - 80), -60, 80, 50, randint(1, 5))
        #     monsters.add(monster)
        if rel_time==True:
            now_time=timer()
            if now_time-last_time<3:
                reload=font2.render("Wait,reloed...",1,(150,0,0))
                window.blit(reload,(260,460))
            else:
                num_fire=0
                rel_time=False
        if life==3:
            life_color=(0,150,0)
        if life ==2:
            life_color=(150,150,0)
        if life==1:
            life_color=(150,0,0)
        text_life=font1.render(str(life),1,life_color)
        window.blit(text_life,(650,10))
        if sprite.spritecollide(ship,bullets2,False):
            sprite.spritecollide(ship,bullets2,True)
            # score+=1
            life=life - 1
        if life==0 or lost >=max_lost:
            finish = True
            window.blit(lose,(200,200))
        if score >=goal:
            finish=True
            window.blit(win,(200,200))
    else:
        time.delay(3000)
        score=0
        lost=0
        life=3
        num_fire=0
        finish=False
        for b in bullets:
            b.kill()
        # for m in monsters:
        #     m.kill()
        # for i in range(1,6):
        #     monster=Enemy(img_enemy,randint(50,win_width-80),-60,80,50,randint(1,5))
        #     monsters.add(monster)

    display.update()
    time.delay(50 )