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
class Bot2(BaseBot):
    def __init__(self, character):
        BaseBot.__init__(self, character)
        self.first = True

    def move(self, player, game):
        if self.first:
            # Initialize stuff on our first move
            self.first = False
            self.push_move_target (Point(0,game.visibility-1), RIGHT)

        (distance_up, what_up) = game.peek (player, UP)
        (distance_down, what_down) = game.peek (player, DOWN)
        if what_up == "$":
            move_targets = self.get_move_targets()
            prize_position = player.position.copy()
            prize_position.y -= distance_up
            if len(move_targets) == 0 or move_targets[-1].position != prize_position: 
                self.push_move_target (player.position, player.direction)                
                self.push_move_target (prize_position, DOWN)                
                return UP
        if what_down == "$":
            move_targets = self.get_move_targets()
            prize_position = player.position.copy()
            prize_position.y += distance_down
            if len(move_targets) == 0 or move_targets[-1].position != prize_position: 
                self.push_move_target (player.position, player.direction)                
                self.push_move_target (prize_position, UP)                
                return DOWN
        target_direction = self.move_using_targets(player, game)
        if target_direction != NONE:
            return target_direction
        else:
            (distance, what) = game.peek (player, player.direction)
            if what == "|" and distance == 0:
                move_destination = player.position.copy()
                move_destination.y += game.visibility * 2
                if player.direction == RIGHT:
                    self.push_move_target (move_destination, LEFT)
                    return DOWN
                if player.direction == LEFT:
                    self.push_move_target (move_destination, RIGHT)
                    return DOWN
        return player.direction