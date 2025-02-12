import json
from pokemon import Pokemon
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