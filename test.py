    def game_music(self):  (class game)
        pygame.mixer.music.stop()
        pygame.mixer.music.load('assets/audio/battle-theme.wav')
        pygame.mixer.music.play(-1) 
        pygame.mixer.music.set_volume(1.0)


        def game_over_sequence(self): (class game)
        pygame.mixer.music.stop()
        pygame.mixer.music.load('assets/audio/game-over-voice.wav')
        pygame.mixer.music.play()
        self.win.blit(self.game_over_img, (0, 0))
        pygame.display.flip()
        pygame.time.delay(5000)


    def menu_music(self):  (class menu)
        pygame.mixer.music.stop()
        pygame.mixer.music.load('assets/audio/menu-theme.wav')
        pygame.mixer.music.play(-1)