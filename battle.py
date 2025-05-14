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
        self.x = 0  # Position X
        self.y = 0  # Position Y
        self.target_x = 0  # Target position to move to
        self.target_y = 0
        self.speed = 2  # Movement speed
        self.width = 80  # Character width
        self.height = 80  # Character height

    def move_towards_target(self):
        if not self.is_dead:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            
            # Calculate distance to target
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > 5:  # Only move if we're not very close to target
                # Normalize direction vector and multiply by speed
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
        
        # Enemy position and movement
        self.enemy_x = 700
        self.enemy_y = 200
        self.enemy_width = 100
        self.enemy_height = 100
        self.enemy_target_x = self.enemy_x
        self.enemy_target_y = self.enemy_y
        self.enemy_speed = 1
        self.enemy_move_cooldown = 0
        
        # Bullet properties
        self.bullets = []
        
        # Convert crew list to Character objects
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
            # Create a bullet from crew to enemy
            start_x = self.selected_crew.x + self.selected_crew.width/2
            start_y = self.selected_crew.y + self.selected_crew.height/2
            
            # Add bullet to list
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
            # Move bullet
            bullet['x'] += bullet['dx']
            bullet['y'] += bullet['dy']
            
            # Check for collision with enemy
            enemy_rect = pygame.Rect(self.enemy_x, self.enemy_y, self.enemy_width, self.enemy_height)
            bullet_rect = pygame.Rect(bullet['x'] - bullet['radius'], bullet['y'] - bullet['radius'], 
                                      bullet['radius']*2, bullet['radius']*2)
                                      
            if enemy_rect.colliderect(bullet_rect):
                # Bullet hit enemy
                self.enemy_hp -= bullet['damage']
                self.battle_log.append(f"Serangan mengenai musuh! Damage: {bullet['damage']}")
                bullets_to_remove.append(i)
                
                if self.enemy_hp <= 0:
                    self.battle_finished = True
                    self.battle_won = True
                    self.sync_hp()
                    self.battle_log.append("Musuh telah dikalahkan!")
                else:
                    # Enemy counter attack
                    self.enemy_attack_crew()
            
            # Remove bullets that go off screen
            if (bullet['x'] < 0 or bullet['x'] > 1000 or 
                bullet['y'] < 0 or bullet['y'] > 600):
                bullets_to_remove.append(i)
        
        # Remove bullets (in reverse to avoid index issues)
        for i in sorted(bullets_to_remove, reverse=True):
            if i < len(self.bullets):
                self.bullets.pop(i)

    def update_enemy_movement(self):
        # Move enemy towards target
        dx = self.enemy_target_x - self.enemy_x
        dy = self.enemy_target_y - self.enemy_y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 5:
            # Move towards target
            self.enemy_x += (dx / distance) * self.enemy_speed
            self.enemy_y += (dy / distance) * self.enemy_speed
        elif self.enemy_move_cooldown <= 0:
            # Set new random target
            self.enemy_target_x = random.randint(600, 850)
            self.enemy_target_y = random.randint(150, 350)
            self.enemy_move_cooldown = 60  # Frames before next movement
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
            
            # Set initial positions for crew members
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
        # This is handled by bullet collision in update_bullets now
        pass

    def enemy_attack_crew(self):
        if not self.battle_finished:
            # Select a random living crew to attack
            living_crew = [crew for crew in self.player_crew if not crew.is_dead]
            
            if living_crew:
                target = random.choice(living_crew)
                if random.random() < 0.6:  # 60% chance to hit
                    target.hp -= self.enemy_attack
                    self.battle_log.append(f"Musuh menyerang {target.nama}! HP: {target.hp}")

                    if target.hp <= 0:
                        target.is_dead = True
                        if target.original_crew:
                            target.original_crew.is_dead = True
                        self.battle_log.append(f"{target.nama} telah gugur!")
                        # Check if all crew members are dead
                        if all(crew.is_dead for crew in self.player_crew):
                            self.battle_finished = True
                            self.sync_hp()
                            self.battle_log.append("Semua kru telah gugur!")
                else:
                    self.battle_log.append("Serangan musuh meleset!")

    def update(self):
        if not self.crew_selection_phase and not self.battle_finished:
            # Update crew movement
            for crew in self.player_crew:
                crew.move_towards_target()
                
            # Update enemy movement
            self.update_enemy_movement()
            
            # Update bullets
            self.update_bullets()

    def draw_battle_scene(self, screen, font):
        # Draw battle background
        pygame.draw.rect(screen, (30, 30, 30), (0, 0, 1000, 600))
        
        # Draw battle interface
        pygame.draw.rect(screen, (50, 50, 50), (50, 50, 900, 500), border_radius=10)
        
        # Draw enemy
        pygame.draw.rect(screen, (200, 50, 50), (int(self.enemy_x), int(self.enemy_y), self.enemy_width, self.enemy_height))
        enemy_health = f"Enemy HP: {self.enemy_hp}"
        health_text = font.render(enemy_health, True, (255, 0, 0))
        screen.blit(health_text, (int(self.enemy_x), int(self.enemy_y) - 30))

        # Draw crew members
        for i, crew in enumerate(self.player_crew):
            color = (0, 255, 0) if crew == self.selected_crew else (100, 100, 100)
            if crew.is_dead:
                color = (100, 0, 0)
            pygame.draw.rect(screen, color, (int(crew.x), int(crew.y), crew.width, crew.height))
            
            # Draw crew info
            crew_name = font.render(crew.nama, True, (255, 255, 255))
            crew_hp = font.render(f"HP: {crew.hp}", True, (255, 255, 255))
            screen.blit(crew_name, (int(crew.x), int(crew.y) - 30))
            screen.blit(crew_hp, (int(crew.x), int(crew.y) + crew.height + 10))

        # Draw bullets
        for bullet in self.bullets:
            pygame.draw.circle(screen, (255, 255, 0), (int(bullet['x']), int(bullet['y'])), bullet['radius'])

        # Draw battle log
        log_surface = pygame.Surface((400, 150))
        log_surface.fill((20, 20, 20))
        for i, log in enumerate(self.battle_log[-5:]):
            log_text = font.render(log, True, (255, 255, 255))
            log_surface.blit(log_text, (10, i * 30))
        screen.blit(log_surface, (50, 50))

        # Draw controls help
        controls = font.render("SPACE: Serang | 1-5: Pilih Kru | WASD/Arrows: Gerak Kru", True, (255, 255, 255))
        screen.blit(controls, (350, 550))
    
    def draw(self, screen):
        # Draw battle interface
        font = pygame.font.Font(None, 36)

        if self.crew_selection_phase:
            # Draw crew selection interface
            title = font.render("Pilih Crew untuk Battle (Max: 3)", True, (255, 255, 255))
            screen.blit(title, (300, 50))

            # Draw all available crew
            for i, crew in enumerate(self.all_crew):
                color = (0, 255, 0) if crew in self.player_crew else (200, 200, 200)
                pygame.draw.rect(screen, color, (100 + i*150, 400, 100, 100))
                crew_name = font.render(crew.nama, True, (0, 0, 0))
                screen.blit(crew_name, (100 + i*150, 360))

            # Draw start battle button if crew is selected
            if len(self.player_crew) > 0:
                pygame.draw.rect(screen, (0, 255, 0), (350, 550, 200, 50))
                start_text = font.render("Mulai Battle!", True, (0, 0, 0))
                screen.blit(start_text, (380, 565))
        else:
            self.draw_battle_scene(screen, font)
    
    def handle_movement_input(self, keys):
        if self.selected_crew and not self.crew_selection_phase:
            move_speed = 5
        
        # Handle WASD and arrow keys
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.selected_crew.target_x -= move_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.selected_crew.target_x += move_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.selected_crew.target_y -= move_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.selected_crew.target_y += move_speed
            
        # Keep crew within bounds
        self.selected_crew.target_x = max(50, min(self.selected_crew.target_x, 500))
        self.selected_crew.target_y = max(100, min(self.selected_crew.target_y, 450))