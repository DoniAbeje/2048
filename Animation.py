#!/usr/bin/python3
'''        
---------------------------------------------------------------------
 Animation.py
---------------------------------------------------------------------
 
--------------------------------------------------------------------- '''
class Animation:
    def __init__(self):
        self.animate_to = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        self.animate_pop = self.moveRight = self.moveDown = self.moveUp = self.moveLeft = False
        self.initialLeft = []
        self.initialTop = []
        self.movement_speed = 800 #px/sec
        self.pop_width_speed = 400 #px/sec
        self.pop_top_speed = 200 #px/sec
        self.tiles = []
        self.poping_tiles = []
        self.distance = []
        self.accept_input = True
        self.time_passed_second = 0
        
    def pop(self, tile, tile_index, game_object):
        dwidth = int(self.time_passed_second * self.pop_width_speed)
        dtop = int(self.time_passed_second * self.pop_top_speed)
        if self.animate_to[tile_index] == 1:
            tile.width += dwidth
            tile.height += dwidth
            tile.top -= dtop
            tile.left -= dtop
        elif self.animate_to[tile_index] == -1:
            tile.width -= dwidth
            tile.height -= dwidth
            tile.top += dtop
            tile.left += dtop
            
        if tile.width >= 124: self.animate_to[tile_index] = -1
        
        elif tile.width <= 100:
            self.animate_pop = False
            self.animate_to[tile_index] = 1
            game_object.update_Tiles()
            self.accept_input = True
            
            
    def mvRight(self, tile,initialLeft, tile_distance , game_object):
        
        if self.moveRight and tile.left < tile_distance * (120) + initialLeft:
            distance = self.time_passed_second * tile_distance * self.movement_speed
            tile.left += distance
            
        else:
            self.moveRight = False
            self.animate_pop = True
            game_object.update_Tiles()
            

            
    def mvDown(self, tile,initialTop, tile_distance , game_object):
        if self.moveDown and tile.top < tile_distance * (120) + initialTop:
            distance = self.time_passed_second * tile_distance * self.movement_speed
            tile.top += distance
            
        else:
            self.moveDown = False
            self.animate_pop = True
            game_object.update_Tiles()
            
    def mvLeft(self, tile,initialLeft, tile_distance , game_object):
        
        if self.moveLeft and tile.left > initialLeft - tile_distance * (120):
            distance = self.time_passed_second * tile_distance * self.movement_speed
            tile.left -= distance
        
        else:
            
            self.moveLeft = False
            self.animate_pop = True
            game_object.update_Tiles()
            
    def mvUp(self, tile,initialTop, tile_distance , game_object):
        if self.moveUp and tile.top > initialTop - tile_distance * (120):
            distance = self.time_passed_second * tile_distance * self.movement_speed
            tile.top -= distance
            
        else:
            self.moveUp = False
            self.animate_pop = True
            game_object.update_Tiles()


