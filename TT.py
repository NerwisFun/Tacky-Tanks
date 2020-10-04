import pygame
import random
from tank import *
import zipfile
import io


archive = zipfile.ZipFile('data.gg', 'r')

def Load_Image_From_Zip(archive,image_name):
    return pygame.image.load(io.BytesIO(archive.read(image_name)))

def Load_Sound_From_Zip(sound_name):
    global archive
    return pygame.mixer.Sound(io.BytesIO(archive.read(sound_name)))

def Load_Font_From_Zip(font_name,size):
    global archive
    return pygame.font.Font(io.BytesIO(archive.read(font_name)), size)

pygame.init()
clock = pygame.time.Clock()
random.seed
#------------------------ CLASS OF BOOSTER BOX --------------------#
class GenerateSkill(pygame.sprite.Sprite): 
    def __init__(self,image_name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Load_Image_From_Zip(archive,image_name).convert_alpha() , [int(SCREEN_WIDTH / 45.53), int(SCREEN_HEIGHT / 25.6)])
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.exists = False

#-------------------------- CLASS OF MAZE -------------------------#
class Maze(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        placer = random.randint(1,12)
        maze_name = f'maps/maze{placer}.png'        
        
        self.image = Load_Image_From_Zip(archive,maze_name).convert_alpha()
        self.image = pygame.transform.scale(self.image,[SCREEN_WIDTH,SCREEN_HEIGHT])
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH / 2,SCREEN_HEIGHT / 2))
        self.mask = pygame.mask.from_surface(self.image)

    def render(self):
        gameDisplay.blit(self.image,self.rect)

pause = False

#--------------------------- COLORS -------------------------------#
white = (255,255,255)
black = (0,0,0)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
night_blue = (0,51,102)
armyellow = (153,153,0)

#------------------------>  GAME SOUNDS <--------------------------#
fire_sound_1 = Load_Sound_From_Zip('sounds/fire1.wav')
fire_sound_1.set_volume(0.2)
fire_sound_2 = Load_Sound_From_Zip('sounds/fire2.wav')
fire_sound_2.set_volume(0.2)
up_buttons = Load_Sound_From_Zip('sounds/credituto.wav')
taptap = Load_Sound_From_Zip('sounds/tap.wav')
pygame.mixer.music.load(io.BytesIO(archive.read('sounds/intro.mp3')))
wall_hit = Load_Sound_From_Zip("sounds/wall_hit.wav")
rotate_sound = Load_Sound_From_Zip("sounds/rotate.wav")
rotate_sound.set_volume(0.1)
forward_sound = Load_Sound_From_Zip("sounds/forward.wav")
forward_sound.set_volume(0.2)
stop_sound = Load_Sound_From_Zip("sounds/stop.wav")
stop_sound.set_volume(0.2)
explosion_sound = Load_Sound_From_Zip("sounds/explosion.wav")


hit_sounds = [Load_Sound_From_Zip('sounds/hit1.wav'),Load_Sound_From_Zip('sounds/hit2.wav'),Load_Sound_From_Zip('sounds/hit3.wav'),Load_Sound_From_Zip('sounds/hit4.wav')]
for i in range(0,4):
    hit_sounds[i].set_volume(0.5)

#------------------------- MONITOR SETTINGS -----------------------#
def Get_Current_Resolution():
    infoObject = pygame.display.Info()
    return infoObject.current_w, infoObject.current_h

SCREEN_WIDTH, SCREEN_HEIGHT = Get_Current_Resolution()
gameDisplay = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT) ,pygame.FULLSCREEN)
pygame.display.set_caption('Sticky TankS') # GAME TITLE 

#--------------------------- TANKS --------------------------------#
tank1 = Tank(52,88,"pictures/tank.png")
tank2 = Tank(SCREEN_WIDTH - 2*tank1.width,SCREEN_HEIGHT - 2*tank1.height, "pictures/tank2.png")

#------------------------ ROTATION ANGLES -------------------------#

maze = Maze()

angle1 = 0
angle2 = 0

#--------------------------- FONTS --------------------------------#
font = pygame.font.SysFont(None, int(SCREEN_WIDTH/57))
fontLarge = pygame.font.SysFont(None,int(SCREEN_WIDTH*2/60))

