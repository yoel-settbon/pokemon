import random
class Pokemon:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.attack = attack

    def attack_pokemon(self, opponent):
        if self == opponent:
            return 0
        damage = random.randint(0, self.attack)
        opponent.hp -= damage
        return damage
    def reset_hp(self):
        self.hp = 100