class Pokemon:
    def __init__(self, name, type, pv, attack, defense, speed, attacks, evolution=None):
        self.name = name
        self.type = type
        self.pv = pv
        self.pv_max = pv
<<<<<<< HEAD
        self.attack = attack  # Garde l'attribut 'attack' pour la puissance de base
=======
        self.attack = attack
>>>>>>> origin/pre-game
        self.defense = defense
        self.speed = speed
        self.attacks = attacks
        self.evolution = evolution

    def display_info(self):
        info = f"{self.name} ({self.type}) - PV: {self.pv}/{self.pv_max}, ATK: {self.attack}, DEF: {self.defense}, VIT: {self.speed}\n"
        info += "Attacks :\n"
        for attack in self.attacks:
            info += f"  - {attack['name']} ({attack['type']}, Power: {attack['power']})\n"
        return info.strip()
    
<<<<<<< HEAD
    def perform_attack(self, other_pokemon, attack_name):  # Nouveau nom pour éviter le conflit
        attack = next((a for a in self.attacks if a["name"] == attack_name), None)
        if attack:
            damage = max(attack["power"] - other_pokemon.defense, 1)
            other_pokemon.pv = max(other_pokemon.pv - damage, 0)  # Corrige aussi 'hp' en 'pv'
            return f"{self.name} used {attack_name}! {other_pokemon.name} lost {damage} HP."
        return f"{self.name} does not know this attack!"

    def is_ko(self):
        return self.pv <= 0  # Correction de 'hp' en 'pv'
=======
    def attack(self, other_pokemon, attack_name):
        attack = next((a for a in self.attacks if a["name"] == attack_name), None)
        if attack:
            damage = max(attack["power"] - other_pokemon.defense, 1)
            other_pokemon.hp = max(other_pokemon.hp - damage, 0)
            return f"{self.name} used {attack_name}! {other_pokemon.name} lost {damage} HP."
        return f"{self.name} does not know this attack !"
    
    def is_ko(self):
        return self.hp <= 0
>>>>>>> origin/pre-game
