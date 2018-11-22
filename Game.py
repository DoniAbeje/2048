#!/usr/bin/python3
'''        
---------------------------------------------------------------------
 Game.py
---------------------------------------------------------------------
 
--------------------------------------------------------------------- '''
import pygame, time, os.path
from Animation import Animation
from Tile import Tile
from Evaluator import Evaluator
from pygame.locals import*

class Game:
    def __init__(self, animation, evaluator):
        pygame.init()
        self.working_dir = os.getcwd()
        self.screen = pygame.display.set_mode((500,650))
        self.clock = pygame.time.Clock()
        self.screen.fill((100, 100, 200))
        self.arrow_sound_file = os.path.join(self.working_dir,'sound', 'arrow.wav')
        try:
        	self.arrow_sound = pygame.mixer.Sound(self.arrow_sound_file)
        except pygame.error:
        	raise SystemExit('Unable to load %s'%self.arrow_sound_file)

        self.font_file = os.path.join(self.working_dir,'font', 'hemi.ttf')
        self.board_font = pygame.font.Font(self.font_file, 20)
        self.tile_font = pygame.font.Font(self.font_file, 36)
        self.splash_font = pygame.font.Font(self.font_file, 65)
        try:
        	self.icon = pygame.image.load(os.path.join(self.working_dir,'img','icon.png'))
        except pygame.error:
        	raise SystemExit('Unable to load %s'%self.font_file)

        pygame.display.set_caption('2048')
        pygame.display.set_icon(self.icon)
        self.tiles = []
        self.evaluator = evaluator
        self.animation = animation
        self.done = False
                        
    def draw_All_Tiles(self):
        for tile in self.tiles:
            if tile.number != 0:
                tile.draw_Tile()
            
    def draw_Board(self):
        '''Draw the game board which includes score, highscore,
           newgame button and backgrounds'''
        
        score = self.board_font.render('SCORE ' + str(self.evaluator.score), 10, (255, 255, 255))
        highscore = self.board_font.render('HIGH SCORE ' + str(self.evaluator.highscore), 10, (255, 255, 255))
        self.newgame = self.board_font.render('NEW GAME', 10, (250, 250, 250))
        self.screen.fill((100, 100, 200))
        self.screen.blit(highscore,(20,20))
        self.screen.blit(score,(20,45))
        self.screen.blit(self.newgame,(480 - self.newgame.get_rect().width,20))
        pygame.draw.rect(self.screen, (90,90,190), pygame.Rect(0, 150, 500, 500))

        for col in range(0, 480, 120):
                 for row in range(150, 630, 120):
                     pygame.draw.rect(self.screen,(100, 100, 220), \
                                      pygame.Rect(col + self.tiles[0].spacing,\
                                                  row + self.tiles[0].spacing, 100, 100))

    def update_Tiles(self):
        '''Updates each tiles at the end of every self.animation'''
        
        numbers = self.evaluator.tiles  

        for index1, row in enumerate(range(150, 630, 120)):
                 for index2, col in enumerate(range(0, 480, 120)):
                     index = (index1 * 4) + index2
                     self.tiles[index].number = numbers[index1][index2]
                     self.tiles[index].left = col + self.tiles[0].spacing
                     self.tiles[index].top = row + self.tiles[0].spacing
                     self.tiles[index].text = self.tile_font.render(str(self.tiles[index].number), 10, (255, 255, 255))
                     self.tiles[index].width = self.tiles[index].height = 100
                     if self.tiles[index].number in self.tiles[index].color_key.keys():
                         self.tiles[index].bg_Color = self.tiles[index].color_key[self.tiles[index].number]
                     else: self.tiles[index].bg_Color = self.tiles[0].color_key[2048]

    def display_Splash(self):
        '''displays the splash screen'''
        
        self.screen.fill((255, 255, 255))
        splash_txt = self.splash_font.render('2048',10,(12 ,0 , 43))
        self.screen.blit(self.icon,(250 - self.icon.get_rect().width / 2,325 - self.icon.get_rect().height / 2))
        pygame.display.update()
        time.sleep(1)

    def triger_Up(self):
        ''' This function is called when up key is pressed. In turn it calls self.animation.mvUp()
            for every tile whose corresponding self.animation.distance value is differnt form zero'''
        for count in range(len(self.tiles)):
                    if self.animation.distance[count] != 0:
                        self.animation.mvUp(self.tiles[count], self.animation.initialTop[count], self.animation.distance[count], self)

    def triger_Down(self):
        ''' This function is called when Down key is pressed. In turn it calls self.animation.mvDown()
            for every tile whose corresponding self.animation.distance value is differnt form zero'''
        
        for count in range(len(self.tiles)):
                    if self.animation.distance[count] != 0:
                        self.animation.mvDown(self.tiles[count], self.animation.initialTop[count], self.animation.distance[count], self)

    def triger_Right(self):
        ''' This function is called when Right key is pressed. In turn it calls self.animation.mvRight()
            for every tile whose corresponding self.animation.distance value is differnt form zero'''
        
        for count in range(len(self.tiles)):
                    if self.animation.distance[count] != 0:
                        self.animation.mvRight(self.tiles[count], self.animation.initialLeft[count], self.animation.distance[count], self)
                        
    def triger_Left(self):
        ''' This function is called when Left key is pressed. In turn it calls self.animation.mvLeft()
            for every tile whose corresponding self.animation.distance value is differnt form zero'''
        
        for count in range(len(self.tiles)):
                    if self.animation.distance[count] != 0:
                        self.animation.mvLeft(self.tiles[count], self.animation.initialLeft[count], self.animation.distance[count], self)
    def triger_pop(self):
        ''' Calls self.animation.pop() for every tile whose corresponding self.animation.poping_tiles value is 1'''
        if 1 in self.animation.poping_tiles:
            for i in range(16):
                if self.animation.poping_tiles[i] != 0:
                    self.animation.pop(self.tiles[i], i, self)

        else:
            self.animation.animate_pop = False
            self.animation.accept_input = True

    def convert_distance(self, evaluator_distance):
        '''Convert multidimentional list into single list'''
        converted_list = []
        
        for col in range(4):
            for row in range(4):
                converted_list.append(evaluator_distance[col][row])
        return converted_list
    
    def update_Game(self):
        ''' updates the game'''
        while not self.done:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.evaluator.save()
                        self.done = True
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            x, y = event.pos
                            if x > 480 - self.newgame.get_rect().width and x < 480:
                                if y > 20  and y < 20 + self.newgame.get_rect().height:
                                    #Start new game
                                    evaluator.start()
                                    self.update_Tiles()

                            
                    elif event.type == pygame.KEYDOWN:                   
                            
                        if self.animation.accept_input:
                            
                            if event.key == pygame.K_RIGHT:
                                self.evaluator.swip_Horizontal()
                                if self.evaluator.is_tiles_changed:self.arrow_sound.play()
                                self.animation.tiles = self.evaluator.tiles
                                self.animation.distance = self.convert_distance(self.evaluator.distance)
                                self.animation.initialLeft = [tile.left for tile in self.tiles]
                                self.animation.moveRight = True
                                self.animation.poping_tiles  = self.convert_distance(self.evaluator.poping_tiles)
                                self.animation.accept_input = False
                                
                            if event.key == pygame.K_DOWN:
                                self.evaluator.swip_Vertical()
                                if self.evaluator.is_tiles_changed:self.arrow_sound.play()
                                self.animation.tiles = self.evaluator.tiles
                                self.animation.distance = self.convert_distance(self.evaluator.distance)
                                self.animation.initialTop = [tile.top for tile in self.tiles]
                                self.animation.moveDown = True
                                self.animation.poping_tiles  = self.convert_distance(self.evaluator.poping_tiles)
                                self.animation.accept_input = False
                                
                            if event.key == pygame.K_UP:
                                self.evaluator.swip_Vertical(True)
                                if self.evaluator.is_tiles_changed:self.arrow_sound.play()
                                self.animation.tiles = self.evaluator.tiles
                                self.animation.distance = self.convert_distance(self.evaluator.distance)
                                self.animation.initialTop = [tile.top for tile in self.tiles]
                                self.animation.moveUp = True
                                self.animation.poping_tiles  = self.convert_distance(self.evaluator.poping_tiles)
                                self.animation.accept_input = False
                                
                            if event.key == pygame.K_LEFT:
                                self.evaluator.swip_Horizontal(True)
                                if self.evaluator.is_tiles_changed:self.arrow_sound.play()
                                self.animation.tiles = self.evaluator.tiles
                                self.animation.distance = self.convert_distance(self.evaluator.distance)
                                self.animation.initialLeft = [tile.left for tile in self.tiles]
                                self.animation.moveLeft = True
                                self.animation.poping_tiles  = self.convert_distance(self.evaluator.poping_tiles)
                                self.animation.accept_input = False

                            if not self.evaluator.is_tiles_changed:
                                self.animation.accept_input = True
                                self.animation.moveLeft = self.animation.moveRight = self.animation.moveUp = self.animation.moveDown = False



            
            self.draw_Board()
            self.draw_All_Tiles()
            self.animation.time_passed_second = self.clock.tick(60) / 1000.0
            
            if self.animation.animate_pop:
                self.triger_pop()

            if self.animation.moveRight :
                self.triger_Right()
                
            if self.animation.moveDown :
                self.triger_Down()
                
            if self.animation.moveLeft :
                self.triger_Left()
                
            if self.animation.moveUp :
                self.triger_Up()
            
            pygame.display.flip()
            
        pygame.quit()

if __name__ == '__main__':
    animation = Animation()
    evaluator = Evaluator()
    evaluator.read()
    game = Game(animation, evaluator)
    tiles = []

    for index1, row in enumerate(range(150, 630, 120)):
                 for index2, col in enumerate(range(0, 480, 120)):
                     tiles.append(Tile(game.screen, col, row,evaluator.tiles[index1][index2], 100, 100))

    game.tiles = tiles
    game.display_Splash()
    game.update_Game()
    
