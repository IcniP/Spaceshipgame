import pygame
from sys import exit 
from random import randint, choice

class Player(pygame.sprite.Sprite):
        def __init__(self, groups, laser_group):
            super().__init__(groups)
            self.laser_group = laser_group
            Player_ship1 = pygame.image.load('Spaceship/space.png').convert_alpha()
            Player_ship2 = pygame.image.load('Spaceship/space2.png').convert_alpha()
            Player_ship1 = pygame.transform.rotozoom(Player_ship1,0,0.2)
            Player_ship2 = pygame.transform.rotozoom(Player_ship2,0,0.2)
            self.player_ship = [Player_ship1,Player_ship2]
            self.player_index = 0
            
            self.image = self.player_ship[self.player_index]
            self.rect = self.image.get_frect(center =(WINDOW_WIDTH/2,640))

            self.can_shoot = True
            self.Laser_shoot_time = 0
            self.cooldown = 700

            self.shoot_bg = pygame.mixer.Sound('Audio/shoot.mp3')
            self.shoot_bg.set_volume(0.2)

        def Laser_timer(self):
             if not self.can_shoot:
                  current_time = pygame.time.get_ticks()
                  if current_time - self.Laser_shoot_time >= self.cooldown:
                       self.can_shoot = True

        def Player_input(self):
             keys = pygame.key.get_pressed()
             if keys[pygame.K_d]:
                  self.rect.x += 10
             if keys[pygame.K_a]:
                  self.rect.x -= 10
             if keys[pygame.K_w]:
                  self.rect.y -= 10
             if keys[pygame.K_s]:
                  self.rect.y += 10
             shoot = pygame.key.get_just_pressed()
             if shoot[pygame.K_SPACE] and self.can_shoot:
                  self.shoot_bg.play()
                  self.laser_group.add(Laser(self.rect.midtop))
                  self.can_shoot = False
                  self.Laser_shoot_time = pygame.time.get_ticks()
                  
        def Player_bound(self):
             if self.rect.left <= 0 :
                self.rect.left = 0
             if self.rect.right >= 1280 :
                self.rect.right = 1280
             if self.rect.top <= 0 :
                self.rect.top = 0
             if self.rect.bottom >= 720 :
                self.rect.bottom = 720

        def animation(self):
             self.player_index += 0.1
             if self.player_index >= len(self.player_ship):self.player_index = 0
             self.image = self.player_ship[int(self.player_index)]

       
        def update(self, dt):
             self.Player_input()
             self.animation()
             self.Player_bound()
             self.Laser_timer()

            
class Laser(pygame.sprite.Sprite):
     def __init__(self,pos):
        super().__init__()
        Laser = pygame.image.load('Spaceship/Laser.png').convert_alpha()
        Laser = pygame.transform.rotozoom(Laser,0,0.2).convert_alpha()
        self.image = Laser
        self.rect = self.image.get_frect(midbottom = pos )
        self.speed = -15

     def update(self):
          self.rect.y += self.speed
          if self.rect.bottom <= 0 :
               self.kill()
             

class Meteor(pygame.sprite.Sprite):
     def __init__(self, groups):
          super().__init__(groups)
          Meteor = pygame.image.load('Spaceship/Meteor.png').convert_alpha()
          Meteor = pygame.transform.rotozoom(Meteor,0,0.25).convert_alpha()
          self.image = Meteor
          self.rect = self.image.get_frect (midbottom = (randint(30,1250),-50))

     def destroy(self):
          if self.rect.y >= 740:
               self.kill()

     def update(self):
          self.rect.y += 3
          self.destroy()
          
def collision():
     if pygame.sprite.spritecollide(player.sprite,Meteors,False):
          Meteors.empty()
          return False
     else :return True


pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('StarShip')
clock = pygame.time.Clock()
game_active = False
score = 0
score_font = pygame.font.Font('Minecraft.ttf',30)

font = pygame.font.Font('Minecraft.ttf',50)
Bg = pygame.image.load('Spaceship/atmos.png').convert()
bg_music = pygame.mixer.Sound('Audio/bgm.mp3')
bg_music.play(loops=-1)
bg_music.set_volume(0.035)
explo_bg = pygame.mixer.Sound('Audio/explo.mp3')
explo_bg.set_volume(0.1)

#intro
Intro = pygame.image.load('Spaceship/space.png').convert_alpha()
Intro = pygame.transform.rotozoom(Intro,90,0.5)
Intro_rect = Intro.get_frect()
Intro_rect.center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2)

player = pygame.sprite.GroupSingle()
lasers = pygame.sprite.Group()
Meteors = pygame.sprite.Group()

player.add(Player(player, lasers))

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,800)

while True:
    dt= clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN and game_active == False :
            if event.key == pygame.K_SPACE:
                game_active = True
                score = 0
        if game_active:
            if event.type == obstacle_timer:
                Meteors.add(Meteor(Meteors))
         

    if game_active:
        screen.blit(Bg,(0,0))
        Score_text = score_font.render(str(score),False,'White').convert()
        Score_rect = Score_text.get_rect()
        Score_rect.topleft = (50,50)
        screen.blit(Score_text,Score_rect)
        player.update(dt)
        Meteors.update()
        lasers.update()

        player.draw(screen)
        lasers.draw(screen)
        Meteors.draw(screen)

        destroy = pygame.sprite.groupcollide(lasers,Meteors,True, True)
        if destroy :
             explo_bg.play()
             score = score +1
        game_active = collision()

    else:
        screen.blit(Bg,(0,0))
        screen.blit(Intro,Intro_rect)
        Score_text = score_font.render(f"HighScore: {score}",False,'White').convert()
        Score_rect = Score_text.get_rect()
        Score_rect.topleft = (50,50)
        Title = font.render('SpaceShooter',False,'White').convert()
        Start = font.render('Press Space To Play',False,'White').convert()
        Start_rect = Start.get_frect (center = (WINDOW_WIDTH/2,580))
        Title_rect = Title.get_frect (center = (WINDOW_WIDTH/2,100))
        screen.blit(Title,Title_rect)
        screen.blit(Start,Start_rect)
        if score >= 1 :
            screen.blit(Score_text,Score_rect)
        


    pygame.display.update()
    clock.tick(60)