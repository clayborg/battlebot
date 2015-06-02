#!/usr/bin/python

import curses
import sys
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
debug = 0
# Define numbers for the directions
UP      = 0
DOWN    = 1
LEFT    = 2
RIGHT   = 3
NONE    = 4

MOVE    = 0 # A target to move to
WALL    = 1
PLAYER  = 2
PRIZE   = 3
ENEMY   = 4

class Point(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def is_zero(self):
        return self.x == 0 and self.y == 0

    def copy(self):
        return Point(self.x, self.y)

    def __str__(self):
        return "(%u, %u)" % (self.x, self.y)

    def __repr__(self):
        return "%s%s" % (self.__class__.__name__, str(self))

    def __eq__(self, rhs):
        return self.x == rhs.x and self.y == rhs.y

    def __ne__(self, rhs):
        return self.x != rhs.x or self.y != rhs.y

    def __add__(self, rhs):
        return Point(self.x + rhs.x, self.y + rhs.y)

    def __sub__(self, rhs):
        return Point(self.x - rhs.x, self.y - rhs.y)

class GameObject(object):

    @classmethod
    def TypeToString(cls, type):
        if type == MOVE:
            return 'move-target'
        if type == WALL:
            return 'wall'
        if type == PLAYER:
            return 'player'
        if type == PRIZE:
            return 'prize'
        if type == ENEMY:
            return 'enemy'

    def __init__(self, name, position, direction, type):
        self.position = position
        self.direction = direction
        self.visible = True
        self.name = name
        self.type = type

    def __repr__(self):
        return "%s%s" % (self.__class__.__name__, str(self))

    def __str__(self):
        return "%s: position = %s, direction = %u, type = %s" % (self.name, self.position, self.direction, GameObject.TypeToString(self.type))

    def is_wall(self):
        return self.type == WALL

    def is_player(self):
        return self.type == PLAYER

    def is_prize(self):
        return self.type == PRIZE
    
    def is_enemy(self):
        return self.type == ENEMY
        
        
    def distance_to_game_object_in_direction(self, game_object, direction):
        if direction == UP:
            return self.position.y - game_object.position.y
        elif direction == DOWN:
            return game_object.position.y - self.position.y
        elif direction == LEFT:
            return self.position.x - game_object.position.x
        elif direction == RIGHT:
            return game_object.position.x - self.position.x
        else:
            raise ValueError
            return 0

    def will_hit_wall(self, game_object):
        if game_object and game_object.is_wall() and self.distance_to_game_object_in_direction(game_object, self.direction) == 1:
            return True
        else:
            return False

class BaseBot(object):
    def __init__(self, character):
        self.character = character
        self.targets = list()

    def push_move_target(self, pt, direction):
        self.targets.append(GameObject("move", pt.copy(), direction, MOVE))

    def has_move_target(self, pt):
        for target in self.targets:
            if target.position == pt:
                return True
        return False

    def get_character(self):
        return self.character

    def get_move_targets(self):
        return self.targets

    def move_using_targets(self, player, game):
        '''Move using the "self.targets" if we have any. Returns NONE
           as the direction if the move wasn't handled. Returns a valid
           direction if the move was handled.'''
        if self.targets:
            move_target = self.targets[-1]
            #we are trying to go to a point in space
            if player.position == move_target.position:
                direction = move_target.direction
                self.targets.pop()
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
        return NONE

    def move(self, player, game):
        target_direction = self.move_using_targets(player, game)
        if target_direction != NONE:
            return target_direction
        game_object = game.peek (player, player.direction)
        if debug:
            game.window.addstr(1, 1, "%s, game (width = %u, height = %u), peek -> distance = %u, what = %s" % (str(player), game.width, game.height, distance, what))
        if player.will_hit_wall(game_object):
            return game.get_random_direction_that_isnt(player.direction)
        else:
            return player.direction

class Prize(GameObject):
    def __init__(self, name, position, direction, points):
        GameObject.__init__(self, name, position, direction, PRIZE)
        self.points = points

    def get_character(self):
        return self.name

class Player(GameObject):
    def __init__(self, bot, position, direction):
        GameObject.__init__(self, bot.get_character(), position, direction, PLAYER)
        self.bot = bot
        self.score = 0

    def get_character(self):
        return self.bot.get_character()

    def move(self, game, force_direction):
        if force_direction == NONE:
            self.direction = self.bot.move(self, game)
        else:
            self.direction = force_direction
        if self.direction == UP:
            if self.position.y > 0:
                self.position.y -= 1
        elif self.direction == DOWN:
            if self.position.y + 1 < game.height:
                self.position.y += 1
        elif self.direction == LEFT:
            if self.position.x > 0:
                self.position.x -= 1
        elif self.direction == RIGHT:
            if self.position.x + 1 < game.width:
                self.position.x += 1

class Game(object):
    def __init__(self, window, num_prizes):
        self.window = window
        self.visibility = 7 # players can see this many blocks in any direction
        (self.height, self.width) = self.window.getmaxyx()
        self.players = list()
        self.prizes = list()
        for i in range(num_prizes):
            self.prizes.append(Prize("$", self.create_random_point(), NONE, 5))

    def finished(self):
        if self.prizes:
            return None
        else:
            winner = None
            for player in self.players:
                if winner is None or winner.score < player.score:
                    winner = player
            return winner

    def create_random_point(self):
        return Point(randint(0,self.width-1), randint(0,self.height-1))

    def add_player(self, bot):
        self.players.append(Player(bot, self.create_random_point(), self.get_random_direction()))

    def get_random_direction_that_isnt(self, direction):
        while 1:
            new_direction = self.get_random_direction()
            if new_direction != direction:
                return new_direction

    def get_random_direction(self):
        return randint(0,3)

    def peek(self, player, direction):
        space = ord(' ')
        prize_distance = sys.maxint
        nearest_prize = None
        if direction == UP:
            for prize in self.prizes:
                if prize.position.x == player.position.x and prize.position.y < player.position.y:
                    distance = player.position.y - prize.position.y
                    if distance < prize_distance:
                        nearest_prize = prize
                        prize_distance = distance
            distance_to_wall = player.position.y
        elif direction == DOWN:
            for prize in self.prizes:
                if prize.position.x == player.position.x and prize.position.y > player.position.y:
                    distance =  prize.position.y - player.position.y
                    if distance < prize_distance:
                        nearest_prize = prize
                        prize_distance = distance
            distance_to_wall = self.height - player.position.y - 1
        elif direction == LEFT:
            for prize in self.prizes:
                if prize.position.y == player.position.y and prize.position.x < player.position.x:
                    distance = player.position.x - prize.position.x
                    if distance < prize_distance:
                        nearest_prize = prize
                        prize_distance = distance
            distance_to_wall = player.position.x
        elif direction == RIGHT:
            for prize in self.prizes:
                if prize.position.y == player.position.y and prize.position.x > player.position.x:
                    distance = prize.position.x - player.position.x
                    if distance < prize_distance:
                        nearest_prize = prize
                        prize_distance = distance
            distance_to_wall = self.width - player.position.x - 1
        else:
            raise ValueError
        if prize_distance <= distance_to_wall:
            if prize_distance <= self.visibility:
                return nearest_prize
        if distance_to_wall < self.visibility:
            wall_pt = player.position.copy()
            if direction == UP:
                wall_pt.y -= (distance_to_wall+1)
            elif direction == DOWN:
                wall_pt.y += (distance_to_wall+1)
            elif direction == LEFT:
                wall_pt.x -= (distance_to_wall+1)
            elif direction == RIGHT:
                wall_pt.x += (distance_to_wall+1)
            return GameObject("wall", wall_pt, NONE, WALL)
        return None

    def update(self, info, force_direction):
        remove_prizes = list()
        for player in self.players:
            player.move(self, force_direction)
            for prize in self.prizes:
                if player.position.x == prize.position.x and player.position.y == prize.position.y:
                    player.score += prize.points
                    if not prize in remove_prizes:
                        remove_prizes.append(prize)
        for remove_prize in remove_prizes:
            self.prizes.remove(remove_prize)
        # Paint the players
        for (idx, player) in enumerate(self.players):
            player_char = player.get_character()
            self.window.addstr(idx, 1, "%s score: %u" % (player_char, player.score))
            try:
                self.window.addch(player.position.y, player.position.x, player_char)
            except:
                pass # exception will be thrown if you try to addch at y = height -1 and x = width - 1...

        for prize in self.prizes:
            self.window.addch(prize.position.y, prize.position.x, prize.get_character())
        if info:
            y = 3
            for player in self.players:
                self.window.addstr(y, 1, str(player))
                y+=1
                game_object = self.peek (player, UP)
                if game_object:
                    distance = player.distance_to_game_object_in_direction(game_object, UP)
                    self.window.addstr(y, 1, "   up: distance = %u, %s" % (distance, str(game_object)))
                else:
                    self.window.addstr(y, 1, "   up: <none>")
                y+=1
                game_object = self.peek (player, DOWN)
                if game_object:
                    distance = player.distance_to_game_object_in_direction(game_object, DOWN)
                    self.window.addstr(y, 1, " down: distance = %u, %s" % (distance, str(game_object)))
                else:
                    self.window.addstr(y, 1, " down: <none>")
                y+=1
                game_object = self.peek (player, LEFT)
                if game_object:
                    distance = player.distance_to_game_object_in_direction(game_object, LEFT)
                    self.window.addstr(y, 1, " left: distance = %u, %s" % (distance, str(game_object)))
                else:
                    self.window.addstr(y, 1, " left: <none>")
                y+=1
                game_object = self.peek (player, RIGHT)
                if game_object:
                    distance = player.distance_to_game_object_in_direction(game_object, RIGHT)
                    self.window.addstr(y, 1, "right: distance = %u, %s" % (distance, str(game_object)))
                else:
                    self.window.addstr(y, 1, "right: <none>")
                y+=1





def main(s):

    (height, width) = s.getmaxyx()
    window = curses.newwin(height, width);

    timeout = 15
    window.timeout(timeout)

    game = Game(window, 51)
    game.add_player(dadbot.Bot('@'))
    game.add_player(prestonbot.Bot2('#'))
    window.keypad(1)

    key = 0
    info = False
    pause = False
    advance_frame = True
    force_direction = NONE
    while key != 27:                                                   # While Esc key is not pressed
        if advance_frame:
            window.erase()
            game.update(info, force_direction)
            force_direction = NONE
            window.move(0,0) # set the cursor to 0,0 since we can't hide the cursor...
            winner = game.finished()
            if winner:
                window.addstr(3,1, "Player %s wins!!!" % (winner.get_character()))
                curses.doupdate()
                window.timeout(2000)
                window.getch() # Delay for 2 seconds
                break
            curses.doupdate()
        else:
            advance_frame = True

        prevKey = key                                                  # Previous key pressed
        event = window.getch()
        key = key if event == -1 else event
        if key == ord('q'):
            break
        elif key == ord('i'):
            advance_frame = False
            info = not info
        elif key == ord(' '):
            if pause:
                pause = False
            else:
                pause = True
            if pause:
                advance_frame = False
                window.timeout(timeout) # Run again
            else:
                advance_frame = True
                window.timeout(-1) # wait for each key to advance a frame
        elif key == KEY_UP:
            force_direction = UP
        elif key == KEY_DOWN:
            force_direction = DOWN
        elif key == KEY_LEFT:
            force_direction = LEFT
        elif key == KEY_RIGHT:
            force_direction = RIGHT

if __name__ == '__main__':
    import prestonbot
    import dadbot
    curses.wrapper(main)
