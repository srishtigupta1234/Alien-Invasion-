import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage ship."""

    def __init__(self, ai_game):
        """Initializing the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect() #rectange

        #Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship1.bmp')
        self.rect = self.image.get_rect()

        #start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom #midtop, midleft, midright
        
        #store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        self.moving_right = False #Movement flag
        self.moving_left = False

    def update_pos(self):
        """Update the ship position based on the movement flag."""
        # Update the ship's x value and not the rect.
        if  self.moving_right and self.rect.right < self.screen_rect.right: #Limiting the ships range.
           self.x += 2.0
        if  self.moving_left and self.rect.left > 0: # in case we used elif in place of if when we pressed both keys together(but in case if ship stand still.) then right key have always priority.
           self.x -= 2.0

        # Update rect object from self.x.
        self.rect.x = self.x
    
    
    def blitme(self):
     """Draw the ship at its currrent location"""
     self.screen.blit(self.image, self.rect)

    def center_ship(self):
       """Center the ship on the screen"""
       self.rect.midbottom = self.screen_rect.midbottom
       self.x = float(self.rect.x)