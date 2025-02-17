import pygame
import random
import time
import json
from pygame import *

pygame.init()

screen = pygame.display.set_mode((1250, 800))
background_fight = pygame.image.load("images/fight_template.png")
background_menu = pygame.image.load("images/menu_template_pokemon.jpg")
logo = pygame.image.load("images/logo_pokemon.png")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

text_font = pygame.font.SysFont("Arial", 30)
title_font = pygame.font.SysFont("Arial", 60)

def draw_text(text, text_font, color, x, y):
    text_surface = text_font.render(text, True, color)
    screen.blit(text_surface, (x, y))

with open('Pokemon.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

with open('Pokedex.json', 'r', encoding='utf-8') as file:
    data2 = json.load(file)


class Pokemon():
    def __init__(self, data):
        self.level = 5 
        self.pokedex_id = data["pokedex_id"]
        self.name = data["name"]["en"]
        self.sprite_front = data["sprites"]["front"]
        self.sprite_back = data["sprites"]["back"]
        self.types = [type_data["name"] for type_data in data["types"]]
        self.hp = int((data["stats"]["hp"]) / 50 * self.level)
        self.atk = (data["stats"]["atk"]) / 50 * self.level
        self.defense = data["stats"]["def"] / 50 * self.level
        self.resistances = [
            (resistance["name"], resistance["multiplier"])
            for resistance in data["resistances"]
        ]
        self.max_hp = int((data["stats"]["hp"]) / 50 * self.level)
        self.xp = 0  
        self.xp_to_next_level = 100  
        self.evolution = data["evolution"]["next"]

    def est_ko(self):
        return self.hp <= 0

    def gain_xp(self, xp_gagnee):
        self.xp += xp_gagnee
        while self.xp >= self.xp_to_next_level:
            self.gain_lvl()

    def gain_lvl(self):
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.15)  
        print(f"{self.name} monte au niveau {self.level} !")


