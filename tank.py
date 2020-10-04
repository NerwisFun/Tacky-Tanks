import math
from pygame import transform, image, mask, sprite, Surface, time
import pygame

class Tank(sprite.Sprite):
    
    Speed = 7.5

    def __init__(self,x,y,image_name):
        from TT import SCREEN_WIDTH,SCREEN_HEIGHT,archive,Load_Image_From_Zip
        sprite.Sprite.__init__(self)
        

        self.initialX = x
        self.initialY = y

        self.initial_image = transform.scale(Load_Image_From_Zip(archive,image_name),[int(SCREEN_WIDTH / 35.025),int(SCREEN_HEIGHT / 11.636)])
        
        self.Image = self.initial_image
        self.width = self.initial_image.get_width()
        self.height = self.initial_image.get_height()
        self.mask = mask.from_surface(self.Image)
        self.rect = self.Image.get_rect(center = (x + self.width / 2,y + self.height / 2))
        self.center = self.rect.center
        self.Xmage = Surface([0, 0]).convert_alpha()

        self.dx = 0
        self.dy = Tank.Speed
    

        self.stuck = False
        self.health = 3
        self.bullet_sprites = sprite.Group()

        self.speed_boosted = False
        self.health_boosted = False

    def rotate(self,angle):

        rotated_surface = transform.rotozoom(self.initial_image,angle,1).convert_alpha()
        rotated_rect = rotated_surface.get_rect(center = self.rect.center)

        self.Image = rotated_surface
        self.rect = rotated_rect     
       
        self.dx = Tank.Speed * math.sin(math.radians(-angle))
        self.dy = Tank.Speed * math.cos(math.radians(-angle))

        self.mask = mask.from_surface(self.Image)

    def forward(self):
        from TT import SCREEN_WIDTH, SCREEN_HEIGHT
        if self.rect.left > 0 and self.rect.right < SCREEN_WIDTH and self.rect.top > 0 and self.rect.bottom < SCREEN_HEIGHT:
            if not self.speed_boosted:
                self.rect.x += self.dx
                self.rect.y -= self.dy
            else:
                self.rect.x += self.dx*2
                self.rect.y -= self.dy*2
            
    def backward(self):
        from TT import SCREEN_WIDTH, SCREEN_HEIGHT
        if self.rect.left >= 0 and self.rect.right <= SCREEN_WIDTH and self.rect.top >=0 and self.rect.bottom <= SCREEN_HEIGHT:
            if not self.speed_boosted:
                self.rect.x -= self.dx
                self.rect.y += self.dy
            else:
                self.rect.x -= self.dx*2
                self.rect.y += self.dy*2

   
    def shoot(self,sound):
        from TT import SCREEN_WIDTH,SCREEN_HEIGHT,archive,Load_Image_From_Zip
        if len(self.bullet_sprites.sprites()) < 3 :
            bullet = Bullet( Tank(   self.rect.center[0]- int(SCREEN_WIDTH/71.89),  self.rect.center[1]-int(SCREEN_HEIGHT/23),"pictures/tank.png"))
            pygame.mixer.Sound.play(sound)
            self.bullet_sprites.add(bullet)
        


    def respawn(self):
        self.rect.center = (self.initialX + self.width / 2, self.initialY + self.height / 2)

    def render(self):
        from TT import gameDisplay
        gameDisplay.blit(self.Image, self.rect)  
    
#---------------------------------------♣---------------------------------------♣---------------------------------------♣---------------------------------------#

class Bullet(sprite.Sprite):
    
    def __init__(self,own_tank):
        from TT import SCREEN_WIDTH,SCREEN_HEIGHT,archive,Load_Image_From_Zip

        sprite.Sprite.__init__(self)
        self.initial_image = transform.scale(Load_Image_From_Zip(archive,"pictures/bullet.png"),[int(SCREEN_WIDTH/195.14),int(SCREEN_HEIGHT/76)])
        self.image = self.initial_image 
        self.mask = mask.from_surface(self.image)
        self.rect = self.image.get_rect(center = own_tank.rect.center)

        self.situation = "stop"


    def update(self,own_tank,angle):

        from TT import SCREEN_WIDTH, SCREEN_HEIGHT
        
        if self.situation == "stop":
            rotated_surface = transform.rotozoom(self.initial_image ,angle,1).convert_alpha()
            rotated_rect = rotated_surface.get_rect(center = self.rect.center)

            self.image = rotated_surface
            self.rect = rotated_rect   

            self.dx = own_tank.dx * 2.5
            self.dy = own_tank.dy * 2.5
            self.mask = mask.from_surface(self.image)
        
        if self.rect.left > 0 and self.rect.right < SCREEN_WIDTH and self.rect.top > 0 and self.rect.bottom < SCREEN_HEIGHT:
                self.rect.x += self.dx
                self.rect.y -= self.dy
                self.situation = "fired"
        else:
            self.kill()
        