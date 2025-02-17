import pygame
import random
from models.pokemon import Pokemon

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.WIDTH, self.HEIGHT = 1100, 700
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Combat Pokémon")

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.background = pygame.image.load("assets/image/battle.webp")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

        self.pikachu_img = pygame.image.load("assets/image/pikachu.png")
        self.charmander_img = pygame.image.load("assets/image/charmander.png")
        self.bulbasaur_img = pygame.image.load("assets/image/bulbasaur.png")
        self.squirtle_img = pygame.image.load("assets/image/squirtle.png")

        self.pikachu = Pokemon("Pikachu", 100, 50, ["Éclair", "Coup de foudre", "Tonnerre"])
        self.charmander = Pokemon("Charmander", 80, 45, ["Flamme", "Griffe", "Flammèche"])
        self.bulbasaur = Pokemon("Bulbasaur", 90, 40, ["Vampigraine", "Fouet Lianes", "Charge"])
        self.squirtle = Pokemon("Squirtle", 110, 35, ["Pistolet à eau", "Charge", "Bulle d'O"])

        self.player_pokemon = None
        self.opponent_pokemon = None
        self.player_message = ""
        self.opponent_message = ""

    def game_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load('assets/audio/battle-theme.wav')
        pygame.mixer.music.play(-1) 
        pygame.mixer.music.set_volume(1.0)

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
                        if selected_index == 0:
                            return self.pikachu
                        elif selected_index == 1:
                            return self.charmander
                        elif selected_index == 2:
                            return self.bulbasaur
                        elif selected_index == 3:
                            return self.squirtle
                    self.display_pokemon_choice(selected_index)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    for i in range(4):
                        x = 50 + i * 150
                        y = 150
                        if x <= mouse_x <= x + 100 and y <= mouse_y <= y + 100:
                            if i == 0:
                                return self.pikachu
                            elif i == 1:
                                return self.charmander
                            elif i == 2:
                                return self.bulbasaur
                            elif i == 3:
                                return self.squirtle
            pygame.display.flip()

    def run(self):
        self.game_music()
        running = True
        player_turn = True
        self.player_pokemon = self.choose_pokemon()
        self.opponent_pokemon = random.choice([self.pikachu, self.charmander, self.bulbasaur, self.squirtle])
        self.opponent_pokemon.reset_hp()
        self.player_pokemon.reset_hp()
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