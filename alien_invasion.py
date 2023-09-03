import sys
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet
from game_stats import GameStats
from settings import Settings
from ship import Ship


class AlienInvasion:
    """Classe geral para gerenciar ativos e comportamento do jogo"""

    def __init__(self) -> None:
        """Inicializa o jogo e cria recursos do jogo"""
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            size=(self.settings.screen_width, self.settings.screen_height)
        )
        # Full screen
        # self.screen = pygame.display.set_mode(size=(0, 0), flags=pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption(title="Alien Invasion")

        # Cria uma instância para armazenar estatísticas do jogo
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        self.game_active = True

    def run_game(self) -> None:
        """Inicia o loop principal do jogo"""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self) -> None:
        """Responde as teclas pressionadas e a eventos de mouse"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event=event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event=event)

    def _check_keydown_events(self, event: pygame.event.Event) -> None:
        """Responde a teclas pressionadas"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event: pygame.event.Event) -> None:
        """Responde a teclas liberadas"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self) -> None:
        """Cria um novo projétil e o adiciona ao grupo de projéteis"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self) -> None:
        """Atualiza a posição dos projéteis e descarta os projéteis antigos"""
        # Atualiza a posição dos projéteis
        self.bullets.update()

        # Descarta os projéteis que desaparecem
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self) -> None:
        """Responde à colisões alienígenas"""
        # Remove todos os projéteis e os alienígenas que tenham colidido
        collisions = pygame.sprite.groupcollide(
            groupa=self.bullets, groupb=self.aliens, dokilla=True, dokillb=True
        )

        if not self.aliens:
            # Destrói os projéteis existentes e cria uma frota nova
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self) -> None:
        """Verifica se a frota está na borda e, em seguida, atualiza as posições"""
        self._check_fleet_edges()
        self.aliens.update()

        # Detecta colisões entre alienígenas e espaçonaves
        if pygame.sprite.spritecollideany(sprite=self.ship, group=self.aliens):
            self._ship_hit()

        # Procura por alienígenas se chocando contra a parte inferior da tela
        self._check_aliens_bottom()

    def _ship_hit(self) -> None:
        """Responde à espaçonave sendo abatida por um alienígena"""
        if self.stats.ships_left > 0:
            # Decrementa ships_left
            self.stats.ships_left -= 1

            # Descarta quaisquer projéteis e alienígenas restantes
            self.bullets.empty()
            self.aliens.empty()

            # Cria uma frota nova e centraliza a espaçonave
            self._create_fleet()
            self.ship.center_ship()
            # Pausa
            sleep(0.5)
        else:
            self.game_active = False

    def _create_fleet(self) -> None:
        """Cria uma frota de alienígenas"""
        # Cria um alienígena e continua adicionando alienígenas
        # até que não haja mais espaço
        # O distanciamento entre alienígenas é de uma largura
        # de alienígena e uma altura de alienígena
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Termina uma fileira; redefine o valor de x e incrementa o valor de y
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position: int, y_position: int) -> None:
        """Cria um alienígena e o posiciona na fileira"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self) -> None:
        """Responde apropriadamente se algum alienígena alcançou uma borda"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self) -> None:
        """Faz toda a frota descer e mudar de direção"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self) -> None:
        """Verifica se algum alienígena chegou à parte inferior da tela"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Trata isso como se a espaçonave tivesse sido abatida
                self._ship_hit()
                break

    def _update_screen(self) -> None:
        """Atualiza as imagens na tela e muda para a nova tela"""
        self.screen.fill(color=self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        pygame.display.flip()


if __name__ == "__main__":
    # Cria uma instância do jogo e executa
    ai = AlienInvasion()
    ai.run_game()
