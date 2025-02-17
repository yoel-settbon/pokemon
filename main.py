import pygame
pygame.mixer.init()

from models.menu import Menu
from models.game import Game

if __name__ == "__main__":
    menu_options = ['New Game', 'Load Game', 'Quit']
    menu = Menu(1100, 700, "assets/image/background.png", "assets/font/upheavtt.ttf", menu_options)
    
    choice = menu.run()
    if choice == "New Game":
        game = Game()
        game.game_music()
        game.run()
