import pygame
from src.Graphics.Elements.text_button import TextButton
from src.Graphics.Elements.image_button import ImageButton
from src.Scenes.scene import Scene
from src.scene_manager import SceneManager

class MenuScene(Scene):
    def __init__(self, scene_manager: SceneManager):
        super().__init__(scene_manager)

        self.selected_button = 0

        # self.buttons = [
        #     TextButton(self.scene_manager.screen, "Play", 100, 100, 100, 50, on_click=self.handle_play_button),
        #     TextButton(self.scene_manager.screen, "Settings", 100, 300, 100, 50, on_click=self.handle_settings_button),
        #     TextButton(self.scene_manager.screen, "Exit", 100, 500, 100, 50, on_click=self.handle_exit_button)
        # ]

        screen_width, screen_height = self.scene_manager.screen.get_size()

        button_x = 0.3 * screen_width
        button_y = screen_height / 2

        self.buttons = [
            ImageButton(self.scene_manager.screen, "resources/art/main_screen/play_button.png", "resources/art/main_screen/play_button_hovered.png", button_x, button_y - 50, 18, 18, on_click=self.handle_play_button),
            ImageButton(self.scene_manager.screen, "resources/art/main_screen/quit_button.png", "resources/art/main_screen/quit_button_hovered.png", button_x, button_y + 100, 18, 18, on_click=self.handle_exit_button)
        ]

        # get window size
        screen_width, screen_height = self.scene_manager.screen.get_size()

        background_image = pygame.image.load("resources/art/main_screen/main_screen_default copy.png")
        self.background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

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
        self.scene_manager.screen.blit(self.background_image, (0, 0))
        
        # Draw all buttons
        for button in self.buttons:
            button.draw()

    def handle_play_button(self):
        self.scene_manager.change_scene("game")

    def handle_settings_button(self):
        self.scene_manager.change_scene("settings")

    def handle_exit_button(self):
        self.scene_manager.shutdown()