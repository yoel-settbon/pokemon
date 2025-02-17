import pygame
pygame.mixer.init()

from models.menu import Menu
from models.game import Game  # ✅ Ajout de l'import du jeu

if __name__ == "__main__":
    menu_options = ['New Game', 'Load Game', 'Quit']
    menu = Menu(1100, 700, "assets/image/background.png", "assets/font/upheavtt.ttf", menu_options)
    
    choice = menu.run()  # ✅ Récupérer le choix du menu
    if choice == "New Game":  # ✅ Si le joueur choisit "New Game"
        game = Game()
        game.game_music()  # ✅ Lancer la musique de combat
        game.run()  # ✅ Lancer le jeu
