class Crew:
    def __init__(self, name, hunger, thirst, attack, health, status="Sehat"):
        self.nama = name
        self.__hunger = hunger
        self.__thirst = thirst
        self.attack = attack
        self.hp = health
        self.status = status
        self.maxh = 100
        self.maxt = 100
        self.is_dead = False

    def change_status(self, new_status):
        self.status = new_status
        if new_status == "Mati":
            self.is_dead = True
            self.hp = 0

    def receive_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.is_dead = True
            print(f"{self.nama} telah gugur!")

    def attack_enemy(self, enemy):
        if not self.is_dead:
            print(f"{self.nama} menyerang musuh!")
            enemy.receive_damage(self.attack)