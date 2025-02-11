from pokemon import Pokemon

class Trainer:
    def __init__(self, name, pokemons):
        self.name = name
        self.pokemons = [Pokemon(**p) for p in pokemons]
    
    def display_team(self):
        return [pokemon.display_info() for pokemon in self.pokemons]
    
    def add_pokemons(self, pokemon):
        self.pokemons.append(Pokemon(**pokemon))
        return f"{self.name} obtained {pokemon['name']} !"
    
    def lose_pokemon(self, pokemon):
        self.pokemons = [p for p in self.pokemons if p.name != pokemon.name]
        return f"{self.name} lost {pokemon.name} !"