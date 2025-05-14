import random
import pygame

class Event:
    def __init__(self):
        self.events_musuh = [
            "Tiba di wilayah musuh! Mereka memantau pergerakan wagon.",
            "Kamu memasuki daerah berbahaya! Musuh bisa menyerang kapan saja."
        ]
        self.events_cuaca = [
            "Terjadi banjir! Perjalanan tertunda dan crew kehilangan stamina.",
            "Badai pasir datang! Crew kesulitan bernapas dan wagon melambat.",
            "Cuaca cerah! Perjalanan lebih cepat dan crew merasa segar.",
            "Hujan turun deras! Crew merasa kedinginan, tapi tanah menjadi subur."
        ]
        self.events_quest = [
            "Berhenti di desa yang menawarkan food dan drink.",
            "Sampai di kota dengan kesempatan untuk membantu warga dan mendapatkan hadiah.",
            "Berjumpa dengan seorang NPC yang menawarkan pencarian misterius."
        ]
        self.current_event = ""

    def get_random_event(self):
        all_events = self.events_musuh + self.events_cuaca + self.events_quest
        return random.choice(all_events)

    def process_event(self, wagon):
        event_terjadi = self.get_random_event()
        self.current_event = f"{event_terjadi}"
        print(self.current_event)

        if len(wagon.crew_list) == 0:
            return self.current_event

        crew_affected = []
        effect_message = ""

        if "banjir" in event_terjadi:
            crew_affected = random.sample(wagon.crew_list, k=1)
            for crew in crew_affected:
                crew.change_status("Penyakit Air")
                effect_message = f"{crew.nama} terkena Penyakit Air!"

        elif "Badai pasir" in event_terjadi:
            crew_affected = random.sample(wagon.crew_list, k=1)
            for crew in crew_affected:
                crew.change_status("Dehidrasi")
                effect_message = f"{crew.nama} mengalami Dehidrasi!"

        elif "Hujan turun deras" in event_terjadi:
            crew_affected = random.sample(wagon.crew_list, k=1)
            for crew in crew_affected:
                crew.change_status("Hipotermia")
                effect_message = f"{crew.nama} terkena Hipotermia!"

        elif "Wilayah Musuh" in event_terjadi or "berbahaya" in event_terjadi:
            crew_affected = random.sample(wagon.crew_list, k=1)
            for crew in crew_affected:
                if random.random() < 0.3:
                    crew.change_status("Mati")
                    effect_message = f"{crew.nama} terluka parah dan meninggal!"

        if effect_message:
            self.current_event += "\n" + effect_message

        dead_crew = wagon.update_crew()
        if dead_crew:
            for crew in dead_crew:
                if effect_message and crew.nama in effect_message:
                    pass
                else:
                    self.current_event += f"\n{crew.nama} telah meninggal dan dihapus dari kru."

        return self.current_event

    def trigger_death_event(self, wagon):
        """Special event that has a high chance of killing a crew member"""
        if len(wagon.crew_list) == 0:
            return "Tidak ada kru yang tersisa untuk dibunuh!"
            
        crew = random.choice(wagon.crew_list)
        crew.change_status("Mati")
        
        wagon.update_crew()
        
        return f"⚠️ Kejadian tragis! {crew.nama} telah meninggal dan dihapus dari kru."
    
    def trigger_death_event(self, wagon):
        """Special event that has a high chance of killing a crew member"""
        if len(wagon.crew_list) == 0:
            return "Tidak ada kru yang tersisa untuk dibunuh!"

        crew = random.choice(wagon.crew_list)
        crew.change_status("Mati")

        wagon.update_crew()

        return f"⚠️ Kejadian tragis! {crew.nama} telah meninggal dan dihapus dari kru."

    def trigger_battle(self, wagon, screen, font):
        """Memulai pertempuran dengan musuh"""
        if len(wagon.crew_list) == 0:
            return "Tidak ada kru yang tersisa untuk bertarung!"

        enemy_hp = random.randint(50, 100)
        enemy_atk = random.randint(10, 25)
        battle_log = []
        selected_crew = None
        turn = 1
        battle_won = False

        # Pilih crew untuk bertarung
        battle_log.append("Pilih crew untuk bertarung (1-" + str(len(wagon.crew_list)) + "):")
        for i, crew in enumerate(wagon.crew_list, 1):
            if not crew.is_dead:
                battle_log.append(f"{i}. {crew.nama} - HP: {crew.hp} - ATK: {crew.attack}")

        # Draw battle scene
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Battle dibatalkan"

                if event.type == pygame.KEYDOWN:
                    if not selected_crew:
                        if pygame.K_1 <= event.key <= pygame.K_9:
                            crew_index = event.key - pygame.K_1
                            if crew_index < len(wagon.crew_list):
                                selected_crew = wagon.crew_list[crew_index]
                                battle_log.append(f"{selected_crew.nama} memasuki pertempuran!")

                    elif event.key == pygame.K_SPACE and selected_crew:
                        # Execute turn
                        if turn <= 3:  # Max 3 turns
                            battle_log.append(f"=== Turn {turn} ===")

                            # Crew attacks
                            if random.random() < 0.7:
                                enemy_hp -= selected_crew.attack
                                battle_log.append(f"Hit! Enemy HP: {enemy_hp}")
                            else:
                                battle_log.append("Serangan meleset!")

                            # Enemy attacks
                            if random.random() < 0.5:
                                selected_crew.hp -= enemy_atk
                                battle_log.append(f"{selected_crew.nama} HP: {selected_crew.hp}")
                            else:
                                battle_log.append("Musuh meleset!")

                            # Check battle end
                            if enemy_hp <= 0:
                                battle_log.append("Musuh dikalahkan!")
                                battle_won = True
                                running = False
                            elif selected_crew.hp <= 0:
                                battle_log.append(f"{selected_crew.nama} telah jatuh!")
                                selected_crew.change_status("Mati")
                                running = False

                            turn += 1
                            if turn > 3:
                                battle_log.append("Waktu habis! Pertempuran berakhir!")
                                running = False

            # Draw battle scene
            screen.fill((0, 0, 0))
            pygame.draw.rect(screen, (50, 50, 50), (100, 100, 600, 400))

            # Draw enemy stats
            pygame.draw.rect(screen, (200, 50, 50), (500, 150, 150, 80))
            enemy_text = font.render(f"Enemy HP: {enemy_hp}", True, (255, 255, 255))
            screen.blit(enemy_text, (520, 170))

            # Draw battle log
            y_pos = 300
            for log in battle_log[-3:]:  # Show last 3 messages
                text = font.render(log, True, (255, 255, 255))
                screen.blit(text, (150, y_pos))
                y_pos += 30

            pygame.display.flip()
            pygame.time.delay(50)

        result = "Pertempuran dimenangkan!" if battle_won else f"{selected_crew.nama} kalah dalam pertempuran!"
        wagon.update_crew()  # Update crew list after battle
        return result