#---------------------------- BACKGROUND -----------------------------#

background = pygame.transform.scale(Load_Image_From_Zip(archive,f"floors/background{random.randint(1,3)}.png"),[SCREEN_WIDTH,SCREEN_HEIGHT])

def drawHP(main_sprite,x,y):
    img = font.render('HP: '+str(main_sprite.health), True, (0,0,0))
    gameDisplay.blit(img, (x, y))

def drawStuck(x,y):
    gameDisplay.blit(pygame.transform.scale(Load_Image_From_Zip(archive,"pictures/stuck.png"),[int(SCREEN_WIDTH / 18),int(SCREEN_HEIGHT / 27.25)]), (x,y))

def text_objects(text, font):
    textsurface = font.render(text, True, black)
    return textsurface

def FPS(x,y):
    font = Load_Font_From_Zip('fonts/Nois.ttf', 12)
    fps = font.render(str(int(clock.get_fps())), True, pygame.Color('green'))
    gameDisplay.blit(fps, (x, y))

def ClearBullets():
    tank1.bullet_sprites.empty()
    tank2.bullet_sprites.empty()

def ClearCollidables():
    collidables_for_tank1.empty()
    collidables_for_tank2.empty()

#THESE ARE COLLIDABLE OBJECTS FOR TANK1 ALSO BULLET1
collidables_for_tank1 = pygame.sprite.Group()

#THESE ARE COLLIDABLE OBJECTS FOR TANK2 ALSO BULLET2    
collidables_for_tank2 = pygame.sprite.Group()

#---------------------- Add random maze to both tanks for plausible collisions (also for bullets) ---------------#
collidables_for_tank2.add(tank1,maze)
collidables_for_tank1.add(tank2,maze)

# SKILL SPRITES' GROUP----------------------------------------------------------------
skill_sprites = pygame.sprite.Group()

# INITIALIZE SKILL SPRITES------------------------------------------------------------
speed = GenerateSkill("pictures/speed.png")
health = GenerateSkill("pictures/health.png")

#--------------------------------------------   GAME FUNCTIONS    ---------------------------------------------------#
def CollisionSingle(main_sprite, sprite_list):
    if pygame.sprite.spritecollideany(main_sprite , sprite_list):
        if pygame.sprite.spritecollide(main_sprite , sprite_list , False,pygame.sprite.collide_mask):
            return True
    return False

def GetCollidedSkill(main_sprite,skills_sprite):
    return pygame.sprite.spritecollideany(main_sprite,skills_sprite)  


def Destroy(tank1,tank2,maze):
        hitank2 = pygame.sprite.groupcollide(collidables_for_tank1, tank1.bullet_sprites, False, True, pygame.sprite.collide_mask)
        hitank1 = pygame.sprite.groupcollide(collidables_for_tank2, tank2.bullet_sprites, False, True, pygame.sprite.collide_mask)
        for k in hitank2:
            if k == tank2:
                tank2.health -= 1 
                pygame.draw.circle(gameDisplay, red, (int(SCREEN_WIDTH/1.04), int(SCREEN_HEIGHT/ 52.5)), int(SCREEN_WIDTH/273.2), 0)
                if tank2.health>1:
                    pygame.mixer.Sound.play(hit_sounds[random.randint(0,3)])
            if k == maze:
                pygame.mixer.Sound.play(wall_hit)

        for m in hitank1:
            if m == tank1:
                tank1.health -= 1
                pygame.draw.circle(gameDisplay, red, (int(SCREEN_WIDTH/ 25), int(SCREEN_HEIGHT/ 52.5)), int(SCREEN_WIDTH/273.2), 0)
                if tank2.health>1:
                    pygame.mixer.Sound.play(hit_sounds[random.randint(0,3)])
            if m == maze:
                pygame.mixer.Sound.play(wall_hit)

