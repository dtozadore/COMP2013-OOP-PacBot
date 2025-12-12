import pygame
from src.Scenes.scene import Scene
from src.scene_manager import SceneManager
from src.GameLogic import GameLogic
from src.Map import StaticMapState
import math

class GameScene(Scene):
    def __init__(self, scene_manager: SceneManager):
        super().__init__(scene_manager)
        self.game_logic = GameLogic()

        # get window size
        screen_width, screen_height = self.scene_manager.screen.get_size()

        # number of tiles
        # self.num_tiles_x = self.game_logic.map.width
        # self.num_tiles_y = self.game_logic.map.height

        self.num_tiles_x = 12
        self.num_tiles_y = 8

        # pixels per tile
        tile_size = min(screen_width / self.num_tiles_x, screen_height / self.num_tiles_y)
        self.tile_size = tile_size
        self.pixel_scale_factor = self.tile_size / 16

        background_tile = pygame.image.load("resources/art/background/background.png")
        self.background_tile = pygame.transform.scale(background_tile, (math.ceil(self.tile_size), math.ceil(self.tile_size))) 

        wall_vertical_tile = pygame.image.load("resources/art/background/walls/wall_2.png")
        self.wall_vertical_tile = pygame.transform.scale(wall_vertical_tile, (math.ceil(self.tile_size), math.ceil(self.tile_size))) 

        wall_horizontal_tile = pygame.image.load("resources/art/background/walls/wall_3.png")
        self.wall_horizontal_tile = pygame.transform.scale(wall_horizontal_tile, (math.ceil(self.tile_size), math.ceil(self.tile_size))) 

        wall_t_up_tile = pygame.image.load("resources/art/background/walls/wall_4.png")
        self.wall_t_up_tile = pygame.transform.scale(wall_t_up_tile, (math.ceil(self.tile_size), math.ceil(self.tile_size))) 

        wall_t_down_tile = pygame.image.load("resources/art/background/walls/wall_5.png")
        self.wall_t_down_tile = pygame.transform.scale(wall_t_down_tile, (math.ceil(self.tile_size), math.ceil(self.tile_size))) 
        
        wall_t_top_right_tile = pygame.image.load("resources/art/background/walls/wall_6.png")
        self.wall_t_top_right_tile = pygame.transform.scale(wall_t_top_right_tile, (math.ceil(self.tile_size), math.ceil(self.tile_size))) 

        wall_t_top_left_tile = pygame.image.load("resources/art/background/walls/wall_7.png")
        self.wall_t_top_left_tile = pygame.transform.scale(wall_t_top_left_tile, (math.ceil(self.tile_size), math.ceil(self.tile_size))) 
        
        
        
        
        

    def handle_events(self, events:list[pygame.event.Event]):
        pass

    def update(self):
        pass

    def draw(self):
        self.draw_background()
        self.draw_map()
        self.draw_entities()
        self.draw_particles()
        self.draw_hud()

    def draw_background(self):
        for i in range(self.num_tiles_x):
            for j in range(self.num_tiles_y):
                # Blit the scaled 16x16 pixel art at each tile position
                x = i * self.tile_size
                y = j * self.tile_size

                self.scene_manager.screen.blit(self.background_tile, (x, y))

    def draw_map(self):
        for i in range(self.num_tiles_x):
            for j in range(self.num_tiles_y):
                # Blit the scaled 16x16 pixel art at each tile position
                x = i * self.tile_size
                y = j * self.tile_size

                #tile = self.game_logic.map.get(i, j)
                tile = None
                if tile is not None:
                    if tile == StaticMapState.WALL_VERTICAL:
                        self.scene_manager.screen.blit(self.wall_vertical_tile, (x, y))
                    elif tile == StaticMapState.WALL_HORIZONTAL:
                        self.scene_manager.screen.blit(self.wall_horizontal_tile, (x, y))
                    elif tile == StaticMapState.WALL_T_UP:
                        self.scene_manager.screen.blit(self.wall_t_up_tile, (x, y))
                    elif tile == StaticMapState.WALL_T_DOWN:
                        self.scene_manager.screen.blit(self.wall_t_down_tile, (x, y))

    def draw_entities(self):
        pass

    def draw_particles(self):
        pass

    def draw_hud(self):
        pass