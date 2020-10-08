# Allow pygame_sdl2 to be imported as pygame.
import pygame_sdl2
pygame_sdl2.import_as_pygame()

import pygame
import time
import random
import math
import os

bird_height = 115
bird_width = 276
laser_width = 114

black = (0,0,0)
white = (255,255,255)
red = (84,58,39)
green = (0,255,0)
blue = (0,0,255)
ground_green = (113,58,34)

clock = pygame.time.Clock()

def save_state(x, y):
    """
    Saves the game state.
    """

    with open("state.txt", "w") as f:
        f.write("{} {}".format(x, y))

def load_state():
    try:
        with open("state.txt", "r") as f:
            x, y = f.read().split()
            x = int(x)
            y = int(y)

        return x, y
    except:
        return None, None

def delete_state():

    if os.path.exists("state.txt"):
        os.unlink("state.txt")

        
class flowers():
    def __init__(self,x):
        self.i = random.randrange(1,9,1)
        self.flowerImg = pygame.image.load(os.path.join('data/',"flower_"+str(self.i)+".png")).convert_alpha()
        self.speed = 12
        self.location_x = random.randrange(0, x)
        if self.i < 7:
            self.location_y = random.randrange(-350, -19)
        elif self.i >= 7:
                self.location_y = random.randrange(-350, -240)
    def update(self,screen,x,y):
         screen.blit(self.flowerImg,(self.location_x,self.location_y))
         self.location_y += self.speed
         if self.location_y > y:
            self.i = random.randrange(1,9,1)
            self.flowerImg = pygame.image.load(os.path.join('data/',"flower_"+str(self.i)+".png")).convert_alpha()
            self.location_x = random.randrange(0, x)
            if self.i < 7:
                self.location_y = random.randrange(-350, -19)
            elif self.i >= 7:
                self.location_y = random.randrange(-350, -240)
                
class features():
    def __init__(self,x):
        self.i = random.randrange(1,10,1)
        if self.i < 3:
            self.featureImg = pygame.image.load(os.path.join('data/',"features_"+str(self.i)+".png")).convert_alpha()
            self.location_x = 0
        elif self.i == 3:
            self.featureImg = pygame.image.load(os.path.join('data/',"features_"+str(self.i)+".png")).convert_alpha()
            self.location_x = x + 675
        else:
            self.featureImg = pygame.image.load(os.path.join('data/',"blank.png")).convert_alpha()
            self.location_x = 0
        self.speed = 12
        self.location_y = -810
    def update(self,screen,x,y):
         screen.blit(self.featureImg,(self.location_x,self.location_y))
         self.location_y += self.speed
         if self.location_y > y:
            self.i = random.randrange(1,4,1)
            if self.i < 3:
                self.featureImg = pygame.image.load(os.path.join('data/',"features_"+str(self.i)+".png")).convert_alpha()
                self.location_x = 0
            elif self.i == 3:
                self.featureImg = pygame.image.load(os.path.join('data/',"features_"+str(self.i)+".png")).convert_alpha()
                self.location_x = x - 675
            else:
                self.featureImg = pygame.image.load(os.path.join('data/',"blank.png")).convert_alpha()
            self.location_y = -810
            
class Player(pygame_sdl2.sprite.Sprite):
    def __init__(self):     
        pygame.sprite.Sprite.__init__(self)    
        self.images = [os.path.join('data/','codnor.png'),os.path.join('data/','codnor_flap1.png'),os.path.join('data/','codnor_flap2.png')]#,os.path.join('data/','codnor_flap2.png')]
        self.image = pygame.image.load(self.images[0]).convert_alpha()
        self.rect = self.image.get_rect()
        self.counter = 0
    def update(self,mouse_down):
        if mouse_down == True:
            self.image = pygame.image.load(self.images[self.counter]).convert_alpha()
            self.counter = (self.counter + 1) % len(self.images)
        else:
            self.image = pygame.image.load(self.images[0]).convert_alpha()
            self.counter = 0

