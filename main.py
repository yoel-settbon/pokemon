from models.trainer import Trainer
from models.pokemon import Pokemon

# Chargement des Pokémon (exemple simple, remplace par une lecture JSON si nécessaire)
pikachu_data = {"name": "Pikachu", "type": "Électrik", "pv": 35, "attack": 55, "defense": 40, "speed": 90, "attacks": [{"name": "Éclair", "type": "Électrik", "power": 40}]}
salameche_data = {"name": "Salamèche", "type": "Feu", "pv": 39, "attack": 52, "defense": 43, "speed": 65, "attacks": [{"name": "Flammèche", "type": "Feu", "power": 40}]}

# Création des dresseurs avec leurs Pokémon
player = Trainer("Sacha", [pikachu_data])
rival = Trainer("Régis", [salameche_data])

# Affichage des équipes
print("Ton équipe :")
for info in player.display_team():
    print(info)

print("\nÉquipe adverse :")
for info in rival.display_team():
    print(info)

# Combat simple
print("\nDébut du combat !")
while not player.pokemons[0].is_ko() and not rival.pokemons[0].is_ko():
    move = input(f"Quelle attaque utiliser ? ({', '.join(a['name'] for a in player.pokemons[0].attacks)}) : ")
    print(player.pokemons[0].perform_attack(rival.pokemons[0], move))
    
    if rival.pokemons[0].is_ko():
        print(f"{rival.name} a perdu !")
        break
    
    print(rival.pokemons[0].perform_attack(player.pokemons[0], "Flammèche"))

    if player.pokemons[0].is_ko():
        print(f"{player.name} a perdu !")
