import pygame
import buttons

class Menu:
    def __init__(self, RES, WINDOW_SIZE):
        start_image = pygame.image.load('images/menu/button1.png')
        start_image = pygame.transform.scale(start_image,
            (63, 32))
        settings_image = pygame.image.load('images/menu/button2.png')
        settings_image = pygame.transform.scale(settings_image,
            (63, 32))
        quit_image = pygame.image.load('images/menu/button3.png')
        quit_image = pygame.transform.scale(quit_image,
            (63, 32))

        start_button = buttons.Button([20, 5], start_image, RES, WINDOW_SIZE, 'start')
        settings_button = buttons.Button([20, 45], settings_image, RES, WINDOW_SIZE, 'settings')
        quit_button = buttons.Button([20, 85], quit_image, RES, WINDOW_SIZE, 'quit')
        
        self.button_list = [
            start_button, 
            settings_button, 
            quit_button
            ]

    def render_buttons(self, surf, mpos, starts, mouse_button_up):
        for button in self.button_list:
            starts = button.process_button(surf, mpos, starts, mouse_button_up)
        return starts