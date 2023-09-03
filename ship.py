import pygame


class Ship:
    """Classe para gerenciar a espeçonave"""

    def __init__(self, ai_game) -> None:
        """Inicializa a espaçonave e define sua posiçào inicial"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Sobe a imagem da espaçonave o obtém seu rect
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()

        # Começa cada espaçonave nova no centro inferior da tela
        self.rect.midbottom = self.screen_rect.midbottom

        # Armazena um float para a posição horizontal exata da espaçonave
        self.x = float(self.rect.x)

        # Flag de movimento; começa com uma espaçonave que não está se movendo
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Atualiza a posição da espaçonave com base na flag de movimento"""
        # Atualiza o valor x da espaçonave, não o rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Atualiza o objeto rect de self.x
        self.rect.x = self.x

    def blitme(self) -> None:
        """Desenha a espaçonave em sua localização atual"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self) -> None:
        """Centraliza a espaçonave na tela"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
