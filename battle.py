import pygame
import random
import math

class Character:
    def __init__(self, nama, hp, attack, original_crew=None):
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

    def move_towards_target(self):
        if not self.is_dead:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > 5: 
                dx = dx / distance * self.speed if distance > 0 else 0
                dy = dy / distance * self.speed if distance > 0 else 0
                
                self.x += dx
                self.y += dy

class Battle:
    def __init__(self, all_crew, enemy_hp, enemy_attack, maxturn=10, max_battle_crew=3):
        self.all_crew = all_crew
        self.player_crew = []
        self.max_battle_crew = max_battle_crew
        self.enemy_hp = enemy_hp
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
        
        self.background_image = pygame.image.load("battle_bg.png").convert()
        self.background_image = pygame.transform.scale(self.background_image, (1000, 600))
        self.enemy_image = pygame.image.load("battle_enemy.png").convert_alpha()
        self.enemy_image = pygame.transform.scale(self.enemy_image, (200, 200))
        self.battle_characters = []
        for crew in all_crew:
            character = Character(crew.nama, crew.hp, crew.attack, original_crew=crew)
            self.battle_characters.append(character)
        self.all_crew = self.battle_characters


    def select_crew(self, crew):
        if self.crew_selection_phase:
            if crew in self.all_crew and crew not in self.player_crew:
                if len(self.player_crew) < self.max_battle_crew:
                    self.player_crew.append(crew)
                    self.battle_log.append(f"{crew.nama} bergabung dalam battle!")
        else:
            self.selected_crew = crew

    def crew_attack(self):
        if not self.crew_selection_phase and self.selected_crew and not self.selected_crew.is_dead:
            start_x = self.selected_crew.x + self.selected_crew.width/2
            start_y = self.selected_crew.y + self.selected_crew.height/2
            
            self.bullets.append({
                'x': start_x,
                'y': start_y,
                'dx': (self.enemy_x + self.enemy_width/2 - start_x) / 10,
                'dy': (self.enemy_y + self.enemy_height/2 - start_y) / 10,
                'damage': self.selected_crew.attack,
                'radius': 5
            })
            
            self.battle_log.append(f"{self.selected_crew.nama} menyerang musuh!")

    def update_bullets(self):
        bullets_to_remove = []
        
        for i, bullet in enumerate(self.bullets):
            bullet['x'] += bullet['dx']
            bullet['y'] += bullet['dy']
            
            enemy_rect = pygame.Rect(self.enemy_x, self.enemy_y, self.enemy_width, self.enemy_height)
            bullet_rect = pygame.Rect(bullet['x'] - bullet['radius'], bullet['y'] - bullet['radius'], bullet['radius']*2, bullet['radius']*2)
                                      
            if enemy_rect.colliderect(bullet_rect):
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

    def update_enemy_movement(self):
        dx = self.enemy_target_x - self.enemy_x
        dy = self.enemy_target_y - self.enemy_y
        distance = math.sqrt(dx**2 + dy**2)
        
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
            self.battle_log.append("Battle dimulai!")
            
            for i, crew in enumerate(self.player_crew):
                crew.x = 100 + i*150
                crew.y = 400
                crew.target_x = crew.x
                crew.target_y = crew.y
                
            return True
        return False

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
        screen.blit(self.background_image, (0, 0))
        screen.blit(self.enemy_image, (int(self.enemy_x), int(self.enemy_y)))
        
        screen.blit(self.enemy_image, (int(self.enemy_x), int(self.enemy_y)))
        enemy_health = f"Enemy HP: {self.enemy_hp}"
        health_text = font.render(enemy_health, True, (255, 0, 0))
        screen.blit(health_text, (int(self.enemy_x), int(self.enemy_y) - 30))

        for i, crew in enumerate(self.player_crew):
            color = (0, 255, 0) if crew == self.selected_crew else (100, 100, 100)
            if crew.is_dead:
                color = (100, 0, 0)
            pygame.draw.rect(screen, color, (int(crew.x), int(crew.y), crew.width, crew.height))
            
            crew_name = font.render(crew.nama, True, (255, 255, 255))
            crew_hp = font.render(f"HP: {crew.hp}", True, (255, 255, 255))
            screen.blit(crew_name, (int(crew.x), int(crew.y) - 30))
            screen.blit(crew_hp, (int(crew.x), int(crew.y) + crew.height + 10))

        for bullet in self.bullets:
            pygame.draw.circle(screen, (255, 255, 0), (int(bullet['x']), int(bullet['y'])), bullet['radius'])
        controls = font.render("SPACE: Serang | 1-5: Pilih Kru | WASD/Arrows: Gerak Kru", True, (255, 255, 255))
        screen.blit(controls, (350, 550))
    
    def draw(self, screen):
        font = pygame.font.Font(None, 36)

        if self.crew_selection_phase:
            title = font.render("Pilih Crew untuk Battle (Max: 3)", True, (255, 255, 255))
            screen.blit(title, (300, 50))

            for i, crew in enumerate(self.all_crew):
                color = (0, 255, 0) if crew in self.player_crew else (200, 200, 200)
                pygame.draw.rect(screen, color, (100 + i*150, 400, 100, 100))
                crew_name = font.render(crew.nama, True, (0, 0, 0))
                screen.blit(crew_name, (100 + i*150, 360))

            if len(self.player_crew) > 0:
                pygame.draw.rect(screen, (0, 255, 0), (350, 550, 200, 50))
                start_text = font.render("Start Battle", True, (0, 0, 0))
                screen.blit(start_text, (380, 565))
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