from pygame import *

window = display.set_mode((700,500))
display.set_caption("Лабиринт")
background = transform.scale(image.load("background.jpg"), (700, 500))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (100,100))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
   def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if key_pressed[K_DOWN] and self.rect.y < 395:
            self.rect.y += self.speed
        if key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed  

class Enemy(GameSprite):
    direction = "left"
    checklist = [transform.scale(image.load("sprite2.png"), (100,100)),transform.scale(image.load("sprite3.png"), (100,100))]
    i = 0
    def update(self):
        if self.rect.x > 630:
            self.direction = "right"
            
        if self.rect.x < 480:
            self.direction = "left"
            
        if self.direction == "right":
            self.rect.x -= self.speed
            self.image = self.checklist[self.i%2]
            self.i += 1
        else:
            self.rect.x += self.speed
            self.image = self.checklist[self.i%2]
            self.i += 1

class Wall(sprite.Sprite):
    def __init__(self, color_1,color_2, color_3, wall_x, wall_y, width_wall, height_wall):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = width_wall
        self.height = height_wall
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1,color_2,color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

font.init()
font = font.Font(None,70)
win = font.render("Ты победил!", True, (255,0,0))
lose = font.render("Ты проиграл!", True, (255,0,0))

pacman = Player("sprite1.png", 50, 400, 10)
enemy = Enemy("sprite2.png", 550, 250, 2)
Treasure = GameSprite("treasure.png", 600, 420, 0) 
wall_1 = Wall(120, 120, 120, 170, 130, 20, 370)
wall_2 = Wall(120, 120, 120, 520, 0, 20, 120)
wall_3 = Wall(120, 120, 120, 300, 110, 300, 20)
wall_4 = Wall(120, 120, 120, 360, 300, 20, 370)
wall_5 = Wall(120, 120, 120, 340, 300, 200, 20)

mixer.init()
mixer.music.load("Metallica_-_Master_of_Puppets.ogg")
mixer.music.play()

kick = mixer.Sound("draka-na-kulakah-s-krikami.ogg")

clock = time.Clock()
FPS = 60

finish = False
game = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        pacman.update()
        enemy.update()
        window.blit(background, (0, 0))
        wall_1.draw_wall()
        wall_2.draw_wall()
        wall_3.draw_wall()
        wall_4.draw_wall()
        wall_5.draw_wall()
        Treasure.reset()
        pacman.reset()
        enemy.reset()
        
        if sprite.collide_rect(pacman, Treasure):
            window.blit(win, (200,200))
            finish = True

        if sprite.collide_rect(pacman, enemy):
            window.blit(lose, (200,200))
            finish = True

        if sprite.collide_rect(pacman, wall_1) or sprite.collide_rect(pacman, wall_2) or sprite.collide_rect(pacman, wall_3) or sprite.collide_rect(pacman, wall_4) or sprite.collide_rect(pacman, wall_5):
            window.blit(lose, (200,200))
            finish = True
            

        

    

    display.update()
    clock.tick(FPS)
