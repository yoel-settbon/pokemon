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
        """Réduit les points de vie du Pokémon après une attaque."""
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def is_alive(self):
        """Retourne True si le Pokémon est toujours en vie."""
        return self.hp > 0

    def attack_pokemon(self, other_pokemon):
        """Attaque un autre Pokémon et inflige des dégâts."""
        if not self.attacks:
            print(f"{self.name} n'a aucune attaque disponible !")
            return 0  # Aucun dégât infligé

        attack = random.choice(self.attacks)  # Choisir une attaque aléatoire
        damage = random.randint(5, self.attack)  # Dégâts entre 5 et la valeur d'attaque du Pokémon
        print(f"{self.name} attaque {other_pokemon.name} avec {attack} et inflige {damage} dégâts.")
        other_pokemon.take_damage(damage)
        return damage
