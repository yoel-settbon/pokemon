import json

class LoadGame:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = {}

    def load(self):
        try:
            with open(self.file_path, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {}

    def save(self, player_name, player_pokemon, encountered_pokemons, defeated_pokemons):
        self.data = {
            'player_name': player_name,
            'player_pokemon': player_pokemon.name,
            'encountered_pokemons': [pokemon.name for pokemon in encountered_pokemons],
            'defeated_pokemons': [pokemon.name for pokemon in defeated_pokemons]
        }
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file)

    def get_data(self):
        return self.data