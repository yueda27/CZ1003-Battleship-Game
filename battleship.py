#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 20:03:44 2019

@author: yueda27
"""
import numpy as np
import hashlib
from random import randint


class GameBoard:
    '''Define a game board for each user.
    inputs: Dimensions(int): Size of board. Default = 10
            layers(int): layers of board. Default = 2'''
    def __init__(self, dimension = 10, layers = 2):
        self.x_size = dimension
        self.y_size = dimension
        self.layers = layers
        self.board = np.zeros((self.layers, self.x_size, self.y_size))
    
    def load_ship(self, ship, x, y, orientation, user_type = ''):
        '''Method to load ship into location
        '''
        #Check if ship has already been loaded
        if ship.loaded:
            raise Exception('Ship has already been loaded!')
        #Check type of ship and auto select which layer to place
        if not ship.submerse:
            layer = 1
        elif ship.submerse:
            layer = 0
        #check for overlap when loading new ship
        self._check_overlap(layer, x, y, ship.length, orientation)
        #Loading algorithm python 2D list= [layer, y, x]
        if orientation == 'vertical':
            for i in range(ship.length):
                self.board[layer, y-1 + i, x-1] = 1
                ship._location.append((layer, y-1 + i, x-1))
        
        elif orientation == 'horizontal':
            for i in range(ship.length):
                self.board[layer, y-1, x-1+i] = 1
                ship._location.append((layer, y-1, x-1+i))
        else:
            raise Exception('Orientation is invalid')
        if user_type != 'Computer':
            print('{} vessel is loaded in at ({},{},{}).'.format(ship.name, layer, x, y))
        #Change ship loaded status
        ship.loaded = True
    
    
    def get_result(self, layer, x, y):
        if self.board[layer, x, y] == 1:
            return True
        else: 
            return False
        
        
    def print_board(self, hide):
        '''Print the board out in the right format for user'''
        #Still need to work on formatting
        #Icon_map to map 0,1,2 to the right sign for display
        icon_map = self._icon_map(hide)
        for layer in range(self.layers):
            if layer == 0:
                print('''
                 ——————————      
                 UNDERWATER
                 ——————————''')
                print()
                print('  ', end = '')
            else:
                print('''  
                    ———————
                    SURFACE
                    ———————''')
                print()
                print('  ', end = '')
                
            #Print x-axis numbering
            print(' ', end = '')
            for i in range(self.x_size-1):
                if i == 0:
                    print("", ' {} '.format(i+1), end ='|')
                else:
                    print(' {} '.format(i+1), end ='|')
            print(' {} '.format(self.x_size))
                                 
            #Print y-axis numbering 
            print("   ", "---------------------------------------",end = ' ')
            print()
            for y in range(self.y_size):
                if y<self.y_size-1:
                    print(" ",y+1 ,"|" ,sep = "", end = ' ')      
                else:
                    print(y+1,"|",sep = "", end = ' ')  
                    
                #Print attack slots
                for x in range(self.x_size):
                    if x == self.x_size-1:
                        print(icon_map.get(self.board[layer][y][x]))
                        print("   ", "---------------------------------------",end = ' ')
                        print()
                    else:
                        print(icon_map.get(self.board[layer][y][x]), end = ' ')
                        
                        
    def _icon_map(self, hide):
        '''Return icon map for correct abstraction. To hide vessel location from enemy'''
        if hide:
            return {0: '[ ]',
                    1: '[ ]',
                    2: ' X ',
                    -1: '___'}
        else:
            return {0: '[ ]',
                    1: ' O ',
                    2: ' X ',
                    -1: '___'}
    def _check_overlap(self, layer, x, y, length, orientation):
        '''Check if the intended loading location is already occupied by a ship. If occupied: raise Exception'''
        
        if orientation == 'vertical':
            for i in range(length):
                if self.board[layer, y-1+i, x-1] == 1:
                    raise Exception('There is a vessel in the way at location: ({},{}.{})'.format(layer, y-1+i, x-1))
                    return False
                
        
        if orientation == 'horizontal':
            for i in range(length):
                if self.board[layer, y-1, x-1+i] == 1:
                    raise Exception('There is a vessel in the way at location: ({},{}.{})'.format(layer, y-1, x-1+i))
                    
                






class Ship:
    '''Ship class that has characteristics of the ship. Parent class to SubmerseShip and SurfaceShip'''
    def __init__(self, length, name = ''):
        self.length = length
        self._location = []
        self.name = name
        self.loaded = False
        self.float_status = True
        self.grids_left = length
        
    def check_status(self):
        '''Check if the vessel has been sunk'''
        if self.grids_left == 0:
            self.float_status = False

#SubmerseShip class and SurfaceShip class both child class of ship. Only difference is the submerse status
class SubmerseShip(Ship):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.submerse = True
        
class SurfaceShip(Ship):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.submerse = False
        
        
        
        
        

class Player:
    '''Player class which is parent for User and Computer.'''
    def __init__(self, name):
        self.name = name
        self.point = 0
        #List of default ships for each player
        self.ships = [#SurfaceShip(length = 5, name = 'Surface Carrier'),
                      #SurfaceShip(length = 3, name = 'Surface Cruiser'),
                      SurfaceShip(length = 2, name = 'Surface Destroyer'),
                      SubmerseShip(length = 1, name = 'Submersive Submarine'),
                      SubmerseShip(length = 1, name = 'Submersive Torpedo')]
        self.game_board = GameBoard()
        self.total_point = self._get_total_points()
        self.ship_map =  {}
        
    def _get_total_points(self):
        total = 0
        for ship in self.ships:
            total += ship.length
        return total
    def attack_enemy(self, enemy, location):
        '''Method to attack enemy. 
        If target is hit, enemy board location will change to 2 and return True'''
        #Unpack location list
        layer, x, y = location
        
        if enemy.game_board.board[layer-1, y-1, x-1] == 1:
            enemy.game_board.board[layer-1, y-1, x-1] = 2
            self.point += 1
            #for ship_name, grid_locations in :
            #Print enemy board with hidden layer
            enemy.game_board.print_board(hide = True)
            print('''   
                            HIT
                             ____
                     __,-~~/~    `---.
                   _/_,---(      ,    )
               __ /        <    /   )  \___
- ------===;;;'====------------------===;;;===----- -  -
                  \/  ~"~"~"~"~"~\~"~)~"/
                  (_ (   \  (     >    \)
                   \_( _ <         >_>'
                      ~ `-i' ::>|--"
                          I;|.|.|
                         <|i::|i|`.
                        (` ^'"`-' ")
------------------------------------------------------------------''')
        else:
            enemy.game_board.board[layer-1, y-1, x-1] = -1
            #Print enemy board with hidden layer
            enemy.game_board.print_board(hide = True)
            print('Nothing there...')
    
    def _get_ship_map(self):
        #Create a list of ship location map to compare if attack location contains a certain ship
        for ship in self.ships:
            self.ship_map.update({ship.name: ship._location})
            

class User(Player):
    
    def __init__(self, name, password):
        super().__init__(name)
        self._password = self._encrypt_pw(password)
        self.is_logged_in = False
        
        
    def _encrypt_pw(self, password):
        '''Encrypt the password with the username and return the hexdigest.''' 
        hash_string = (self.name + password)
        hash_string = hash_string.encode('utf8')
        return hashlib.sha256(hash_string).hexdigest()
    
    def check_password(self, password):
        '''Return True if the password is valid for this user, false otherwise'''
        encrypted = self._encrypt_pw(password)
        return encrypted == self._password
    

class Computer(Player):
    '''Computer class that generates auto attack'''
    
    def __init__(self):
        super().__init__(name = 'Computer')
    
    def auto_attack(self, enemy):
        '''Algorithm to generate random coordinates with in range to attack'''
        layer = randint(0,1)
        x = randint(1, self.game_board.x_size)
        y = randint(1, self.game_board.y_size)
        #Call attack_enemy method using generated coordinates
        self.attack_enemy(enemy,[layer,x,y])
    
    def load_ship_auto(self):
        '''Method in Computer to automatically load ships at random orientation'''
        #Orientation map for randomly choosing orientation to be put in
        orientation_map = {0: 'horizontal',
                        1: 'vertical'}
        #For loop to iterate through self.ships to be loaded in at random orientation
        for ship in self.ships:
            while True:
                try:
                    self.game_board.load_ship(ship, randint(1, self.game_board.x_size), 
                                              randint(1, self.game_board.y_size),
                                              orientation_map[randint(0,1)], user_type = self.name)
                    break
                except Exception:
                    continue
        #Update ship map via _get_ship_map method to create dictionary of ships and their location
        self._get_ship_map()
        #Commented out line is hack to show enemy map
        #self.game_board.print_board(hide = False)
        print('Enemy vessels have been deployed')
        print('For demo purpose, showing enemy map')
        self.game_board.print_board(hide = False)
        input('Press Enter')
        
    
        
        
        
        
#yueda = User('yueda', 'password')
#comp = Computer()
#s1 = SubmerseShip(length = 3, name = 'submarine')
#s2 = SurfaceShip(length = 4, name = 'destroyer')
#yueda.ships.append(s1)
#yueda.game_board.load_ship(s1, 1,1, 'vertical')
#comp.ships.append(s2)
#comp.game_board.load_ship(s2, 1,1, 'horizontal')

'''Things to do. 
-Find a place to call _add_ship_map when all ships are loaded.
- Find a place to update ship.grids_left using
for k, v in comp.ship_map.items():
    if (1,0,1) in v:
        print(k)'''
