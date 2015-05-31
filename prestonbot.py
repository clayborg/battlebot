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
            if player.position.x == 0:
                return RIGHT
            return game.get_random_direction_that_isnt(player.direction)
        else:
            return player.direction 
class Bot2(object):
    def __init__(self, character):
        self.character = character
        self.move_target = GameObject("Move", Point(0,0), RIGHT, MOVE)
        
    def get_character(self):
        return self.character

    def move(self, player, game):
        if self.move_target:
            #we are trying to go to a point in space
            if player.position == self.move_target.position:
                direction = self.move_target.direction
                self.move_target = None
                return direction
            vector = player.position - self.move_target.position
            if vector.x > 0:
                return LEFT
            if vector.x < 0:
                return RIGHT
            if vector.y > 0:
                return UP
            if vector.y < 0:
                return DOWN
        else:
            (distance, what) = game.peek (player, player.direction)
            if what == "|" and distance == 0:
                if player.direction == RIGHT:
                    self.move_target = GameObject("move", player.position.copy(), LEFT, MOVE)
                    self.move_target.position.y += 1
                    return DOWN
                if player.direction == LEFT:
                    self.move_target = GameObject("move", player.position.copy(), RIGHT, MOVE)
                    self.move_target.position.y += 1
                    return DOWN
        return player.direction