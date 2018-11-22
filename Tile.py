#!/usr/bin/python3
'''        
---------------------------------------------------------------------
 Tile.py
---------------------------------------------------------------------
 
--------------------------------------------------------------------- '''
import pygame
class Tile:
    def __init__(self, screen, left, top, number, height = 100, width = 100):
        self.color_key = {0:(100, 100, 220),2:(50 ,50 ,200 ),4:( 200, 0 , 100),8:( 235,60 ,60 ), \

        16:( 110, 15, 115),32:( 12, 100 , 100),64:(0 ,0 , 120),128:(190 ,78 ,123 ),256:(12 ,0 , 43), \

        512:( 111,111 , 0),1024:(90 ,12 ,255 ),2048:( 255, 0, 0)}
        
        self.screen = screen
        self.height = height
        self.width = width
        self.number = number
        self.spacing = 20
        self.font = pygame.font.Font('./font/hemi.ttf', 36)
        self.text = self.font.render(str(self.number), 10, (255,255,255))
        self.left = left + self.spacing
        self.top = top + self.spacing
        if self.number in self.color_key.keys(): self.bg_Color = self.color_key[number]
        else: self.bg_Color = self.color_key[2048]
        
    def draw_Tile(self):
        pygame.draw.rect(self.screen, self.bg_Color,pygame.Rect(self.left, self.top, self.width, self.width))
        self.screen.blit(self.text, self.text.get_rect(centerx = self.left + (self.width/2), centery = self.top + (self.width/2)))
