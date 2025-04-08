class GameStat:
    """Track statistic for alien invasion."""

    def __init__(self, ai_game):
        """Initialize the statistics"""
        self.settings = ai_game.settings
        self.reset_stats()
        # Start alieninvasion in an active stat
        self.game_active = False
        # High score should no. be reset.
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ships_limit
        self.score = 0
        self.level = 1

