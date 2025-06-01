from crew import Crew
import random

class Chef(Crew):
    def __init__(self, name):
        super().__init__(name, hunger=50, thirst=50, attack=10, health=100)
    
    def cook(self):
        print(f"{self.nama} sedang memasak makanan lezat!")
        self.hp = min(self.hp + 30, 100) 

class Hunter(Crew):
    def __init__(self, name):
        super().__init__(name, hunger=50, thirst=50, attack=20, health=100)
    
    def hunt(self):
        print(f"{self.nama} sedang berburu mangsa.")
        self.attack += 20  
    
class Police(Crew):
    def __init__(self, name):
        super().__init__(name, hunger=50, thirst=50, attack=35, health=100)
        self.damage_reduction = 0.85  
        self.protected_radius = 20

    def enforce_law(self):
        print(f"{self.nama} sedang menegakkan hukum dan mengurangi ancaman kriminal.")
        print(f"Selama {self.protected_radius} km perjalanan, tidak akan ada aktivitas kriminal.")

    def receive_damage(self, damage):
        reduced_damage = damage * self.damage_reduction
        self.hp -= reduced_damage
        print(f"{self.nama} menerima {reduced_damage:.2f} damage setelah pengurangan.")

class Infantry(Crew):
    def __init__(self, name):
        super().__init__(name, hunger=50, thirst=50, attack=35, health=100)
        self.damage_reduction = 0.65  
        self.protected_radius = 20
        self.bonus_damage = 1.07

    def enforce_law(self):
        print(f"{self.nama} sedang menegakkan hukum dan mengurangi ancaman kriminal.")
        print(f"Selama {self.protected_radius} km perjalanan, tidak akan ada aktivitas kriminal.")

    def receive_damage(self, damage):
        reduced_damage = damage * self.damage_reduction
        self.hp -= reduced_damage
        print(f"{self.nama} menerima {reduced_damage:.2f} damage setelah pengurangan.")

    def shoot(self):
        fire_damage = self.attack * self.bonus_damage 
        print(f"{self.nama} menembakkan senjata api! Damage meningkat menjadi {fire_damage:.2f}.")
        return fire_damage

class Nurse(Crew):
    def __init__(self, name):
        super().__init__(name, hunger=45, thirst=50, attack=10, health=100)

    def heal_crew(self, target_crew):
        heal_amount = int(target_crew.hp * 0.25) 
        target_crew.hp = min(target_crew.hp + heal_amount, 100)
        print(f"{self.nama} menyembuhkan {target_crew.nama}. HP sekarang: {target_crew.hp}")

class Doctor(Crew):
    def __init__(self, name):
        super().__init__(name, hunger=40, thirst=45, attack=12, health=100)

    def medical_treatment(self, target_crew):
        heal_amount = int(target_crew.hp * 0.40) 
        target_crew.hp = min(target_crew.hp + heal_amount, 100)
        print(f"{self.nama} memberikan perawatan medis kepada {target_crew.nama}. HP sekarang: {target_crew.hp}")

class Thief(Crew):
    def __init__(self, name):
        super().__init__(name, hunger=50, thirst=50, attack=15, health=100)
        self.dodge_chance = 0.40  
        self.loot_bonus = 1.15  

    def dodge(self):
        if random.random() < self.dodge_chance:
            print(f"{self.nama} berhasil menghindari serangan saat perjalanan!")
            return True
        else:
            print(f"{self.nama} gagal menghindar.")
            return False

    def loot(self, wagon):
        loot_items = ["Makanan", "Minuman", "Item General"]
        loot_count = random.randint(1, 4)
        for _ in range(loot_count):
            item = random.choice(loot_items)
            bonus_qty = int(self.loot_bonus * 100 - 100)  
            wagon.inventory[item.lower()].append(f"{item} (Bonus {bonus_qty}%)")
        
        print(f"{self.nama} berhasil mencuri {loot_count} item dengan peningkatan loot {bonus_qty}%.")

class Agent(Crew):
    def __init__(self, name):
        super().__init__(name, hunger=45, thirst=50, attack=20, health=100)
        self.dodge_chance = 0.45 
        self.damage_bonus = 1.05  

    def dodge(self):
        if random.random() < self.dodge_chance:
            print(f"{self.nama} berhasil menghindari serangan saat perjalanan!")
            return True
        else:
            print(f"{self.nama} gagal menghindar.")
            return False

    def attack_boost(self):
        boosted_damage = self.attack * self.damage_bonus
        print(f"{self.nama} melakukan serangan dengan peningkatan damage {boosted_damage:.2f}.")
        return boosted_damage

class Musician(Crew):
    def __init__(self, name):
        super().__init__(name, hunger=45, thirst=50, attack=18, health=100)
        self.attack_bonus = 1.12  
        self.dodge_bonus = 0.07  

    def inspire_team(self, battle):
        print(f"{self.nama} memainkan musik yang membangkitkan semangat tim!")
        for crew in battle.crew_list:
            crew.attack *= self.attack_bonus
            print(f"{crew.nama} mendapatkan peningkatan attack: {crew.attack:.2f}")
            base_dodge = 0.15
            total_dodge_chance = base_dodge + self.dodge_bonus
            crew.dodge_chance = total_dodge_chance
            print(f"{crew.nama} mendapatkan peningkatan dodge: {total_dodge_chance * 100:.2f}%")

class Firefighter(Crew):
    def __init__(self, name):
        super().__init__(name, hunger=50, thirst=50, attack=20, health=100)
        self.damage_reduction = 0.83  
        self.heat_resistance = 0.75  

    def extinguish_fire(self):
        print(f"{self.nama} memadamkan api dan melindungi tim dari bahaya panas!")

    def receive_damage(self, damage, is_fire_damage=False):
        if is_fire_damage:
            final_damage = damage * self.heat_resistance 
            print(f"{self.nama} menerima {final_damage:.2f} damage akibat panas.")
        else:
            final_damage = damage * self.damage_reduction  
            print(f"{self.nama} menerima {final_damage:.2f} damage dari serangan biasa.")
        self.hp -= final_damage