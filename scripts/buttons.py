from email.mime import image
import pygame, sys

class Button:
    def __init__(self, pos, image, RES, WINDOW_SIZE, type):
        self.type = type
        self.pos = pos
        self.x_diff = WINDOW_SIZE[0]/RES[0]
        self.y_diff = WINDOW_SIZE[1]/RES[1]
        self.rect = pygame.Rect(pos[0], pos[1], 64, 32)
        self.image = image
        self.pressed_image = pygame.transform.scale(self.image, (32, 16))
        self.pressed_down = False

    def process_button(self, surf, mpos, starts, mouse_button_up):
        image = self.image
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        if pygame.mouse.get_pressed()[0]:
            if self.rect.colliderect((mpos[0]/self.x_diff, mpos[1]/self.y_diff, 1, 1)):
                image = self.pressed_image
                self.rect.x = self.pos[0] + self.rect.width/4
                self.rect.y = self.pos[1] + self.rect.height/4
                self.pressed_down = True
        if mouse_button_up and self.pressed_down:
            match self.type:
                case 'start':
                    starts['game'] = True
                    starts['menu'] = False
                case 'settings':
                    self.pressed_down = False
                case 'quit':
                    pygame.quit()
                    sys.exit()

        surf.blit(image, (self.rect.x, self.rect.y))

        return starts

