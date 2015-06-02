import battlebot


class Bot(battlebot.BaseBot):
    def __init__(self, character):
        battlebot.BaseBot.__init__(self, character)
        self.change_direction_count = 10
        self.count = 0
        self.first = True

    def move(self, player, game):
        if self.first:
            # Initialize stuff on our first move
            left = False
            for y in range(game.height-game.visibility, 0, -game.visibility*2):
                if left:
                    left = False
                    self.push_move_target (battlebot.Point(game.width-1,y), battlebot.LEFT)
                    self.push_move_target (battlebot.Point(0,y), battlebot.UP)
                else:
                    left = True
                    self.push_move_target (battlebot.Point(0,y), battlebot.RIGHT)
                    self.push_move_target (battlebot.Point(game.width-1,y), battlebot.UP)
            self.targets = list(reversed(self.targets))
            self.first = False
            
        pushed_return = False
        for direction in [battlebot.UP, battlebot.DOWN, battlebot.LEFT, battlebot.RIGHT]:
            game_object = game.peek (player, direction)
            if game_object and game_object.is_prize():
                if self.has_move_target(game_object.position):
                    continue
                if pushed_return == False:
                    self.push_move_target (player.position, player.direction)
                    pushed_return = True
                self.push_move_target (game_object.position, direction)
        target_direction = self.move_using_targets(player, game)
        if target_direction != battlebot.NONE:
            return target_direction
        game_object = game.peek (player, player.direction)
        if player.will_hit_wall(game_object):
            if player.position.x == 0:
                return battlebot.RIGHT
            return game.get_random_direction_that_isnt(player.direction)
        else:
            return player.direction
        
        # if player.will_hit_wall(game_object):
        #     move_destination = player.position.copy()
        #     move_destination.y += game.visibility * 2
        #     if player.direction == battlebot.RIGHT:
        #         self.push_move_target (move_destination, battlebot.LEFT)
        #         return battlebot.UP
        #     if player.direction == battlebot.LEFT:
        #         self.push_move_target (move_destination, battlebot.RIGHT)
        #         return battlebot.UP
        # return player.direction
