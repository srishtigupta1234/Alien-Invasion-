import sys
from time import sleep

import pygame

from settings import Setting
from game_stats import GameStat
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Create an overall classto manage game asset and behaviour."""
    def __init__(self):
     """Initializing the game, and create game resources. """
     pygame.init()#pygame.init() function initializes the background settings that Pygame needs to work properly u
     
     self.settings = Setting()
     self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN) #Fullscreen mode
     self.settings.screen_width = self.screen.get_rect().width
     self.settings.screen_height = self.screen.get_rect().height     
     
     pygame.display.set_caption("Alien Invasion")
     
     #create an instance to store game statistics
      # and create a scoreboard.

     self.stats  = GameStat(self)
     self.sb = Scoreboard(self) 
     self.ship = Ship(self)
     self.bullets = pygame.sprite.Group()
     self.aliens = pygame.sprite.Group()
     self._create_fleet_()

     #make the play button
     self.play_button = Button(self, "Play")
   #  # Set background colour Colors in Pygame are specified as RGB colors: a mix of red, green,and blue. Each color value can range from 0 to 255. The color value (255,0, 0) is red, (0, 255, 0) is green, and (0, 0, 255) is blue. You can mix differentRGB values to create up to 16 million colors. The color value (230, 230,230) mixes equal amounts of red, blue, and green, which produces a lightgray background color. We assign this color to self.bg_color u.At v, we fill the screen with the background color using the fill()method, which acts on a surface and takes only one argument: a color.
   #   self.bg_color = (230,230,230)
   #   self.screen.fill(self.bg_color)
    
    def run_game(self):
       """Start the main loop for the game."""
       while True: #An event is an action that the user performs while playing the game, such as pressing a key or moving the mouse. To make our program respond to events, we write this event loop to listen for events and perform appropriate tasks depending on the kinds of events that occur
          self._check_events()

          if self.stats.game_active:
           self.ship.update_pos()
           self._update_bullets()
           self._update_aliens()  
          
          self.update_screen()


    def _ship_hit(self):
       """Respond to the ship being hity by an alien.""" 
       if self.stats.ships_left > 0:
          #Decreament ship_left.
          self.stats.ships_left -= 1
          self.sb.prep_ships()
          #Get rid of remaining alien and ship
          self.aliens.empty()
          self.bullets.empty()
          #Create a new fleet and center the ship
          self._create_fleet_()
          self.ship.center_ship()
          #Pause
          sleep(0.5)
       else:
          self.stats.game_active = False 
          pygame.mouse.set_visible(True)



    def _update_bullets(self): 
          """Update position of bullets and get rid of old bullets"""
          # Update bullets position      
          self.bullets.update()
         
         #Get rid of bullets.
          for bullet in self.bullets.copy(): 
             if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
          print(len(self.bullets))

         # check for any bullet that have hits aliens
         # if so, get rid of bullet and aliens
          self._check_bullet_alien_collisions()
    
    def _check_bullet_alien_collisions(self):
       """Respond trhe bullet alien collision"""
       #Remove any bullets and aliens that have collided
       collisions = pygame.sprite.groupcollide(
                   self.bullets, self.aliens, True, True)
       
       if collisions:
          for aliens in collisions.values():
             self.stats.score += self.settings.alien_points * len(aliens)
          self.sb.prep_score()
          self.sb.check_high_score()
       if not self.aliens:
             # Destroy exisxting bullets and create new fleet.
             self.bullets.empty()
             self._create_fleet_()
             self.settings.increase_speed()

             # Increase level
             self.stats.level += 1
             self.sb.prep_level()

   
    def _update_aliens(self):
       """ Check the fleet is at an edge
       Update the position of all aliens in the fleet """
       self._check_fleet_edges()
       self.aliens.update()

       #Look for alien_ship collision
       if pygame.sprite.spritecollideany(self.ship, self.aliens):
          self._ship_hit()

       # Look for alien hitting the bottom of the screen.
       self._check_aliens_bottom()

    
    def _check_aliens_bottom(self):
       """Check if any alien have reached the bottom of the screen"""
       screen_rect = self.screen.get_rect()
       for alien in self.aliens.sprites():
          if alien.rect.bottom >= screen_rect.bottom:
             #Treat the same as if ship got hit
             self._ship_hit()
             break

    def _check_fleet_edges(self):
       """Respond appropriately  if any alien reached on edge"""
       for alien in self.aliens.sprites():
          if alien.check_edges():
             self.change_fleet_direction()
             break

    def change_fleet_direction(self):
       """Drop the entire fleet and change the fleet's direction."""
       for alien in self.aliens.sprites():
          alien.rect.y += self.settings.fleet_drop_speed
       self.settings.fleet_direction *= -1    

    def _check_events(self): #refactoring check event.
         for event in pygame.event.get():   #To access the events that Pygame detects, we’ll use the pygame.event .get() function This function returns a list of events that have taken place since the last time this function was called. Any keyboard or mouse event will cause this for loop to run. Inside the loop, we’ll write a series of if statements to detect and respond to specific events
            if event.type == pygame.QUIT: 
               sys.exit()
            elif event.type == pygame.KEYDOWN: #right key press registered as keydown event.
               self._check_kewdown_events(event)
            elif event.type == pygame.KEYUP:
               self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
               mouse_pos = pygame.mouse.get_pos()
               self._check_play_button(mouse_pos)
    
    def _check_play_button(self,mouse_pos):
       """Start a new game when a player clicks play."""
       button_clicked = self.play_button.rect.collidepoint(mouse_pos) 
       if button_clicked and not self.stats.game_active:
          # Reset the game settings.
          self.settings.initialize_dynamic_settings()
          # Reset the game statistics. 
          self.stats.reset_stats()
          self.stats.game_active = True
          self.sb.prep_score()
          self.sb.prep_level()
          self.sb.prep_ships()
         #Get rid of any rfemaining alien and bullet 
          self.aliens.empty()
          self.bullets.empty()

         # Create a new fleet and center the ship
          self._create_fleet_()
          self.ship.center_ship()

          #Hide the mouse cursor .
          pygame.mouse.set_visible(False)


    def _check_kewdown_events(self,event):
       """Respond to keypress"""
       if event.key == pygame.K_RIGHT:
         #move the ship to right
         self.ship.moving_right = True
       elif event.key == pygame.K_LEFT:
         self.ship.moving_left = True
       elif event.key == pygame.K_q:
          sys.exit()
       elif event.key == pygame.K_SPACE:
          self._fire_bullet()

    def _check_keyup_events(self,event):
       """Respond to keyreleases."""
       if event.key == pygame.K_RIGHT:
         self.ship.moving_right = False
       elif event.key == pygame.K_LEFT:
         self.ship.moving_left = False
    

    def _create_fleet_(self):
       """Create rthe fleet of ALIENS"""
       # make an alien
       alien = Alien(self)
       alien_width,alien_height = alien.rect.size
       available_space_x = self.settings.screen_width - (2 * alien_width) 
       number_aliens_x = available_space_x // (2 * alien_width )

       # Determine the number of rows of alien fits on the screen
       ship_height = self.ship.rect.height
       available_space_y = (self.settings.screen_height -
                            (3 * alien_height) - ship_height)
       number_rows = available_space_y // (2* alien_height) 

       #Create the full fleet of alien
       
       for row_number in range(number_rows):
         for alien_number in range(number_aliens_x):
           self._create_alien(alien_number,row_number)
          
    def _create_alien(self, alien_number , row_number):
          """Create  an alien and place it in the row"""
          alien = Alien(self) 
          alien_width , alien_height = alien.rect.size
          alien.x = alien_width + 2 * alien_width * alien_number
          alien.rect.x = alien.x
          alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
          self.aliens.add(alien)  

      
    def _fire_bullet(self):
       """Create a new bullet and add it to bullet group."""
       if len(self.bullets) < self.settings.bullets_allowed:
          new_bullet = Bullet(self)
          self.bullets.add(new_bullet) 

    def update_screen(self): #update theimage on the screen, and flip to the new screen. 
         #redraw the screen during each pass through the loop.
          self.screen.fill(self.settings.bg_color)
          self.ship.blitme()
          for bullet in self.bullets.sprites():
             bullet.draw_bullet()
          self.aliens.draw(self.screen) 

          # Draw the score info.
          self.sb.show_score()

          #Draw the play button
          if not self.stats.game_active:
             self.play_button.draw_button()
    

          #Make the most recently drawn school visible.
          pygame.display.flip() #The call to pygame.display.flip() at z tells Pygame to make the most recently drawn screen visible.
if __name__ =='__main__': #file, we create an instance of the game,We place run_game() in an if block that only runs if the file is called directly.
#make a game instance and run the game
 ai = AlienInvasion()
 ai.run_game()
     