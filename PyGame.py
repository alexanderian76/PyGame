from World import World
import pygame
import os
from PIL import Image, ImageFilter  
import csv
from Consts import ROWS, COLS, SCREEN_HEIGHT, SCREEN_WIDTH, level, TILE_SIZE, TILE_TYPES, enemy_group, screen, bg_scroll, MONITOR_SIZE
import Consts
from Soldier import Soldier

pygame.init()
pygame.joystick.init()
try:
    controller = pygame.joystick.Joystick(0)
    controller.init()
except:
    print("Can't connect first gamepad")



#img = Image.open('Char/Idle/2.png')  
#img.load()
#print(img.format, img.size, img.mode)


pygame.display.set_caption('Shooter')

moving_left = False
moving_right = False

clock = pygame.time.Clock()
FPS = 60

#Colors
BG = (144, 201, 120)
blackBG = (100,110,100)
RED = (255, 0, 0)





def Draw_BG():
    screen.fill(blackBG)
    #pygame.draw.line(screen,RED, (0, 300), (SCREEN_WIDTH, 300))


#player = Soldier('player', 200, 300, 1, 5)
#player2 = Soldier('player', 250, 300, 1, 3)
x = 300
y = 300
scale = 1

#player2 = World().process_data()

#print(player.animation_list[2])


#Prepare the World
world_data = []
for row in range(ROWS):
	r = [-1] * COLS
	world_data.append(r)
#load in level data and create world
with open(f'levels/level{level}_data.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for x, row in enumerate(reader):
		for y, tile in enumerate(row):
			world_data[x][y] = int(tile)
world = World()
player = world.process_data(world_data)
###############
player.TILES = world.obstacle_list
player.level_length = world.level_length
run = True 
for enemy in enemy_group:
    enemy.TILES = world.obstacle_list
    enemy.level_length = world.level_length
while run: 
    clock.tick(FPS)
    Draw_BG()
    player.update_animation()
    
    
    world.draw(Consts.screen_scroll, screen)

    for enemy in enemy_group:
        if enemy.alive:
            enemy.ai(player, Consts.screen_scroll, screen)
            enemy.update()
            enemy.update_animation()
            enemy.Draw(screen)
            if (abs(player.rect.left - enemy.rect.right) < 10 and player.direction == -1 or abs(player.rect.right - enemy.rect.left) < 10 and player.direction == 1) and player.deal_damage and abs(player.rect.y - enemy.rect.y) < 15:
                enemy.alive = False
            if (abs(player.rect.left - enemy.rect.right) < 10 and enemy.direction == 1 or abs(player.rect.right - enemy.rect.left) < 10 and enemy.direction == -1) and enemy.deal_damage and abs(player.rect.y - enemy.rect.y) < 15:
                player.alive = False
    player.Draw(screen)
    #if player2.alive:
    #    player2.update_animation()
    #    player2.Draw(screen)
    if player.rect.y > SCREEN_HEIGHT or not player.alive:
        run = False
    if player.alive:
        if player.in_air:
            player.update_action(2)
        elif player.isAttacking:
            player.update_action(3)
        elif moving_left or moving_right:
            player.update_action(1)
        else:
            player.update_action(0)
        Consts.screen_scroll = player.Move(moving_left, moving_right, screen)
        bg_scroll -= Consts.screen_scroll
        
    #player.Move(moving_left,moving_right)
    #player2.Move(False,False)
    #if player2.alive:
    #    player2.ai(player)
        
        #if (abs(player.rect.left - player2.rect.right) < 10 and player.direction == -1 or abs(player.rect.right - player2.rect.left) < 10 and player.direction == 1) and player.deal_damage:
        #    player2.alive = False
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 1:
                player.jump = True
        if event.type == pygame.JOYHATMOTION:
           # print(event.value[0])
            if event.value[0] == 1:
                moving_right = True
            elif event.value[0] == -1:
                moving_left = True
            elif event.value[1] == 1:
                player.jump = True
            else:
                moving_left = False
                moving_right = False
       # if event.type == pygame.JOYAXISMOTION:
        #    if round(event.value,2) <= 1 and round(event.value,2) > 0.5:
         #       moving_right = True
          #  elif round(event.value,2) >= -1 and round(event.value,2) < -0.5:
           #     moving_left = True
            #else:
             #   moving_left = False
              #  moving_right = False
        #if event.type == pygame.JOYBUTTONDOWN:
          #  print(event.button)
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                screen = pygame.display.set_mode(MONITOR_SIZE, pygame.FULLSCREEN)
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_f:
                player.attack = True
            if event.key == pygame.K_ESCAPE:
                run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
        
    pygame.display.update()        

pygame.quit()            

