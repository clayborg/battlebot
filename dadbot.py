import battlebot

class Bot(object):
    def __init__(self, character):
        self.character = character
        self.change_direction_count = 10
        self.count = 0

    def get_character(self):
        return self.character

    def move(self, player, game):
        game_object_up    = game.peek (player, battlebot.UP)
        game_object_down  = game.peek (player, battlebot.DOWN)
        game_object_left  = game.peek (player, battlebot.LEFT)
        game_object_right = game.peek (player, battlebot.RIGHT)
        game_object       = None
        if game_object_up:
            game_object = game_object_up
            if game_object_up.type == battlebot.PRIZE:
                return battlebot.UP
        if game_object_down:
            game_object = game_object_down
            if game_object_down.type == battlebot.PRIZE:
                return battlebot.DOWN
        if game_object_right:
            game_object = game_object_right
            if game_object_right.type == battlebot.PRIZE:
                return  battlebot.RIGHT
        if game_object_left:
            game_object = game_object_left
            if game_object_left.type == battlebot.PRIZE:
                return battlebot.LEFT

        if player.will_hit_wall(game_object):
            self.count = 0;
            return game.get_random_direction_that_isnt(player.direction)
        else:
            self.count += 1
            if self.count >= self.change_direction_count:
                self.count = 0;
                return game.get_random_direction_that_isnt(player.direction)
            else:
                return player.direction
