import pygame
import random
from event import Event
from wagon import Wagon
from crew import Crew
from interface import draw_text, draw_choices, draw_story_scene, draw_dead_crew_list, draw_event_box
from input_box import InputBox
from battle import Battle, Character

pygame.init()

font = pygame.font.SysFont("Arial", 26, bold=True)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000, 600))

background_img = pygame.image.load("assets/LNS_BG_TRY_2.png").convert()
background_img = pygame.transform.scale(background_img, (1000, 600))
battle_background = pygame.image.load('assets/battle_bg.png').convert()
battle_background = pygame.transform.scale(battle_background, (1000, 600))
story_backgrounds = [pygame.image.load("assets/BACKGROUND_OPENING_TRY.png").convert()]
story_backgrounds = [pygame.transform.scale(bg, (1000, 600)) for bg in story_backgrounds * 3]
enemy_image = pygame.image.load("assets/battle_enemy.png").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (200, 200))

wagon_frames = [
    pygame.transform.scale(pygame.image.load("assets/WAGON_IMUT_TRY.png").convert_alpha(), (150, 100)),
    pygame.transform.scale(pygame.image.load("assets/WAGON_IMUT_TRY_1.png").convert_alpha(), (150, 100)),
    pygame.transform.scale(pygame.image.load("assets/WAGON_IMUT_TRY_2.png").convert_alpha(), (150, 100))
]
wagon_frame_index = 0
frame_count = 0
frame_delay = 10

