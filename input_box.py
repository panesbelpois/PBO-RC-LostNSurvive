import pygame

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('gray')
        self.color_active = pygame.Color('pink')
        self.color = self.color_inactive
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return self.text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

def draw_add_crew_input_box(screen, font, user_input):
    box_width = 400
    box_height = 200
    box_x = (screen.get_width() - box_width) // 2
    box_y = (screen.get_height() - box_height) // 2

    pygame.draw.rect(screen, (80, 30, 20), (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, (200, 140, 50), (box_x, box_y, box_width, box_height), 3)

    draw_text(screen, font, "Masukkan nama kru pertama:", box_x + 20, box_y + 30)
    draw_text(screen, font, user_input, box_x + 20, box_y + 80, color=(255, 255, 0))

def draw_text(screen, font, text, x, y, color=(255, 255, 255)):
    text_surf = font.render(text, True, color)
    screen.blit(text_surf, (x, y))
