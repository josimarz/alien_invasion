import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Classe para gerenciar os projéteis disparados da espaçonave"""

    def __init__(self, ai_game) -> None:
        """Cria um objeto bullet na posição atual da espaçonave"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Cria um bullet na posição correta
        left, top = ai_game.ship.rect.midtop
        self.rect = pygame.Rect(
            left, top, self.settings.bullet_width, self.settings.bullet_height
        )

        # Armazena a posição do projétil como um float
        self.y = float(self.rect.y)

    def update(self) -> None:
        """Desloca o projétil veticalmente pela tela"""
        # Atualiza a posição exata do projétil
        self.y -= self.settings.bullet_speed
        # Atualiza a posição do rect
        self.rect.y = self.y

    def draw_bullet(self) -> None:
        """Desenha o projétil na tela"""
        pygame.draw.rect(surface=self.screen, color=self.color, rect=self.rect)
