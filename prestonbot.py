from battlebot import *

class Bot(object):
    def __init__(self, character):
        self.character = character

    def get_character(self):
        return self.character

    def move(self, player, game):
        (distance, what) = game.peek (player, player.direction)
        (distance_up, what_up) = game.peek (player, UP)
        (distance_down, what_down) = game.peek (player, DOWN)
        (distance_left, what_left) = game.peek (player, LEFT)
        (distance_right, what_right) = game.peek (player, RIGHT)
        if what_up == "$":
            return UP
        if what_down == "$":
            return DOWN
        if what_right == "$":
            return  RIGHT
        if what_left == "$":
            return LEFT
        if what == "|" and distance == 0:
            if player.x == 0:
                return RIGHT
            return game.get_random_direction_that_isnt(player.direction)
        else:
            return player.direction 
class Bot2(object):
    def __init__(self, character):
        self.character = character
        self.move_x = 0
        self.move_y = 0
        self.move_direction = RIGHT
        
    def get_character(self):
        return self.character

    def move(self, player, game):
        if self.move_x == -1:
            (distance, what) = game.peek (player, player.direction)
            if what == "|" and distance == 0:
                if player.direction == RIGHT:
                    self.move_x = player.x
                    self.move_y = player.y + 1
                    self.move_direction = LEFT
                    return DOWN
                if player.direction == LEFT:
                    self.move_x = player.x
                    self.move_y = player.y + 1
                    self.move_direction = RIGHT
                    return DOWN
                
        else:
            #we are trying to go to a point in space
            if player.x == self.move_x and player.y == self.move_y:
                self.move_x = -1
                return self.move_direction
            if player.x > self.move_x:
                return LEFT
            if player.x < self.move_x:
                return RIGHT
            if player.y > self.move_y:
                return UP
            if player.y < self.move_y:
                return DOWN
                
        
        return player.direction