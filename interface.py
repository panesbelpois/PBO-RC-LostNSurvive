import pygame

def draw_text(screen, font, text, x, y, color=(255, 255, 255), with_button=False, center_x=False):
    text_width, text_height = font.size(text)

    if center_x:
        text_x = x - text_width // 2
    else:
        text_x = x

    if with_button:
        button_width = text_width + 30
        button_height = text_height + 15

        button_bg_color = (150, 80, 20)
        button_border_color = (200, 140, 50)

        if center_x:
            button_x = x - button_width // 2
        else:
            button_x = x - 15

        button_rect = pygame.Rect(button_x, y - 8, button_width, button_height)
        pygame.draw.rect(screen, button_bg_color, button_rect, border_radius=5)
        pygame.draw.rect(screen, button_border_color, button_rect, 2, border_radius=5)

        screen.blit(font.render(text, True, color), (text_x, y))
    else:
        rendered = font.render(text, True, color)
        screen.blit(rendered, (text_x, y))

    if with_button:
        return button_width, button_height
    return 0, 0


def draw_multi_line_text(screen, font, text, x, y, color=(255, 255, 255), with_button=False, center_x=False, line_spacing=30):
    lines = text.split('\n')

    if with_button:
        max_width = max(font.size(line)[0] for line in lines)
        button_height = (len(lines) * line_spacing) + 20
        button_width = max_width + 40
        button_x = x - button_width // 2 if center_x else x - 20
        button_rect = pygame.Rect(button_x, y - 15, button_width, button_height)
        pygame.draw.rect(screen, (150, 80, 20), button_rect, border_radius=5)
        pygame.draw.rect(screen, (200, 140, 50), button_rect, 2, border_radius=5)

    current_y = y
    for line in lines:
        draw_text(screen, font, line, x, current_y, color, center_x=center_x)
        current_y += line_spacing



def draw_story_scene(screen, font, scene_text, background_image, screen_width, screen_height):
    screen.blit(background_image, (0, 0))

    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))

    text_x = screen_width // 2
    text_y = screen_height // 2 - 50

    text_width = font.size(scene_text)[0]
    button_width = text_width + 40
    button_height = 60
    button_x = text_x - button_width // 2
    button_y = text_y - 15

    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, (150, 80, 20), button_rect, border_radius=5)
    pygame.draw.rect(screen, (200, 140, 50), button_rect, 2, border_radius=5)

    draw_text(screen, font, scene_text, text_x, text_y, center_x=True)

    continue_text = "Tekan [SPACE] untuk lanjut..."
    continue_width = font.size(continue_text)[0]
    continue_button_width = continue_width + 40
    continue_button_x = text_x - continue_button_width // 2
    continue_button_y = text_y + 70

    continue_rect = pygame.Rect(continue_button_x, continue_button_y, continue_button_width, 50)
    pygame.draw.rect(screen, (150, 80, 20), continue_rect, border_radius=5)
    pygame.draw.rect(screen, (200, 140, 50), continue_rect, 2, border_radius=5)

    draw_text(screen, font, continue_text, text_x, continue_button_y + 15, center_x=True)

def draw_choices(screen, font, screen_width, screen_height):
    menu_width = 500
    menu_height = 350
    menu_x = (screen_width - menu_width) // 2
    menu_y = (screen_height - menu_height) // 2

    s = pygame.Surface((menu_width, menu_height))
    s.fill((80, 30, 20))
    screen.blit(s, (menu_x, menu_y))

    title_y = menu_y + 50
    draw_text(screen, font, "Apa yang ingin kamu lakukan?", screen_width // 2, title_y, center_x=True)

    button1_y = title_y + 60
    button2_y = button1_y + 60
    button3_y = button2_y + 60

    draw_text(screen, font, "[1] Mulai perjalanan", screen_width // 2, button1_y, with_button=True, center_x=True)
    draw_text(screen, font, "[2] Cek status kru", screen_width // 2, button2_y, with_button=True, center_x=True)
    draw_text(screen, font, "[3] Lihat inventaris", screen_width // 2, button3_y, with_button=True, center_x=True)

    instruction_y = button3_y + 60
    draw_text(screen, font, "Tekan angka 1/2/3 untuk memilih.", screen_width // 2, instruction_y, center_x=True)


def draw_event_box(screen, font, event_text, screen_width, screen_height):
    if not event_text:
        return

    lines = event_text.split('\n')
    max_line_width = max(font.size(line)[0] for line in lines)

    event_width = max(500, min(screen_width - 100, max_line_width + 60))
    event_height = 60 if len(lines) == 1 else 100

    event_x = (screen_width - event_width) // 2
    event_y = screen_height - event_height - 50

    s = pygame.Surface((event_width, event_height))
    s.set_alpha(230)
    s.fill((80, 30, 20))
    screen.blit(s, (event_x, event_y))

    pygame.draw.rect(screen, (200, 140, 50), pygame.Rect(event_x, event_y, event_width, event_height), 2, border_radius=8)

    text_y = event_y + 15
    line_spacing = 35

    for i, line in enumerate(lines):
        draw_text(screen, font, line, screen_width // 2, text_y + (i * line_spacing), center_x=True)


def draw_dead_crew_list(screen, font, wagon, screen_width):
    if not wagon.dead_crew_list:
        return

    padding = 10
    line_height = font.get_height() + 5
    title_height = line_height
    content_height = len(wagon.dead_crew_list) * line_height
    box_height = padding * 2 + title_height + content_height
    box_width = 300
    box_x = screen_width - box_width - 20
    box_y = 20

    s = pygame.Surface((box_width, box_height))
    s.set_alpha(200)
    s.fill((60, 20, 20))
    screen.blit(s, (box_x, box_y))

    pygame.draw.rect(screen, (120, 50, 50), pygame.Rect(box_x, box_y, box_width, box_height), 2, border_radius=5)

    draw_text(screen, font, "Dead Crew", box_x + padding, box_y + padding, color=(255, 200, 200))

    for i, crew in enumerate(wagon.dead_crew_list):
        line_y = box_y + padding + title_height + i * line_height
        draw_text(screen, font, f"- {crew.nama}", box_x + padding + 10, line_y, color=(255, 200, 200))