class Fight():
    def __init__(self, player_pokemon, enemy_pokemon):
        self.player_pokemon = player_pokemon
        self.enemy_pokemon = enemy_pokemon
        self.run = True

    def display_pokemon(self):
        player_sprite = pygame.image.load(self.player_pokemon.sprite_back)
        screen.blit(player_sprite, (100, 500))
        draw_text(f"{self.player_pokemon.name} - Nv. {self.player_pokemon.level} - {self.player_pokemon.hp} HP", text_font, BLACK, 100, 450)

        enemy_sprite = pygame.image.load(self.enemy_pokemon.sprite_front)
        screen.blit(enemy_sprite, (800, 100))
        draw_text(f"{self.enemy_pokemon.name} - Nv. {self.enemy_pokemon.level} - {self.enemy_pokemon.hp} HP", text_font, BLACK, 800, 50)

    def menu_between(self):
        self.choose = ["Fight","Pokedex","Save & Quit"] 
        self.choose_index = 0
        screen.blit(background_menu, (0, 0))
        draw_text("Fight", text_font, BLACK, 100, 450)
        draw_text("Pokedex", text_font, BLACK, 300, 450)
        draw_text("Save & Quit", text_font, BLACK, 500, 450)
        while True : 
            for i, choice in enumerate(self.choose):
                x_position = 100 + i * 200
                x_position2 = 105 + i * 200
                color = YELLOW if i == self.choose_index else BLUE
                pygame.draw.rect(screen, YELLOW, (x_position, 20, 410, 160))
                pygame.draw.rect(screen, color, (x_position2, 25, 400, 150))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.choose_index = (self.choose_index - 1) % len(self.choose)
                    if event.key == pygame.K_RIGHT:
                        self.choose_index = (self.choose_index + 1) % len(self.choose)
                    if event.key == pygame.K_RETURN:
                        if self.choose_index == 0:
                            self.fight()
                        if self.choose_index == 1:
                            self.fight()
                        if self.choose_index == 2:
                            game.save_player_pokedex()
                            return False
            pygame.display.update()

    def attack(self):
        damage = int(max(0, self.player_pokemon.atk - (self.enemy_pokemon.defense) / 2))
        self.enemy_pokemon.hp -= damage
        draw_text(f"{self.player_pokemon.name} attaque et inflige {damage} dégâts !", text_font, BLACK, 100, 600)

        if self.enemy_pokemon.hp <= 0:
            draw_text(f"{self.enemy_pokemon.name} est KO !", text_font, BLACK, 100, 650)
            xp_gained = self.calculate_xp_gain()
            self.player_pokemon.gain_xp(xp_gained)
            draw_text(f"{self.player_pokemon.name} gagne {xp_gained} points d'expérience !", text_font, BLACK, 100, 700)
            
            game.add_pokemon_to_pokedex(self.enemy_pokemon)
            
            self.player_pokemon.hp = self.player_pokemon.max_hp
            
            self.enemy_pokemon = game.new_wild_pokemon()
            
            self.menu_between()

        if self.player_pokemon.hp <= 0:
            draw_text(f"{self.player_pokemon.name} est KO !", text_font, BLACK, 100, 750)
            self.menu_between()

    def enemy_attack(self):
        damage = int(max(0, self.enemy_pokemon.atk - (self.player_pokemon.defense / 2)))
        self.player_pokemon.hp -= damage
        draw_text(f"{self.enemy_pokemon.name} attaque et inflige {damage} dégâts !", text_font, BLACK, 100, 700)

        if self.player_pokemon.hp <= 0:
            draw_text(f"{self.player_pokemon.name} est KO !", text_font, BLACK, 100, 750)
            self.menu_between()

    def calculate_xp_gain(self):
        base_xp = 50 
        xp_gained = base_xp * (self.enemy_pokemon.level/2)  
        return max(10, xp_gained)  
    
    def fight(self):
        self.fight_options = ["Attack", "Run", "Switch Pokemon"]
        self.fight_index = 0
        while self.run:
            screen.blit(background_fight, (0, 0))
            self.display_pokemon()
            draw_text(f"Exp : {self.player_pokemon.xp} / {self.player_pokemon.xp_to_next_level}", text_font, BLACK, 100, 350) 
            draw_text("Attack", text_font, BLACK, 100, 650)
            draw_text("Run", text_font, BLACK, 300, 650)
            draw_text("Pokemon", text_font, BLACK, 500, 650)
            for i, option in enumerate(self.fight_options):
                x_position = 100 + i * 200
                x_position2 = 105 + i * 200
                color = YELLOW if i == self.fight_index else BLUE
                pygame.draw.rect(screen, YELLOW, (x_position, 620, 410, 160))
                pygame.draw.rect(screen, color, (x_position2, 625, 400, 150))
                draw_text(option, text_font, BLACK, x_position2 + 50, 650)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.fight_index = (self.fight_index - 1) % len(self.fight_options)
                    if event.key == pygame.K_RIGHT:
                        self.fight_index = (self.fight_index + 1) % len(self.fight_options)
                    if event.key == pygame.K_RETURN:
                        if self.fight_index == 0:  
                            self.attack()  
                            if not self.enemy_pokemon.est_ko(): 
                                self.enemy_attack()  
                            else:
                                self.player_pokemon.hp = self.player_pokemon.max_hp
                                self.enemy_pokemon = game.new_wild_pokemon()
                                self.menu_between()  
                        elif self.fight_index == 1: 
                            self.player_pokemon.hp = self.player_pokemon.max_hp
                            self.enemy_pokemon = game.new_wild_pokemon()
                            self.menu_between()
                        elif self.fight_index == 2: 
                            self.menu_between()

            pygame.display.update()


