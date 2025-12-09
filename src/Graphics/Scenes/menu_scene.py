import pygame
from src.Graphics.Elements.button import Button
from src.Graphics.scene_manager import SceneManager

class MenuScene():
    def __init__(self, scene_manager: SceneManager):
        self.scene_manager = scene_manager

        self.selected_button = 0

        self.buttons = [
            Button(self.scene_manager.screen, "Play", 100, 100, 100, 50, on_click=self.handle_play_button),
            Button(self.scene_manager.screen, "Settings", 100, 300, 100, 50, on_click=self.handle_settings_button),
            Button(self.scene_manager.screen, "Exit", 100, 500, 100, 50, on_click=self.handle_exit_button)
        ]

    def update(self):
        pass

    def handle_events(self, events:list[pygame.event.Event]):
        # Pass events to buttons for mouse hover highlighting
        for button in self.buttons:
            button.handle_events(events)
        
        # Handle keyboard navigation
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_button = (self.selected_button - 1) % len(self.buttons)
                elif event.key == pygame.K_DOWN:
                    self.selected_button = (self.selected_button + 1) % len(self.buttons)
                elif event.key == pygame.K_RETURN:
                    self.buttons[self.selected_button].on_click()

    def draw(self):
        # Highlight the selected button (keyboard navigation)
        for i, button in enumerate(self.buttons):
            if i == self.selected_button:
                button.is_keyboard_selected = True
                button.colour = (150, 150, 255)  # Light blue for selected
            else:
                button.is_keyboard_selected = False
                # Restore default color if it was highlighted by keyboard
                if button.colour == (150, 150, 255):
                    button.colour = button.default_colour
        
        # Draw all buttons
        for button in self.buttons:
            button.draw()

    def handle_play_button(self):
        self.scene_manager.change_scene("game")

    def handle_settings_button(self):
        self.scene_manager.change_scene("settings")

    def handle_exit_button(self):
        self.scene_manager.shutdown()