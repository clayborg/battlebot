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

class Prize(object):
    def __init__(self, x, y, character, points):
        self.x = x
        self.y = y
        self.character = character
        self.points = points
        
    def __str__(self):
        return 'Prize: %c (%3u, %3u)' % (self.get_character(), self.x, self.y)
    
    def get_character(self):
        return self.character

class Player(object):
    def __init__(self, bot, x, y, direction):
        self.bot = bot
        self.x = x
        self.y = y
        self.direction = direction
        self.score = 0
    
    def __str__(self):
        return 'Player: %c (%3u, %3u) direction = %u' % (self.get_character(), self.x, self.y, self.direction)
        
    def get_character(self):
        return self.bot.get_character()
    
    def move(self, game):
        self.direction = self.bot.move(self, game)
        if self.direction == UP:
            if self.y > 0:
                self.y -= 1
        elif self.direction == DOWN:
            if self.y + 1 < game.height:
                self.y += 1
        elif self.direction == LEFT:
            if self.x > 0:
                self.x -= 1
        elif self.direction == RIGHT:
            if self.x + 1 < game.width:
                self.x += 1
        
class Game(object):
    def __init__(self, window, num_prizes):
        self.window = window
        self.visibility = 7 # players can see this many blocks in any direction
        (self.height, self.width) = self.window.getmaxyx()
        self.players = list()
        self.prizes = list()
        for i in range(num_prizes):
            self.prizes.append(Prize(randint(1,self.width-1), randint(1,self.height-1), "$", 5))
        # self.prizes.append(Prize(10, 10, "$", 5))
        # self.prizes.append(Prize(20, 20, "$", 5))
        # self.prizes.append(Prize(30, 30, "$", 5))
        # self.prizes.append(Prize(40, 40, "$", 5))

    
    def add_player(self, bot):
        self.players.append(Player(bot, randint(1,self.width-1), randint(1,self.height-1), self.get_random_direction()))

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
                if prize.x == player.x and prize.y < player.y:
                    distance = player.y - prize.y
                    if distance < prize_distance:
                        nearest_prize = prize
                        prize_distance = distance
            distance_to_wall = player.y
        elif direction == DOWN:
            for prize in self.prizes:
                if prize.x == player.x and prize.y > player.y:
                    distance =  prize.y - player.y
                    if distance < prize_distance:
                        nearest_prize = prize
                        prize_distance = distance
            distance_to_wall = self.height - player.y - 1
        elif direction == LEFT:
            for prize in self.prizes:
                if prize.y == player.y and prize.x < player.x:
                    distance = player.x - prize.x
                    if distance < prize_distance:
                        nearest_prize = prize
                        prize_distance = distance
            distance_to_wall = player.x
        elif direction == RIGHT:
            for prize in self.prizes:
                if prize.y == player.y and prize.x > player.x:
                    distance = prize.x - player.x
                    if distance < prize_distance:
                        nearest_prize = prize
                        prize_distance = distance
            distance_to_wall = self.width - player.x - 1
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
                if player.x == prize.x and player.y == prize.y:
                    player.score += prize.points
                    remove_prizes.append(prize)
        for remove_prize in remove_prizes:
            self.prizes.remove(remove_prize)
        # Paint the players
        for (idx, player) in enumerate(self.players):
            player_char = player.get_character()
            self.window.addstr(idx, 1, "%s score: %u" % (player_char, player.score))
            try:
                self.window.addch(player.y, player.x, player_char)
            except:
                pass # exception will be thrown if you try to addch at y = height -1 and x = width - 1...
                
        for prize in self.prizes:
            self.window.addch(prize.y, prize.x, prize.get_character())

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
        window.move(0,0)
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