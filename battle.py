import pygame
import random
import math
import os
from crew_inherit import Chef, Nurse, Hunter, Police, Infantry, Doctor, Musician, Thief, Agent, Firefighter

class Character:
    def __init__(self, nama, hp, attack, original_crew=None, avatar_path=None):
        self.nama = nama
        self.hp = hp
        self.attack = attack
        self.is_dead = False
        self.original_crew = original_crew
        self.x = 0  
        self.y = 0 
        self.target_x = 0 
        self.target_y = 0
        self.speed = 2
        self.width = 80 
        self.height = 80  
        self.avatar = None
        self.walking_right_frames = None
        self.walking_left_frames = None
        self.current_direction = "right"
        self.animation_frame = 0
        self.animation_counter = 0
        self.animation_delay = 30
        
        if avatar_path and pygame.get_init():
            try:
                self.avatar = pygame.image.load(avatar_path).convert_alpha()
            except pygame.error:
                print(f"Warning: Could not load avatar {avatar_path}")
                self.avatar = None
    
    def load_walking_animations(self, avatar_name):
        if pygame.get_init():
            try:
                # Remove the _pp.png suffix and use the base name for walking animations
                base_name = avatar_name.replace("_pp.png", "")
                right_path = f"{base_name}_walkingright.png"
                left_path = f"{base_name}_walkingleft.png"
                
                if os.path.exists(right_path):
                    walking_right_sheet = pygame.image.load(right_path).convert_alpha()
                    frame_width = walking_right_sheet.get_width() // 2
                    frame_height = walking_right_sheet.get_height()
                    self.walking_right_frames = []
                    for i in range(2):
                        frame = walking_right_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
                        self.walking_right_frames.append(frame)
                else:
                    self.walking_right_frames = [self.avatar, self.avatar] if self.avatar else None
                    
                if os.path.exists(left_path):
                    walking_left_sheet = pygame.image.load(left_path).convert_alpha()
                    frame_width = walking_left_sheet.get_width() // 2
                    frame_height = walking_left_sheet.get_height()
                    self.walking_left_frames = []
                    for i in range(2):
                        frame = walking_left_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
                        self.walking_left_frames.append(frame)
                else:
                    self.walking_left_frames = [self.avatar, self.avatar] if self.avatar else None
                    
                print(f"Mencoba memuat: {right_path}, {left_path}")
            except pygame.error as e:
                print(f"Warning: Could not load walking animations for {avatar_name}: {e}")
                self.walking_right_frames = [self.avatar, self.avatar] if self.avatar else None
                self.walking_left_frames = [self.avatar, self.avatar] if self.avatar else None
        
    def move_towards_target(self):
        if not self.is_dead:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            
            if dx > 0:
                self.current_direction = "right"
            elif dx < 0:
                self.current_direction = "left"
                
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > 5: 
                dx = dx / distance * self.speed if distance > 0 else 0
                dy = dy / distance * self.speed if distance > 0 else 0
                
                self.x += dx
                self.y += dy
                
                self.animation_counter += 1
                if self.animation_counter >= self.animation_delay:
                    self.animation_counter = 0
                    self.animation_frame = 1 - self.animation_frame
    
    def get_current_sprite(self):
        if self.walking_right_frames and self.walking_left_frames:
            if self.current_direction == "right":
                return self.walking_right_frames[self.animation_frame]
            else:
                return self.walking_left_frames[self.animation_frame]
        return self.avatar

