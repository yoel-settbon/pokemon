class Pokemon:
    def __init__(self, name, type, pv, attack, defense, speed, attacks, evolution=None):
        self.name = name
        self.type = type
        self.pv = pv
        self.pv_max = pv
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.attacks = attacks
        self.evolution = evolution

    def display_stats(self):
        info = f"{self.name} ({self.type}) - PV: {self.pv}/{self.pv_max}, ATK: {self.attack}, DEF: {self.defense}, VIT: {self.speed}\n"
        info += "Attacks :\n"
        for attack in self.attacks:
            info += f"  - {attack['name']} ({attack['type']}, Power: {attack['power']})\n"
        return info.strip()