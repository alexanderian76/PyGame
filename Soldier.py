import pygame
import os
from PIL import Image, ImageFilter
from Consts import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE, TILE_TYPES, SCROLL_THRESH, bg_scroll

GRAVITY = 0.75


class Soldier(pygame.sprite.Sprite):
    def __init__(self, chat_type, x, y, scale, speed):
        self.char_type = chat_type
        self.speed = speed
        self.alive = True
        self.direction = 1
        self.vel_y = 0
        self.moving = False
        #Attack
        self.isAttacking = False
        self.attack = False
        self.deal_damage = False
        self.attack_time = pygame.time.get_ticks()
        #
        
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        pygame.sprite.Sprite.__init__(self)
        animation_types = ['Idle', 'Run', 'Jump', 'Attack']
        index = 0
        #TILES
        self.TILES = pygame.sprite.Group()
        self.level_length = 0
        #
        for animation in animation_types:
			#reset temporary list of images 
            temp_list = []
			#count number of files in the folder
            num_of_frames = len(os.listdir(f'Char/{animation}'))
            for i in range(num_of_frames - 1, 0, -1):
                #img = pygame.image.load(f'Char/{animation}/{i}.bmp')
                img = Image.open(f'Char/{animation}/{i}.png')
                img.load()
                img1 = pygame.image.frombuffer(img.tobytes(),(img.width, img.height) ,"RGBA")
                img1 = pygame.transform.scale(img1, (int(img1.get_width() * scale), int(img1.get_height() * scale)))
                temp_list.append(img1)
                img.close()
                
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        #self.image = pygame.image.frombuffer(img.tobytes(),(53,92),"RGBA")
        self.rect = self.image.get_rect()
        #self.rect = pygame.Rect(200,300,50,50)
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
    def Move(self, moving_left, moving_right, screen):
        screen_scroll = 0
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
            self.isAttacking = False
            self.deal_damage = False
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
            self.isAttacking = False
            self.deal_damage = False
    #Jumping
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
            self.isAttacking = False
        self.vel_y += GRAVITY
        dy += self.vel_y

        #check floor collision
        
        for tile in self.TILES:
            #check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                #if the ai has hit a wall then make it turn around
            if self.char_type == 'enemy':
                self.direction *= -1
                self.move_counter = 0
            #check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        #Attacking
        if self.attack and not self.isAttacking and not self.in_air:
            self.attack = False
            self.isAttacking = True
            self.attack_time = pygame.time.get_ticks()
        if self.isAttacking and pygame.time.get_ticks() - self.attack_time > 700:
            self.deal_damage = True
        if self.isAttacking and pygame.time.get_ticks() - self.attack_time > 720:
            self.isAttacking = False
            self.deal_damage = False
        
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > screen.get_width():
                dx = 0
        self.rect.x += dx
        self.rect.y += dy
        
        if self.char_type == 'player':
            if (self.rect.right > screen.get_width() - SCROLL_THRESH and bg_scroll < (self.level_length * TILE_SIZE) - screen.get_height())\
                or (self.rect.left < SCROLL_THRESH and bg_scroll < abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll
    
    def update_animation(self):
		#update animation
        ANIMATION_COOLDOWN = 100
		#update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
		#check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
		#if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
		#check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
			#update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def Draw(self, screen):
        #screen.blit(self.image,self.rect)
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


    def ai(self, player, screen_scroll, screen):
        ai_moving_right = False
        ai_moving_left = False
        if self.alive and not self.isAttacking:
            if self.direction == 1:
                #ai_moving_right = True
                if abs(player.rect.right - self.rect.left - self.speed) > abs(player.rect.right - self.rect.left):
                    if abs(player.rect.right - self.rect.left - self.speed) > abs(player.rect.right - self.rect.left + self.speed):
                        ai_moving_right = False
                        ai_moving_left = True 
                        self.direction = -1
                    else:
                        ai_moving_right = True
                        ai_moving_left = False 
                        self.direction = 1
                    
                elif abs(player.rect.right - self.rect.right) < 300:
                    ai_moving_right = True
                    ai_moving_left = False 
                    self.direction = 1
            else:
                #ai_moving_right = False
                if abs(player.rect.right - self.rect.left + self.speed) > abs(player.rect.right - self.rect.left):
                    if abs(player.rect.left - self.rect.right - self.speed) < abs(player.rect.left - self.rect.right + self.speed):
                        ai_moving_right = True
                        ai_moving_left = False 
                        self.direction = 1
                    else:
                        ai_moving_right = False
                        ai_moving_left = True 
                        self.direction = -1
                elif abs(player.rect.right - self.rect.right) < 200:
                    ai_moving_right = False
                    ai_moving_left = True 
                    self.direction = -1
            
            #ai_moving_left = not ai_moving_right

        if abs(-player.rect.left + self.rect.right) < 10 and self.direction == 1 or abs(-player.rect.right + self.rect.left) < 10 and self.direction == -1:
            self.attack = True
            self.update_action(3)
        if ai_moving_left or ai_moving_right:
            self.update_action(1)
        elif not self.isAttacking:
            self.update_action(0) 
        self.Move(ai_moving_left, ai_moving_right, screen)
        self.rect.x += screen_scroll