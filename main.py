import pygame
import sys
pygame.mixer.init()

from models.menu import Menu
from models.game import Game

if __name__ == "__main__":
    try:
        menu_options = ['New Game', 'Load Game', 'Quit']
        menu = Menu(1100, 700, "assets/image/background.png", "assets/font/upheavtt.ttf", menu_options)
        
        choice = menu.run()
        print(f"Option sélectionnée : {choice}")
        if choice == "New Game":
            game = Game()
            game.run()
    except Exception as e:
        print(f"Erreur dans main.py : {e}")
        pygame.quit()
        sys.exit()