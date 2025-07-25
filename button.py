import pygame.font

class Button:

    def __init__(self, ai_game, msg):
        """Initialize button attribute"""
        self.screen = ai_game.screen
        self.screen_rect =  self.screen.get_rect()

        #set the dimensions and properties of button.
        self.width , self.height =  200 , 50
        self.button_color = (0,255,0)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None, 48)

        #Buit the button 's rect object and cenrter it.
        self.rect = pygame.Rect(0, 0, self.width, self.height) 
        self.rect.center = self.screen_rect.center

        # The button msg need to prep only once
        self._prep_msg(msg)

    def _prep_msg(self,msg):
        """Turn the text into a reendered image and enter text on the screen"""
        self.msg_image = self.font.render(msg, True , self.text_color,
                self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw a message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)