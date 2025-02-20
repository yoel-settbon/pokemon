
def menu(self):
        from models.menu import Menu
        menu = Menu(1100, 700, "assets/image/background.png", "assets/font/upheavtt.ttf", ['New Game', 'Load Game', 'Quit'])
        menu.run()

    def game_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load('assets/audio/battle-theme.wav')
        pygame.mixer.music.play(-1) 
        pygame.mixer.music.set_volume(1.0)