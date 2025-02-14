class Player:
    def __init__(self, name):
        self.name = name
        self.pokemon = []

    def add_pokemon(self, pokemon):
        self.pokemon.append(pokemon)

    def remove_pokemon(self, pokemon):
        self.pokemon.remove(pokemon)

    def has_pokemon(self):
        return len(self.pokemon) > 0