screen_width = 1000
screen_height = 600
input_box = InputBox((screen_width - 200) // 2, (screen_height - 50) // 2 + 20, 200, 50)
show_input_box = False
result = None
input_result = None

my_wagon = Wagon()
game_event = Event()

story_scenes = [
    "YOU'RE LOST! Tiba-tiba kamu terbangun di wilayah misterius..",
    "Kamu harus berjalan menuju tempat dengan pemukiman terdekat,",
    "Kamu akan berkelana bersama dengan orang-orang yang bernasib sama sepertimu",
    "Kereta tua dengan kuda yang terlihat mencolok..",
    "menjadi satu-satunya harapan perjalanan kalian."
]

show_story = True
show_choices = False
show_crew_status = False
show_event_message = False
show_dead_crew = True
story_completed = False
game_started = False
in_battle = False
current_battle = None
current_event_message = ""
status_message = ""
status_timer = 0
STATUS_DISPLAY_TIME = 120
displayed_text = ""
char_index = 0
current_scene = 0
CHAR_DELAY = 30
last_char_time = pygame.time.get_ticks()

def draw_battle_scene(screen, font, battle):
    screen.blit(battle_background, (0, 0))
    for crew in battle.player_crew:
        pygame.draw.rect(screen, (100, 100, 100), (crew.x, crew.y, crew.width, crew.height))
        draw_text(screen, font, crew.name, crew.x + 5, crew.y - 20, (255, 255, 255))
        draw_text(screen, font, f'HP: {crew.hp}', crew.x + 5, crew.y + crew.height + 5, (255, 255, 255))
    screen.blit(enemy_image, (battle.enemy_x, battle.enemy_y))
    draw_text(screen, font, f'Enemy HP: {battle.enemy_hp}', battle.enemy_x, battle.enemy_y - 20, (255, 0, 0))

def start_battle(crew_list):
    battle_characters = [Character(crew.nama, crew.hp, crew.attack, original_crew=crew) for crew in crew_list]
    battle = Battle(battle_characters, enemy_hp=100, enemy_attack=10)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if battle.crew_selection_phase:
                    for i, crew in enumerate(battle.all_crew):
                        crew_rect = pygame.Rect(100 + i*150, 400, 100, 100)
                        if crew_rect.collidepoint(mouse_pos):
                            battle.select_crew(crew)
                    if len(battle.player_crew) > 0: 
                        start_button = pygame.Rect(350, 550, 200, 50)
                        if start_button.collidepoint(mouse_pos):
                            battle.start_battle()
                else:
                    for crew in battle.player_crew:
                        crew_rect = pygame.Rect(int(crew.x), int(crew.y), crew.width, crew.height)
                        if crew_rect.collidepoint(mouse_pos):
                            battle.select_crew(crew)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not battle.crew_selection_phase:
                    battle.shoot()

                if not battle.crew_selection_phase and battle.selected_crew:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        battle.selected_crew.target_x -= 10
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        battle.selected_crew.target_x += 10
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        battle.selected_crew.target_y -= 10
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        battle.selected_crew.target_y += 10

                    battle.selected_crew.target_x = max(50, min(battle.selected_crew.target_x, 500))
                    battle.selected_crew.target_y = max(100, min(battle.selected_crew.target_y, 450))

        keys = pygame.key.get_pressed()
        if battle.selected_crew is not None:
            battle.handle_movement_input(keys)
            battle.update()

        screen.fill((0, 0, 0))
        if battle.crew_selection_phase:
            battle.draw(screen)
        else:
            battle.draw_battle_scene(screen, font)

        if battle.battle_finished:
            running = False

        pygame.display.flip()
        clock.tick(60)

    for c in crew_list:
        for b in battle.player_crew:
            if c.nama == b.nama:
                c.hp = b.hp
                c.is_dead = b.is_dead 

    return battle.battle_won

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if show_input_box:
            input_result = input_box.handle_event(event)
            if input_result:
                if len(my_wagon.crew_list) < my_wagon.capacity:
                    new_crew = Crew(input_result, 50, 50, random.randint(5, 10), 100)
                    my_wagon.crew_list.append(new_crew)
                    status_message = f"{input_result} telah ditambahkan ke kru!"
                    show_input_box = False
                    status_timer = STATUS_DISPLAY_TIME
                else:
                    status_message = "Kru sudah penuh! (Maks. 5)"
                    show_input_box = False
                    status_timer = STATUS_DISPLAY_TIME
            continue

        if event.type == pygame.KEYDOWN:
            if show_story:
                if event.key == pygame.K_SPACE:
                    if char_index < len(story_scenes[current_scene]):
                        displayed_text = story_scenes[current_scene]
                        char_index = len(displayed_text)
                    else:
                        current_scene += 1
                        if current_scene >= len(story_scenes):
                            show_story = False
                            show_input_box = True
                            input_box.text = ""
                            input_box.active = True
                            input_box.color = input_box.color_active
                            input_box.txt_surface = pygame.font.Font(None, 32).render("", True, input_box.color)
                            story_completed = True
                        else:
                            displayed_text = ""
                            char_index = 0
                            last_char_time = pygame.time.get_ticks()
            else:
                if event.key == pygame.K_n or event.key == pygame.K_a:
                    if len(my_wagon.crew_list) < my_wagon.capacity:
                        show_input_box = True
                        input_box.text = ""
                        input_box.active = True
                        input_box.color = input_box.color_active
                        input_box.txt_surface = pygame.font.Font(None, 32).render("", True, input_box.color)
                    else:
                        status_message = "Kru sudah penuh! (Maks. 5)"
                        status_timer = STATUS_DISPLAY_TIME

                elif event.key == pygame.K_x and show_event_message:
                    show_event_message = False
                    if in_battle:
                        in_battle = False
                        current_battle = None

                elif event.key == pygame.K_1:
                    result = my_wagon.berjalan()
                    status_message = "Perjalanan dimulai!" if not game_started else result
                    game_started = True
                    status_timer = STATUS_DISPLAY_TIME
                    show_choices = False

                elif event.key == pygame.K_2:
                    show_crew_status = not show_crew_status
                    status_message = "Menampilkan status kru" if show_crew_status else "Menyembunyikan status kru"
                    status_timer = STATUS_DISPLAY_TIME

                elif event.key == pygame.K_3:
                    status_message = "Melihat inventaris"
                    status_timer = STATUS_DISPLAY_TIME

                elif event.key == pygame.K_SPACE:
                    if in_battle and current_battle:
                        current_battle.crew_attack()
                        if current_battle.battle_finished:
                            in_battle = False
                            current_battle = None
                    else:
                        result = my_wagon.berjalan()
                        status_message = result
                        status_timer = STATUS_DISPLAY_TIME

                elif event.key == pygame.K_s:
                    result = my_wagon.berhenti()
                    status_message = result
                    status_timer = STATUS_DISPLAY_TIME

                elif event.key == pygame.K_e:
                    current_event_message = game_event.process_event(my_wagon)
                    if "musuh" in current_event_message.lower():
                        in_battle = True
                        is_battle_won = start_battle(my_wagon.crew_list)
                    show_event_message = True

                elif event.key == pygame.K_d:
                    if len(my_wagon.crew_list) > 0:
                        current_event_message = game_event.trigger_death_event(my_wagon)
                        show_event_message = True
                    else:
                        status_message = "Tidak ada kru yang tersisa!"
                        status_timer = STATUS_DISPLAY_TIME

                elif event.key == pygame.K_m:
                    show_choices = True

                elif event.key == pygame.K_g:
                    show_dead_crew = not show_dead_crew
                    status_message = "Menampilkan kru yang mati" if show_dead_crew else "Menyembunyikan kru yang mati"
                    status_timer = STATUS_DISPLAY_TIME

    if status_timer > 0:
        status_timer -= 1

    if show_story:
        screen.blit(story_backgrounds[0], (0, 0))
        now = pygame.time.get_ticks()
        if char_index < len(story_scenes[current_scene]) and now - last_char_time >= CHAR_DELAY:
            displayed_text += story_scenes[current_scene][char_index]
            char_index += 1
            last_char_time = now

        for i in range(current_scene + 1):
            draw_text(screen, font,
                      displayed_text if i == current_scene else story_scenes[i],
                      screen_width // 2, 150 + i * 40, (255, 255, 255), center_x=True)
        draw_text(screen, font, "Tekan [SPACE] untuk lanjut...", screen_width // 2, 500, (255, 255, 255), center_x=True)

    else:
        screen.blit(background_img, (0, 0))

        if show_choices:
            draw_choices(screen, font, screen_width, screen_height)
            if game_started:
                screen.blit(wagon_frames[wagon_frame_index], (750, 350))
        else:
            if my_wagon.is_moving:
                frame_count += 1
                if frame_count >= frame_delay:
                    frame_count = 0
                    wagon_frame_index = (wagon_frame_index + 1) % len(wagon_frames)
            else:
                wagon_frame_index = 0
            screen.blit(wagon_frames[wagon_frame_index], (750, 350))

            draw_text(screen, font, f"Status: {my_wagon.status.capitalize()}", 30, 80, with_button=True)
            draw_text(screen, font, f"Posisi Wagon: {my_wagon.position} km", 30, 30, with_button=True)
            draw_text(screen, font, "Tekan [SPACE] untuk lanjut...", screen_width // 2, 500, center_x=True)

            if show_crew_status:
                status_width = 400
                status_height = 300
                status_x = (screen_width - status_width) // 2
                status_y = (screen_height - status_height) // 2

                s = pygame.Surface((status_width, status_height))
                s.set_alpha(230)
                s.fill((100, 50, 20))
                screen.blit(s, (status_x, status_y))

                pygame.draw.rect(
                    screen,
                    (180, 130, 80),
                    pygame.Rect(status_x, status_y, status_width, status_height),
                    3,
                    border_radius=10
                )

                draw_text(screen, font, "Status Kru", status_x + status_width//2, status_y + 20, (255, 255, 255), center_x=True)

                if len(my_wagon.crew_list) == 0:
                    draw_text(screen, font, "Tidak ada kru yang hidup!", status_x + status_width//2, status_y + 120, (255, 200, 200), center_x=True)
                else:
                    for i, c in enumerate(my_wagon.crew_list):
                        crew_y = status_y + 70 + i * 40
                        pygame.draw.rect(
                            screen,
                            (120, 60, 30),
                            pygame.Rect(status_x + 20, crew_y, status_width - 40, 30),
                            0,
                            border_radius=5
                        )
                        draw_text(screen, font, f"{c.nama} - HP: {c.hp} - Status: {c.status}",
                                status_x + status_width//2, crew_y + 0, (255, 255, 255), center_x=True)

                draw_text(screen, font, "Tekan [2] untuk menutup", status_x + status_width//2,
                         status_y + status_height - 40, (200, 200, 200), center_x=True)
                pass

            if show_dead_crew and my_wagon.dead_crew_list:
                draw_dead_crew_list(screen, font, my_wagon, screen_width)

            draw_text(screen, font, "Tekan [M] untuk menu atau 1/2/3 untuk aksi cepat", screen_width // 2, 540, (255, 255, 255), with_button=True, center_x=True)

    if show_event_message:
        if in_battle and current_battle:
            current_battle.draw_battle_scene(screen, font)
        else:
            draw_event_box(screen, font, current_event_message, screen_width, screen_height)

    if status_timer > 0:
        alpha = min(255, status_timer * 2)
        text_width = font.size(status_message)[0]
        msg_rect = pygame.Rect(screen_width//2 - (text_width + 40)//2, 200, text_width + 40, 50)
        s = pygame.Surface((text_width + 40, 50))
        s.set_alpha(alpha)
        s.fill((150, 80, 20))
        screen.blit(s, msg_rect.topleft)
        pygame.draw.rect(screen, (200, 140, 50), msg_rect, 2, border_radius=8)
        draw_text(screen, font, status_message, screen_width//2, 213, (255, 255, 255), center_x=True)

    if show_input_box:
        bg_rect = pygame.Rect(screen_width // 2 - 220, screen_height // 2 - 70, 440, 140)
        pygame.draw.rect(screen, (100, 50, 20), bg_rect, border_radius=12)
        pygame.draw.rect(screen, (180, 130, 80), bg_rect, 3, border_radius=12)
        draw_text(screen, font, "Masukkan nama anggota kru:", screen_width // 2, screen_height // 2 - 45, (255,255,255), center_x=True)
        input_box.update()
        input_box.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()