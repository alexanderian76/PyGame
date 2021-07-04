import pygame

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
level = 1
enemy_group = pygame.sprite.Group()
MONITOR_SIZE = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
screen_scroll = 0
bg_scroll = 0
SCROLL_THRESH = 200
