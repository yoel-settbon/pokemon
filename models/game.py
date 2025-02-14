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

    class Pokemon:
        def __init__(self, name, hp, attack):
            self.name = name
            self.hp = hp
            self.attack = attack

        def attack_pokemon(self, other):
            damage = random.randint(0, self.attack)
            other.hp -= damage
            return damage

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
        running = True
        player_turn = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and player_turn:
                        damage = self.player_pokemon.attack_pokemon(self.opponent_pokemon)
                        print(f"{self.player_pokemon.name} attaque {self.opponent_pokemon.name} et inflige {damage} dégâts!")
                        if self.opponent_pokemon.hp <= 0:
                            print(f"{self.opponent_pokemon.name} est KO!")
                            running = False
                        player_turn = False

            if not player_turn and self.opponent_pokemon.hp > 0:
                damage = self.opponent_pokemon.attack_pokemon(self.player_pokemon)
                print(f"{self.opponent_pokemon.name} attaque {self.player_pokemon.name} et inflige {damage} dégâts!")
                if self.player_pokemon.hp <= 0:
                    print(f"{self.player_pokemon.name} est KO!")
                    running = False
                player_turn = True

            self.win.blit(self.background, (0, 0))
            font = pygame.font.Font(None, 36)
            text = font.render(f"{self.player_pokemon.name} HP: {self.player_pokemon.hp}", True, self.WHITE)
            self.win.blit(text, (50, 50))
            text = font.render(f"{self.opponent_pokemon.name} HP: {self.opponent_pokemon.hp}", True, self.WHITE)
            self.win.blit(text, (50, 100))
            if player_turn:
                turn_text = font.render("C'est votre tour!", True, self.WHITE)
            else:
                turn_text = font.render("Tour de l'adversaire...", True, self.WHITE)
            self.win.blit(turn_text, (50, 150))
            pygame.display.flip()

            pygame.time.delay(1000)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()