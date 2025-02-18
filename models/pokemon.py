import random

class Pokemon:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack

    def attack_pokemon(self, other):
        damage = random.randint(0, 25)
        other.hp -= damage
        return damage

    def reset_hp(self):
        self.hp = self.max_hp