#---------------------------------------- COVER FUNCTIONS ----------------------------------------------#
def Button(msg,x,y,ac,ic,action=None,func=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    smallText = Load_Font_From_Zip('fonts/Nois.ttf', int(SCREEN_HEIGHT / 38.4))
    a = pygame.transform.scale(Load_Image_From_Zip(archive,'pictures/flag.png'),[int(SCREEN_WIDTH/21),int(SCREEN_HEIGHT/14.6)])
    e = y
    if x+int(SCREEN_WIDTH/16.4) > mouse[0] > x and y+int(SCREEN_HEIGHT/9.6) > mouse[1] > y:
        pygame.draw.circle(gameDisplay, ac, (x+int(SCREEN_WIDTH/32) , y+int(SCREEN_HEIGHT/18)),int(SCREEN_WIDTH/34), int(SCREEN_WIDTH/34))
        e -= 5
        if click[0] and action == 'play':
            pygame.mixer.Sound.play(taptap)
            GameLoop()

        elif click[0] and action == 'quit':
            pygame.quit()
            quit()
    else:
        pygame.draw.circle(gameDisplay, ic, (x+int(SCREEN_WIDTH/32) , y+int(SCREEN_HEIGHT/18)),int(SCREEN_WIDTH/34), int(SCREEN_WIDTH/34))

    textSurf = text_objects(msg, smallText)
    gameDisplay.blit(textSurf, (x+int(SCREEN_WIDTH/75),y+int(SCREEN_HEIGHT/24)))
    if func == game_intro:
        gameDisplay.blit(a, (x-int(SCREEN_WIDTH/34),e))
    elif func == GameOver:
        pass

def Tuto_Credit(msg,x,y,ac,action=None):
    pygame.mixer.Sound.stop(taptap)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    smallText = Load_Font_From_Zip('fonts/Nois.ttf', int(SCREEN_HEIGHT / 58.3)) 
    if x+60 >= mouse[0] > x and y+12.8 > mouse[1] >= y:    
        pygame.draw.line(gameDisplay, ac, (x, y+12.8), (x+60, y+12.8), 2)
        if click[0] and action == 'tutorial':
            pygame.mixer.Sound.play(up_buttons)
            credits("pictures/tutorial.png")

        elif click[0] and action == 'credits':
            pygame.mixer.Sound.play(up_buttons)
            credits("pictures/credits.png")

        elif click[0] and action == 'menu':
            pygame.mixer.music.unpause()
            game_intro()

    textSurf = text_objects(msg, smallText)
    gameDisplay.blit(textSurf, (x, y))

def credits(image_name):
    pygame.mixer.music.pause()
    Us = pygame.transform.smoothscale(Load_Image_From_Zip(archive,image_name),[SCREEN_WIDTH, SCREEN_HEIGHT])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.unpause()
                        tank1.respawn()
                        tank2.respawn()
                        game_intro()
        gameDisplay.blit(Us, (0, 0))
        Tuto_Credit('GO BACK', 0, 0,night_blue , 'menu')
        pygame.display.update()

def GameOver(player):
    global maze, collidables_for_tank1, collidables_for_tank2, background

    #-------------------Empty bullets sprite group /// empty collidables sprite group /// empty skills sprite group -------------------------------#
    ClearBullets()
    ClearCollidables()
    skill_sprites.empty()
    
    #----------------------Generate Random Maze Each Time-----------------------#
    maze = Maze()

    #---------------------- Add random maze to both tanks for plausible collisions (also for bullets) ---------------#
    collidables_for_tank2.add(tank1,maze)
    collidables_for_tank1.add(tank2,maze)

    #----------------- Generate random floor texture each time ----------------------------------------#
    background = pygame.transform.scale(Load_Image_From_Zip(archive,f"floors/background{random.randint(1,3)}.png"),[SCREEN_WIDTH,SCREEN_HEIGHT])
    
    pygame.mixer.Sound.stop(rotate_sound)
    pygame.mixer.Sound.stop(forward_sound)

    tank1.speed_boosted = False
    tank2.speed_boosted = False
    LargeText = Load_Font_From_Zip('fonts/Games.ttf',int(SCREEN_WIDTH / 11.75))
    boradImg = pygame.transform.scale(Load_Image_From_Zip(archive,'pictures/board.png'),[int(SCREEN_WIDTH / 1.13), int(SCREEN_HEIGHT / 3.84)])

    if player == tank1:
        TextSurf = text_objects('PLAYER 2 WINS !!!', LargeText)
    elif player == tank2:
        TextSurf = text_objects('PLAYER 1 WINS !!!', LargeText)
    gameDisplay.blit(boradImg, (SCREEN_WIDTH / 10.5, SCREEN_HEIGHT / 8))
    gameDisplay.blit(TextSurf, (SCREEN_WIDTH / 6, SCREEN_HEIGHT / 5))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()           
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(io.BytesIO(archive.read('sounds/intro.mp3')))
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(-1)
                    tank1.respawn()
                    tank2.respawn()
                    game_intro()

        Button('AGAIN',int(SCREEN_WIDTH / 2.12) ,int(SCREEN_HEIGHT / 1.79) , bright_green, black, 'play',GameOver)
        Button(' EXIT',int(SCREEN_WIDTH / 2.12) ,int(SCREEN_HEIGHT / 1.45) , bright_red, black, 'quit' ,GameOver)

        pygame.display.update()
        clock.tick(30)

def Expo(tank):
    imageName = ""
    for i in range(0,43):
        imageName = f"explosion/tile{i}.png"
        image = pygame.transform.scale(Load_Image_From_Zip(archive,imageName),[int(tank.height+tank.width+SCREEN_WIDTH/68.3),int(tank.height+tank.width+SCREEN_HEIGHT/76.8)])
        gameDisplay.blit(image, (tank.rect.x-SCREEN_WIDTH/34.15,tank.rect.y-SCREEN_HEIGHT/30.72))
        pygame.display.update()
   

def paused():
    pygame.mixer.Sound.stop(forward_sound)
    pygame.mixer.Sound.stop(rotate_sound)
    pause = True
    while pause:
        LargeText = Load_Font_From_Zip('fonts/Games.ttf',int(SCREEN_WIDTH / 11.75))
        SmallText = Load_Font_From_Zip('fonts/Nois.ttf',int(SCREEN_WIDTH / 28))
        TextSurf = text_objects('PAUSED', LargeText)
        conti = text_objects(' P to continue', SmallText)
        home = text_objects(' ESC to MainPage', SmallText)
        FPS(SCREEN_WIDTH /250,0)
        gameDisplay.blit(TextSurf, (SCREEN_WIDTH / 8.5, SCREEN_HEIGHT / 4.5))
        gameDisplay.blit(conti, (SCREEN_WIDTH / 1.875, SCREEN_HEIGHT / 2))
        gameDisplay.blit(home, (SCREEN_WIDTH / 1.875, SCREEN_HEIGHT / 1.65))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()           
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    GameLoop()
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(io.BytesIO(archive.read('sounds/intro.mp3')))
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(-1)
                    tank1.respawn()
                    tank2.respawn()
                    game_intro()
        pygame.display.update()

def game_intro():
    tank1.health = tank2.health = 3
    pygame.mixer.Sound.stop(fire_sound_1)
    pygame.mixer.Sound.stop(fire_sound_2)
    ClearBullets()
    tank1.speed_boosted = False
    tank2.speed_boosted = False
    left = pygame.transform.scale(Load_Image_From_Zip(archive,"pictures/left.png"),[int(SCREEN_WIDTH / 3.90), int(SCREEN_HEIGHT / 3.41)])
    right = pygame.transform.scale(Load_Image_From_Zip(archive,"pictures/right.png"),[int(SCREEN_WIDTH / 3.41), int(SCREEN_HEIGHT / 2.64)])
    tnkImg = pygame.transform.scale(Load_Image_From_Zip(archive,'pictures/punk.png'),[int(SCREEN_WIDTH / 0.872), int(SCREEN_HEIGHT / 0.698)])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()           
                quit()
        
        gameDisplay.fill((138,155,142))
        gameDisplay.blit(tnkImg, (SCREEN_WIDTH / -17.74,0))
        LargeText = Load_Font_From_Zip('fonts/Thuner.ttf',int(SCREEN_WIDTH / 11.75))
        TextSurf = text_objects('TACKY TANKS', LargeText)
        gameDisplay.blit(TextSurf, (SCREEN_WIDTH / 8.5, SCREEN_HEIGHT / 4.5))
        gameDisplay.blit(left, (SCREEN_WIDTH / 4.55, SCREEN_HEIGHT / 153.6))
        gameDisplay.blit(right, (SCREEN_WIDTH / 1.95,SCREEN_HEIGHT / SCREEN_HEIGHT-1))
        Button('START',int(SCREEN_WIDTH / 2.12), int(SCREEN_HEIGHT / 1.79) , bright_green, black, 'play', game_intro)
        Button(' EXIT',int(SCREEN_WIDTH / 2.12), int(SCREEN_HEIGHT / 1.47) , bright_red, black, 'quit', GameOver)
        Tuto_Credit('TUTORIAL', int(SCREEN_WIDTH / 22.5), 0, armyellow, 'tutorial')
        Tuto_Credit('CREDITS', int(SCREEN_WIDTH / 1.1), 0, armyellow, 'credits')
        pygame.display.update()

#•••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••• GAME LOOP ••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••

def GameLoop():
    global  angle1, angle2
    #--------------- Play engine sound at the very beginning----------------------#
    pygame.mixer.music.stop()
    pygame.mixer.music.load(io.BytesIO(archive.read('sounds/engine.mp3')))
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)
    start_ticks=pygame.time.get_ticks()
    
    gameQuit = False

    


    while not gameQuit:
        
        seconds = (pygame.time.get_ticks()-start_ticks)/1000

        if tank1.health== 0:
            pygame.mixer.Sound.play(explosion_sound)

            Expo(tank1)
            tank1.respawn()
            tank2.respawn()
            tank1.health = tank2.health =  3   # this will reset each tank's hp to standard (3)
            pygame.mixer.music.stop()
            GameOver(tank1)
            pygame.mixer.Sound.stop(fire_sound_1)

        if tank2.health == 0:
            pygame.mixer.Sound.play(explosion_sound)

            Expo(tank2)
            tank1.respawn()
            tank2.respawn()
            tank1.health = tank2.health =  3
            pygame.mixer.music.stop()
            GameOver(tank2)
            pygame.mixer.Sound.stop(fire_sound_2)
            
        
                
    #------------------------- BUTTONS ---------------------------#
        gameDisplay.fill(white)
        gameDisplay.blit(background, (0, 0))
        maze.render()
        FPS(SCREEN_WIDTH/250,SCREEN_HEIGHT / 1.012)
        keyState = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.mixer.music.stop()
                    paused()
                if event.key == pygame.K_SPACE:
                    tank1.shoot(fire_sound_1)
                if event.key == pygame.K_RSHIFT:
                    tank2.shoot(fire_sound_2)
                if event.key == pygame.K_r:
                    if tank1.stuck:
                        tank1.respawn()
                        tank1.stuck = False
                if event.key == pygame.K_RCTRL:
                    if tank2.stuck:
                        tank2.respawn()
                        tank2.stuck = False
                        state = False

                if event.key == pygame.K_a or event.key == pygame.K_d:
                    pygame.mixer.Sound.play(rotate_sound)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    pygame.mixer.Sound.play(rotate_sound)
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s :
                    pygame.mixer.Sound.play(forward_sound)
                

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    pass
                if event.key == pygame.K_a or event.key == pygame.K_d or  event.key == pygame.K_LEFT  or  event.key == pygame.K_RIGHT :
                    pygame.mixer.Sound.stop(rotate_sound)
                if event.key == pygame.K_w or event.key == pygame.K_s or  event.key == pygame.K_DOWN  or  event.key == pygame.K_UP :
                    pygame.mixer.Sound.stop(forward_sound)
                    pygame.mixer.Sound.play(stop_sound)
            


    #-----------------------ADJUST STUCK STATEMENT------------------
        if not CollisionSingle(tank1,collidables_for_tank1):
            tank1.stuck = False
        else:
            tank1.stuck = True

        if not CollisionSingle(tank2,collidables_for_tank2):
            tank2.stuck = False
        else:
            tank2.stuck = True

    #*********************** CONTROLS **************************#
        #-> PLAYER 1
            
        if keyState[pygame.K_d]:
            angle1 += -5
            tank1.rotate(angle1)
            
        elif  keyState[pygame.K_a]:
            angle1 += 5
            tank1.rotate(angle1)
            
        elif  keyState[pygame.K_w]:
            if not CollisionSingle(tank1,collidables_for_tank1):
                tank1.forward()
                
        elif  keyState[pygame.K_s]:
            if not CollisionSingle(tank1,collidables_for_tank1):
                tank1.backward()

        #-> PLAYER 2

        if keyState[pygame.K_RIGHT]:
            angle2 += -5
            tank2.rotate(angle2)
            
        elif  keyState[pygame.K_LEFT]:
            angle2 += 5
            tank2.rotate(angle2)
            
        elif  keyState[pygame.K_UP]:
            if not CollisionSingle(tank2,collidables_for_tank2):
                tank2.forward()
                
        elif  keyState[pygame.K_DOWN]:
            if not CollisionSingle(tank2,collidables_for_tank2):
                tank2.backward()
        
    #  ----------------------- OBLITERATING the bullets---------------------------#
        Destroy(tank1,tank2,maze)
        
    #------------------------- Drawing Bullets Remotely -------------------------#
        tank1.bullet_sprites.draw(gameDisplay)
        tank2.bullet_sprites.draw(gameDisplay)
    
    #----------------------------- Drawing Skills------------------------------------#
        
        if int(seconds) == 2:
            if not speed.exists:
                speed.rect.center = (random.randint(0,SCREEN_WIDTH),random.randint(0,SCREEN_HEIGHT))
                skill_sprites.add(speed)
                speed.exists = True
            if not health.exists:
                health.rect.center = (random.randint(0,SCREEN_WIDTH),random.randint(0,SCREEN_HEIGHT))
                skill_sprites.add(health)
                health.exists = True

        collided_skill_for_tank1 = GetCollidedSkill(tank1,skill_sprites)
        collided_skill_for_tank2 = GetCollidedSkill(tank2,skill_sprites)

        if int(seconds) < 12:
            
            if collided_skill_for_tank1 == speed:
                speed.exists= False
                tank1.speed_boosted = True
                skill_sprites.remove(speed)
            if collided_skill_for_tank1 == health:
                health.exists= False
                tank1.health += 2
                skill_sprites.remove(health)

            
            if collided_skill_for_tank2 == speed:
                speed.exists= False
                tank2.speed_boosted = True
                skill_sprites.remove(speed)
            if collided_skill_for_tank2 == health:
                health.exists= False
                tank2.health += 2
                skill_sprites.remove(health)
        else:
            skill_sprites.remove(speed)
            speed.exists = False
            skill_sprites.remove(health)
            health.exists = False
            

        
    # ------------------- draw skills on map --------------------------#
        skill_sprites.draw(gameDisplay)
        
    #       ---    *    ---    *    --- TANK RENDERING ---    *     ---        #    
        tank1.render()
        tank2.render()
    #------------------------------DRAW HP--------------------------------#
        drawHP(tank1, SCREEN_HEIGHT/100,SCREEN_HEIGHT/100 )
        drawHP(tank2, SCREEN_WIDTH-SCREEN_HEIGHT/18 , SCREEN_HEIGHT/100)

    #------------------------DRAW STUCK MESSAGE ---------------------#
        if tank1.stuck:
            drawStuck(SCREEN_HEIGHT/100 + 70 ,SCREEN_HEIGHT/100-10)
        if tank2.stuck:
            drawStuck( SCREEN_WIDTH-SCREEN_HEIGHT/18 - 100,  SCREEN_HEIGHT/100-10)

    #--------------------------------UPDATE BULLET SPRITES  (their movements)---------------------------------

        tank1.bullet_sprites.update(tank1,angle1)
        tank2.bullet_sprites.update(tank2,angle2)


    #-------------------------------------------------------------------------#
        pygame.display.update()
        clock.tick(30)

    # END OF THE GAME LOOP  ->
pygame.mixer.music.play(-1)
game_intro()
pygame.quit()
quit()