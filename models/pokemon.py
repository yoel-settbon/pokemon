import random

class Pokemon:
    def __init__(self, name, level, hp, attacks):
        self.name = name
        self.level = level
        self.hp = hp
        self.attacks = attacks

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def is_alive(self):
        return self.hp > 0

    def attack(self, other_pokemon):
        attack = random.choice(self.attacks)
        damage = random.randint(5, 15)
        print(f"{self.name} attaque {other_pokemon.name} avec {attack} pour {damage} dégâts.")
        other_pokemon.take_damage(damage)