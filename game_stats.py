class GameStats:
    """Rastreia as estatísticas de Invasão Alienígena"""

    def __init__(self, ai_game) -> None:
        """Inicializa as estatísticas"""
        self.settings = ai_game.settings
        self.reset_stats()

        # A pontuação máxima nunca dever ser redefinida
        self.high_score = 0

    def reset_stats(self) -> None:
        """Inicializa as estatíticas que podem mudar durante o jogo"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