class Game():
    def __init__(self):
        self.player_pokedex = self.load_player_pokedex()
        self.starter_index = 0 
        self.starters = self.load_starters()

    def load_player_pokedex(self):
        try:
            with open("Pokedex.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"pokemons": []}

    def save_player_pokedex(self):
        with open("Pokedex.json", "w", encoding="utf-8") as file:
            json.dump(self.player_pokedex, file, ensure_ascii=False, indent=4)

    def load_starters(self):
        with open("Pokemon.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        
        starters_data = [
            next(pokemon for pokemon in data["pokemons"] if pokemon["name"]["en"] == "Bulbasaur"),
            next(pokemon for pokemon in data["pokemons"] if pokemon["name"]["en"] == "Charmander"),
            next(pokemon for pokemon in data["pokemons"] if pokemon["name"]["en"] == "Squirtle"),
        ]
        return starters_data

    def add_pokemon_to_pokedex(self, pokemon):
    
        self.player_pokedex["pokemons"].append({
            "pokedex_id": pokemon.pokedex_id,
            "name": {"en": pokemon.name},
            "sprites": {"front": pokemon.sprite_front, "back": pokemon.sprite_back},
            "types": [{"name": type_name} for type_name in pokemon.types],
            "stats": {"hp": pokemon.max_hp, "atk": pokemon.atk, "def": pokemon.defense},
            "resistances": [{"name": name, "multiplier": multiplier} for name, multiplier in pokemon.resistances],
            "evolution": {"pre": None, "next": None}  
        })
        self.save_player_pokedex()

    def new_wild_pokemon(self):
        enemy_data = random.choice(data["pokemons"])
        enemy_pokemon = Pokemon(enemy_data)
        enemy_pokemon.level = max(1, self.player_pokemon.level - random.randint(0, 5))
        return enemy_pokemon

    def starter_selection(self):
        screen.blit(background_menu, (0, 0))
        draw_text("Choisissez votre Pokémon starter :", title_font, BLACK, 200, 100)
        selected_starter = self.starters[self.starter_index]
        for i, starter in enumerate(self.starters):
            x_position = 200 + i * 300
            color = YELLOW if i == self.starter_index else BLUE
            pygame.draw.rect(screen, YELLOW, (x_position - 10, 300 - 10, 220, 220))
            pygame.draw.rect(screen, color, (x_position - 5, 300 - 5, 210, 210))
            screen.blit(pygame.image.load(starter["sprites"]["front"]), (x_position, 350))
            draw_text(starter["name"]["en"].upper(), text_font, BLACK, x_position + 30, 300)
    
    def main_game(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.starter_index = (self.starter_index - 1) % len(self.starters)
                    if event.key == pygame.K_RIGHT:
                        self.starter_index = (self.starter_index + 1) % len(self.starters)
                    if event.key == pygame.K_RETURN:
                        if event.key == pygame.K_RETURN:
                            selected_starter_data = self.starters[self.starter_index]
                            selected_starter = Pokemon(selected_starter_data) 
                            self.add_pokemon_to_pokedex(selected_starter)
                            
                            self.player_pokemon = selected_starter  
                            
                            enemy_data = random.choice(data["pokemons"])
                            enemy_pokemon = Pokemon(enemy_data)
                            enemy_pokemon.level = max(1, self.player_pokemon.level - random.randint(0, 5)) 
                            
                            fight = Fight(self.player_pokemon, enemy_pokemon)
                            fight.fight()
                        
                    elif event.key == pygame.K_ESCAPE:
                        menu()

            self.starter_selection()
            pygame.display.update()

def menu():
    run_menu = True
    screen.blit(background_menu, (0, 0))
    screen.blit(logo, (355, 10))
    menu_index = 0
    options = ["NEW GAME", "LOAD GAME", "QUIT"] 

    while run_menu:
        for i, option in enumerate(options):
            y_position = 200 + i * 200
            y_position2 = 205 + i * 200
            color = YELLOW if i == menu_index else BLUE
            pygame.draw.rect(screen, YELLOW, (420, y_position, 410, 160))
            pygame.draw.rect(screen, color, (425, y_position2, 400, 150))
            draw_text(option, text_font, BLACK, 450, y_position2 + 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_menu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    menu_index = (menu_index + 1) % len(options)  
                elif event.key == pygame.K_UP:
                    menu_index = (menu_index - 1) % len(options)  
                elif event.key == pygame.K_RETURN:  
                    if menu_index == 0:
                        game.main_game()
                    elif menu_index == 1:
                        print("LAST SAVE")
                    elif menu_index == 2:
                        run_menu = False
                        pygame.quit()  

        pygame.display.update()

game = Game()
menu()