class Laser(pygame_sdl2.sprite.Sprite):
    def __init__(self,x,y,laserposx):
        pygame.sprite.Sprite.__init__(self)
        self.images = [os.path.join('data/','laser.png'),os.path.join('data/','laser2.png')]
        self.image = pygame.image.load(self.images[0]).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = self.image.get_masks()
        self.newpos = self.rect
        self.rect.x = random.choice(laserposx)
        self.rect.y = random.randrange(0,y-laser_width)
        self.facing = 0
        self.counter = 0
        self.speed_y = random.randrange(-20,20)
        self.speed_change = 60
        self.laser_counter = 1
        self.laser_speed_init = 1
        self.laser_speed = 16
        self.vectoring = random.randrange(0,100)
        if self.rect.x == x - 1:
            self.facing = 1
    def update(self):
        if self.laser_counter == 0:
            self.image = pygame.image.load(self.images[self.counter]).convert_alpha()
            self.counter = (self.counter + 1) % len(self.images)
            self.laser_counter = 1
        self.laser_counter -= 1
        self.speed_change -= 1
        if self.vectoring < 74:
            if self.facing == 0:
                if self.speed_change <= 0:
                    self.rect.x += self.laser_speed
                elif self.speed_change > 0:
                    self.rect.x += self.laser_speed_init
            elif self.facing == 1:
                if self.speed_change <= 0:
                    self.rect.x += -self.laser_speed
                elif self.speed_change > 0:
                    self.rect.x += -self.laser_speed_init
        if self.vectoring >= 75:
            if self.facing == 0:
                if self.speed_change <= 0:
                    self.rect.x += self.laser_speed
                    self.rect.y += self.speed_y
                elif self.speed_change > 0:
                    self.rect.x += self.laser_speed_init
            elif self.facing == 1:
                if self.speed_change <= 0:
                    self.rect.x += -self.laser_speed
                    self.rect.y += self.speed_y
                elif self.speed_change > 0:
                    self.rect.x += -self.laser_speed_init              
                
    def remake(self,x,y,laserposx,score):
        self.rect.x = random.choice(laserposx)
        self.rect.y = random.randrange(0,y-laser_width)
        self.facing = 0
        self.counter = 0
        self.vectoring = random.randrange(0,100)
        self.speed_y = random.randrange(-20,20)
        self.speed_change = 60
        self.laser_counter = 1
        if score > 30 and score % 10 == 0:
            self.laser_speed += 2
        if self.rect.x == x - 1:
            self.facing = 1
            
