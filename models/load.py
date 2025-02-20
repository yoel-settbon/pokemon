import json
import random
from models.pokemon import Pokemon

class PokemonLoader:
    def __init__(self, json_file):
        self.json_file = json_file
        self.pokemons_data = self.load_pokemon_data()

    def load_pokemon_data(self):
        with open(self.json_file, 'r') as file:
            data = json.load(file)
        return data["pokemons"]

    def get_random_pokemon(self):
        random_pokemon_data = random.choice(self.pokemons_data)

        name = random_pokemon_data["name"]["en"]
        sprite_face = random_pokemon_data["sprites"]["face"]
        sprite_back = random_pokemon_data["sprites"]["back"]
        types = [t["name"] for t in random_pokemon_data["types"]]
        stats = random_pokemon_data["stats"]
        
        pokemon = Pokemon(
            name = name,
            hp = ["hp"],
            attack=stats["atk"],
            sprite_back=sprite_back
        )
        pokemon.types = types

        return pokemon
