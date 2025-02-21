import pygame
import random
import json
from pygame import *
import time


pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1250, 800))
background_fight = pygame.image.load("images/fight_template.png")
background_menu = pygame.image.load("images/menu_template_pokemon.jpg")
logo = pygame.image.load("images/logo_pokemon.png")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 228, 54)
BLUE = (0, 128, 255)

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

        self.base_hp = data["stats"]["hp"]
        self.base_atk = data["stats"]["atk"]
        self.base_def = data["stats"]["def"]

        self.update_stats()

        self.hp = int((self.base_hp / 10) * self.level)
        self.atk = (self.base_atk / 10) * self.level
        self.defense = (self.base_def / 10) * self.level
        self.resistances = [
            (resistance["name"], resistance["multiplier"])
            for resistance in data["resistances"]
        ]
        self.max_hp = (self.base_hp) / 10 * self.level
        self.xp = 0  
        self.xp_to_next_level = 100  
        self.evolution = data["evolution"]["next"]

    def update_stats(self):
        self.hp = int((2 * self.base_hp * self.level) / 100 + self.level + 10)
        self.atk = int((2 * self.base_atk * self.level) / 100 + 5)
        self.defense = int((2 * self.base_def * self.level) / 100 + 5)
        self.max_hp = self.hp

    def est_ko(self):
        return self.hp <= 0

    def gain_xp(self, xp_gagnee):
        self.xp += xp_gagnee
        while self.xp >= self.xp_to_next_level:
            self.gain_lvl()
        
        game.update_pokedex(self)

    def gain_lvl(self):
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.15)  
    
        self.update_stats()
 
        self.evolve()

    def get_damage_multiplier(self, attack_type):
        multiplier = 1
        for resistance in self.resistances:
            if resistance[0] == attack_type:
                multiplier *= resistance[1]
        return multiplier
    
    def evolve(self):
        if self.evolution is None:
            return  

        for evo in self.evolution:
            if self.level >= evo["condition"]:
                with open('Pokemon.json', 'r', encoding='utf-8') as file:
                    pokemon_data = json.load(file)
                
                evolved_pokemon_data = next(
                    (p for p in pokemon_data["pokemons"] if p["pokedex_id"] == evo["pokedex_id"]),
                    None
                )
                
                if evolved_pokemon_data is None:
                    return
            
                self.name = evolved_pokemon_data["name"]["en"]
                self.pokedex_id = evolved_pokemon_data["pokedex_id"]
                self.sprite_front = evolved_pokemon_data["sprites"]["front"]
                self.sprite_back = evolved_pokemon_data["sprites"]["back"]
                self.types = [type_data["name"] for type_data in evolved_pokemon_data["types"]]
                
                self.base_hp = evolved_pokemon_data["stats"]["hp"]
                self.base_atk = evolved_pokemon_data["stats"]["atk"]
                self.base_def = evolved_pokemon_data["stats"]["def"]
                
                self.resistances = [
                    (resistance["name"], resistance["multiplier"])
                    for resistance in evolved_pokemon_data["resistances"]
                ]
                self.evolution = evolved_pokemon_data["evolution"]["next"]

                self.update_stats()

                print(f"{self.name} a évolué en {evo['name']} !")
                break

