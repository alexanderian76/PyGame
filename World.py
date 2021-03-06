from Soldier import Soldier
import pygame
from PIL import Image, ImageFilter
from Consts import ROWS, COLS, SCREEN_HEIGHT, SCREEN_WIDTH, level, TILE_SIZE, TILE_TYPES, enemy_group, screen

pygame.init()
img_list = []
for x in range(TILE_TYPES):
    try:
        img = Image.open(f'Char/tiles/{x}.png')
        img.load()
        img1 = pygame.image.frombuffer(img.tobytes(),(img.width, img.height) ,"RGBA")
        img1 = pygame.transform.scale(img1, (TILE_SIZE, TILE_SIZE))
        img_list.append(img1)
        img.close()
    except:
        print("No such file in directory")
class World():
    def __init__(self):
        self.obstacle_list = []


    def process_data(self, data):
        self.level_length = len(data[0])
		#iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
					#elif tile >= 9 and tile <= 10:
					#	water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
					#	water_group.add(water)
					#elif tile >= 11 and tile <= 14:
					#	decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
					#	decoration_group.add(decoration)
                    elif tile == 15:#create player
                        player = Soldier('player', x * TILE_SIZE, y * TILE_SIZE, 0.65, 5)
					#	health_bar = HealthBar(10, 10, player.health, player.health)
                    elif tile == 16:#create enemies
                        enemy = Soldier('enemy', x * TILE_SIZE, y * TILE_SIZE, 0.65, 3)
                        enemy_group.add(enemy)
					#elif tile == 17:#create ammo box
					#	item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
					#	item_box_group.add(item_box)
					#elif tile == 18:#create grenade box
					#	item_box = ItemBox('Grenade', x * TILE_SIZE, y * TILE_SIZE)
					#	item_box_group.add(item_box)
					#elif tile == 19:#create health box
					#	item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
					#	item_box_group.add(item_box)
					#elif tile == 20:#create exit
					#	exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
					#	exit_group.add(exit)

        return player #, health_bar
        
    def draw(self, screen_scroll, screen):
        for tile in self.obstacle_list:
           # print(screen_scroll)
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
