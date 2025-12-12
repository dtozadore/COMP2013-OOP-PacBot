import pygame
from typing import Optional

class Button():
    def __init__(self, 
                screen, 
                text:str, 
                x:int, 
                y:int, 
                width:int, 
                height:int, 
                colour:tuple[int, int, int]=(255, 255, 255), 
                text_colour:tuple[int, int, int]=(0, 0, 0), 
                font:Optional[pygame.font.Font]=None, 
                on_click=None):
        self.screen = screen
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.default_colour = colour
        self.text_colour = text_colour
        self.font = font if font is not None else pygame.font.Font(None, 32)
        self.on_click_callback = on_click
        self.is_keyboard_selected = False  # Track if selected via keyboard

    def draw(self):
        pygame.draw.rect(self.screen, self.colour, (self.x, self.y, self.width, self.height))
        text = self.font.render(self.text, True, self.text_colour)
        self.screen.blit(text, (self.x + self.width/2 - text.get_width()/2, self.y + self.height/2 - text.get_height()/2))

    def handle_events(self, events:list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                if self.is_hovered(event.pos):
                    # Only change to hover color if not keyboard selected
                    if not self.is_keyboard_selected:
                        self.colour = (200, 200, 200)
                else:
                    # Only reset to default if not keyboard selected
                    if not self.is_keyboard_selected:
                        self.colour = self.default_colour

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_hovered(event.pos):
                    self.on_click()

    def on_click(self):
        if self.on_click_callback is not None:
            self.on_click_callback()

    def is_hovered(self, mouse_pos:tuple[int, int]) -> bool:
        return self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height