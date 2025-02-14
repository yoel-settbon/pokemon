from models.menu import Menu
if __name__ == "__main__":
    menu_options = ['New Game', 'Load Game', 'Quit']
    menu = Menu(1100, 700, "assets/image/background.png", "assets/font/upheavtt.ttf", menu_options)
    menu.run()