class Battle:
    def __init__(self, all_crew, enemy_hp, enemy_attack, maxturn=10, max_battle_crew=3, crew_bullet_img=None, enemy_bullet_img=None):
        self.all_crew = all_crew
        self.player_crew = []
        self.max_battle_crew = max_battle_crew
        self.enemy_hp = enemy_hp
        self.max_enemy_hp = enemy_hp
        self.enemy_attack = enemy_attack
        self.turn = 1
        self.maxturn = maxturn
        self.battle_log = []
        self.battle_finished = False
        self.battle_won = False
        self.crew_selection_phase = True
        self.selected_crew = None
        self.enemy_x = 700
        self.enemy_y = 200
        self.enemy_width = 100
        self.enemy_height = 100
        self.enemy_target_x = self.enemy_x
        self.enemy_target_y = self.enemy_y
        self.enemy_speed = 1
        self.enemy_move_cooldown = 0
        self.bullets = []
        self.enemy_bullets = []
        
        if pygame.get_init():
            try:
                self.background_image = pygame.image.load("battle_bg.png").convert()
                self.background_image = pygame.transform.scale(self.background_image, (1000, 600))
            except pygame.error:
                print("Warning: Could not load battle_bg.png, using default background")
                self.background_image = pygame.Surface((1000, 600))
                self.background_image.fill((50, 50, 100)) 
                
            try:
                self.enemy_img_right = pygame.image.load("mutant_right.png").convert_alpha()
                self.enemy_img_right = pygame.transform.scale(self.enemy_img_right, (200, 200))
            except pygame.error:
                self.enemy_img_right = pygame.Surface((200, 200))
                self.enemy_img_right.fill((200, 0, 0))
            try:
                self.enemy_img_left = pygame.image.load("mutant_left.png").convert_alpha()
                self.enemy_img_left = pygame.transform.scale(self.enemy_img_left, (200, 200))
            except pygame.error:
                self.enemy_img_left = pygame.Surface((200, 200))
                self.enemy_img_left.fill((200, 0, 0))
        self.enemy_direction = "right"
        self.enemy_anim_frame = 0
        self.enemy_anim_counter = 0
        self.enemy_anim_delay = 20
        
        self.battle_characters = []
        for crew in all_crew:
            character = Character(crew.nama, crew.hp, crew.attack, original_crew=crew)
            self.battle_characters.append(character)
            
        self.all_crew = self.battle_characters
        self.avatar_selection_phase = False
        self.selected_avatar_index = 0
        self.crew_avatar_paths = [
            "butcher_pp.png",
            "chef_pp.png", 
            "cowboy_pp.png",
            "cowgirl_pp.png",
            "doctor_pp.png"
        ]
        self.crew_bullet_img = crew_bullet_img
        self.enemy_bullet_img = enemy_bullet_img

    def select_crew(self, crew):
        if self.crew_selection_phase:
            if crew in self.all_crew and crew not in self.player_crew:
                if len(self.player_crew) < self.max_battle_crew:
                    self.player_crew.append(crew)
                    self.battle_log.append(f"{crew.nama} bergabung dalam battle!")
        else:
            self.selected_crew = crew

    def get_target_crew(self):
        living_crew = [crew for crew in self.player_crew if not crew.is_dead and crew.hp < 100]
        
        if not living_crew:
            return None
        
        living_crew.sort(key=lambda x: x.hp)
        return living_crew[0]

    def crew_attack(self):
        if not self.crew_selection_phase and self.selected_crew and not self.selected_crew.is_dead:
            original_crew = self.selected_crew.original_crew
            
            start_x = self.selected_crew.x + self.selected_crew.width
            start_y = self.selected_crew.y + self.selected_crew.height // 2
            
            if isinstance(original_crew, Chef):
                original_crew.cook()  
                self.selected_crew.hp = min(self.selected_crew.hp + 30, 100)
                self.bullets.append({
                    'x': start_x,
                    'y': start_y,
                    'dx': 15,
                    'dy': 0,
                    'damage': self.selected_crew.attack,
                    'radius': 5
                })
                self.battle_log.append(f"{self.selected_crew.nama} memasak dan menyerang!")
                
            elif isinstance(original_crew, Hunter):
                original_crew.hunt()  
                self.selected_crew.attack = original_crew.attack
                self.bullets.append({
                    'x': start_x,
                    'y': start_y,
                    'dx': 15,
                    'dy': 0,
                    'damage': self.selected_crew.attack,
                    'radius': 6
                })
                self.battle_log.append(f"{self.selected_crew.nama} berburu dan meningkatkan serangan!")
                
            elif isinstance(original_crew, Police):
                original_crew.enforce_law()
                self.bullets.append({
                    'x': start_x,
                    'y': start_y,
                    'dx': 15,
                    'dy': 0,
                    'damage': self.selected_crew.attack,
                    'radius': 5
                })
                self.battle_log.append(f"{self.selected_crew.nama} menegakkan hukum dan menyerang!")
                
            elif isinstance(original_crew, Infantry):
                damage = original_crew.shoot() 
                self.bullets.append({
                    'x': start_x,
                    'y': start_y,
                    'dx': 15,
                    'dy': 0,
                    'damage': int(damage),
                    'radius': 5
                })
                self.battle_log.append(f"{self.selected_crew.nama} menembak dengan damage {damage:.2f}!")
                
            elif isinstance(original_crew, Nurse):
                target_crew = self.get_target_crew()
                if target_crew and target_crew != self.selected_crew:
                    target_battle_crew = None
                    for battle_crew in self.player_crew:
                        if battle_crew.original_crew == target_crew.original_crew:
                            target_battle_crew = battle_crew
                            break
                    
                    if target_battle_crew:
                        original_crew.heal_crew(target_crew.original_crew)
                        heal_amount = int(target_battle_crew.hp * 0.25)
                        target_battle_crew.hp = min(target_battle_crew.hp + heal_amount, 100)
                        self.battle_log.append(f"{self.selected_crew.nama} menyembuhkan {target_battle_crew.nama}!")
                    else:
                        self.bullets.append({
                            'x': start_x,
                            'y': start_y,
                            'dx': 15,
                            'dy': 0,
                            'damage': self.selected_crew.attack,
                            'radius': 5
                        })
                        self.battle_log.append(f"{self.selected_crew.nama} menyerang musuh!")
                else:
                    self.bullets.append({
                        'x': start_x,
                        'y': start_y,
                        'dx': 15,
                        'dy': 0,
                        'damage': self.selected_crew.attack,
                        'radius': 5
                    })
                    self.battle_log.append(f"{self.selected_crew.nama} menyerang musuh!")
                    
            elif isinstance(original_crew, Doctor):
                target_crew = self.get_target_crew()
                if target_crew and target_crew != self.selected_crew:
                    target_battle_crew = None
                    for battle_crew in self.player_crew:
                        if battle_crew.original_crew == target_crew.original_crew:
                            target_battle_crew = battle_crew
                            break
                    
                    if target_battle_crew:
                        original_crew.medical_treatment(target_crew.original_crew)
                        heal_amount = int(target_battle_crew.hp * 0.40)
                        target_battle_crew.hp = min(target_battle_crew.hp + heal_amount, 100)
                        self.battle_log.append(f"{self.selected_crew.nama} memberikan perawatan medis pada {target_battle_crew.nama}!")
                    else:
                        self.bullets.append({
                            'x': start_x,
                            'y': start_y,
                            'dx': 15,
                            'dy': 0,
                            'damage': self.selected_crew.attack,
                            'radius': 5
                        })
                        self.battle_log.append(f"{self.selected_crew.nama} menyerang musuh!")
                else:
                    self.bullets.append({
                        'x': start_x,
                        'y': start_y,
                        'dx': 15,
                        'dy': 0,
                        'damage': self.selected_crew.attack,
                        'radius': 5
                    })
                    self.battle_log.append(f"{self.selected_crew.nama} menyerang musuh!")
                    
            elif isinstance(original_crew, Thief):
                if hasattr(self, 'wagon'):
                    original_crew.loot(self.wagon)
                    self.battle_log.append(f"{self.selected_crew.nama} mencuri item!")
                self.bullets.append({
                    'x': start_x,
                    'y': start_y,
                    'dx': 20,  
                    'dy': 0,
                    'damage': self.selected_crew.attack,
                    'radius': 4
                })
                self.battle_log.append(f"{self.selected_crew.nama} menyerang dengan cepat!")
                
            elif isinstance(original_crew, Agent):
                damage = original_crew.attack_boost()
                self.bullets.append({
                    'x': start_x,
                    'y': start_y,
                    'dx': 18,
                    'dy': 0,
                    'damage': int(damage),
                    'radius': 5
                })
                self.battle_log.append(f"{self.selected_crew.nama} menggunakan serangan khusus dengan damage {damage:.2f}!")
                
            elif isinstance(original_crew, Musician):
                if hasattr(self, 'crew_list'):
                    original_crew.inspire_team(self)
                else:
                    for crew in self.player_crew:
                        if not crew.is_dead:
                            crew.attack = int(crew.attack * 1.12)  #
                self.bullets.append({
                    'x': start_x,
                    'y': start_y,
                    'dx': 15,
                    'dy': 0,
                    'damage': self.selected_crew.attack,
                    'radius': 5
                })
                self.battle_log.append(f"{self.selected_crew.nama} menginspirasi tim dan menyerang!")
                
            elif isinstance(original_crew, Firefighter):
                original_crew.extinguish_fire()
                self.bullets.append({
                    'x': start_x,
                    'y': start_y,
                    'dx': 15,
                    'dy': 0,
                    'damage': self.selected_crew.attack,
                    'radius': 5
                })
                self.battle_log.append(f"{self.selected_crew.nama} memadamkan api dan menyerang!")
                
            else:
                self.bullets.append({
                    'x': start_x,
                    'y': start_y,
                    'dx': 15,
                    'dy': 0,
                    'damage': self.selected_crew.attack,
                    'radius': 5
                })
                self.battle_log.append(f"{self.selected_crew.nama} menyerang musuh!")

    def update_bullets(self):
        bullets_to_remove = []
        for i, bullet in enumerate(self.bullets):
            bullet['x'] += bullet['dx']
            bullet['y'] += bullet['dy']
            
            if (
                bullet['dx'] > 0 and
                bullet['x'] >= self.enemy_x and
                self.enemy_y <= bullet['y'] <= self.enemy_y + self.enemy_height
            ):
                self.enemy_hp -= bullet['damage']
                self.battle_log.append(f"Serangan mengenai musuh! Damage: {bullet['damage']}")
                bullets_to_remove.append(i)

                if self.enemy_hp <= 0:
                    self.battle_finished = True
                    self.battle_won = True
                    self.sync_hp()
                    self.battle_log.append("Musuh telah dikalahkan!")
                else:
                    self.enemy_attack_crew()

            if (bullet['x'] < 0 or bullet['x'] > 1000 or bullet['y'] < 0 or bullet['y'] > 600):
                bullets_to_remove.append(i)

        for i in sorted(bullets_to_remove, reverse=True):
            if i < len(self.bullets):
                self.bullets.pop(i)

        enemy_bullets_to_remove = []
        for i, bullet in enumerate(self.enemy_bullets):
            bullet['x'] += bullet['dx']
            bullet['y'] += bullet['dy']
            for crew in self.player_crew:
                if not crew.is_dead and crew.x <= bullet['x'] <= crew.x + crew.width and crew.y <= bullet['y'] <= crew.y + crew.height:
                    crew.hp -= bullet['damage']
                    if crew.hp <= 0:
                        crew.is_dead = True
                    enemy_bullets_to_remove.append(i)
                    break
            if bullet['x'] < 0 or bullet['x'] > 1000 or bullet['y'] < 0 or bullet['y'] > 600:
                enemy_bullets_to_remove.append(i)
        for i in sorted(set(enemy_bullets_to_remove), reverse=True):
            if i < len(self.enemy_bullets):
                self.enemy_bullets.pop(i)
            
    def update_enemy_movement(self):
            dx = self.enemy_target_x - self.enemy_x
            dy = self.enemy_target_y - self.enemy_y
            distance = math.sqrt(dx**2 + dy**2)

            # Update direction
            if dx > 0:
                self.enemy_direction = "right"
            elif dx < 0:
                self.enemy_direction = "left"

            # Update animation frame
            self.enemy_anim_counter += 1
            if self.enemy_anim_counter >= self.enemy_anim_delay:
                self.enemy_anim_counter = 0
                self.enemy_anim_frame = 1 - self.enemy_anim_frame

            if distance > 5:
                self.enemy_x += (dx / distance) * self.enemy_speed
                self.enemy_y += (dy / distance) * self.enemy_speed
            elif self.enemy_move_cooldown <= 0:
                self.enemy_target_x = random.randint(600, 850)
                self.enemy_target_y = random.randint(150, 350)
                self.enemy_move_cooldown = 60 
            else:
                self.enemy_move_cooldown -= 1

    def sync_hp(self):
        for crew in self.player_crew:
            if crew.original_crew:
                crew.original_crew.hp = crew.hp
                crew.original_crew.is_dead = crew.is_dead
                
    def remove_crew(self, crew):
        if self.crew_selection_phase and crew in self.player_crew:
            self.player_crew.remove(crew)
            self.battle_log.append(f"{crew.nama} keluar dari battle!")

    def start_battle(self):
        if len(self.player_crew) > 0:
            self.crew_selection_phase = False
            self.avatar_selection_phase = True
            self.selected_avatar_index = 0
            self.battle_log.append("Battle dimulai!")  
            
            for i, crew in enumerate(self.player_crew):
                crew.x = 100 + i*150
                crew.y = 400
                crew.target_x = crew.x
                crew.target_y = crew.y
                if crew.avatar:  # Tambahkan ini
                    crew.load_walking_animations(crew.avatar)
                
            return True
        return False
    
    def draw_avatar_selection(self, screen, font):
        crew = self.player_crew[self.selected_avatar_index]
        title = font.render(f"Pilih Avatar untuk {crew.nama}", True, (255, 255, 255))
        screen.blit(title, (300, 50))
        for i, path in enumerate(self.crew_avatar_paths):
            x = 150 + i * 150
            y = 200
            if pygame.get_init():
                try:
                    avatar_img = pygame.image.load(path).convert_alpha()
                    avatar_img = pygame.transform.scale(avatar_img, (100, 100))
                    screen.blit(avatar_img, (x, y))
                except pygame.error:
                    pygame.draw.rect(screen, (100, 100, 100), (x, y, 100, 100))
                    name_text = font.render(f"Avatar {i+1}", True, (255, 255, 255))
                    screen.blit(name_text, (x + 10, y + 40))
        instr = font.render("Klik avatar untuk memilih", True, (255, 255, 255))
        screen.blit(instr, (300, 350))

    def select_avatar_for_crew(self, avatar_index):
        """Select avatar for the current crew member in avatar selection phase"""
        if self.avatar_selection_phase and 0 <= avatar_index < len(self.crew_avatar_paths):
            crew = self.player_crew[self.selected_avatar_index]
            avatar_path = self.crew_avatar_paths[avatar_index]
            
            # Load the selected avatar
            if pygame.get_init():
                try:
                    crew.avatar = pygame.image.load(avatar_path).convert_alpha()
                    # Load walking animations based on avatar name
                    crew.load_walking_animations(avatar_path)
                    print(f"Avatar {avatar_path} dipilih untuk {crew.nama}")
                except pygame.error as e:
                    print(f"Error loading avatar {avatar_path}: {e}")
            
            # Move to next crew or finish avatar selection
            self.selected_avatar_index += 1
            if self.selected_avatar_index >= len(self.player_crew):
                self.avatar_selection_phase = False
                self.battle_log.append("Semua avatar telah dipilih. Battle siap dimulai!")

    def shoot(self):
        if self.selected_crew and not self.battle_finished and not self.selected_crew.is_dead:
            self.crew_attack()

    def hit_enemy(self):
        pass

    def enemy_attack_crew(self):
        if not self.battle_finished:
            living_crew = [crew for crew in self.player_crew if not crew.is_dead]
            if living_crew:
                target = random.choice(living_crew)
                start_x = self.enemy_x
                start_y = self.enemy_y + self.enemy_height // 2
                target_x = target.x + target.width // 2
                target_y = target.y + target.height // 2
                dx = target_x - start_x
                dy = target_y - start_y
                distance = max(1, (dx**2 + dy**2) ** 0.5)
                speed = 10
                self.enemy_bullets.append({
                    'x': start_x,
                    'y': start_y,
                    'dx': dx / distance * speed,
                    'dy': dy / distance * speed,
                    'damage': self.enemy_attack,
                    'radius': 7
                })
                if random.random() < 0.6:
                    target.hp -= self.enemy_attack
                    self.battle_log.append(f"Musuh menyerang {target.nama}! HP: {target.hp}")

                    if target.hp <= 0:
                        target.is_dead = True
                        if target.original_crew:
                            target.original_crew.is_dead = True
                        self.battle_log.append(f"{target.nama} telah gugur!")
                        if all(crew.is_dead for crew in self.player_crew):
                            self.battle_finished = True
                            self.sync_hp()
                            self.battle_log.append("Semua kru telah gugur!")
                else:
                    self.battle_log.append("Serangan musuh meleset!")

    def update(self):
        if not self.crew_selection_phase and not self.battle_finished:
            for crew in self.player_crew:
                crew.move_towards_target()
                
            self.update_enemy_movement()
            
            self.update_bullets()

    def draw_battle_scene(self, screen, font):
        if pygame.get_init():
            screen.blit(self.background_image, (0, 0))
            if self.enemy_direction == "right":
                enemy_img = self.enemy_img_right
            else:
                enemy_img = self.enemy_img_left

        for i, crew in enumerate(self.player_crew):
            if not crew.is_dead:
                current_sprite = crew.get_current_sprite()
                if current_sprite:
                    sprite_scaled = pygame.transform.scale(current_sprite, (crew.width, crew.height))
                    screen.blit(sprite_scaled, (int(crew.x), int(crew.y)))
                else:
                    color = (0, 255, 0) if crew == self.selected_crew else (100, 100, 100)
                    pygame.draw.rect(screen, color, (int(crew.x), int(crew.y), crew.width, crew.height))
            else:
                pygame.draw.rect(screen, (100, 0, 0), (int(crew.x), int(crew.y), crew.width, crew.height))
                
            crew_name = font.render(crew.nama, True, (255, 255, 255))
            screen.blit(crew_name, (int(crew.x), int(crew.y) - 30))
            
        if self.enemy_direction == "right":
            enemy_img = self.enemy_img_right
        else:
            enemy_img = self.enemy_img_left
        screen.blit(enemy_img, (int(self.enemy_x), int(self.enemy_y)))

        if self.crew_bullet_img:
            for bullet in self.bullets:
                bx, by = int(bullet['x']), int(bullet['y'])
                screen.blit(self.crew_bullet_img, (bx - self.crew_bullet_img.get_width() // 2, by - self.crew_bullet_img.get_height() // 2))
        else:
            for bullet in self.bullets:
                pygame.draw.circle(screen, (255, 255, 0), (int(bullet['x']), int(bullet['y'])), bullet['radius'])
                
        if self.enemy_bullet_img:
            for bullet in self.enemy_bullets:
                bx, by = int(bullet['x']), int(bullet['y'])
                screen.blit(self.enemy_bullet_img, (bx - self.enemy_bullet_img.get_width() // 2, by - self.enemy_bullet_img.get_height() // 2))
        else:
            for bullet in self.enemy_bullets:
                pygame.draw.circle(screen, (255, 0, 0), (int(bullet['x']), int(bullet['y'])), bullet['radius'])
        
        bar_width = 200
        bar_height = 25
        margin = 20
        base_y = screen.get_height() - margin - (len(self.player_crew) + 2) * (bar_height + 10)
        
        self.draw_hp_bar(
            screen,
            screen.get_width() - bar_width - margin,
            base_y,
            bar_width,
            bar_height,
            self.enemy_hp,
            self.max_enemy_hp, 
            (200, 50, 50),
            "Enemy HP",
            font
        )
        
        for idx, crew in enumerate(self.player_crew):
            max_hp = crew.original_crew.hp if crew.original_crew else 100
            self.draw_hp_bar(
                screen,
                screen.get_width() - bar_width - margin,
                base_y + (idx + 1) * (bar_height + 10),
                bar_width,
                bar_height,
                crew.hp,
                max_hp,
                (139, 69, 19) if not crew.is_dead else (100, 0, 0),
                f"{crew.nama}",
                font
            )
        
    def draw_hp_bar(self, screen, x, y, width, height, hp, max_hp, color, label, font):
        max_hp = max(1, max_hp)
        pygame.draw.rect(screen, (60, 60, 60), (x, y, width, height), border_radius=5)
        hp_width = int(width * max(0, min(1, hp / max_hp)))
        pygame.draw.rect(screen, color, (x, y, hp_width, height), border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height), 2, border_radius=5)
        label_text = font.render(f"{label}: {hp}/{max_hp}", True, (255, 255, 255))
        screen.blit(label_text, (x + 5, y + height // 2 - label_text.get_height() // 2))
    
    def draw(self, screen):
        font = pygame.font.Font(None, 36)
        if self.crew_selection_phase:
            title = font.render("Pilih Kru untuk Battle (Maksimal 3)", True, (255, 255, 255))
            screen.blit(title, (300, 50))
            header = font.render("Nama      |   HP   | Status", True, (255, 255, 0))
            screen.blit(header, (120, 120))
            for i, crew in enumerate(self.all_crew):
                status = "Mati" if crew.is_dead else "Hidup"
                color = (0, 255, 0) if crew in self.player_crew else (255, 255, 255)
                text = f"{crew.nama:<10} | {crew.hp:<5} | {status}"
                crew_text = font.render(text, True, color)
                screen.blit(crew_text, (120, 170 + i * 40))
            if len(self.player_crew) > 0:
                pygame.draw.rect(screen, (0, 255, 0), (350, 550, 200, 50))
                start_text = font.render("Lanjut Pilih Avatar", True, (0, 0, 0))
                screen.blit(start_text, (360, 565))
        elif self.avatar_selection_phase:
            self.draw_avatar_selection(screen, font)
        else:
            self.draw_battle_scene(screen, font)
    
    def handle_movement_input(self, keys):
        if self.selected_crew and not self.crew_selection_phase:
            move_speed = 5
        
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.selected_crew.target_x -= move_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.selected_crew.target_x += move_speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.selected_crew.target_y -= move_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.selected_crew.target_y += move_speed
                
            self.selected_crew.target_x = max(50, min(self.selected_crew.target_x, 500))
            self.selected_crew.target_y = max(100, min(self.selected_crew.target_y, 450))