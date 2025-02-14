import pygame
import sys

pygame.init()

class Menu:
    def __init__(self, width, height, background_image, font_path, menu_options):
        self.width = width
        self.height = height
        self.menu_options = menu_options
        self.selected_option = 0

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pokemon Fighters")

        self.background = pygame.image.load(background_image)
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        self.menu_font = pygame.font.Font(font_path, 60)
        self.title_font = pygame.font.Font(font_path, 100)

    def draw_text(self, text, font, color, x, y):
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        self.screen.blit(text_surf, text_rect)

    def draw_menu(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_text("FIGHTERS", self.title_font, (255, 255, 255), self.width // 2.6, self.height // 2.4)
        
        for i, option in enumerate(self.menu_options):
            color = (255, 150, 203) if i == self.selected_option else (255, 255, 255)
            text = self.menu_font.render(option, True, color)
            text_rect = text.get_rect(center=(self.width // 2.6, self.height // 1.5 + i * 50))
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                elif event.key == pygame.K_RETURN:
                    if self.menu_options[self.selected_option] == 'New Game':
                        game = Game()
                        game.run()
                    elif self.menu_options[self.selected_option] == 'Load Game':
                        print("Chargement du jeu...")
                    elif self.menu_options[self.selected_option] == 'Quit':
                        return False
        return True

    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.draw_menu()
        
        pygame.quit()
        sys.exit()

class Player:
    def __init__(self, name):
        self.name = name
        self.pokemon = []

    def add_pokemon(self, pokemon):
        self.pokemon.append(pokemon)

    def remove_pokemon(self, pokemon):
        self.pokemon.remove(pokemon)

    def has_pokemon(self):
        return len(self.pokemon) > 0

import json
class Pokedex:
    def __init__(self, json_file):
        with open(json_file, "r", encoding="utf-8") as f:
            self.data = json.load(f)
    
    def get_pokemon_by_name(self, name):
        for p in self.data["all_pokemons"]:
            if p["name"] == name:
                return Pokemon(**p)
        return None
    
    def get_player_pokemon(self):
        return [Pokemon(**p) for p in self.data["player_pokemon"]]

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

import pygame
import random

class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1100, 700
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Combat Pokémon")

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.background = pygame.image.load("assets/image/battle.webp")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

        self.pikachu = self.Pokemon("Pikachu", 100, 20)
        self.charmander = self.Pokemon("Charmander", 100, 15)
        self.bulbasaur = self.Pokemon("Bulbasaur", 100, 18)
        self.squirtle = self.Pokemon("Squirtle", 100, 16)

        self.player_pokemon = self.choose_pokemon()
        self.opponent_pokemon = random.choice([self.pikachu, self.charmander, self.bulbasaur, self.squirtle])
        self.player_message = ""
        self.opponent_message = ""

    class Pokemon:
        def __init__(self, name, hp, attack):
            self.name = name
            self.hp = hp
            self.max_hp = hp
            self.attack = attack

        def attack_pokemon(self, other):
            damage = random.randint(0, self.attack)
            other.hp -= damage
            return damage

        def reset_hp(self):
            self.hp = self.max_hp

    def display_pokemon_choice(self, selected_index):
        self.win.blit(self.background, (0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render("Choisissez votre Pokémon:", True, self.WHITE)
        self.win.blit(text, (50, 50))
        options = ["Pikachu", "Charmander", "Bulbasaur", "Squirtle"]
        for i, option in enumerate(options):
            color = self.WHITE if i != selected_index else (255, 0, 0)
            text = font.render(option, True, color)
            self.win.blit(text, (50, 100 + i * 50))
        pygame.display.flip()

    def choose_pokemon(self):
        selected_index = 0
        self.display_pokemon_choice(selected_index)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_index = (selected_index - 1) % 4
                    elif event.key == pygame.K_DOWN:
                        selected_index = (selected_index + 1) % 4
                    elif event.key == pygame.K_RETURN:
                        return [self.pikachu, self.charmander, self.bulbasaur, self.squirtle][selected_index]
                    self.display_pokemon_choice(selected_index)

    def run(self):
        while True:
            running = True
            player_turn = True
            self.player_pokemon.reset_hp()
            self.opponent_pokemon = random.choice([self.pikachu, self.charmander, self.bulbasaur, self.squirtle])
            self.opponent_pokemon.reset_hp()
            self.player_message = ""
            self.opponent_message = ""

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and player_turn:
                            damage = self.player_pokemon.attack_pokemon(self.opponent_pokemon)
                            self.player_message = f"{self.player_pokemon.name} attaque {self.opponent_pokemon.name} et inflige {damage} dégâts!"
                            if self.opponent_pokemon.hp <= 0:
                                self.player_message += f" {self.opponent_pokemon.name} est KO!"
                                running = False
                            player_turn = False

                if not player_turn and self.opponent_pokemon.hp > 0:
                    damage = self.opponent_pokemon.attack_pokemon(self.player_pokemon)
                    self.opponent_message = f"{self.opponent_pokemon.name} attaque {self.player_pokemon.name} et inflige {damage} dégâts!"
                    if self.player_pokemon.hp <= 0:
                        self.opponent_message += f" {self.player_pokemon.name} est KO!"
                        running = False
                    player_turn = True

                self.win.blit(self.background, (0, 0))
                font = pygame.font.Font(None, 36)
                text = font.render(f"{self.player_pokemon.name} HP: {self.player_pokemon.hp}", True, self.WHITE)
                self.win.blit(text, (30, 500))
                text = font.render(f"{self.opponent_pokemon.name} HP: {self.opponent_pokemon.hp}", True, self.WHITE)
                self.win.blit(text, (860, 200))
                player_message_text = font.render(self.player_message, True, self.WHITE)
                self.win.blit(player_message_text, (30, 450))
                opponent_message_text = font.render(self.opponent_message, True, self.WHITE)
                self.win.blit(opponent_message_text, (50, 200))
                pygame.display.flip()

                pygame.time.delay(1000)

            if self.player_pokemon.hp <= 0:
                self.player_pokemon = self.choose_pokemon()
            else:
                self.player_pokemon.reset_hp()

if __name__ == "__main__":
    game = Game()
    game.run()