class Button(pygame_sdl2.sprite.Sprite):
    def __init__(self,index,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = [os.path.join('data/','button_1.png'),os.path.join('data/','button_2.png'),os.path.join('data/','button_3.png'),os.path.join('data/','button_4.png'),os.path.join('data/','button_5.png')]
        self.image = pygame.image.load(self.images[index]).convert_alpha()
        self.rect = self.image.get_rect()
        if index == 0:
            self.rect.x = (x/2) - 170
            self.rect.y = y*0.2
        elif index == 1:
            self.rect.x = (x/2) - 170
            self.rect.y = y*0.8
        elif index == 2:
            self.rect.x = (x/2) - 170
            self.rect.y = y*0.2
        elif index == 3:
            self.rect.x = (x/2) - 170
            self.rect.y = y*0.5 - 90
        elif index == 4:
            self.rect.x = ((x/2) - 400) + (x/2 + 100)
            self.rect.y = y/2 - 195

class Op_Button(pygame_sdl2.sprite.Sprite):
    def __init__(self,index,x,y,current):
        pygame.sprite.Sprite.__init__(self)
        self.images = [os.path.join('data/','op_3.png'),os.path.join('data/','op_4.png'),os.path.join('data/','op_1.png'),os.path.join('data/','op_2.png')]
        self.on = current
        self.i = index
        if self.on == False:
            self.image = pygame.image.load(self.images[self.i]).convert_alpha()
        elif self.on == True:
            self.image = pygame.image.load(self.images[self.i + 2]).convert_alpha()
        self.rect = self.image.get_rect()
        if index == 0:
            self.rect.x = (x/2) - 325  
            self.rect.y = y/2 - 180
        elif index == 1:
            self.rect.x = (x/2) - 325
            self.rect.y = y/2 - 10
    def update(self):
        if self.on == False:
            self.image = pygame.image.load(self.images[self.i + 2]).convert_alpha()
            self.on = True
        elif self.on == True:
            self.image = pygame.image.load(self.images[self.i]).convert_alpha()
            self.on = False    
    
def lasers_dodged(count,screen,font):
    text = font.render("Score: "+str(count), True, black)
    screen.blit(text,(0,0))
    
##def fill_screen(x,y,img,screen):
##    for y_img in range(0,y,709):
##        for x_img in range(0,x,673):
##            screen.blit(img,(y_img,x_img))
            
def main():
    pygame.init()

    clicked = False
  
    screen = pygame.display.set_mode((640, 480))
    screen_w, screen_h = screen.get_size()

    titleImg = pygame.image.load(os.path.join('data/','title.png')).convert_alpha()   
    titleImg = pygame.transform.scale(titleImg, (screen_w, screen_h),screen).convert_alpha(screen)

    endImg = pygame.image.load(os.path.join('data/','end.png')).convert_alpha()   
    endImg = pygame.transform.scale(endImg, (screen_w, screen_h),screen).convert_alpha(screen)
   
    laserposx = [-laser_width+1,screen_w - 1]

    sleeping = False

    x = (screen_w/2) - (bird_width/2)
    y = (screen_h * 0.5)
    
    x_change = 0
    y_change = 0

    counter = 15

    score_font = pygame.font.Font('Gabriola.ttf', 70)
    menu_font = pygame.font.Font('Gabriola.ttf',125)
    
    playerBird = Player()
    playerBird.rect.x = x
    playerBird.rect.y = y

    score = 0
    plants_off = False
    rocks_off = False
    try:
        with open("score.txt", "r") as s:
            top_score,plants_off,rocks_off = s.read().split()
            top_score = int(top_score)
            if plants_off == 'False':
                plants_off = False
            elif plants_off == 'True':
                plants_off = True
            if rocks_off == 'False':
                rocks_off = False
            elif rocks_off == 'True':
                rocks_off = True
    except:
        with open("score.txt", "w") as s:
            s.write("{} {} {}".format(str(score),str(plants_off), str(rocks_off)))
            top_score = int(score)
    
    laserEnemy = Laser(screen_w,screen_h,laserposx)
    drones = list()
    drones.append(laserEnemy)

    rocks = list()
    feature1 = features(screen_w)
    rocks.append(feature1)
                 
    plants = list()
    flwr1 = flowers(screen_w)
    flwr2 = flowers(screen_w)
    flwr3 = flowers(screen_w)
    flwr4 = flowers(screen_w)
    flwr5 = flowers(screen_w)
    plants.append(flwr1)
    plants.append(flwr2)
    plants.append(flwr3)
    plants.append(flwr4)
    plants.append(flwr5)

    start_button = Button(0,screen_w,screen_h)
    exit_button = Button(1,screen_w,screen_h)
    restart_button = Button(2,screen_w,screen_h)
    options_button = Button(3,screen_w,screen_h)
    op_exit = Button(4,screen_w,screen_h)
    op1_button = Op_Button(0,screen_w,screen_h,plants_off)
    op2_button = Op_Button(1,screen_w,screen_h,rocks_off)
    
    all_sprites_list = pygame.sprite.Group()

    mouse_state = pygame.mouse.get_pressed()

    gameExit = False

    dead = False

    menuExit = False

    gameRestart = True

    optionsExit = True

    all_sprites_list.add(start_button)
    all_sprites_list.add(exit_button)
    all_sprites_list.add(options_button)
    
    # On startup, load state saved by APP_WILLENTERBACKGROUND, and the delete
    # that state.
    x, y = load_state()
    delete_state()

    while gameRestart:
        if not sleeping:
            while not menuExit:
                for event in pygame.event.get():
                    if start_button.rect.collidepoint(pygame.mouse.get_pos()):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_state = pygame.mouse.get_pressed()
                            if mouse_state == (1,0,0):
                                menuExit = True
                                gameExit = False
                                all_sprites_list.add(playerBird)
                                all_sprites_list.add(laserEnemy)
                                all_sprites_list.remove(start_button)
                                all_sprites_list.remove(exit_button)
                                all_sprites_list.remove(options_button)
                                mouse_state = (0,0,0)
                    if options_button.rect.collidepoint(pygame.mouse.get_pos()):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            menuExit = True
                            optionsExit = False
                            all_sprites_list.add(op1_button)
                            all_sprites_list.add(op2_button)
                            all_sprites_list.add(op_exit)
                            all_sprites_list.remove(start_button)
                            all_sprites_list.remove(exit_button)
                            all_sprites_list.remove(options_button)
                    if exit_button.rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                            menuExit = True
                            gameExit = True
                            gameRestart = False
                            dead = False
                
                screen.blit(titleImg,(0,0))
                title = menu_font.render("Majestic Codnor", True, black)
                screen.blit(title,((screen_w/2 - 275),60))
                all_sprites_list.draw(screen)
                pygame.display.flip()

            while not optionsExit:
                for event in pygame.event.get():
                    if op1_button.rect.collidepoint(pygame.mouse.get_pos()):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_state = pygame.mouse.get_pressed()
                            if mouse_state == (1,0,0):
                                op1_button.update()
                                plants_off = not plants_off
                                print(plants_off)
                                mouse_state = (0,0,0)
                    if op2_button.rect.collidepoint(pygame.mouse.get_pos()):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_state = pygame.mouse.get_pressed()
                            if mouse_state == (1,0,0):
                                op2_button.update()
                                rocks_off = not rocks_off
                                mouse_state = (0,0,0)
                    if op_exit.rect.collidepoint(pygame.mouse.get_pos()):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_state = pygame.mouse.get_pressed()
                            if mouse_state == (1,0,0):
                                optionsExit = True
                                menuExit = False
                                gameExit = True
                                dead = False
                                all_sprites_list.add(start_button)
                                all_sprites_list.add(exit_button)
                                all_sprites_list.add(options_button)
                                all_sprites_list.remove(op1_button)
                                all_sprites_list.remove(op2_button)
                                all_sprites_list.remove(op_exit)
                                with open("score.txt", "w") as s:
                                    s.write("{} {} {}".format(str(top_score),str(plants_off), str(rocks_off)))
                                
                screen.fill(white,(screen_w/2 - 325,screen_h/2 - 200,screen_w/2 +100, 321))
                all_sprites_list.draw(screen)
                pygame.display.update()
            

            
            while not gameExit:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            gameExit = True
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_state = pygame.mouse.get_pressed()
                            if mouse_state == (1,0,0):
                                y_change -= 12
                                clicked = True
                        if event.type == pygame.MOUSEBUTTONUP:
                            if mouse_state == (1,0,0):
                                y_change += 12
                                clicked = False

                    playerBird.rect.y += 7

                    screen.fill(ground_green)
                    
                    if rocks_off == False:
                        for all in rocks:
                            all.update(screen,screen_w,screen_h)
                            
                    if plants_off == False:
                        for all in plants:
                            all.update(screen,screen_w,screen_h)
                    
                    playerBird.rect.y += y_change
                         
                    if counter == 0:            
                        playerBird.update(clicked)
                        counter = 15

                    for all in drones:
                        all.update()
                        
                    counter -= 1
                                        
                    if playerBird.rect.y > screen_h or playerBird.rect.y + bird_height - 4 < 0:
                        gameExit = True
                        dead = True
                        all_sprites_list.remove(playerBird)
                        for all in drones:
                            all_sprites_list.remove(all)
                        all_sprites_list.add(restart_button)
                        all_sprites_list.add(exit_button)
                        y_change = 0
                    for all in drones:
                        if all.rect.x > screen_w or all.rect.x + laser_width < 0 or all.rect.y > screen_h or all.rect.y + laser_width < 0:
                            all.remake(screen_w,screen_h,laserposx,score)
                            score += 1
                            if score == 15:
                                laserEnemy2 = Laser(screen_w,screen_h,laserposx)
                                drones.append(laserEnemy2)
                                all_sprites_list.add(laserEnemy2)
                            if score == 30:
                                laserEnemy3 = Laser(screen_w,screen_h,laserposx)
                                drones.append(laserEnemy3)
                                all_sprites_list.add(laserEnemy3)
                            if score == 80:
                                laserEnemy4 = Laser(screen_w,screen_h,laserposx)
                                drones.append(laserEnemy4)
                                all_sprites_list.add(laserEnemy4)
##                            if score == 80:
##                                laserEnemy5 = Laser(screen_w,screen_h,laserposx)
##                                drones.append(laserEnemy5)
##                                all_sprites_list.add(laserEnemy5)
                    for all in drones:
                       if pygame_sdl2.sprite.spritecollideany(playerBird, drones):
                            gameExit = True
                            dead = True
                            all_sprites_list.remove(playerBird)
                            for all in drones:
                                all_sprites_list.remove(all)
                            all_sprites_list.add(restart_button)
                            all_sprites_list.add(exit_button)
                            mouse_state = (0,0,0)
                            y_change = 0

                    all_sprites_list.draw(screen)
                    lasers_dodged(score,screen,score_font)
##                    fps = clock.get_fps()
##                    font = pygame.font.Font('Gabriola.ttf',30)
##                    frames = font.render(str(fps), True, black)
##                    screen.blit(frames,((screen_w/2),60))
                    pygame.display.update()
                    clock.tick(30)

            while dead:
                screen.blit(endImg,(0,0))
                all_sprites_list.draw(screen)
                if score > top_score:
                    with open("score.txt", "w") as s:
                        s.write("{} {} {}".format(str(score),str(plants_off), str(rocks_off)))
                    top_score = score
                font = pygame.font.Font('Gabriola.ttf',40)
                text = font.render("Score: "+str(score), True, black)
                top_text = font.render("Top Score: "+str(top_score),True,black)
                screen.blit(text,(screen_w/2 - 60 , 160))
                screen.blit(top_text,(screen_w/2 - 60 , 40))
                pygame.display.update()
                for event in pygame.event.get():
                    if restart_button.rect.collidepoint(pygame.mouse.get_pos()):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_state = pygame.mouse.get_pressed()
                            if mouse_state == (1,0,0):
                                menuExit = True
                                gameExit = False
                                dead = False
                                playerBird.rect.x = (screen_w/2) - (bird_width/2)
                                playerBird.rect.y = (screen_h * 0.5)
                                score = 0
                                for all in drones:
                                    all.remake(screen_w,screen_h,laserposx,score)
                                    del drones[1:3]
                                all_sprites_list.add(playerBird)
                                all_sprites_list.add(laserEnemy)
                                all_sprites_list.remove(restart_button)
                                all_sprites_list.remove(exit_button)
                                mouse_state = (0,0,0)
                    if exit_button.rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                            menuExit = True
                            gameExit = True
                            dead = False
                            gameRestart = False
        

        elif ev.type == pygame.APP_WILLENTERBACKGROUND:
            # The app is about to go to sleep. It should save state, cancel
            # any timers, and stop drawing the screen until an APP_DIDENTERFOREGROUND
            # event shows up.

            save_state(x, y)

            sleeping = True

        elif ev.type == pygame.APP_DIDENTERFOREGROUND:
            # The app woke back up. Delete the saved state (we don't need it),
            # restore any times, and start drawing the screen again.

            delete_state()
            sleeping = False

            # For now, we have to re-open the window when entering the
            # foreground.
            screen = pygame.display.set_mode((1280, 720))
if __name__ == "__main__":
    main()
pygame.quit()
quit()


