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
        self.first = True
    def get_character(self):
        return self.character

    def move(self, player, game):
        if self.first:
            # Initialize stuff on our first move
            self.first = False
            self.move_targets = list()
            target = GameObject("Move", Point(0,game.visibility-1), RIGHT, MOVE)
            self.move_targets.append(target)

        (distance_up, what_up) = game.peek (player, UP)
        (distance_down, what_down) = game.peek (player, DOWN)
        if what_up == "$":
            prize_position = player.position.copy()
            prize_position.y -= distance_up
            if len( self.move_targets) == 0 or self.move_targets[-1].position != prize_position: 
                self.move_targets.append(GameObject("return", player.position.copy(), player.direction, MOVE))
                move_target = GameObject("return", prize_position, DOWN, MOVE)
                self.move_targets.append(move_target)
                return UP
        if what_down == "$":
            prize_position = player.position.copy()
            prize_position.y += distance_down
            if len( self.move_targets) == 0 or self.move_targets[-1].position != prize_position: 
                self.move_targets.append(GameObject("return", player.position.copy(), player.direction, MOVE))
                move_target = GameObject("return", prize_position, UP, MOVE)
                self.move_targets.append(move_target)
                return DOWN
        if self.move_targets:
            move_target = self.move_targets[-1]
            #we are trying to go to a point in space
            if player.position == move_target.position:
                direction = move_target.direction
                self.move_targets.pop()
                return move_target.direction
            vector = player.position - move_target.position
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
                    move_target = GameObject("move", player.position.copy(), LEFT, MOVE)
                    move_target.position.y += game.visibility * 2
                    self.move_targets.append(move_target)
                    return DOWN
                if player.direction == LEFT:
                    move_target = GameObject("move", player.position.copy(), RIGHT, MOVE)
                    move_target.position.y += game.visibility * 2
                    self.move_targets.append(move_target)
                    return DOWN
        return player.direction