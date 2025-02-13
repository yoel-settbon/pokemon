import pygame

class Pokemon:
    def __init__(self, name, type, pv, attack, defense, speed, attacks, evolution=None):
        self.name = name
        self.type = type
        self.pv = pv
        self.pv_max = pv
        self.attack = attack
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.attacks = attacks
        self.evolution = evolution

    def display_info(self):
        info = f"{self.name} ({self.type}) - PV: {self.pv}/{self.pv_max}, ATK: {self.attack}, DEF: {self.defense}, VIT: {self.speed}\n"
        info += "Attacks :\n"
        for attack in self.attacks:
            info += f"  - {attack['name']} ({attack['type']}, Power: {attack['power']})\n"
        return info.strip()
    
    def perform_attack(self, other_pokemon, attack_name):
        attack = next((a for a in self.attacks if a["name"] == attack_name), None)
        if attack:
            damage = max(attack["power"] - other_pokemon.defense, 1)
            other_pokemon.pv = max(other_pokemon.pv - damage, 0)
            return f"{self.name} used {attack_name}! {other_pokemon.name} lost {damage} HP."
        return f"{self.name} does not know this attack!"

    def is_ko(self):
        return self.pv <= 0

class Trainer:
    def __init__(self, name, pokemons):
        self.name = name
        self.pokemons = [
            p if isinstance(p, Pokemon) else Pokemon(**p) for p in pokemons
        ]
    
    def display_team(self):
        return [pokemon.display_info() for pokemon in self.pokemons]
    
    def add_pokemons(self, pokemon):
        if isinstance(pokemon, dict):
            pokemon = Pokemon(**pokemon)
        self.pokemons.append(pokemon)
        return f"{self.name} obtained {pokemon.name}!"
    
    def lose_pokemon(self, pokemon):
        if isinstance(pokemon, dict):
            pokemon_name = pokemon["name"]
        else:
            pokemon_name = pokemon.name
        self.pokemons = [p for p in self.pokemons if p.name != pokemon_name]
        return f"{self.name} lost {pokemon_name}!"

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

class Menu:
    def __init__(self, width=900, height=600):
        self.HEIGHT = height
        self.WIDTH = width
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pokemon Fighters")
              
        self.background = pygame.image.load("assets/image/background.png")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        self.battle = pygame.image.load("assets/image/battle.webp")
        self.battle = pygame.transform.scale(self.battle, (self.WIDTH, self.HEIGHT)) 
             
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        self.tittle_font = pygame.font.Font("assets/font/upheavtt.ttf", 80)
        self.menu_font = pygame.font.Font("assets/font/upheavtt.ttf", 45)

    def draw_text(self, text, font, color, x, y):
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        self.window.blit(text_surf, text_rect)

    def menu(self):
        self.window.blit(self.background, (0, 0))
        self.draw_text("FIGHTERS", self.tittle_font, self.WHITE, self.WIDTH // 2.6, self.HEIGHT // 2.4)
        self.draw_text("NEW GAME", self.menu_font, self.WHITE, self.WIDTH // 2.6, self.HEIGHT // 1.8)
        pygame.display.update()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.start()

    def start(self):
        self.window.blit(self.background, (0, 0))
        self.draw_text("FIGHTERS", self.tittle_font, self.WHITE, self.WIDTH // 2.6, self.HEIGHT // 2.4)
        self.draw_text("Press ENTER to start", self.menu_font, self.WHITE, self.WIDTH // 2.6, self.HEIGHT // 1.3)
        pygame.display.update()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.menu()