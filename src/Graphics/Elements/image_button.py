import pygame
from typing import Optional

class ImageButton():
    def __init__(self, 
                screen, 
                image_path:str, 
                highlighted_image_path:str,
                x:int, 
                y:int, 
                scale_x:float,
                scale_y:float,
                on_click=None):
        self.screen = screen
        self.x = x
        self.y = y
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.on_click_callback = on_click
        self.hovered = False

        self.image = pygame.image.load(image_path)
        self.highlighted_image = pygame.image.load(highlighted_image_path)

        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        self.highlighted_image_width = self.highlighted_image.get_width()
        self.highlighted_image_height = self.highlighted_image.get_height()

        self.width = self.image_width * self.scale_x
        self.height = self.image_height * self.scale_y

        self.highlighted_width = self.highlighted_image_width * self.scale_x
        self.highlighted_height = self.highlighted_image_height * self.scale_y

        self.scaled_image = pygame.transform.scale(self.image, (self.width, self.height))
        self.scaled_highlighted_image = pygame.transform.scale(self.highlighted_image, (self.highlighted_width, self.highlighted_height))

    def draw(self):
        if self.hovered:
            self.screen.blit(self.scaled_highlighted_image, (self.x, self.y))
        else:
            self.screen.blit(self.scaled_image, (self.x, self.y))

    def handle_events(self, events:list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                if self.is_hovered(event.pos):
                    self.hovered = True
                else:
                    self.hovered = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_hovered(event.pos):
                    self.on_click()

    def on_click(self):
        if self.on_click_callback is not None:
            self.on_click_callback()

    def is_hovered(self, mouse_pos:tuple[int, int]) -> bool:
        return self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height