from pokemon import Pokemon

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