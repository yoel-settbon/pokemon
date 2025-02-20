import json
import pygame
import random
from models.pokemon import Pokemon

class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1100, 700
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pokemon Fighters")

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.background = pygame.image.load("assets/image/battle.webp")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        self.background2 = pygame.image.load("assets\image/background.png")
        self.background2 = pygame.transform.scale(self.background2, (self.WIDTH, self.HEIGHT))

        self.pikachu_back_img = pygame.image.load("assets\image\pikachu_.png")
        self.charmander_back_img = pygame.image.load("assets\image\charmander_.png")
        self.bulbasaur_back_img = pygame.image.load("assets\image/bulbasaur_.png")
        self.squirtle_back_img = pygame.image.load("assets\image\squirtle_.png")

        self.pikachu_img = pygame.image.load("assets/image/pikachu.png")
        self.charmander_img = pygame.image.load("assets/image/charmander.png")
        self.bulbasaur_img = pygame.image.load("assets/image/bulbasaur.png")
        self.squirtle_img = pygame.image.load("assets/image/squirtle.png")
        self.snorlax_img = pygame.image.load("assets\image\pokemon-face\snorlax.png")
        self.lapras_img = pygame.image.load("assets\image\pokemon-face\lapras.png")
        self.lugia_img = pygame.image.load("assets\image\pokemon-face\lugia.png")
        self.dragonite_img = pygame.image.load("assets\image\pokemon-face\dragonite.png")
        self.mew_img = pygame.image.load("assets\image\pokemon-face\mew.png")

        self.pikachu = Pokemon("Pikachu", 100, 20, "assets\image\pikachu_.png")
        self.charmander = Pokemon("Charmander", 100, 15, "assets\image\charmander_.png")
        self.bulbasaur = Pokemon("Bulbasaur", 100, 18, "assets\image/bulbasaur_.png")
        self.squirtle = Pokemon("Squirtle", 100, 16, "assets/image/squirtle.png")
        self.snorlax = Pokemon("Snorlax",100,14, "assets\image\pokemon-face\snorlax.png")
        self.lapras = Pokemon("Lapras",100, 12,"assets\image\pokemon-face\lapras.png")
        self.lugia = Pokemon("Lugia", 100, 10, "assets\image\pokemon-face\lugia.png")
        self.dragonite = Pokemon("Dragonite", 100,8, "assets\image\pokemon-face\dragonite.png")
        self.mew = Pokemon("Mew", 100, 6, "assets\image\pokemon-face\mew.png")

        self.player_name = self.get_player_name()
        self.player_pokemon = self.choose_pokemon()
        self.opponent_pokemon = random.choice([self.pikachu, self.charmander, self.bulbasaur, self.squirtle, self.snorlax, self.lapras, self.lugia, self.dragonite, self.mew])

        self.pokemon_encountered = [self.opponent_pokemon.name]
        self.pokemon_defeated = []

        while self.opponent_pokemon == self.player_pokemon:
            self.opponent_pokemon = random.choice([self.pikachu, self.charmander, self.bulbasaur, self.squirtle, self.snorlax, self.lapras, self.lugia, self.dragonite, self.mew])

        self.player_message = ""
        self.opponent_message = ""

        self.last_attack_time = 0
        self.attack_delay = 2000
        self.show_player_message = True
        self.message_display_time = 0

        self.game_over_img = pygame.image.load("assets/image/game-over.png")
        self.game_over_img = pygame.transform.scale(self.game_over_img, (self.WIDTH, self.HEIGHT))

        self.attack_animation_player = False
        self.attack_animation_opponent = False
        self.animation_time_player = 0
        self.animation_time_opponent = 0
    def menu(self):
        from models.menu import Menu
        menu = Menu(1100, 700, "assets/image/background.png", "assets/font/upheavtt.ttf", ['New Game', 'Load Game', 'Quit'])
        menu.run()

    def game_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load('assets/audio/battle-theme.wav')
        pygame.mixer.music.play(-1) 
        pygame.mixer.music.set_volume(1.0)

    def get_player_name(self):
        font = pygame.font.Font("assets/font\Daydream.ttf", 36)
        name = ""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_RETURN:
                        return name
                    else:
                        name += event.unicode
            self.win.blit(self.background2, (0, 0))
            text = font.render(f"Entrez votre nom: {name}", True, self.WHITE)
            self.win.blit(text, (100, 350))
            pygame.display.flip()

    def save_game_data(self):
        game_data = {
            "player_name": self.player_name,
            "chosen_pokemon": self.player_pokemon.name,
            "pokemon_encountered": self.pokemon_encountered,
            "pokemon_defeated": self.pokemon_defeated
        }
        
        with open("data/pokedex.json", "w") as file:
            json.dump(game_data, file, indent=4)

    def choose_pokemon(self):
        selected_index = 0
        self.display_pokemon_choice(selected_index)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        selected_index = (selected_index - 1) % 4
                    elif event.key == pygame.K_RIGHT:
                        selected_index = (selected_index + 1) % 4
                    elif event.key == pygame.K_RETURN:
                        return [self.pikachu, self.charmander, self.bulbasaur, self.squirtle][selected_index]
                    self.display_pokemon_choice(selected_index)

    def game_over_sequence(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load('assets/audio/game-over-voice.wav')
        pygame.mixer.music.play()
        self.win.blit(self.game_over_img, (0, 0))
        pygame.display.flip()
        pygame.time.delay(5000)

    def run(self):
        self.game_music()
        while True:
            running = True
            player_turn = True
            self.player_pokemon.reset_hp()
            self.opponent_pokemon = random.choice([self.pikachu, self.charmander, self.bulbasaur, self.squirtle, self.snorlax, self.lapras, self.lugia, self.dragonite, self.mew])

            while self.opponent_pokemon == self.player_pokemon:
                self.opponent_pokemon = random.choice([self.pikachu, self.charmander, self.bulbasaur, self.squirtle, self.snorlax, self.lapras, self.lugia, self.dragonite, self.mew])

            self.opponent_pokemon.reset_hp()
            self.player_message = ""
            self.opponent_message = ""

            while running:
                current_time = pygame.time.get_ticks()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and player_turn:
                            self.attack_animation_player = True
                            self.animation_time_player = current_time + 500

                            damage = self.player_pokemon.attack_pokemon(self.opponent_pokemon)
                            if damage == 0:
                                self.player_message = f"{self.player_pokemon.name}'s attack missed!"
                            else:
                                self.player_message = f"{self.player_pokemon.name} attacks {self.opponent_pokemon.name} dealing {damage} damage!"
                            self.last_attack_time = current_time
                            self.show_player_message = True
                            self.message_display_time = current_time + self.attack_delay
                            if self.opponent_pokemon.hp <= 0:
                                self.player_message += f" {self.opponent_pokemon.name} is KO!"
                                self.player_pokemon.gain_experience(15)
                                self.pokemon_defeated.append(self.opponent_pokemon.name)

                                self.opponent_pokemon = random.choice([self.pikachu, self.charmander, self.bulbasaur, self.squirtle])

                                while self.opponent_pokemon == self.player_pokemon:
                                    self.opponent_pokemon = random.choice([self.pikachu, self.charmander, self.bulbasaur, self.squirtle, self.snorlax, self.lapras, self.lugia, self.dragonite, self.mew])

                                self.opponent_pokemon.reset_hp()
                                self.pokemon_encountered.append(self.opponent_pokemon.name)
                                self.player_message += f" A wild {self.opponent_pokemon.name} appeared!"
                                running = False
                            player_turn = False

                self.save_game_data()

                if self.attack_animation_player and current_time >= self.animation_time_player:
                    self.attack_animation_player = False
                    self.attack_animation_opponent = True
                    self.animation_time_opponent = current_time + 500

                if self.attack_animation_opponent and current_time >= self.animation_time_opponent:
                    self.attack_animation_opponent = False

                if not player_turn and self.opponent_pokemon.hp > 0 and current_time >= self.message_display_time:
                    damage = self.opponent_pokemon.attack_pokemon(self.player_pokemon)

                    if damage == 0:
                        self.opponent_message = f"{self.opponent_pokemon.name}'s attack missed!"
                    else:
                        self.opponent_message = f"{self.opponent_pokemon.name} attacks {self.player_pokemon.name} dealing {damage} damage!"

                    self.last_attack_time = current_time
                    self.show_player_message = False
                    self.message_display_time = current_time + self.attack_delay

                    if self.player_pokemon.hp <= 0:
                        self.opponent_message += f" {self.player_pokemon.name} is KO!"
                        running = False
                        self.game_over_sequence()
                        return self.menu()
                    player_turn = True

                self.win.blit(self.background, (0, 0))
                self.display_pokemon_images()

                font = pygame.font.Font(None, 36)
                text = font.render(f"{self.player_pokemon.name} HP: {self.player_pokemon.hp} Level: {self.player_pokemon.level}", True, self.WHITE)
                self.win.blit(text, (30, 450))
                text = font.render(f"{self.opponent_pokemon.name} HP: {self.opponent_pokemon.hp} Level: {self.opponent_pokemon.level}", True, self.WHITE)
                self.win.blit(text, (790, 150))

                if self.show_player_message and current_time < self.message_display_time:
                    player_message_text = font.render(self.player_message, True, self.WHITE)
                    self.win.blit(player_message_text, (30, 400))

                if not self.show_player_message and current_time < self.message_display_time:
                    opponent_message_text = font.render(self.opponent_message, True, self.WHITE)
                    self.win.blit(opponent_message_text, (30, 150))

                pygame.display.flip()

            if self.player_pokemon.hp <= 0:
                self.player_pokemon = self.choose_pokemon()
            else:
                self.player_pokemon.reset_hp()


    def display_pokemon_images(self):
        player_offset = 0
        opponent_offset = 0
        if self.attack_animation_player:
            player_offset = 20
        if self.attack_animation_opponent:
            opponent_offset = -20

        player_pokemon_img = pygame.transform.scale(self.get_pokemon_back(self.player_pokemon), (450, 450))
        opponent_pokemon_img = pygame.transform.scale(self.get_pokemon_image(self.opponent_pokemon), (350, 350))

        self.win.blit(player_pokemon_img, (150 + player_offset, 370))
        self.win.blit(opponent_pokemon_img, (680 + opponent_offset, 200))

    def get_pokemon_back(self, pokemon):
        if pokemon.name == "Pikachu":
            return self.pikachu_back_img
        elif pokemon.name == "Charmander":
            return self.charmander_back_img
        elif pokemon.name == "Bulbasaur":
            return self.bulbasaur_back_img
        elif pokemon.name == "Squirtle":
            return self.squirtle_back_img
        
    def get_pokemon_image(self, pokemon):
        if pokemon.name == "Pikachu":
            return self.pikachu_img
        elif pokemon.name == "Charmander":
            return self.charmander_img
        elif pokemon.name == "Bulbasaur":
            return self.bulbasaur_img
        elif pokemon.name == "Squirtle":
            return self.squirtle_img
        elif pokemon.name == "Snorlax":
            return self.snorlax_img
        elif pokemon.name == "Lapras":
            return self.lapras_img
        elif pokemon.name == "Lugia":
            return self.lugia_img
        elif pokemon.name == "Dragonite":
            return self.dragonite_img
        elif pokemon.name == "Mew":
            return self.mew_img

    def display_pokemon_choice(self, selected_index):
        self.win.blit(self.background, (0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render("Choisissez votre Pokémon:", True, self.WHITE)
        self.win.blit(text, (50, 50))

        pokemon_images = [self.pikachu_img, self.charmander_img, self.bulbasaur_img, self.squirtle_img]
        for i, img in enumerate(pokemon_images):
            img = pygame.transform.scale(img, (100, 100))
            x = 50 + i * 150
            y = 150
            color = self.WHITE if i != selected_index else (255, 0, 0)
            self.win.blit(img, (x, y))
            pygame.draw.rect(self.win, color, (x, y, 100, 100), 3)

        pygame.display.flip()