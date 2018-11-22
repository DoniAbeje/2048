#!/usr/bin/python3
'''        
---------------------------------------------------------------------
 Evaluator.py
---------------------------------------------------------------------
 
--------------------------------------------------------------------- '''
import random, pickle
class Evaluator:
    def __init__(self):
        self.tiles = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.distance = self.tiles[:]
        self.poping_tiles = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.is_tiles_changed = True
        self.score = 0
        
    def transpose(self, input_list):
        transposed_list = [[],[],[],[]]
        for i in range(4):
            for j in range(4):
                transposed_list[i].append(input_list[j][i])
        return transposed_list
    
    def sort_list(self, input_list, isreversed = False):

            sorted_list = [] 
            for item in input_list:
                    if item == 0: sorted_list.insert(0, 0)
            
                    else:sorted_list.append(item)

            if isreversed:
                    sorted_list.reverse()
                    sorted_list = self.sort_list(sorted_list)
            return sorted_list


    def swip_Horizontal(self, isToTheLeft = False):
        self.poping_tiles = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.distance = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.is_tiles_changed = False
        self.distance_calculator(self.tiles, False, isToTheLeft)

        for i in range(4):
            self.tiles[i] = self.evaluate(self.sort_list(self.tiles[i], isToTheLeft), isToTheLeft, i, self.tiles[i][:])
      
        self.random_generetor()
        #update high score
        if self.score > self.highscore:
                self.highscore = self.score
                
    def swip_Vertical(self, isUp = False):
            self.poping_tiles = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
            self.distance = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
            self.is_tiles_changed = False
            transposed_tiles = self.transpose(self.tiles)
            self.distance_calculator(transposed_tiles, True, isUp)

            for i in range(4):
                    transposed_tiles[i] = self.evaluate(self.sort_list(transposed_tiles[i], isUp), isUp, i, transposed_tiles[i], True)  

            self.tiles = self.transpose(transposed_tiles)
            self.poping_tiles = self.transpose(self.poping_tiles)
           
            self.random_generetor()
            #update high score
            if self.score > self.highscore:
                self.highscore = self.score
            
    def distance_calculator(self, tiles, isvertical = False, isreversed = False):
        ''' calculates the distance each tile has to travel'''
        checking_order = range(3, 0, -1)
        distance = self.distance
        if isvertical:
            distance = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        if isreversed:
            checking_order = range(3)
        for row in range(4):
            for col in checking_order:
                if tiles[row][col] == 0:
                    changing_order = range(col)
                    if isreversed:
                        changing_order = range(col + 1, 4)
                    for i in changing_order:
                        if tiles[row][i] != 0:
                            distance[row][i] += 1
                            self.is_tiles_changed = True
        if isvertical:
                distance = self.transpose(distance)
                for row in range(4):
                    for col in range(4):
                        self.distance[row][col] += distance[row][col]
                        
    def random_generetor(self):
        if self.is_tiles_changed:
            select_from_list = []
            # select_from_list contains index of empty tiles
            for row in range(4):
                for col in range(4):
                    if self.tiles[row][col] == 0:
                        select_from_list.append((row, col))
            selected_index = random.choice(select_from_list)
            #select 2 or 4 from 80% occurrence probability given to 2
            self.tiles[selected_index[0]][selected_index[1]] = random.choice([2, 2, 2, 2, 4])

    def start(self):
        #called on new game
        self.__init__()
        first_index = random.choice(range(4)), random.choice(range(4))
        second_index = random.choice(range(4)) , random.choice(range(4))
        
        #make sure first index is different from second_index
        while first_index == second_index:
            first_index = random.choice(range(4)), random.choice(range(4))
            second_index = random.choice(range(4)) , random.choice(range(4))
        self.tiles[first_index[0]][first_index[1]] = self.tiles[second_index[0]][second_index[1]] = 2

    def save(self):
        ''' save game state '''
        file_handler = open('data.dat', 'wb')
        self.data['score'] = self.score
        self.data['tiles'] = self.tiles
        self.data['highscore'] = self.highscore
        pickle.dump(self.data, file_handler)
        file_handler.close()
        
    def read(self):
        ''' read game state '''
        try:
            file_handler = open('data.dat', 'rb')
            self.data = pickle.load(file_handler)
            self.tiles = self.data['tiles']
            self.score = self.data['score']
            self.highscore = self.data['highscore']
            file_handler.close()
        except:
            
            self.start()
            self.highscore = 0
            self.data = {}

        
    def evaluate(self, sorted_list, isreversed, tile_index, tile, isvertical = False):
            ''' does all the math '''
            reversedl = tile[:]
            distance = self.distance
            if isvertical:
                distance= [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
            if not isreversed:
                    reversedl.reverse()

            for i in range(3,0,-1):
                    if sorted_list[i] == 0: break
                    else:
                            if sorted_list[i] == sorted_list[i-1]:
                                    if i == 3:sorted_list[1] ,sorted_list[2] = sorted_list[0], sorted_list[1]
                                    elif i == 2:
                                            sorted_list[1] = sorted_list[0] 

                                    
                                    first_last_index= reversedl.index(sorted_list[i])
                                    reversedl[first_last_index] = -1
                                    next_last_index = reversedl.index(sorted_list[i])
                                    reversedl[next_last_index] = -1
                                    distance_change_index = first_last_index
                                    
                                    if not isreversed:
                                            distance_change_index =3 - first_last_index
                                    changing_range = range(distance_change_index + 1, 4)
                                    if not isreversed:
                                            changing_range = range(distance_change_index)
                                    
                                    for x in changing_range:
                                            if tile[x] != 0:
                                                    distance[tile_index][x] += 1
                                                

                                    sorted_list[i] *= 2
                                    self.score += sorted_list[i]
                                    sorted_list[0] = 0
                                    self.is_tiles_changed = True
                                    if isreversed:
                                        self.poping_tiles[tile_index][first_last_index] = 1
                                    else:
                                        self.poping_tiles[tile_index][i] = 1
                            
            if isvertical:
                distance = self.transpose(distance)
                for row in range(4):
                    for col in range(4):
                        self.distance[row][col] += distance[row][col]
            if isreversed: sorted_list.reverse()
            return sorted_list
if __name__ == '__main__':
    #----------Test-----------
    e = Evaluator()
    e.read()
    for item in e.tiles:
        print(item)
    swip = input()

    while swip != 'q':
            if swip == 'l':
                    e.swip_Horizontal(True)
                    
            if swip == 'r':
                    e.swip_Horizontal()

            if swip == 'd':
                    e.swip_Vertical()

            if swip == 'u':
                    e.swip_Vertical(True)
            
            for item in e.tiles:
                print (item)
            print(e.poping_tiles)
            print(e.is_tiles_changed)
            swip = input()
    e.save()
