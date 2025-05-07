import pygame
import random
from event import Event
from wagon import Wagon
from crew import Crew
from interface import draw_text, draw_choices, draw_story_scene, draw_dead_crew_list, draw_event_box

pygame.init()

font = pygame.font.SysFont("Arial", 26, bold=True)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Wagon Adventure")

background_img = pygame.image.load("LNS_BG_TRY_2.png").convert()
background_img = pygame.transform.scale(background_img, (1000, 600))

story_backgrounds = [
    pygame.image.load("BACKGROUND_OPENING_TRY.png").convert()
]
for i in range(3):
    if i >= len(story_backgrounds):
        story_backgrounds.append(story_backgrounds[0])
        
for i in range(len(story_backgrounds)):
    story_backgrounds[i] = pygame.transform.scale(story_backgrounds[i], (1000, 600))

wagon_frames = [
    pygame.transform.scale(pygame.image.load("WAGON_IMUT_TRY.png").convert_alpha(), (150, 100)),
    pygame.transform.scale(pygame.image.load("WAGON_IMUT_TRY_1.png").convert_alpha(), (150, 100)),
    pygame.transform.scale(pygame.image.load("WAGON_IMUT_TRY_2.png").convert_alpha(), (150, 100))
]
wagon_frame_index = 0
frame_count = 0
frame_delay = 10

screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

new_width = screen_width


my_wagon = Wagon()
my_wagon.crew_list.append(Crew("Lelouch", 50, 50, 10, 100))
my_wagon.crew_list.append(Crew("Light Yagami", 50, 50, 8, 100, "Hipotermia"))

available_names = ["Ibrahim", "Anisah", "Abel", "Ardi"]

game_event = Event()

story_scenes = [
    "YOU'RE LOST! Tiba-tiba kamu terbangun di wilayah misterius..",
    "Kamu harus berjalan menuju tempat dengan pemukiman terdekat,",
    "Kamu akan berkelana bersama dengan orang-orang yang bernasib sama sepertimu",
    "Kereta tua dengan kuda yang terlihat mencolok..",
    "menjadi satu-satunya harapan perjalanan kalian."
]
current_scene = 0
show_story = True
show_choices = False
show_crew_status = False
show_event_message = False
show_dead_crew = True 
story_completed = False
game_started = False

