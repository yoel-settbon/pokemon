import random

class Pokemon:
    def __init__(self, name, hp, attack, attacks):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.attacks = attacks

    def reset_hp(self):
        """Réinitialise les points de vie du Pokémon à leur valeur maximale."""
        self.hp = self.max_hp

    def take_damage(self, damage):
        """Réduit les points de vie du Pokémon après un attaque."""
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def is_alive(self):
        """Retourne True si le Pokémon est encore en vie, sinon False."""
        return self.hp > 0

    def attack(self, other_pokemon):
        """Attaque un autre Pokémon en choisissant un mouvement au hasard."""
        attack = random.choice(self.attacks)
        damage = random.randint(5, 15)
        print(f"{self.name} attaque {other_pokemon.name} avec {attack} pour {damage} dégâts.")
        other_pokemon.take_damage(damage)