class Fight():
    def __init__(self, player_pokemon, enemy_pokemon):
        self.player_pokemon = player_pokemon
        self.enemy_pokemon = enemy_pokemon
        self.run = True
    
    def fight_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load('assets/audio/battle-theme.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(1.0)

    def display_pokemon(self):
        player_sprite = pygame.image.load(self.player_pokemon.sprite_back)
        screen.blit(player_sprite, (100, 300))
        draw_text(f"{self.player_pokemon.name} - Nv. {self.player_pokemon.level}", text_font, BLACK, 50, 400)

        enemy_sprite = pygame.image.load(self.enemy_pokemon.sprite_front)
        screen.blit(enemy_sprite, (800, 100))
        draw_text(f"{self.enemy_pokemon.name} - Nv. {self.enemy_pokemon.level}", text_font, BLACK, 800, 50)

        self.draw_health_bar(self.player_pokemon, 40, 460) 
        self.draw_health_bar(self.enemy_pokemon, 800, 110) 

    def menu_between(self):
        self.choose = ["Fight", "Pokedex", "Save & Quit"]
        self.choose_index = 0
        screen.blit(background_menu, (0, 0))
    
        while True:
            for i, choice in enumerate(self.choose):
                x_position = 100 + i * 200
                x_position2 = 105 + i * 200
                color = BLUE if i == self.choose_index else YELLOW
                pygame.draw.rect(screen, BLUE, (x_position, 20, 410, 160))
                pygame.draw.rect(screen, color, (x_position2, 25, 400, 150))

            draw_text("Fight", text_font, BLACK, 150, 75)
            draw_text("Pokedex", text_font, BLACK, 350, 75)
            draw_text("Save & Quit", text_font, BLACK, 550, 75)
            
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
                            game.display_pokedex_menu()
                        if self.choose_index == 2:
                            game.save_game()
                            menu()
            pygame.display.update()

    def attack(self, attack_type):
        base_damage = int(max(0, self.player_pokemon.atk - (self.enemy_pokemon.defense * 0.25)))
        multiplier = self.enemy_pokemon.get_damage_multiplier(attack_type)
        damage = int(base_damage * multiplier)
        damage = max(1, damage)  
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

    def enemy_attack(self, attack_type):
        base_damage = int(max(0, self.enemy_pokemon.atk - (self.player_pokemon.defense * 0.5)))
        multiplier = self.player_pokemon.get_damage_multiplier(attack_type)
        damage = int(base_damage * multiplier)
        damage = max (1, damage)
        self.player_pokemon.hp -= damage

        draw_text(f"{self.enemy_pokemon.name} attaque et inflige {damage} dégâts !", text_font, BLACK, 100, 700)

        if self.player_pokemon.hp <= 0:
            draw_text(f"{self.player_pokemon.name} est KO !", text_font, BLACK, 100, 750)

            game.remove_pokemon_from_pokedex(self.player_pokemon)

            if len(game.player_pokedex["pokemons"]) == 0:
                game.game_over()
                time.sleep(3)
                menu()
                pygame.display.update()
            else:
                self.switch_pokemon()

    def calculate_xp_gain(self):
        base_xp = 50 
        xp_gained = base_xp * (self.enemy_pokemon.level/2)  
        return max(10, xp_gained)  
    
    def switch_pokemon(self):
        selected_pokemon = game.display_pokedex_menu()
        if selected_pokemon:
            selected_pokemon.update_stats()
      
            self.player_pokemon = selected_pokemon
            draw_text(f"{self.player_pokemon.name} est envoyé au combat !", text_font, BLACK, 100, 600)

    def draw_health_bar(self, pokemon, x, y):
        pygame.draw.rect(screen, (169, 169, 169), (x, y, 200, 20))
        
        health_percentage = pokemon.hp / pokemon.max_hp
        health_width = 200 * health_percentage
        
        health_color = (0, 255, 0) if health_percentage > 0.5 else (255, 0, 0)
        pygame.draw.rect(screen, health_color, (x, y, health_width, 20))
        
        draw_text(f"{pokemon.hp}/{pokemon.max_hp}", text_font, (255, 255, 255), x + 5, y - 25)

    def fight(self):
        self.fight_music()
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
                x_position = 10 + i * 200
                x_position2 = 15 + i * 200
                color = BLUE if i == self.fight_index else YELLOW
                pygame.draw.rect(screen, BLUE, (x_position, 620, 410, 175))
                pygame.draw.rect(screen, color, (x_position2, 625, 400, 165))
                draw_text(option, text_font, BLACK, x_position2 + 50, 675)

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
                            self.attack(self.player_pokemon.types[0])
                            if not self.enemy_pokemon.est_ko(): 
                                self.enemy_attack(self.enemy_pokemon.types[0]) 
                            else:
                                self.player_pokemon.hp = self.player_pokemon.max_hp
                                self.enemy_pokemon = game.new_wild_pokemon()
                                self.menu_between()  
                        elif self.fight_index == 1: 
                            self.player_pokemon.hp = self.player_pokemon.max_hp
                            self.enemy_pokemon = game.new_wild_pokemon()
                            self.menu_between()
                        elif self.fight_index == 2: 
                            self.switch_pokemon()

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

    def update_pokedex(self, pokemon):
        for pokedex_pokemon in self.player_pokedex["pokemons"]:
            if pokedex_pokemon["pokedex_id"] == pokemon.pokedex_id:
                pokedex_pokemon["level"] = pokemon.level
                pokedex_pokemon["xp"] = pokemon.xp
                pokedex_pokemon["xp_to_next_level"] = pokemon.xp_to_next_level
                pokedex_pokemon["stats"]["hp"] = pokemon.max_hp
                pokedex_pokemon["stats"]["atk"] = pokemon.atk
                pokedex_pokemon["stats"]["def"] = pokemon.defense
                break
        self.save_player_pokedex()

    def reset_pokedex(self):
        self.player_pokedex = {"pokemons": []}  
        with open("Pokedex.json", "w", encoding="utf-8") as file:
            json.dump(self.player_pokedex, file, ensure_ascii=False, indent=4)
        print("Pokédex réinitialisé pour une nouvelle partie.")


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
        existing_pokemon = None
        for pokedex_pokemon in self.player_pokedex["pokemons"]:
            if pokedex_pokemon["pokedex_id"] == pokemon.pokedex_id:
                existing_pokemon = pokedex_pokemon
                break

        if existing_pokemon:
            if pokemon.level > existing_pokemon.get("level", 1):
                existing_pokemon["level"] = pokemon.level
                existing_pokemon["xp"] = pokemon.xp
                existing_pokemon["xp_to_next_level"] = pokemon.xp_to_next_level
                existing_pokemon["stats"]["hp"] = pokemon.max_hp
                existing_pokemon["stats"]["atk"] = pokemon.atk
                existing_pokemon["stats"]["def"] = pokemon.defense
        else:
            self.player_pokedex["pokemons"].append({
                "pokedex_id": pokemon.pokedex_id,
                "name": {"en": pokemon.name},
                "sprites": {"front": pokemon.sprite_front, "back": pokemon.sprite_back},
                "types": [{"name": type_name} for type_name in pokemon.types],
                "stats": {"hp": pokemon.max_hp, "atk": pokemon.atk, "def": pokemon.defense},
                "resistances": [{"name": name, "multiplier": multiplier} for name, multiplier in pokemon.resistances],
                "evolution": {"pre": None, "next": None},
                "level": pokemon.level,
                "xp": pokemon.xp,
                "xp_to_next_level": pokemon.xp_to_next_level
            })

        self.save_player_pokedex()

    def remove_pokemon_from_pokedex(self, pokemon):
        for pokedex_pokemon in self.player_pokedex["pokemons"]:
            if pokedex_pokemon["pokedex_id"] == pokemon.pokedex_id:
                self.player_pokedex["pokemons"].remove(pokedex_pokemon)
                self.save_player_pokedex()
                break


    def new_wild_pokemon(self):
        enemy_data = random.choice(data["pokemons"])
        enemy_pokemon = Pokemon(enemy_data)
        enemy_pokemon.level = max( self.player_pokemon.level - random.randint(0, 5), 1)
        return enemy_pokemon

    def starter_selection(self):
        screen.blit(background_menu, (0, 0))
        selected_starter = self.starters[self.starter_index]
        for i, starter in enumerate(self.starters):
            x_position = 200 + i * 300
            x_position2 = 140 + i * 300
            color = BLUE if i == self.starter_index else YELLOW
            pygame.draw.rect(screen, BLUE, (x_position - 10, 300 - 10, 220, 220))
            pygame.draw.rect(screen, color, (x_position - 5, 300 - 5, 210, 210))
            screen.blit(pygame.image.load(starter["sprites"]["front"]), (x_position2, 250))
            draw_text(starter["name"]["en"].upper(), text_font, BLACK, x_position + 20, 300)

    def game_over(self):
        game_over_image = pygame.image.load('assets/images/game-over.png')
        game_over_image = pygame.transform.scale(game_over_image, (1250, 800))
        screen.blit(game_over_image, (0, 0))
        pygame.mixer.music.stop()
        pygame.mixer.music.load('assets/audio/game-over-voice.wav')
        pygame.display.update()
        pygame.mixer.music.play()
        pygame.time.delay(5000)
        
    def save_game(self):
        save_data = {
            "player_pokedex": self.player_pokedex,
            "current_pokemon": {
                "pokedex_id": self.player_pokemon.pokedex_id if self.player_pokemon else None,
                "name": self.player_pokemon.name if self.player_pokemon else None,
                "level": self.player_pokemon.level if self.player_pokemon else None,
                "xp": self.player_pokemon.xp if self.player_pokemon else None,
                "xp_to_next_level": self.player_pokemon.xp_to_next_level if self.player_pokemon else None,
                "hp": self.player_pokemon.hp if self.player_pokemon else None,
                "max_hp": self.player_pokemon.max_hp if self.player_pokemon else None,
                "atk": self.player_pokemon.atk if self.player_pokemon else None,
                "defense": self.player_pokemon.defense if self.player_pokemon else None,
            }
        }

        with open("Pokedex.json", "w", encoding="utf-8") as file:
            json.dump(save_data, file, ensure_ascii=False, indent=4)

    def load_game(self):
        try:
            with open("Pokedex.json", "r", encoding="utf-8") as file:
                save_data = json.load(file)

            self.player_pokedex = save_data.get("player_pokedex", {"pokemons": []})
            current_pokemon_data = save_data.get("current_pokemon", None)
            if current_pokemon_data:
                with open("Pokemon.json", "r", encoding="utf-8") as file:
                    pokemon_data = json.load(file)

                pokemon_info = next(
                    (p for p in pokemon_data["pokemons"] if p["pokedex_id"] == current_pokemon_data["pokedex_id"]),
                    None
                )
                
                if pokemon_info:
                    self.player_pokemon = Pokemon(pokemon_info)
                    self.player_pokemon.level = current_pokemon_data["level"]
                    self.player_pokemon.xp = current_pokemon_data["xp"]
                    self.player_pokemon.xp_to_next_level = current_pokemon_data["xp_to_next_level"]
                    self.player_pokemon.hp = current_pokemon_data["hp"]
                    self.player_pokemon.max_hp = current_pokemon_data["max_hp"]
                    self.player_pokemon.atk = current_pokemon_data["atk"]
                    self.player_pokemon.defense = current_pokemon_data["defense"]

            return True
        except FileNotFoundError:
            return False


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

    def display_pokedex_menu(self):
        run = True
        pokedex_index = 0  

        while run:
            screen.blit(background_menu, (0, 0))
            for i, pokemon_data in enumerate(self.player_pokedex["pokemons"]):
                y_position = 150 + i * 100
                color = BLUE if i == pokedex_index else YELLOW
                pygame.draw.rect(screen, BLUE, (100, y_position - 10, 1050, 90))
                pygame.draw.rect(screen, color, (105, y_position - 5, 1040, 80))
                draw_text(f"{pokemon_data['name']['en']} - Nv. {pokemon_data.get('level', 1)}", text_font, BLACK, 200, y_position + 20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        pokedex_index = (pokedex_index + 1) % len(self.player_pokedex["pokemons"])
                    elif event.key == pygame.K_UP:
                        pokedex_index = (pokedex_index - 1) % len(self.player_pokedex["pokemons"])
                    elif event.key == pygame.K_RETURN:
                        selected_pokemon_data = self.player_pokedex["pokemons"][pokedex_index]
                        selected_pokemon = Pokemon(selected_pokemon_data)
                        
                        selected_pokemon.update_stats()
                        
                        return selected_pokemon
                    elif event.key == pygame.K_ESCAPE:
                        return None  

            pygame.display.update()

def menu():
    run_menu = True
    pygame.mixer.music.stop()
    pygame.mixer.music.load('assets/audio/menu-theme.wav')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1.0)
    screen.blit(background_menu, (0, 0))
    screen.blit(logo, (355, 10))
    menu_index = 0
    options = ["NEW GAME", "LOAD GAME", "QUIT"] 

    while run_menu:
        for i, option in enumerate(options):
            y_position = 200 + i * 200
            y_position2 = 205 + i * 200
            color = BLUE if i == menu_index else YELLOW
            pygame.draw.rect(screen, BLUE, (420, y_position, 410, 160))
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
                        game.reset_pokedex()
                        game.main_game()
                    elif menu_index == 1:
                        game.load_game()
                        enemy_data = random.choice(data["pokemons"])
                        enemy_pokemon = Pokemon(enemy_data)
                        enemy_pokemon.level = max(1, game.player_pokemon.level - random.randint(0, 5))     
                        fight = Fight(game.player_pokemon, enemy_pokemon)
                        fight.fight()
                    elif menu_index == 2:
                        run_menu = False
                        pygame.quit()  

        pygame.display.update()

game = Game()
menu()