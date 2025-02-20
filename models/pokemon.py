import random
import pygame

class Pokemon:
    def __init__(self, name, hp, attack, image_path):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 30
        self.image_path = image_path
        self.image = pygame.image.load(self.image_path)
        self.max_level = 100

    def gain_experience(self, points):
        self.message = ""
        self.experience += points
        while self.experience >= self.experience_to_next_level:
            self.level_up()

    def level_up(self):
        self.experience -= self.experience_to_next_level
        self.level += 1
        self.attack += 5
        self.experience_to_next_level = 30 + (self.level - 2) * 20
    
    def reset_hp(self):
        self.hp = self.max_hp

    def attack_pokemon(self, opponent):
        damage = random.randint(1, self.attack)
        opponent.hp -= damage
        return damage