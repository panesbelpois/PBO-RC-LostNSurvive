import random

class Wagon:
    def __init__(self):
        self.inventory = {
            "food": [],
            "drink": [],
            "general": [],
            "uang": 0
        }
        self.is_moving = False
        self.position = 0
        self.end_position = 170
        self.capacity = 5
        self.crew_list = []
        self.dead_crew_list = [] 
        self.crew_list = []
        self.dead_crew_list = []

    def berjalan(self):
        if self.position >= self.end_position:
            print("Wagon telah mencapai tujuan akhir! 🎉 Game selesai.")
            return "Wagon telah mencapai tujuan akhir! 🎉 Game selesai."

        if not self.is_moving:
            self.is_moving = True
            jarak_tempuh = random.randint(4, 14)
            self.position += jarak_tempuh

            if self.position >= self.end_position:
                self.position = self.end_position
                return f"Wagon berjalan sejauh {jarak_tempuh} km dan mencapai tujuan akhir! 🎉"
            else:
                return f"Wagon berjalan sejauh {jarak_tempuh} km. Posisi sekarang: {self.position} km."
        else:
            return "Wagon sudah berjalan."

    def berhenti(self):
        if self.is_moving:
            self.is_moving = False
            return f"Wagon berhenti di posisi {self.position} km."
        else:
            return "Wagon sudah berhenti."

    def add_crew(self, crew):
        for existing_crew in self.crew_list:
            if existing_crew.nama == crew.nama:
                return False, f"Sudah ada kru bernama {crew.nama}!"
                
        if len(self.crew_list) < self.capacity:
            self.crew_list.append(crew)
            return True, f"{crew.nama} bergabung dengan kru."
        return False, "Kru sudah penuh! (Maks. 5)"
    
    def get_crew_names(self):
        return [crew.nama for crew in self.crew_list]

    def update_crew(self):
        dead_crew = []
        for crew in self.crew_list:
            if crew.is_dead or crew.status == "Mati":
                dead_crew.append(crew)
        
        for crew in dead_crew:
            self.crew_list.remove(crew)
            self.dead_crew_list.append(crew)
            
        return dead_crew
    
    @property
    def status(self):
        return "berjalan" if self.is_moving else "berhenti"