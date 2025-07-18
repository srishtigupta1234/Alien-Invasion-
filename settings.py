class Setting:
   """A class to store all settings of alien invasion"""
   def __init__(self):
        """Initializing the game settings"""
        #screen setting
      
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (135,206,250)
        
         # ship setting
        self.ships_limit = 3
        
        # Bullet setting
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 10
        
        
        self.fleet_drop_speed = 10
        
         
         # How quickly the game speed up
        self.speedup_scale = 1.2

        # How quickly the alien point val;ue increases.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

       

   def initialize_dynamic_settings(self):
       """Initialize the settings that change throughout the game."""
       self.ship_speed = 1.5
       self.bullet_speed = 3.0
       self.alien_speed = 1.0
        # scoring
       self.alien_points = 50
       
     # fleet directon of 1 represent right and -1 represent left
        
       self.fleet_direction = 1

   def increase_speed(self):
       """Increase speed settings"""
       self.ship_speed *= self.speedup_scale
       self.bullet_speed *= self.speedup_scale
       self.alien_speed *= self.speedup_scale
       self.alien_points = int(self.alien_points * self.score_scale)