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

        self.pikachu_img = pygame.image.load("assets/image/pikachu.png")
        self.charmander_img = pygame.image.load("assets/image/charmander.png")
        self.bulbasaur_img = pygame.image.load("assets/image/bulbasaur.png")
        self.squirtle_img = pygame.image.load("assets/image/squirtle.png")

        self.pikachu = Pokemon("Pikachu", 100, 20)
        self.charmander = Pokemon("Charmander", 100, 15)
        self.bulbasaur = Pokemon("Bulbasaur", 100, 18)
        self.squirtle = Pokemon("Squirtle", 100, 16)

        self.player_pokemon = self.choose_pokemon()
        self.opponent_pokemon = random.choice([self.pikachu, self.charmander, self.bulbasaur, self.squirtle])
        self.player_message = ""
        self.opponent_message = ""

        self.last_attack_time = 0
        self.attack_delay = 2000
        self.show_player_message = True
        self.message_display_time = 0

        self.game_over_img = pygame.image.load("assets/image/game-over.png")
        self.game_over_img = pygame.transform.scale(self.game_over_img, (self.WIDTH, self.HEIGHT))

    def menu(self):
        from models.menu import Menu
        menu = Menu(1100, 700, "assets/image/background.png", "assets/font/upheavtt.ttf", ['New Game', 'Load Game', 'Quit'])
        menu.run()

    def game_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load('assets/audio/battle-theme.wav')
        pygame.mixer.music.play(-1) 
        pygame.mixer.music.set_volume(1.0)

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
            self.opponent_pokemon = random.choice([self.pikachu, self.charmander, self.bulbasaur, self.squirtle])
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
                                running = False
                            player_turn = False

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
                font = pygame.font.Font(None, 36)
                text = font.render(f"{self.player_pokemon.name} HP: {self.player_pokemon.hp}", True, self.WHITE)
                self.win.blit(text, (30, 500))
                text = font.render(f"{self.opponent_pokemon.name} HP: {self.opponent_pokemon.hp}", True, self.WHITE)
                self.win.blit(text, (860, 200))

                if self.show_player_message and current_time < self.message_display_time:
                    player_message_text = font.render(self.player_message, True, self.WHITE)
                    self.win.blit(player_message_text, (30, 450))

                if not self.show_player_message and current_time < self.message_display_time:
                    opponent_message_text = font.render(self.opponent_message, True, self.WHITE)
                    self.win.blit(opponent_message_text, (30, 200))

                pygame.display.flip()

            if self.player_pokemon.hp <= 0:
                self.player_pokemon = self.choose_pokemon()
            else:
                self.player_pokemon.reset_hp()

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