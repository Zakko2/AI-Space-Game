import pygame
from ai_space_game.player import *
from ai_space_game.enemy import *
from ai_space_game.bullet import *
from ai_space_game.texttypewriter import *
from ai_space_game.stagemanager import *
from ai_space_game.settings import FONT_PATH, FONT_SIZE



def load_assets():
    player_image = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha()
    player_image = pygame.transform.scale(player_image, (50, 38))

    enemy_image = pygame.image.load(ENEMY_IMAGE_PATH).convert_alpha()
    enemy_image = pygame.transform.scale(enemy_image, (50, 38))

    bullet_image = pygame.image.load(BULLET_IMAGE_PATH).convert_alpha()
    bullet_image = pygame.transform.scale(bullet_image, (10, 20))

    font = pygame.font.Font(FONT_PATH, scaled_font_size)
    
    return player_image, enemy_image, bullet_image, font

def initialize_game(screen, font):
    player_image, enemy_image, bullet_image, font = load_assets()

    player = Player(screen, x, y)
    bullets = []
    enemies = []

    text_typewriter = TextTypewriter()

    stage_manager = StageManager(font)
    stage_manager.add_stage(GameStage(1, 10))
    stage_manager.add_stage(GameStage(2, 20))
    stage_manager.add_stage(GameStage(3, 30))

    return player, bullets, enemies, text_typewriter, stage_manager

def setup_font(windowed_width):
    scaled_font_size = int(FONT_SIZE * windowed_width / windowed_width)
    font = pygame.font.Font(FONT_PATH, scaled_font_size)
    return font
