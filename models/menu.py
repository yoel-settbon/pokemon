import pygame
import sys
from models.game import Game

pygame.init()

class Menu:
    def __init__(self, width, height, background_image, font_path, menu_options):
        self.width = width
        self.height = height
        self.menu_options = menu_options
        self.selected_option = 0

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pokemon Fighters")

        self.background = pygame.image.load(background_image)
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        self.menu_font = pygame.font.Font(font_path, 60)
        self.title_font = pygame.font.Font(font_path, 100)

    def draw_text(self, text, font, color, x, y):
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        self.screen.blit(text_surf, text_rect)

    def draw_menu(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_text("FIGHTERS", self.title_font, (255, 255, 255), self.width // 2.6, self.height // 2.4)
        
        for i, option in enumerate(self.menu_options):
            color = (255, 150, 203) if i == self.selected_option else (255, 255, 255)
            text = self.menu_font.render(option, True, color)
            text_rect = text.get_rect(center=(self.width // 2.6, self.height // 1.5 + i * 50))
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                elif event.key == pygame.K_RETURN:
                    if self.menu_options[self.selected_option] == 'New Game':
                        game = Game()
                        game.run()
                    elif self.menu_options[self.selected_option] == 'Load Game':
                        print("Chargement du jeu...")
                    elif self.menu_options[self.selected_option] == 'Quit':
                        return False
        return True

    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.draw_menu()
        
        pygame.quit()
        sys.exit()