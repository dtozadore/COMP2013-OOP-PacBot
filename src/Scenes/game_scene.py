import pygame
import math
import numpy as np

from src.Scenes.scene import Scene
from src.scene_manager import SceneManager
from src.GameLogic import GameLogic
from src.Map import StaticMapState
from src.Graphics.sprite import Sprite


class GameScene(Scene):
    def __init__(self, scene_manager: SceneManager):
        super().__init__(scene_manager)
        self.game_logic = GameLogic()

        # get window size
        screen_width, screen_height = self.scene_manager.screen.get_size()

        # number of tiles
        # self.num_tiles_x = self.game_logic.map.width
        # self.num_tiles_y = self.game_logic.map.height

        self.map: np.ndarray = None
        self.entities: list[Sprite] = []

        self.num_tiles_x = self.game_logic.scenario.map.cols
        self.num_tiles_y = self.game_logic.scenario.map.rows

        # pixels per tile
        tile_size = min(screen_width / self.num_tiles_x, screen_height / self.num_tiles_y)
        self.tile_size = tile_size
        self.pixel_scale_factor = self.tile_size / 16

        background_tile = pygame.image.load("resources/art/background/background.png")
        self.background_tile = pygame.transform.scale(background_tile, (math.ceil(self.tile_size), math.ceil(self.tile_size)))

        wall_vertical_tile = pygame.image.load("resources/art/walls/wall_2.png")
        self.wall_vertical_tile = pygame.transform.scale(wall_vertical_tile, (math.ceil(self.tile_size), math.ceil(self.tile_size)))

        wall_horizontal_tile = pygame.image.load("resources/art/walls/wall_3.png")
        self.wall_horizontal_tile = pygame.transform.scale(wall_horizontal_tile, (math.ceil(self.tile_size), math.ceil(self.tile_size)))

        wall_t_up_tile = pygame.image.load("resources/art/walls/wall_4.png")
        self.wall_t_up_tile = pygame.transform.scale(wall_t_up_tile, (math.ceil(self.tile_size), math.ceil(self.tile_size)))

        wall_t_down_tile = pygame.image.load("resources/art/walls/wall_5.png")
        self.wall_t_down_tile = pygame.transform.scale(wall_t_down_tile, (math.ceil(self.tile_size), math.ceil(self.tile_size)))

        wall_t_top_right_tile = pygame.image.load("resources/art/walls/wall_6.png")
        self.wall_t_top_right_tile = pygame.transform.scale(wall_t_top_right_tile, (math.ceil(self.tile_size), math.ceil(self.tile_size)))

        wall_t_top_left_tile = pygame.image.load("resources/art/walls/wall_7.png")
        self.wall_t_top_left_tile = pygame.transform.scale(wall_t_top_left_tile, (math.ceil(self.tile_size), math.ceil(self.tile_size)))

        wall_corner_ne_tile = pygame.image.load("resources/art/walls/wall_8.png")
        self.wall_corner_ne_tile = pygame.transform.scale(wall_corner_ne_tile, (math.ceil(self.tile_size), math.ceil(self.tile_size)))

        wall_corner_nw_tile = pygame.image.load("resources/art/walls/wall_9.png")
        self.wall_corner_nw_tile = pygame.transform.scale(wall_corner_nw_tile, (math.ceil(self.tile_size), math.ceil(self.tile_size)))

        wall_corner_se_tile = pygame.image.load("resources/art/walls/wall_10.png")
        self.wall_corner_se_tile = pygame.transform.scale(wall_corner_se_tile, (math.ceil(self.tile_size), math.ceil(self.tile_size)))

        wall_corner_sw_tile = pygame.image.load("resources/art/walls/wall_11.png")
        self.wall_corner_sw_tile = pygame.transform.scale(wall_corner_sw_tile, (math.ceil(self.tile_size), math.ceil(self.tile_size)))

    def handle_events(self, events: list[pygame.event.Event]):
        pass

    def update(self):
        map, entities, is_game_over = self.game_logic.update()
        self.map = map
        self.entities = entities

        if is_game_over:
            self.scene_manager.change_scene("menu")

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
        if self.map is None:
            return

        for i in range(self.num_tiles_x):
            for j in range(self.num_tiles_y):
                # Blit the scaled 16x16 pixel art at each tile position
                x = i * self.tile_size
                y = j * self.tile_size

                tile = self.map[j, i]

                if tile is not None:
                    if tile == StaticMapState.WALL_VERTICAL.value:
                        self.scene_manager.screen.blit(
                            self.wall_vertical_tile, (x, y))
                    elif tile == StaticMapState.WALL_HORIZONTAL.value:
                        self.scene_manager.screen.blit(
                            self.wall_horizontal_tile, (x, y))
                    elif tile == StaticMapState.WALL_T_UP.value:
                        self.scene_manager.screen.blit(
                            self.wall_t_up_tile, (x, y))
                    elif tile == StaticMapState.WALL_T_DOWN.value:
                        self.scene_manager.screen.blit(
                            self.wall_t_down_tile, (x, y))
                    elif tile == StaticMapState.WALL_T_TOP_RIGHT.value:
                        self.scene_manager.screen.blit(
                            self.wall_t_top_right_tile, (x, y))
                    elif tile == StaticMapState.WALL_T_TOP_LEFT.value:
                        self.scene_manager.screen.blit(
                            self.wall_t_top_left_tile, (x, y))
                    elif tile == StaticMapState.WALL_CORNER_NE.value:
                        self.scene_manager.screen.blit(
                            self.wall_corner_ne_tile, (x, y))
                    elif tile == StaticMapState.WALL_CORNER_NW.value:
                        self.scene_manager.screen.blit(
                            self.wall_corner_nw_tile, (x, y))
                    elif tile == StaticMapState.WALL_CORNER_SE.value:
                        self.scene_manager.screen.blit(
                            self.wall_corner_se_tile, (x, y))
                    elif tile == StaticMapState.WALL_CORNER_SW.value:
                        self.scene_manager.screen.blit(
                            self.wall_corner_sw_tile, (x, y))

    def draw_entities(self):
        for entity in self.entities:
            sprite = entity.draw(math.ceil(self.tile_size))
            self.scene_manager.screen.blit(sprite, (entity.x*self.tile_size, entity.y*self.tile_size))

    def draw_particles(self):
        pass

    def draw_hud(self):
        pass
