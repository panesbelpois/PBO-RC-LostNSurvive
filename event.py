import pygame
import random

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
