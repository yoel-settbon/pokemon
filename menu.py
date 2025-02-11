# menu.py
import pygame

class Menu:
    def __init__(self, width=900, height=600):
        self.HEIGHT = height
        self.WIDTH = width
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pokemon Fighters")

        self.background = pygame.image.load("assets/image/background2.jpg")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        self.battle = pygame.image.load("assets/image/battle.webp")
        self.battle = pygame.transform.scale(self.battle, (self.WIDTH, self.HEIGHT)) 
        self.tittle = pygame.image.load("assets/image/tittle.png")

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        self.tittle_font = pygame.font.Font("assets/font/upheavtt.ttf", 80)
        self.menu_font = pygame.font.Font("assets/font/upheavtt.ttf", 45)

    def draw_text(self, text, font, color, x, y):
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        self.window.blit(text_surf, text_rect)

    def menu(self):
        self.window.blit(self.background, (0, 0))
        self.window.blit(self.tittle, (150, 0))
        self.draw_text("FIGHTERS", self.tittle_font, self.WHITE, self.WIDTH // 1.9, self.HEIGHT // 2.4)
        self.draw_text("NEW GAME", self.menu_font, self.WHITE, self.WIDTH // 1.9, self.HEIGHT // 1.8)
        pygame.display.update()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.start()

    def start(self):
        self.window.blit(self.background, (0, 0))
        self.window.blit(self.tittle, (150, 0))
        self.draw_text("FIGHTERS", self.tittle_font, self.WHITE, self.WIDTH // 1.9, self.HEIGHT // 2.4)
        self.draw_text("Press ENTER to start", self.menu_font, self.WHITE, self.WIDTH // 1.9, self.HEIGHT // 1.5)
        pygame.display.update()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.menu()