current_event_message = ""
status_message = ""
status_timer = 0
STATUS_DISPLAY_TIME = 120

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x and show_event_message:
                show_event_message = False
                
            elif show_story:
                if event.key == pygame.K_SPACE:
                    current_scene += 1
                    if current_scene >= len(story_scenes):
                        show_story = False
                        show_choices = True
                        story_completed = True
            elif show_choices:
                if event.key == pygame.K_1:
                    result = my_wagon.berjalan()
                    show_choices = False
                    game_started = True
                    status_message = "Perjalanan dimulai!"
                    status_timer = STATUS_DISPLAY_TIME
                elif event.key == pygame.K_2:
                    show_crew_status = not show_crew_status
                    status_message = "Menampilkan status kru" if show_crew_status else "Menyembunyikan status kru"
                    status_timer = STATUS_DISPLAY_TIME
                elif event.key == pygame.K_3:
                    status_message = "Melihat inventaris"
                    status_timer = STATUS_DISPLAY_TIME
            else:
                if event.key == pygame.K_SPACE:
                    result = my_wagon.berjalan()
                    status_message = result
                    status_timer = STATUS_DISPLAY_TIME
                elif event.key == pygame.K_s:
                    result = my_wagon.berhenti()
                    status_message = result
                    status_timer = STATUS_DISPLAY_TIME
                elif event.key == pygame.K_e:
                    current_event_message = game_event.process_event(my_wagon)
                    show_event_message = True
                elif event.key == pygame.K_d: 
                    if len(my_wagon.crew_list) > 0:
                        current_event_message = game_event.trigger_death_event(my_wagon)
                        show_event_message = True
                    else:
                        status_message = "Tidak ada kru yang tersisa!"
                        status_timer = STATUS_DISPLAY_TIME
                elif event.key == pygame.K_a:
                    if len(my_wagon.crew_list) < my_wagon.capacity:
                        if available_names:
                            name = random.choice(available_names)
                            available_names.remove(name)
                            
                            new_crew = Crew(name, hunger=50, thirst=50, attack=10, health=100)
                            success, message = my_wagon.add_crew(new_crew)
                            status_message = message
                        else:
                            status_message = "Tidak ada lagi kru yang tersedia!"
                        status_timer = STATUS_DISPLAY_TIME
                    else:
                        status_message = "Kru sudah penuh! (Maks. 5)"
                        status_timer = STATUS_DISPLAY_TIME
                elif event.key == pygame.K_m:
                    show_choices = True
                elif event.key == pygame.K_1:
                    result = my_wagon.berjalan()
                    status_message = result
                    status_timer = STATUS_DISPLAY_TIME
                elif event.key == pygame.K_2:
                    show_crew_status = not show_crew_status
                    status_message = "Menampilkan status kru" if show_crew_status else "Menyembunyikan status kru"
                    status_timer = STATUS_DISPLAY_TIME
                elif event.key == pygame.K_3:
                    status_message = "Melihat inventaris"
                    status_timer = STATUS_DISPLAY_TIME
                elif event.key == pygame.K_g:
                    show_dead_crew = not show_dead_crew
                    status_message = "Menampilkan kru yang mati" if show_dead_crew else "Menyembunyikan kru yang mati"
                    status_timer = STATUS_DISPLAY_TIME

    if status_timer > 0:
        status_timer -= 1

    if show_story:
        scene_text = story_scenes[current_scene % len(story_scenes)]
        background_image = story_backgrounds[current_scene % len(story_backgrounds)]
        draw_story_scene(screen, font, scene_text, background_image, screen_width, screen_height)

        background_index = current_scene % len(story_backgrounds)
        draw_story_scene(screen, font, scene_text, background_image, screen_width, screen_height)

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
            
            continue_text = "Tekan [SPACE] untuk lanjut..."
            draw_text(screen, font, continue_text, screen_width // 2, 500, center_x=True)
            draw_text(screen, font, "Status: Berjalan", 30, 80, with_button=True)
            draw_text(screen, font, "Status: Berjalan", 30, 80, with_button=True)
            draw_text(screen, font, f"Posisi Wagon: {my_wagon.position} km", 30, 30, with_button=True)

            
            if show_crew_status:
                y_offset = 130
                draw_text(screen, font, "Status Kru:", 30, y_offset, with_button=True)
                if len(my_wagon.crew_list) == 0:
                    draw_text(screen, font, "Tidak ada kru yang hidup!", 30, y_offset + 50, with_button=True)
                else:
                    for i, c in enumerate(my_wagon.crew_list):
                        draw_text(screen, font, f"{c.nama} - HP: {c.hp} - Status: {c.status}", 30, y_offset + 50 + i * 50, with_button=True)
            
            if show_dead_crew and my_wagon.dead_crew_list:
                draw_dead_crew_list(screen, font, my_wagon, screen_width)
                
            draw_text(screen, font, "Tekan [M] untuk menu atau 1/2/3 untuk aksi cepat", screen_width // 2, 540, (255, 255, 255), with_button=True, center_x=True)
    
    if show_event_message:
        draw_event_box(screen, font, current_event_message, screen_width, screen_height)
    
    if status_timer > 0:
        alpha = min(255, status_timer * 2)
        text_width = font.size(status_message)[0]
        
        msg_rect = pygame.Rect(screen_width//2 - (text_width + 40)//2, 200, text_width + 40, 50)
        s = pygame.Surface((text_width + 40, 50))
        s.set_alpha(alpha)
        s.fill((150, 80, 20))
        screen.blit(s, (screen_width//2 - (text_width + 40)//2, 200))
        
        pygame.draw.rect(screen, (200, 140, 50), msg_rect, 2, border_radius=8)
        
        draw_text(screen, font, status_message, screen_width//2, 213, (255, 255, 255), center_x=True)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()