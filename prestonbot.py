import battlebot

class Bot(object):
    def __init__(self, character):
        self.character = character

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
            if game_object_up.is_prize():
                return battlebot.UP
        if game_object_down:
            game_object = game_object_down
            if game_object_down.is_prize():
                return battlebot.DOWN
        if game_object_right:
            game_object = game_object_right
            if game_object_right.is_prize():
                return battlebot.RIGHT
        if game_object_left:
            game_object = game_object_left
            if game_object_left.is_prize():
                return battlebot.LEFT
        if player.will_hit_wall(game_object):
            if player.position.x == 0:
                return battlebot.RIGHT
            return game.get_random_direction_that_isnt(player.direction)
        else:
            return player.direction
class Bot2(battlebot.BaseBot):
    def __init__(self, character):
        battlebot.BaseBot.__init__(self, character)
        self.first = True

    def move(self, player, game):
        if self.first:
            # Initialize stuff on our first move
            self.first = False
            self.push_move_target (battlebot.Point(0,game.visibility-1), battlebot.RIGHT)

        game_object_up = game.peek (player, battlebot.UP)
        if game_object_up and game_object_up.is_prize():
            move_targets = self.get_move_targets()
            if len(move_targets) == 0 or move_targets[-1].position != game_object_up.position:
                self.push_move_target (player.position, player.direction)
                self.push_move_target (game_object_up.position, battlebot.DOWN)
                return battlebot.UP
        game_object_down  = game.peek (player, battlebot.DOWN)
        if game_object_down and game_object_down.is_prize():
            move_targets = self.get_move_targets()
            if len(move_targets) == 0 or move_targets[-1].position != game_object_down.position:
                self.push_move_target (player.position, player.direction)
                self.push_move_target (game_object_down.position, battlebot.UP)
                return battlebot.DOWN
        target_direction = self.move_using_targets(player, game)
        if target_direction != battlebot.NONE:
            return target_direction
        else:
            game_object = game.peek (player, player.direction)
            if player.will_hit_wall(game_object):
                move_destination = player.position.copy()
                move_destination.y += game.visibility * 2
                if player.direction == battlebot.RIGHT:
                    self.push_move_target (move_destination, battlebot.LEFT)
                    return battlebot.DOWN
                if player.direction == battlebot.LEFT:
                    self.push_move_target (move_destination, battlebot.RIGHT)
                    return battlebot.DOWN
        return player.direction