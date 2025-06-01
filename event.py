import random
import pygame
from battle import Battle, Character

class Event:
    def __init__(self):
        self.events_musuh = [
            {"deskripsi": "Tiba di wilayah musuh!",
             "pilihan": ["Melawan", "Memutari jalan"],
             "konsekuensi": {"Melawan": "Pertarungan dimulai!", "Memutari jalan": "Jarak perjalanan dikurangi 1-4 km."}},
            {"deskripsi": "Kamu memasuki daerah berbahaya!",
             "pilihan": ["Melawan", "Menghindari pertempuran"],
             "konsekuensi": {"Melawan": "Pertarungan dimulai!", "Menghindari pertempuran": "Kehilangan sedikit persediaan akibat bergerak diam-diam."}},
            {"deskripsi": "Geng kriminal menghadang perjalanan!",
             "pilihan": ["Melawan", "Memutari jalan"],
             "konsekuensi": {"Melawan": "Pertarungan dimulai!", "Memutari jalan": "Jarak perjalanan dikurangi 1-4 km."}},
            {"deskripsi": "Bandit gurun muncul dari balik bukit!",
             "pilihan": ["Melawan", "Menghindari pertempuran"],
             "konsekuensi": {"Melawan": "Pertarungan dimulai!", "Menghindari pertempuran": "Kehilangan sedikit persediaan akibat bergerak diam-diam."}}
        ]
        self.events_cuaca = [
            {"deskripsi": "Terjadi banjir!.",
             "pilihan": ["Istirahat", "Tetap melanjutkan perjalanan"],
             "konsekuensi": {"Istirahat": "Crew memulihkan stamina dengan istirahat.", "Tetap melanjutkan perjalanan": "Crew kehilangan stamina akibat banjir."}},
            {"deskripsi": "Badai pasir datang!",
             "pilihan": ["Gunakan masker khusus", "Tetap berjalan dengan lambat"],
             "konsekuensi": {"Gunakan masker khusus": "Crew tetap sehat.", "Tetap berjalan dengan lambat": "Wagon berjalan lebih lambat, perjalanan tertunda."}},
            {"deskripsi": "Cuaca cerah!",
             "pilihan": ["Nikmati cuaca", "Tetap waspada"],
             "konsekuensi": {"Nikmati cuaca": "Perjalanan lebih cepat!", "Tetap waspada": "Crew tetap siaga terhadap kemungkinan kejutan."}},
            {"deskripsi": "Hujan turun deras! Crew merasa kedinginan.",
             "pilihan": ["Menepi dan berlindung", "Tetap melanjutkan perjalanan"],
             "konsekuensi": {"Menepi dan berlindung": "Crew menghindari kedinginan.", "Tetap melanjutkan perjalanan": "Crew kehilangan stamina akibat cuaca dingin."}}
        ]
        self.events_quest = [
            {"deskripsi": "Berhenti di desa yang menawarkan food dan drink.",
             "pilihan": ["Terima", "Tolak"],
             "konsekuensi": {"Terima": "Mendapatkan makanan dan minuman.", "Tolak": "Melanjutkan perjalanan tanpa persediaan tambahan."}},
            {"deskripsi": "Menjelajahi kota mati!",
             "pilihan": ["Menjelajah", "Mengabaikan"],
             "konsekuensi": {"Menjelajah": "Menemukan persediaan!", "Mengabaikan": "Melanjutkan perjalanan dengan risiko kelaparan."}},
            {"deskripsi": "Sampai di kota dan membantu warga",
             "pilihan": ["Bantu warga", "Lanjutkan perjalanan"],
             "konsekuensi": {"Bantu warga": "Mendapatkan hadiah dari penduduk.", "Lanjutkan perjalanan": "Tidak mendapatkan bantuan atau hadiah."}},
            {"deskripsi": "Berburu di kota mati! Crew mencari persediaan!",
             "pilihan": ["Berburu", "Lewati lokasi"],
             "konsekuensi": {"Berburu": "Berhasil mendapatkan beberapa persediaan!", "Lewati lokasi": "Melanjutkan perjalanan tanpa tambahan persediaan."}}
        ]
        self.events = {
            "musuh": self.events_musuh,
            "cuaca": self.events_cuaca,
            "quest": self.events_quest
        }

    def generate_event(self):
        tipe_event = random.choice(list(self.events.keys()))
        event = random.choice(self.events[tipe_event])
        jarak = random.randint(1, 20)
        return jarak, event

    def tampilkan_event(self):
        jarak, event_terpilih = self.generate_event()
        print(f"Event dalam {jarak} km: {event_terpilih['deskripsi']}")
        print(f"Pilihan: {event_terpilih['pilihan'][0]} / {event_terpilih['pilihan'][1]}")
        return jarak, event_terpilih

    def proses_pilihan(self, event, pilihan):
        if pilihan in event["konsekuensi"]:
            print(f"Konsekuensi: {event['konsekuensi'][pilihan]}")

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

    def trigger_event(self, game_hour):
        if 6 <= game_hour < 18:
            tipe_event = random.choice(list(self.events.keys()))
            event_terpilih = random.choice(self.events[tipe_event])
            event_terpilih["tipe"] = tipe_event 
            return event_terpilih
        else:
            return None
    
    def trigger_death_event(self, wagon):
        if len(wagon.crew_list) == 0:
            return "Tidak ada kru yang tersisa untuk dibunuh!"
            
        crew = random.choice(wagon.crew_list)
        crew.change_status("Mati")
        
        wagon.update_crew()
        
        return f"⚠ Kejadian tragis! {crew.nama} telah meninggal dan dihapus dari kru."
    
    def trigger_death_event(self, wagon):
        """Special event that has a high chance of killing a crew member"""
        if len(wagon.crew_list) == 0:
            return "Tidak ada kru yang tersisa untuk dibunuh!"

        crew = random.choice(wagon.crew_list)
        crew.change_status("Mati")

        wagon.update_crew()

        return f"⚠ Kejadian tragis! {crew.nama} telah meninggal dan dihapus dari kru."

    def apply_consequence(self, event, pilihan, wagon):
        tipe = event.get("tipe", "")
        msg = event["konsekuensi"].get(pilihan, "")
        if tipe == "musuh":
            if pilihan == "Memutari jalan":
                lost = random.randint(1, 4)
                wagon.position = max(0, wagon.position - lost)
                msg += f" (Jarak berkurang {lost} km)"
            elif pilihan == "Menghindari pertempuran":
                lost_food = random.randint(1, 3)
                lost_drink = random.randint(1, 2)
                if hasattr(wagon, "inventory"):
                    food = wagon.inventory.get("food", [])
                    drink = wagon.inventory.get("drink", [])
                    for _ in range(lost_food):
                        if food: food.pop()
                    for _ in range(lost_drink):
                        if drink: drink.pop()
                msg += f" (Kehilangan {lost_food} makanan & {lost_drink} minuman)"
        elif tipe == "cuaca":
            desc = event["deskripsi"].lower()
            if "banjir" in desc:
                if pilihan == "Istirahat":
                    for crew in getattr(wagon, "crew_list", []):
                        crew.hp = min(100, crew.hp + 10)
                    msg += " (+10 HP untuk semua kru)"
                elif pilihan == "Tetap melanjutkan perjalanan":
                    for crew in getattr(wagon, "crew_list", []):
                        crew.hp = max(1, crew.hp - 15)
                        if random.random() < 0.3:
                            crew.change_status("Penyakit Air")
                    msg += " (Crew kehilangan stamina dan berisiko sakit)"
            elif "badai pasir" in desc:
                if pilihan == "Gunakan masker khusus":
                    if hasattr(wagon, "inventory"):
                        food = wagon.inventory.get("food", [])
                        if food: food.pop()
                    msg += " (Menggunakan 1 makanan untuk masker)"
                elif pilihan == "Tetap berjalan dengan lambat":
                    for crew in getattr(wagon, "crew_list", []):
                        if random.random() < 0.4:
                            crew.change_status("Dehidrasi")
                    msg += " (Crew berisiko dehidrasi)"
            elif "cuaca cerah" in desc:
                if pilihan == "Nikmati cuaca":
                    wagon.position += 2
                    msg += " (+2 km perjalanan)"
                elif pilihan == "Tetap waspada":
                    for crew in getattr(wagon, "crew_list", []):
                        crew.attack += 2
                    msg += " (+2 ATK untuk semua kru)"
            elif "hujan" in desc:
                if pilihan == "Menepi dan berlindung":
                    msg += " (Waktu perjalanan bertambah)"
                elif pilihan == "Tetap melanjutkan perjalanan":
                    for crew in getattr(wagon, "crew_list", []):
                        crew.hp = max(1, crew.hp - 10)
                        if random.random() < 0.25:
                            crew.change_status("Hipotermia")
                    msg += " (Crew kedinginan dan kehilangan stamina)"
        elif tipe == "quest":
            if pilihan == "Terima":
                if hasattr(wagon, "inventory"):
                    wagon.inventory.setdefault("food", []).append(("Roti", 10))
                    wagon.inventory.setdefault("drink", []).append(("Air", 8))
                msg += " (+Roti & Air)"
            elif pilihan == "Menjelajah":
                if random.random() < 0.7:
                    if hasattr(wagon, "inventory"):
                        wagon.inventory.setdefault("food", []).append(("Daging", 12))
                    msg += " (+Daging)"
                else:
                    if wagon.crew_list:
                        crew = random.choice(wagon.crew_list)
                        crew.hp = max(1, crew.hp - 20)
                        msg += f" ({crew.nama} terluka -20 HP)"
            elif pilihan == "Bantu warga":
                if hasattr(wagon, "inventory"):
                    wagon.inventory.setdefault("food", []).append(("Hadiah", 15))
                msg += " (+Hadiah)"
            elif pilihan == "Berburu":
                if random.random() < 0.8:
                    if hasattr(wagon, "inventory"):
                        wagon.inventory.setdefault("food", []).append(("Hasil Buruan", 10))
                    msg += " (+Hasil Buruan)"
                else:
                    msg += " (Berburu gagal)"
        return msg

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

        battle_log.append("Pilih crew untuk bertarung (1-" + str(len(wagon.crew_list)) + "):")
        for i, crew in enumerate(wagon.crew_list, 1):
            if not crew.is_dead:
                battle_log.append(f"{i}. {crew.nama} - HP: {crew.hp} - ATK: {crew.attack}")

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
                        if turn <= 3: 
                            battle_log.append(f"=== Turn {turn} ===")

                            if random.random() < 0.7:
                                enemy_hp -= selected_crew.attack
                                battle_log.append(f"Hit! Enemy HP: {enemy_hp}")
                            else:
                                battle_log.append("Serangan meleset!")

                            if random.random() < 0.5:
                                selected_crew.hp -= enemy_atk
                                battle_log.append(f"{selected_crew.nama} HP: {selected_crew.hp}")
                            else:
                                battle_log.append("Musuh meleset!")

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

            screen.fill((0, 0, 0))
            pygame.draw.rect(screen, (50, 50, 50), (100, 100, 600, 400))

            pygame.draw.rect(screen, (200, 50, 50), (500, 150, 150, 80))
            enemy_text = font.render(f"Enemy HP: {enemy_hp}", True, (255, 255, 255))
            screen.blit(enemy_text, (520, 170))

            y_pos = 300
            for log in battle_log[-3:]: 
                text = font.render(log, True, (255, 255, 255))
                screen.blit(text, (150, y_pos))
                y_pos += 30

            pygame.display.flip()
            pygame.time.delay(50)

        result = "Pertempuran dimenangkan!" if battle_won else f"{selected_crew.nama} kalah dalam pertempuran!"
        wagon.update_crew()
        return result