import battlebot

class Bot(object):
    def __init__(self, character):
        self.character = character
        self.change_direction_count = 10
        self.count = 0

    def get_character(self):
        return self.character

    def move(self, player, game):
        (distance_up, what_up) = game.peek (player, battlebot.UP)
        (distance_down, what_down) = game.peek (player, battlebot.DOWN)
        (distance_left, what_left) = game.peek (player, battlebot.LEFT)
        (distance_right, what_right) = game.peek (player, battlebot.RIGHT)
        if what_up == "$":
            return battlebot.UP
        if what_down == "$":
            return battlebot.DOWN
        if what_right == "$":
            return  battlebot.RIGHT
        if what_left == "$":
            return battlebot.LEFT

        (distance, what) = game.peek (player, player.direction)
        if what == "|" and distance == 0:
            self.count = 0;
            return game.get_random_direction_that_isnt(player.direction)
        else:
            self.count += 1
            if self.count >= self.change_direction_count:
                self.count = 0;
                return game.get_random_direction_that_isnt(player.direction)
            else:
                return player.direction
