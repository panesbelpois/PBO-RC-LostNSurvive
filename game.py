
import pygame
import random
from event import Event
from wagon import Wagon
from crew import Crew
from interface import draw_text, draw_choices, draw_story_scene, draw_dead_crew_list, draw_event_box
from input_box import InputBox
from battle import Battle, Character
import time
from crew_inherit import Chef, Hunter, Police, Infantry, Nurse, Doctor, Thief, Agent, Musician, Firefighter

def run_game():
    pygame.init()

    font_path = "joystix.ttf"
    font = pygame.font.Font(font_path, 15) 
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1000, 600))
    battle_background = pygame.image.load('battle_bg.png').convert()
    battle_background = pygame.transform.scale(battle_background, (1000, 600))
    story_backgrounds = [pygame.image.load("LNS_BG_TRY_2.png").convert()]
    story_backgrounds = [pygame.transform.scale(bg, (1000, 600)) for bg in story_backgrounds * 3]
    enemy_image = pygame.image.load("battle_enemy.png").convert_alpha()
    enemy_image = pygame.transform.scale(enemy_image, (200, 200))
    day = 1
    max_day = 3
    wagon_frames = [
        pygame.transform.scale(pygame.image.load("WAGON_IMUT_TRY.png").convert_alpha(), (150, 100)),
        pygame.transform.scale(pygame.image.load("WAGON_IMUT_TRY_1.png").convert_alpha(), (150, 100)),
        pygame.transform.scale(pygame.image.load("WAGON_IMUT_TRY_2.png").convert_alpha(), (150, 100))
    ]
    pygame.mixer.init()
    pygame.mixer.music.load("lns_bgm.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1) 
    wagon_frame_index = 0
    frame_count = 0
    frame_delay = 10

    avatar_animations = {
        "doctor": [
            pygame.image.load("doctor_walkingright.png").convert_alpha(),
            pygame.image.load("doctor_walkingleft.png").convert_alpha()
        ],
        "cowgirl": [
            pygame.image.load("cowgirl_walkingright.png").convert_alpha(),
            pygame.image.load("cowgirl_walkingleft.png").convert_alpha()
        ],
        "cowboy": [
            pygame.image.load("cowboy_walkingright.png").convert_alpha(),
            pygame.image.load("cowboy_walkingleft.png").convert_alpha()
        ],
        "chef": [
            pygame.image.load("chef_walkingright.png").convert_alpha(),
            pygame.image.load("chef_walkingleft.png").convert_alpha()
        ],
        "butcher": [
            pygame.image.load("butcher_walkingright.png").convert_alpha(),
            pygame.image.load("butcher_walkingleft.png").convert_alpha()
        ]
    }

    # Available avatar types for random selection
    available_avatar_types = ["doctor", "cowgirl", "cowboy", "chef", "butcher"]

    screen_width = 1000
    screen_height = 600
    input_box = InputBox((screen_width - 200) // 2, (screen_height - 50) // 2 + 20, 200, 50)
    show_input_box = False
    result = None
    input_result = None
    my_wagon = Wagon()
    game_event = Event()
    DAY_COLOR = (135, 206, 250) 
    NIGHT_COLOR = (25, 25, 112) 
    day_duration = 60
    night_duration = 15
    game_hour = 6
    start_time = time.time()
    speed_time = 12 / day_duration     
    speed_night = 12 / night_duration  
    is_day = True
    story_scenes = [
        "YOU'RE LOST! Tiba-tiba kamu terbangun di wilayah misterius..",
        "Kamu harus berjalan menuju tempat dengan pemukiman terdekat,",
        "Kamu akan berkelana bersama dengan orang-orang yang bernasib sama sepertimu",
        "Kereta tua dengan kuda yang terlihat mencolok..",
        "menjadi satu-satunya harapan perjalanan kalian."
    ]
    show_story = False
    show_choices = False
    show_crew_status = False
    show_event_message = False
    show_dead_crew = False
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
    battle_phase = None
    show_story_event = False
    current_story_event = None
    selected_option = None
    background_day = pygame.image.load("background_day.png").convert()
    background_day = pygame.transform.scale(background_day, (1600, 600))
    bg_scroll_x = 0 
    BG_SCROLL_SPEED = 2
    background_night = pygame.image.load("BACKGROUND_NIGHT.png").convert()
    background_night = pygame.transform.scale(background_night, (1000, 600))
    last_game_hour = game_hour
    show_inventory_menu = False
    selected_inventory_type = None 
    selected_inventory_index = 0
    km_per_day = 34
    km_per_hour = round((km_per_day / 12) * 2) / 2
    km_today = 0
    last_day = day
    last_hour = game_hour
    event_hours = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    last_event_hour = None
    selected_event_option = None
    active_event_data = None
    show_start_menu = True
    show_pause_menu = False
    game_over = False
    game_finished = False
    show_main_menu = False
    main_menu_rect = pygame.Rect(20, screen_height - 70, 100, 40) 
    main_menu_options = ["Lihat Status Kru", "Lihat Inventaris", "Lihat Kru Mati"]
    main_menu_option_rects = [
        pygame.Rect(20, screen_height - 75 - (i+1)*50, 220, 40) for i in range(len(main_menu_options))
    ]
    crew_classes = [Chef, Hunter, Police, Infantry, Nurse, Doctor, Thief, Agent, Musician, Firefighter]
    crew_anim_frame = 0
    crew_anim_delay = 30  # Slower animation for walking effect
    crew_anim_counter = 0
    show_pause_menu = False
    pause_for_event = False
    game_paused_time = 0
    last_pause_start = None 
    background_start_menu = pygame.image.load("background_start_menu.png").convert()
    background_start_menu = pygame.transform.scale(background_start_menu, (screen_width, screen_height))
    button_start_menu = pygame.image.load("button_start_menu.png").convert_alpha()
    judul_start_menu = pygame.image.load("judul_start_menu.png").convert_alpha()
    cursor_img = pygame.image.load("cursor.png").convert_alpha()
    cursor_img = pygame.transform.smoothscale(cursor_img, (40, 40)) 
    pygame.mouse.set_visible(False)
    next_arrow_img = pygame.image.load("next_arrow.png").convert_alpha()
    next_arrow_img = pygame.transform.smoothscale(next_arrow_img, (60, 60))  
    crew_bullet_img = pygame.image.load("crew_bullet.png").convert_alpha()
    crew_bullet_img = pygame.transform.smoothscale(crew_bullet_img, (30,304))
    enemy_bullet_img = pygame.image.load("enemy_bullet.png").convert_alpha()
    enemy_bullet_img = pygame.transform.smoothscale(enemy_bullet_img, (30, 30))
    game_over_img = pygame.image.load("game_over.png").convert_alpha()
    game_over_img = pygame.transform.scale(game_over_img, (1000, 600))

    def is_game_paused():
        """Check if game should be paused"""
        return (show_pause_menu or show_input_box or show_crew_status or 
                show_dead_crew or show_inventory_menu or show_event_message or 
                pause_for_event)

    def get_crew_animated_sprite(crew_name, frame_index=0):
        """Get animated sprite for crew member based on their assigned avatar type"""
        if not hasattr(crew_name, 'avatar_type'):
            # Assign random avatar type if not set
            avatar_type = random.choice(available_avatar_types)
            setattr(crew_name, 'avatar_type', avatar_type)
        else:
            avatar_type = crew_name.avatar_type
        
        return avatar_animations[avatar_type][frame_index % 2]

    def draw_crew_with_animation(screen, crew_list, x_offset=0, y_offset=0):
        """Draw crew members with walking animation"""
        global crew_anim_counter, crew_anim_frame, crew_anim_delay
        
        # Update animation frame
        crew_anim_counter += 1
        if crew_anim_counter >= crew_anim_delay:
            crew_anim_counter = 0
            crew_anim_frame = (crew_anim_frame + 1) % 2  # Toggle between 0 and 1
        
        # Draw each crew member with their animated sprite
        for i, crew in enumerate(crew_list):
            if not crew.is_dead:
                sprite = get_crew_animated_sprite(crew, crew_anim_frame)
                sprite = pygame.transform.scale(sprite, (60, 80))  # Resize to appropriate size
                x = x_offset + (i * 70)
                y = y_offset
                screen.blit(sprite, (x, y))

    def get_battle_avatar_frame(crew, frame_index, direction="right"):
        avatar_type = getattr(crew, "avatar_type", "cowboy")
        if direction == "left":
            return avatar_animations[avatar_type][1]
        else:
            return avatar_animations[avatar_type][0]
    
    def draw_start_menu(screen, font):
        screen.blit(background_start_menu, (0, 0))

        # Judul (diperkecil)
        judul_scaled = pygame.transform.smoothscale(judul_start_menu, (384, 256))
        judul_rect = judul_scaled.get_rect(center=(screen_width // 2, 160))
        screen.blit(judul_scaled, judul_rect)

        # Tombol start (di tengah bawah)
        button_width, button_height = 220, 220
        button_scaled = pygame.transform.smoothscale(button_start_menu, (button_width, button_height))
        button_x = screen_width // 2 - button_width // 2
        button_y = screen_height // 2 + 50  # Tengah agak bawah
        start_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        screen.blit(button_scaled, (button_x, button_y))

        # (Opsional) Tambahkan instruksi kecil di bawah tombol
        instruction_font = pygame.font.Font(font_path, 18)
        draw_text(screen, instruction_font, "Klik tombol START untuk memulai petualangan", screen_width//2, button_y + button_height + 30, (150, 150, 150), center_x=True)

        return start_button_rect

    def draw_battle_scene(screen, font, battle, color):
        screen.blit(battle_background, (0, 0))
        global crew_anim_frame, crew_anim_counter, crew_anim_delay

        bar_w = 200
        bar_h = 24
        margin = 12
        base_x = screen.get_width() - bar_w - 30
        base_y = screen.get_height() - 30

        max_enemy_hp = getattr(battle, "max_enemy_hp", 100)
        enemy_hp = getattr(battle, "enemy_hp", 100)
        hp_ratio = max(0, min(enemy_hp / max_enemy_hp, 1))
        pygame.draw.rect(screen, (60, 60, 60), (base_x, base_y - bar_h, bar_w, bar_h), border_radius=8)
        pygame.draw.rect(screen, (200, 50, 50), (base_x, base_y - bar_h, int(bar_w * hp_ratio), bar_h), border_radius=8)
        pygame.draw.rect(screen, (255, 255, 255), (base_x, base_y - bar_h, bar_w, bar_h), 2, border_radius=8)
        draw_text(screen, font, f"Musuh: {enemy_hp} / {max_enemy_hp}", base_x + bar_w // 2, base_y - bar_h + bar_h // 2 - 2, (255,255,255), center_x=True)

        for i, crew in enumerate(reversed(battle.player_crew)):
            max_hp = getattr(crew, "max_hp", 100)
            hp_ratio = max(0, min(crew.hp / max_hp, 1))
            y = base_y - bar_h * (i + 2) - margin * (i + 1)
            pygame.draw.rect(screen, (60, 60, 60), (base_x, y, bar_w, bar_h), border_radius=8)
            pygame.draw.rect(screen, (50, 200, 50), (base_x, y, int(bar_w * hp_ratio), bar_h), border_radius=8)
            pygame.draw.rect(screen, (255, 255, 255), (base_x, y, bar_w, bar_h), 2, border_radius=8)
            draw_text(screen, font, f"{crew.nama}: {crew.hp} / {max_hp}", base_x + bar_w // 2, y + bar_h // 2 - 2, (255,255,255), center_x=True)

        crew_anim_counter += 1
        if crew_anim_counter >= crew_anim_delay:
            crew_anim_counter = 0
            crew_anim_frame = (crew_anim_frame + 1) % 2

        for i, crew in enumerate(battle.player_crew):
            if not crew.is_dead:
                # Tentukan arah berdasarkan dx (atau pakai crew.current_direction jika ada)
                direction = crew.current_direction if hasattr(crew, "current_direction") else "right"
                sprite = get_battle_avatar_frame(crew, crew_anim_frame, direction)
                sprite = pygame.transform.scale(sprite, (80, 80))
                screen.blit(sprite, (crew.x, crew.y))
        
    def draw_event_choices(screen, font, event_data, selected_idx=None):
        box_width, box_height = 600, 220
        box_x = (screen.get_width() - box_width) // 2
        box_y = (screen.get_height() - box_height) // 2
        pygame.draw.rect(screen, (120, 60, 30), (box_x, box_y, box_width, box_height), border_radius=16)
        pygame.draw.rect(screen, (180, 130, 80), (box_x, box_y, box_width, box_height), 4, border_radius=16)

        draw_text(screen, font, event_data['deskripsi'], box_x + 30, box_y + 30, (255, 255, 255))

        for i, pilihan in enumerate(event_data['pilihan']):
            pilihan_rect = pygame.Rect(box_x + 60, box_y + 80 + i*60, 480, 45)
            color = (160, 90, 40) if selected_idx == i else (150, 75, 0)
            pygame.draw.rect(screen, color, pilihan_rect, border_radius=10)
            pygame.draw.rect(screen, (200, 140, 50), pilihan_rect, 2, border_radius=10)
            draw_text(screen, font, pilihan, pilihan_rect.centerx, pilihan_rect.centery - 10, (255,255,255), center_x=True)

    def start_battle(crew_list):
        battle_characters = [Character(crew.nama, crew.hp, crew.attack, original_crew=crew) for crew in crew_list]
        battle = Battle(battle_characters, enemy_hp=100, enemy_attack=10)

        global current_battle 
        current_battle = battle 

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
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

            if not battle.crew_selection_phase:
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
            
            # Handle start menu
            if show_start_menu:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    start_button_rect = draw_start_menu(screen, font)
                    if start_button_rect.collidepoint(mouse_pos):
                        show_start_menu = False
                        show_story = True
                        start_time = time.time()  # Reset start time when game actually starts
                continue
            
            if show_input_box:
                input_result = input_box.handle_event(event)
                if input_result:
                    if len(my_wagon.crew_list) < my_wagon.capacity:
                        crew_class = random.choice(crew_classes)
                        new_crew = crew_class(input_result)
                        # Assign random avatar type to new crew
                        new_crew.avatar_type = random.choice(available_avatar_types)
                        my_wagon.crew_list.append(new_crew)
                        status_message = f"{input_result} adalah {crew_class.__name__} dan telah ditambahkan ke kru!"
                        show_input_box = False
                        show_pause_menu = False
                        pause_for_event = False
                        status_timer = STATUS_DISPLAY_TIME
                        if last_pause_start is not None:
                            game_paused_time += time.time() - last_pause_start
                            last_pause_start = None
                    else:
                        status_message = "Kru sudah penuh! (Maks. 5)"
                        show_input_box = False
                        show_pause_menu = False
                        pause_for_event = False
                        status_timer = STATUS_DISPLAY_TIME
                        if last_pause_start is not None:
                            game_paused_time += time.time() - last_pause_start
                            last_pause_start = None
                continue
            
            if show_crew_status:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    show_crew_status = False
                    status_message = "Menutup status kru"
                    status_timer = STATUS_DISPLAY_TIME
                    if last_pause_start is not None:
                        game_paused_time += time.time() - last_pause_start
                        last_pause_start = None
                continue
            
            if show_dead_crew:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                    show_dead_crew = False
                    status_message = "Menyembunyikan kru yang mati"
                    status_timer = STATUS_DISPLAY_TIME
                    if last_pause_start is not None:
                        game_paused_time += time.time() - last_pause_start
                        last_pause_start = None
                continue
            
            if show_inventory_menu:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        show_inventory_menu = False
                        if last_pause_start is not None:
                            game_paused_time += time.time() - last_pause_start
                            last_pause_start = None
                    elif event.key == pygame.K_LEFT:
                        selected_inventory_type = "food"
                        selected_inventory_index = 0
                    elif event.key == pygame.K_RIGHT:
                        selected_inventory_type = "drink"
                        selected_inventory_index = 0
                    elif event.key == pygame.K_UP:
                        selected_inventory_index = max(0, selected_inventory_index - 1)
                    elif event.key == pygame.K_DOWN:
                        items = my_wagon.inventory.get(selected_inventory_type, [])
                        selected_inventory_index = min(len(items)-1, selected_inventory_index + 1)
                    elif event.key == pygame.K_RETURN:
                        items = my_wagon.inventory.get(selected_inventory_type, [])
                        if items:
                            item, restore = items[selected_inventory_index]
                            target_crew = None
                            for c in my_wagon.crew_list:
                                if c.hp < 100 and not c.is_dead:
                                    target_crew = c
                                    break
                            if target_crew:
                                target_crew.hp = min(100, target_crew.hp + restore)
                                status_message = f"{item} digunakan untuk {target_crew.nama} (+{restore} HP)"
                                del items[selected_inventory_index]
                                if selected_inventory_index >= len(items):
                                    selected_inventory_index = max(0, len(items)-1)
                            else:
                                status_message = "Semua kru sudah HP penuh!"
                            status_timer = STATUS_DISPLAY_TIME
                        else:
                            status_message = "Tidak ada item!"
                            status_timer = STATUS_DISPLAY_TIME
                continue
            
            if in_battle and current_battle:
                if battle_phase == 'crew_select':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        box_x, box_y, box_w, box_h = 100, 120, 800, 350
                        header_y = box_y + 60
                        for i, crew in enumerate(current_battle.all_crew):
                            row_y = header_y + 40 + i * 40
                            row_rect = pygame.Rect(box_x + 20, row_y - 10, box_w - 40, 36)
                            if row_rect.collidepoint(mouse_pos):
                                if crew in current_battle.player_crew:
                                    current_battle.remove_crew(crew)
                                else:
                                    current_battle.select_crew(crew)
                        start_button = pygame.Rect(
                            screen.get_width()//2 - 100, box_y + box_h - 60, 200, 45
                        )
                        if start_button.collidepoint(mouse_pos) and len(current_battle.player_crew) > 0:
                            current_battle.crew_selection_phase = False
                            current_battle.avatar_selection_phase = True
                            current_battle.selected_avatar_index = 0
                            for i, crew in enumerate(current_battle.player_crew):
                                crew.x = 100 + i*150
                                crew.y = 400
                                crew.target_x = crew.x
                                crew.target_y = crew.y
                            battle_phase = 'avatar_select'
                            
                elif battle_phase == 'avatar_select':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        # Modified to use new avatar system
                        for i, avatar_type in enumerate(available_avatar_types):
                            x = 150 + i * 150
                            y = 200
                            avatar_rect = pygame.Rect(x, y, 100, 100)
                            if avatar_rect.collidepoint(mouse_pos):
                                crew = current_battle.player_crew[current_battle.selected_avatar_index]
                                crew.avatar_type = avatar_type
                                crew.avatar = avatar_animations[avatar_type][0]  # Use first frame as default
                                current_battle.selected_avatar_index += 1
                                if current_battle.selected_avatar_index >= len(current_battle.player_crew):
                                    current_battle.avatar_selection_phase = False
                                    current_battle.selected_crew = current_battle.player_crew[0]
                                    battle_phase = 'battle'
                                break
                                
                elif battle_phase == 'battle':
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and current_battle.selected_crew:
                            current_battle.shoot()
                            if current_battle.battle_finished:
                                in_battle = False
                                current_battle = None
                                battle_phase = None
                                status_message = "Pertempuran selesai!"
                                status_timer = STATUS_DISPLAY_TIME
                continue
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                pause_btn_rect = pygame.Rect(screen_width - 120, screen_height - 60, 100, 40)
                if pause_btn_rect.collidepoint(mouse_pos):
                    if show_pause_menu:
                        show_pause_menu = False
                        if last_pause_start is not None:
                            game_paused_time += time.time() - last_pause_start
                            last_pause_start = None
                    else:
                        show_pause_menu = True
                        last_pause_start = time.time()
                    continue
                
            if event.type == pygame.MOUSEBUTTONDOWN and not show_story:
                mouse_pos = pygame.mouse.get_pos()
                if main_menu_rect.collidepoint(mouse_pos):
                    show_main_menu = not show_main_menu
                elif show_main_menu:
                    for i, rect in enumerate(main_menu_option_rects):
                        if rect.collidepoint(mouse_pos):
                            show_main_menu = False
                            if i == 0:
                                show_crew_status = True
                                last_pause_start = time.time()
                            elif i == 1:
                                show_inventory_menu = True
                                selected_inventory_type = "food"
                                selected_inventory_index = 0
                                last_pause_start = time.time()
                            elif i == 2:
                                show_dead_crew = True
                                last_pause_start = time.time()
                
            if show_pause_menu and not pause_for_event:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    pause_btn_rect = pygame.Rect(screen_width - 120, screen_height - 60, 100, 40)
                    if pause_btn_rect.collidepoint(mouse_pos):
                        show_pause_menu = False
                        if last_pause_start is not None:
                            game_paused_time += time.time() - last_pause_start
                            last_pause_start = None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        show_pause_menu = False
                        if last_pause_start is not None:
                            game_paused_time += time.time() - last_pause_start
                            last_pause_start = None
                continue
            
            if show_story:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if next_btn_rect.collidepoint(mouse_pos):
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
                                show_pause_menu = True
                                pause_for_event = True 
                                story_completed = True
                                last_pause_start = time.time()
                            else:
                                displayed_text = ""
                                char_index = 0
                                last_char_time = pygame.time.get_ticks()
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
                                show_pause_menu = True
                                pause_for_event = True 
                                story_completed = True
                                last_pause_start = time.time()
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
                            show_pause_menu = True
                            pause_for_event = True
                            last_pause_start = time.time() 
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
                        if not show_crew_status:
                            show_crew_status = True
                            last_pause_start = time.time()
                            status_message = "Menampilkan status kru"
                        else:
                            show_crew_status = False
                            if last_pause_start is not None:
                                game_paused_time += time.time() - last_pause_start
                                last_pause_start = None
                            status_message = "Menyembunyikan status kru"
                        status_timer = STATUS_DISPLAY_TIME

                    elif event.key == pygame.K_3:
                        show_inventory_menu = True
                        selected_inventory_type = "food"
                        selected_inventory_index = 0
                        status_message = ""
                        status_timer = 0
                        show_choices = False
                        last_pause_start = time.time()
                        inventory_text = "--- Inventaris Wagon ---\nMakanan:\n"
                        for item, restore in my_wagon.inventory.get("food", []):
                            inventory_text += f"- {item}: Memulihkan {restore} Hunger\n"
                        inventory_text += "\nMinuman:\n"
                        for item, restore in my_wagon.inventory.get("drink", []):
                            inventory_text += f"- {item}: Memulihkan {restore} Thirst\n"
                        status_message = inventory_text
                        status_timer = STATUS_DISPLAY_TIME * 2  

                    elif event.key == pygame.K_4:
                        reward_msg = my_wagon.quest_reward()
                        status_message = f"Reward didapatkan:\n{reward_msg}"
                        status_timer = STATUS_DISPLAY_TIME * 2

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
                            current_battle = Battle(
                                [Character(crew.nama, crew.hp, crew.attack, original_crew=crew) for crew in my_wagon.crew_list],
                                enemy_hp=100, enemy_attack=10,
                                crew_bullet_img=crew_bullet_img,
                                enemy_bullet_img=enemy_bullet_img
                            )
                            battle_phase = 'crew_select'
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
                        if not show_dead_crew:
                            show_dead_crew = True
                            last_pause_start = time.time()
                            status_message = "Menampilkan kru yang mati"
                        else:
                            show_dead_crew = False
                            if last_pause_start is not None:
                                game_paused_time += time.time() - last_pause_start
                                last_pause_start = None
                            status_message = "Menyembunyikan kru yang mati"
                        status_timer = STATUS_DISPLAY_TIME

                    elif event.key == pygame.K_p:
                        if not show_pause_menu:
                            show_pause_menu = True
                            last_pause_start = time.time()
                        else:
                            show_pause_menu = False
                            if last_pause_start is not None:
                                game_paused_time += time.time() - last_pause_start
                                last_pause_start = None

        if status_timer > 0:
            status_timer -= 1

        # Display start menu
        if show_start_menu:
            draw_start_menu(screen, font)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            screen.blit(cursor_img, (mouse_x, mouse_y))
            pygame.display.flip()
            clock.tick(60)
            continue

        if in_battle and current_battle:
            screen.fill((0, 0, 0))
            if battle_phase == 'crew_select':
                screen.fill((90, 60, 30))
                box_x, box_y, box_w, box_h = 100, 120, 800, 350
                pygame.draw.rect(screen, (120, 80, 40), (box_x, box_y, box_w, box_h), border_radius=18)
                pygame.draw.rect(screen, (180, 130, 80), (box_x, box_y, box_w, box_h), 4, border_radius=18)

                draw_text(screen, font, "Pilih Kru untuk Battle", screen.get_width()//2, box_y + 20, (255, 255, 255), center_x=True)

                header_y = box_y + 60
                col_x = [box_x + 40, box_x + 320, box_x + 520]
                draw_text(screen, font, "Nama", col_x[0], header_y, (255, 255, 0))
                draw_text(screen, font, "HP", col_x[1], header_y, (255, 255, 0))
                draw_text(screen, font, "Status", col_x[2], header_y, (255, 255, 0))

                for i, crew in enumerate(current_battle.all_crew):
                    row_y = header_y + 40 + i * 40
                    row_rect = pygame.Rect(box_x + 20, row_y - 10, box_w - 40, 36)
                    color = (160, 120, 60) if crew in current_battle.player_crew else (120, 80, 40)
                    pygame.draw.rect(screen, color, row_rect, border_radius=8)
                    pygame.draw.rect(screen, (180, 130, 80), row_rect, 2, border_radius=8)
                    draw_text(screen, font, crew.nama, col_x[0], row_y, (255, 255, 255))
                    draw_text(screen, font, str(crew.hp), col_x[1], row_y, (255, 255, 255))
                    draw_text(screen, font, "Dipilih" if crew in current_battle.player_crew else "Cadangan", col_x[2], row_y, (255, 255, 255))

                start_button = pygame.Rect(screen.get_width()//2 - 100, box_y + box_h - 60, 200, 45)
                pygame.draw.rect(screen, (120, 60, 30), start_button, border_radius=10)
                pygame.draw.rect(screen, (180, 130, 80), start_button, 3, border_radius=10)
                draw_text(screen, font, "Mulai Battle", start_button.centerx, start_button.centery, (255,255,255), center_x=True)
                
            elif battle_phase == 'avatar_select':
                screen.fill((60, 40, 20))
                draw_text(screen, font, "Pilih Avatar untuk " + current_battle.player_crew[current_battle.selected_avatar_index].nama, screen.get_width()//2, 100, (255, 255, 255), center_x=True)
                
                # Draw available avatar options
                for i, avatar_type in enumerate(available_avatar_types):
                    x = 150 + i * 150
                    y = 200
                    avatar_rect = pygame.Rect(x, y, 100, 100)
                    pygame.draw.rect(screen, (120, 80, 40), avatar_rect, border_radius=10)
                    pygame.draw.rect(screen, (180, 130, 80), avatar_rect, 3, border_radius=10)
                    
                    # Show preview of avatar (first frame)
                    preview_sprite = pygame.transform.scale(avatar_animations[avatar_type][0], (80, 80))
                    screen.blit(preview_sprite, (x + 10, y + 10))
                    
                    draw_text(screen, font, avatar_type.capitalize(), x + 50, y + 120, (255, 255, 255), center_x=True)
                
            elif battle_phase == 'battle':
                keys = pygame.key.get_pressed()
                current_battle.handle_movement_input(keys)
                current_battle.update()
                current_battle.draw_battle_scene(screen, font)
                if all(crew.is_dead for crew in current_battle.player_crew):
                    in_battle = False
                    current_battle = None
                    battle_phase = None
                    status_message = "Semua kru gugur! Battle berakhir."
                    status_timer = STATUS_DISPLAY_TIME
                elif current_battle.battle_finished:
                    if all(crew.is_dead for crew in current_battle.player_crew):
                        for c in my_wagon.crew_list:
                            for b in current_battle.player_crew:
                                if c.nama == b.nama:
                                    c.hp = b.hp
                                    c.is_dead = b.is_dead
                        in_battle = False
                        current_battle = None
                        battle_phase = None
                        status_message = "Semua kru gugur! Battle berakhir."
                        status_timer = STATUS_DISPLAY_TIME
                    elif current_battle.battle_finished:
                        for c in my_wagon.crew_list:
                            for b in current_battle.player_crew:
                                if c.nama == b.nama:
                                    c.hp = b.hp
                                    c.is_dead = b.is_dead
                        in_battle = False
                        current_battle = None
                        battle_phase = None
                        
                elif battle_phase == 'battle':
                    keys = pygame.key.get_pressed()
                    current_battle.handle_movement_input(keys)
                    current_battle.update()
                    current_battle.draw_battle_scene(screen, font)
                    if all(crew.is_dead for crew in current_battle.player_crew):
                        for c in my_wagon.crew_list:
                            for b in current_battle.player_crew:
                                if c.nama == b.nama:
                                    c.hp = b.hp
                                    c.is_dead = b.is_dead
                        in_battle = False
                        current_battle = None
                        battle_phase = None
                        status_message = "Semua kru gugur! Battle berakhir."
                        status_timer = STATUS_DISPLAY_TIME
                    elif current_battle.battle_finished:
                        for c in my_wagon.crew_list:
                            for b in current_battle.player_crew:
                                if c.nama == b.nama:
                                    c.hp = b.hp
                                    c.is_dead = b.is_dead
                        in_battle = False
                        current_battle = None
                        battle_phase = None
                
            mouse_x, mouse_y = pygame.mouse.get_pos()
            screen.blit(cursor_img, (mouse_x, mouse_y))
            pygame.display.flip()
            clock.tick(60)
            continue

        if show_story:
            screen.fill((100, 60, 30))  # warna coklat polos
            now = pygame.time.get_ticks()
            if char_index < len(story_scenes[current_scene]) and now - last_char_time >= CHAR_DELAY:
                displayed_text += story_scenes[current_scene][char_index]
                char_index += 1
                last_char_time = now

            for i in range(current_scene + 1):
                draw_text(screen, font,
                        displayed_text if i == current_scene else story_scenes[i],
                        screen_width // 2, 150 + i * 40, (255, 255, 255), center_x=True)

            # --- Tambahkan ini ---
            next_btn_size = 60
            next_btn_x = screen_width - next_btn_size - 30
            next_btn_y = screen_height - next_btn_size - 30
            next_btn_rect = pygame.Rect(next_btn_x, next_btn_y, next_btn_size, next_btn_size)
            screen.blit(next_arrow_img, (next_btn_x, next_btn_y))

        else:
            # Hitung waktu hanya jika game tidak di-pause
            if not is_game_paused():
                elapsed_time = time.time() - start_time - game_paused_time
            else:
                elapsed_time = time.time() - start_time - game_paused_time
                # Jika game sedang di-pause, gunakan waktu terakhir yang diketahui
                if last_pause_start is not None:
                    elapsed_time = last_pause_start - start_time - game_paused_time
            
            cycle_time = elapsed_time % (day_duration + night_duration)
            if cycle_time < day_duration:
                is_day = True
                wagon_moving = True and not is_game_paused()
                game_hour = int(6 + speed_time * cycle_time)
                if game_hour >= 18:
                    game_hour = 18
                screen.blit(background_day, (0, 0))
                
                if wagon_moving:
                    bg_scroll_x -= BG_SCROLL_SPEED
                    if bg_scroll_x < 0:
                        bg_scroll_x = 1600 - screen_width 
                else:
                    pass
                screen.blit(background_day, (0, 0), (int(bg_scroll_x), 0, screen_width, screen_height))
            else:
                is_day = False
                wagon_moving = False
                night_time = cycle_time - day_duration
                game_hour = int(18 + speed_night * night_time)
                if game_hour >= 24:
                    game_hour -= 24
                bg_scroll_x = 0
                screen.blit(background_night, (0, 0))

            # Update waktu game hanya jika tidak di-pause
            if not is_game_paused():
                if game_hour == 0 and last_game_hour != 0:
                    day += 1
                    if day > max_day:
                        day = max_day  
                last_game_hour = game_hour
                if game_hour in event_hours and last_event_hour != game_hour and is_day and not show_event_message:
                    event_data = game_event.trigger_event(game_hour)
                    if event_data:
                        current_event_message = event_data['deskripsi']
                        show_event_message = True
                        active_event_data = event_data
                        selected_event_option = None
                        show_pause_menu = True
                        pause_for_event = True
                        last_pause_start = time.time()
                    last_event_hour = game_hour
                elif game_hour not in event_hours:
                    last_event_hour = None
                
                if is_day and my_wagon.is_moving:
                    if game_hour != last_hour:
                        if km_today < km_per_day:
                            km_to_add = min(km_per_hour, km_per_day - km_today)
                            my_wagon.position += km_to_add
                            km_today += km_to_add
                        last_hour = game_hour
                if day != last_day:
                    km_today = 0
                    last_day = day
            
            draw_text(screen, font, f"Day {day}", screen_width - 100, 30, with_button=True)
            draw_text(screen, font, f"Jam Game: {game_hour:02}:00", screen_width - 220, 80, with_button=True)

            my_wagon.is_moving = wagon_moving
            
            pause_btn_rect = pygame.Rect(screen_width - 120, screen_height - 60, 100, 40)
            pygame.draw.rect(screen, (120, 60, 30), pause_btn_rect, border_radius=10)
            pygame.draw.rect(screen, (180, 130, 80), pause_btn_rect, 3, border_radius=10)
            draw_text(screen, font, "Resume" if show_pause_menu else "Pause", pause_btn_rect.centerx, pause_btn_rect.centery - 15, (255,255,255), center_x=True)
            
            if show_pause_menu and not pause_for_event:
                overlay = pygame.Surface((screen_width, screen_height))
                overlay.set_alpha(180)
                overlay.fill((30, 30, 30))
                screen.blit(overlay, (0, 0))
                pause_btn_rect = pygame.Rect(screen_width - 120, screen_height - 60, 100, 40)
                pygame.draw.rect(screen, (120, 60, 30), pause_btn_rect, border_radius=10)
                pygame.draw.rect(screen, (180, 130, 80), pause_btn_rect, 3, border_radius=10)
                draw_text(screen, font, "Resume", pause_btn_rect.centerx, pause_btn_rect.centery, (255,255,255), center_x=True)
                draw_text(screen, font, "GAME PAUSED", screen_width//2, screen_height//2 - 20, (255,255,255), center_x=True)
                draw_text(screen, font, "Klik tombol [Resume] atau tekan [P] untuk lanjut", screen_width//2, screen_height//2 + 30, (200,200,200), center_x=True)
                        
            if show_choices:
                draw_choices(screen, font, screen_width, screen_height)
                if game_started:
                    screen.blit(wagon_frames[wagon_frame_index], (750, 350))
                    # Draw animated crew members next to wagon
                    draw_crew_with_animation(screen, my_wagon.crew_list, 550, 380)
            else:
                if my_wagon.is_moving and not is_game_paused():
                    frame_count += 1
                    if frame_count >= frame_delay:
                        frame_count = 0
                        wagon_frame_index = (wagon_frame_index + 1) % len(wagon_frames)
                else:
                    wagon_frame_index = 0
                screen.blit(wagon_frames[wagon_frame_index], (750, 350))
                
                # Draw animated crew members next to wagon when not in choices menu
                if game_started:
                    draw_crew_with_animation(screen, my_wagon.crew_list, 550, 380)

                draw_text(screen, font, "Wagon: Bergerak" if wagon_moving else "Wagon: Berhenti", screen_width - 970, 80, with_button=True)
                draw_text(screen, font, f"Posisi Wagon: {my_wagon.position} km", 30, 30, with_button=True)

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
                            avatar_type = getattr(c, 'avatar_type', 'cowboy')
                            draw_text(screen, font, f"{c.nama} - HP: {c.hp} - Status: {c.status}",
                                    status_x + status_width//2, crew_y + 0, (255, 255, 255), center_x=True)

                if show_dead_crew and my_wagon.dead_crew_list:
                    draw_dead_crew_list(screen, font, my_wagon, screen_width)

                if show_inventory_menu:
                    inv_width, inv_height = 400, 300
                    inv_x, inv_y = (screen_width - inv_width)//2, (screen_height - inv_height)//2
                    pygame.draw.rect(screen, (100, 50, 20), (inv_x, inv_y, inv_width, inv_height), border_radius=10)
                    pygame.draw.rect(screen, (180, 130, 80), (inv_x, inv_y, inv_width, inv_height), 3, border_radius=10)
                    draw_text(screen, font, "INVENTARIS", inv_x + inv_width//2, inv_y + 20, (255,255,255), center_x=True)
                    types = ["food", "drink"]
                    for i, t in enumerate(types):
                        color = (255,255,0) if selected_inventory_type == t else (200,200,200)
                        draw_text(screen, font, t.capitalize(), inv_x + 80 + i*120, inv_y + 60, color, center_x=True)
                    items = my_wagon.inventory.get(selected_inventory_type, [])
                    if not items:
                        draw_text(screen, font, "Kosong", inv_x + inv_width//2, inv_y + 120, (255,200,200), center_x=True)
                    else:
                        for i, (item, restore) in enumerate(items):
                            color = (255,255,0) if i == selected_inventory_index else (255,255,255)
                            draw_text(screen, font, f"{item} (+{restore} HP)", inv_x + 40, inv_y + 110 + i*40, color)
                    
                if not game_over and not game_finished:
                    if my_wagon.position >= 120:
                        game_finished = True
                    elif (day >= max_day and my_wagon.position < 170) or (game_started and (len(my_wagon.crew_list) == 0 or all(c.is_dead for c in my_wagon.crew_list))):
                        game_over = True

                if game_over:
                    screen.fill((0, 0, 0))
                    rect = game_over_img.get_rect(center=(screen_width // 2, screen_height // 2))
                    screen.blit(game_over_img, rect)
                    pygame.display.flip()
                    continue

                if game_finished:
                    screen.fill((0, 30, 0))
                    draw_text(screen, font, "SELAMAT!", screen_width//2, screen_height//2 - 30, (50, 255, 50), center_x=True)
                    draw_text(screen, font, "Kamu berhasil sampai tujuan!", screen_width//2, screen_height//2 + 10, (255,255,255), center_x=True)
                    draw_text(screen, font, "Tekan [ESC] untuk keluar.", screen_width//2, screen_height//2 + 50, (200,200,200), center_x=True)
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                            running = False
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    screen.blit(cursor_img, (mouse_x, mouse_y))
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                            running = False
                    clock.tick(60)
                    continue 
                    
        if show_input_box:
            bg_rect = pygame.Rect(screen_width // 2 - 220, screen_height // 2 - 70, 440, 140)
            pygame.draw.rect(screen, (100, 50, 20), bg_rect, border_radius=12)
            pygame.draw.rect(screen, (180, 130, 80), bg_rect, 3, border_radius=12)
            draw_text(screen, font, "Masukkan nama anggota kru:", screen_width // 2, screen_height // 2 - 45, (255,255,255), center_x=True)
            input_box.update()
            input_box.draw(screen)
        
        if show_dead_crew:
            status_width = 400
            status_height = 300
            status_x = (screen_width - status_width) // 2
            status_y = (screen_height - status_height) // 2

            s = pygame.Surface((status_width, status_height))
            s.set_alpha(230)
            s.fill((60, 20, 20))
            screen.blit(s, (status_x, status_y))

            pygame.draw.rect(
                screen,
                (180, 80, 80),
                pygame.Rect(status_x, status_y, status_width, status_height),
                3,
                border_radius=10
                )

            draw_text(screen, font, "Kru Mati", status_x + status_width//2, status_y + 20, (255, 220, 220), center_x=True)

            if len(my_wagon.dead_crew_list) == 0:
                draw_text(screen, font, "Tidak ada kru yang mati!", status_x + status_width//2, status_y + 120, (255, 200, 200), center_x=True)
            else:
                for i, c in enumerate(my_wagon.dead_crew_list):
                    crew_y = status_y + 70 + i * 40
                    pygame.draw.rect(
                        screen,
                        (120, 60, 60),
                        pygame.Rect(status_x + 20, crew_y, status_width - 40, 30),
                        0,
                        border_radius=5
                    )
                    avatar_type = getattr(c, 'avatar_type', 'unknown')
                    draw_text(screen, font, f"{c.nama} ({avatar_type}) - HP: {c.hp} - Status: {c.status}",
                            status_x + status_width//2, crew_y + 0, (255, 220, 220), center_x=True)

        
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
                    avatar_type = getattr(c, 'avatar_type', 'cowboy')
                    draw_text(screen, font, f"{c.nama} - HP: {c.hp} - Status: {c.status}",
                            status_x + status_width//2, crew_y + 0, (255, 255, 255), center_x=True)
        
        if show_inventory_menu:
            inv_width, inv_height = 400, 300
            inv_x, inv_y = (screen_width - inv_width)//2, (screen_height - inv_height)//2
            pygame.draw.rect(screen, (100, 50, 20), (inv_x, inv_y, inv_width, inv_height), border_radius=10)
            pygame.draw.rect(screen, (180, 130, 80), (inv_x, inv_y, inv_width, inv_height), 3, border_radius=10)
            draw_text(screen, font, "INVENTARIS", inv_x + inv_width//2, inv_y + 20, (255,255,255), center_x=True)
            types = ["food", "drink"]
            for i, t in enumerate(types):
                color = (255,255,0) if selected_inventory_type == t else (200,200,200)
                draw_text(screen, font, t.capitalize(), inv_x + 80 + i*120, inv_y + 60, color, center_x=True)
            items = my_wagon.inventory.get(selected_inventory_type, [])
            if not items:
                draw_text(screen, font, "Kosong", inv_x + inv_width//2, inv_y + 120, (255,200,200), center_x=True)
            else:
                for i, (item, restore) in enumerate(items):
                    color = (255,255,0) if i == selected_inventory_index else (255,255,255)
                    draw_text(screen, font, f"{item} (+{restore} HP)", inv_x + 40, inv_y + 110 + i*40, color)
            
        if show_event_message and active_event_data:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                box_width, box_height = 600, 220
                box_x = (screen.get_width() - box_width) // 2
                box_y = (screen.get_height() - box_height) // 2
                for i, pilihan in enumerate(active_event_data['pilihan']):
                    pilihan_rect = pygame.Rect(box_x + 60, box_y + 90 + i*60, 480, 45)
                    if pilihan_rect.collidepoint(mouse_pos):
                        if pilihan == "Melawan" and active_event_data.get("tipe") == "musuh":
                            in_battle = True
                            current_battle = Battle(
                                [Character(crew.nama, crew.hp, crew.attack, original_crew=crew) for crew in my_wagon.crew_list],
                                enemy_hp=100, enemy_attack=10,
                                crew_bullet_img=crew_bullet_img,
                                enemy_bullet_img=enemy_bullet_img
                            )
                            battle_phase = 'crew_select'
                            status_message = "Pertempuran dimulai!"
                            status_timer = STATUS_DISPLAY_TIME
                        else:
                            hasil = game_event.apply_consequence(active_event_data, pilihan, my_wagon)
                            status_message = f"{pilihan}: {hasil}"
                            status_timer = STATUS_DISPLAY_TIME * 2
                        show_event_message = False
                        active_event_data = None
                        selected_event_option = None
                        show_pause_menu = False
                        pause_for_event = False
                        if last_pause_start is not None:
                            game_paused_time += time.time() - last_pause_start
                            last_pause_start = None

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

        if show_event_message and active_event_data:
            draw_event_choices(screen, font, active_event_data)
            
        if not show_story:
            button_width, button_height = 220, 55
            gap = 40
            btn_y = screen_height - button_height - 25

            crew_btn_rect = pygame.Rect(screen_width//2 - button_width - gap//2, btn_y, button_width, button_height)
            inv_btn_rect = pygame.Rect(screen_width//2 + gap//2, btn_y, button_width, button_height)
            dead_btn_rect = pygame.Rect(screen_width//2 - button_width//2, btn_y - button_height - 15, button_width, button_height)
            
            pygame.draw.rect(screen, (120, 60, 30), main_menu_rect, border_radius=10)
            pygame.draw.rect(screen, (180, 130, 80), main_menu_rect, 2, border_radius=10)
            draw_text(screen, font, "Menu", main_menu_rect.centerx, main_menu_rect.centery - 15, (255,255,255), center_x=True)

        if show_main_menu:
            for i, rect in enumerate(main_menu_option_rects):
                pygame.draw.rect(screen, (120, 60, 30), rect, border_radius=8)
                pygame.draw.rect(screen, (180, 130, 80), rect, 2, border_radius=8)
                draw_text(screen, font, main_menu_options[i], rect.centerx, rect.centery - 10, (255,255,255), center_x=True)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(cursor_img, (mouse_x, mouse_y))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
