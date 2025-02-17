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

        self.pikachu = Pokemon("Pikachu", 100, 20)
        self.charmander = Pokemon("Charmander", 100, 15)
        self.bulbasaur = Pokemon("Bulbasaur", 100, 18)
        self.squirtle = Pokemon("Squirtle", 100, 16)

        self.player_pokemon = self.choose_pokemon()
        self.opponent_pokemon = random.choice([self.pikachu, self.charmander, self.bulbasaur, self.squirtle])
        self.player_message = ""
        self.opponent_message = ""

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
                            self.player_message = f"{self.player_pokemon.name} attack {self.opponent_pokemon.name} deals {damage} damages!"
                            if self.opponent_pokemon.hp <= 0:
                                self.player_message += f"{self.opponent_pokemon.name} is KO!"
                                running = False
                            player_turn = False

                if not player_turn and self.opponent_pokemon.hp > 0:
                    damage = self.opponent_pokemon.attack_pokemon(self.player_pokemon)
                    self.opponent_message = f"{self.opponent_pokemon.name} attack {self.player_pokemon.name} deals {damage} damages!"
                    if self.player_pokemon.hp <= 0:
                        self.opponent_message += f" {self.player_pokemon.name} is KO!"
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
                
    def display_pokemon_choice(self, selected_index):
        self.win.blit(self.background, (0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render("Pick your Pokémon:", True, self.WHITE)
        self.win.blit(text, (50, 50))
        options = ["Pikachu", "Charmander", "Bulbasaur", "Squirtle"]
        for i, option in enumerate(options):
            color = self.WHITE if i != selected_index else (255, 0, 0)
            text = font.render(option, True, color)
            self.win.blit(text, (50, 100 + i * 50))
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
