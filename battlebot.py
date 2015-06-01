#!/usr/bin/python

import curses
import sys
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
import prestonbot
import dadbot
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

    def __str__(self):
        return "%s: position = %s, direction = %u, type = %s" % (self.name, self.position, self.direction, GameObject.TypeToString(self.type))

class Bot(object):
    def __init__(self, character):
        self.character = character

    def get_character(self):
        return self.character

    def move(self, player, game):
        (distance, what) = game.peek (player, player.direction)
        if debug:
            game.window.addstr(1, 1, "%s, game (width = %u, height = %u), peek -> distance = %u, what = %s" % (str(player), game.width, game.height, distance, what))
        if what == "|" and distance == 0:
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
    
    def move(self, game):
        self.direction = self.bot.move(self, game)
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
            return False
        else:
            return True
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
                if prize.position == player.position:
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
        if prize_distance < distance_to_wall:
            if debug:
                self.window.addstr(2, 1, "%s" % (str(nearest_prize)))
            
            if prize_distance > self.visibility:
                return (self.visibility, " ")
            else:
                return (prize_distance, nearest_prize.get_character())
        else:
            if distance_to_wall > self.visibility:
                return (self.visibility, " ")
            else:
                return (distance_to_wall, "|")

    def update(self):
        remove_prizes = list()
        for player in self.players:
            player.move(self)
            for prize in self.prizes:
                if player.position.x == prize.position.x and player.position.y == prize.position.y:
                    player.score += prize.points
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

def main(s):    

    (height, width) = s.getmaxyx()
    window = curses.newwin(height, width);
    
    window.timeout(50)

    game = Game(window, 50)
    game.add_player(dadbot.Bot('@'))
    game.add_player(prestonbot.Bot2('~'))
    window.keypad(1)
    
    key = 0

    while key != 27:                                                   # While Esc key is not pressed
        window.erase()
        game.update()
        if game.finished():
            break
        window.move(0,0) # set the cursor to 0,0 since we can't hide the cursor...
        curses.doupdate()
        prevKey = key                                                  # Previous key pressed
        event = window.getch()
        key = key if event == -1 else event 

    
        if key == ord(' '):                                            # If SPACE BAR is pressed, wait for another
            key = -1                                                   # one (Pause/Resume)
            while key != ord(' '):
                key = window.getch()
            key = prevKey
            continue    
    
        # if key == KEY_UP:
        #     for player in game.players:
        #         player.direction = UP
        # elif key == KEY_DOWN:
        #     for player in game.players:
        #         player.direction = DOWN
        # elif key == KEY_LEFT:
        #     for player in game.players:
        #         player.direction = LEFT
        # elif key == KEY_RIGHT:
        #     for player in game.players:
        #         player.direction = RIGHT
        
if __name__ == '__main__':
    curses.wrapper(main)
        