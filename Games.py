from random import shuffle, randint
import pygame
from pygame.locals import QUIT
from pygameGUIs import updateScoreDemolition, drawDemolition

class InvalidScore(Exception):
    pass

def Score(scoreIn, useMultiplier=True):
    if scoreIn == '':
        return False
    elif scoreIn[-1] == 'D':
        if any(char.isalpha() for char in scoreIn[:-1]):
            print(f'Invalid score: {scoreIn[:-1]}')
            return False
        value, multiplier = int(scoreIn[:-1]), 2
    elif scoreIn[-1] == 'T':
        if any(char.isalpha() for char in scoreIn[:-1]):
            print(f'Invalid score: {scoreIn[:-1]}')
            return False
        value, multiplier = int(scoreIn[:-1]), 3
    elif any(char.isalpha() for char in scoreIn):
        print(f'Invalid score: {scoreIn}')
        return False
    else:
        value, multiplier = int(scoreIn), 1
    if value >= 0 and value <= 20:
        if useMultiplier:
            return value*multiplier
        else:
            return value
    else:
        print(f'Invalid score: {value}')
        return False

class Demolition:
    def __init__(self, window, players, fpsClock, FPS, target=180):
        self.window = window
        self.players = players
        self.scores = [target]*len(players)
        self.fpsClock = fpsClock
        self.FPS = FPS
        # os.environ['SDL_VIDEO_WINDOW_POS'] = "768,216"

    def shot(self, player, turnNum):
        score = False
        while type(score) != int:
            scoreIn = input(f'Turn {turnNum+1}: ')
            score = Score(scoreIn)
        if self.scores[self.players.index(player)] - score == 0:
            updateScoreDemolition(self.window, player, turnNum, self.scores[self.players.index(player)]-score, self.players, self.scores)
            return 'GameOver'
        elif self.scores[self.players.index(player)] - score < 0:
            print(f'{player} has gone bust!')
            return 'Bust'
        else:
            updateScoreDemolition(self.window, player, turnNum, self.scores[self.players.index(player)]-score, self.players, self.scores)
            return 'Continue'

    def turn(self, player):
        print(f'\n{player}\'s turn:')
        for i in range(3):
            drawDemolition(self.window, player, i, self.players, self.scores)
            status = self.shot(player, i)
            if status == 'GameOver':
                return True
            elif status == 'Bust':
                break
        return False

    def play(self):
        player = 0
        gameOver = False
        while not gameOver:
            self.fpsClock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
            gameOver = self.turn(self.players[player])
            player += 1
            player %= len(self.players)

        print(f'{self.players[player - 1]} wins!')
        return

class Killer:
    def __init__(self, window, players, fpsClock, FPS, max_round=12):
        self.window = window
        self.players = players
        self.segments = [0]*len(players)
        self.positions = []
        all_positions = [[[16, 8, 11, 14, 9], [4, 13, 6, 10, 15]],
                         [[12, 9, 14], [8, 16, 7], [18, 4, 13], [10, 15, 2]],
                         [[5, 12, 9, 14], [8, 16, 7, 19], [1, 18, 4, 13], [10, 15, 2, 17]],
                         [[5, 20, 1], [11, 14, 9], [16, 7, 19], [17, 2, 15], [6, 13, 4]],
                         [[5, 20], [14, 9], [8, 16, 7], [3, 17], [15, 10, 6], [4, 18]]][len(players)-2]
        indices = list(range(len(players)))
        shuffle(indices)
        for i in indices:
            self.positions.append(all_positions[i][randint(0, len(all_positions[i])-1)])
        self.max_round = max_round

    def shot(self, player, turnNum, multiplier):
        score = False
        while type(score) != int:
            scoreIn = input(f'Turn {turnNum+1}: ')
            score = Score(scoreIn, False)
        if score == self.positions[self.players.index(player)]:
            if self.segments[self.players.index(player)] < 3:
                self.segments[self.players.index(player)] = min(self.segments[self.players.index(player)] + multiplier,
                                                                3)
        elif score in self.positions and self.segments[self.players.index(player)] == 3:
            if self.segments[self.positions.index(score)] == 0 or self.segments[self.positions.index(score)] <= multiplier:
                eliminated = self.players.pop(self.positions.index(score))
                self.segments.pop(self.positions.index(score))
                self.positions.pop(self.positions.index(score))
                return eliminated

            else:
                self.segments[self.positions.index(score)] -= multiplier

        return False

    def turn(self, player, multiplier):
        print(f'\n{player}\'s turn:')
        for i in range(3):
            # drawKiller(self.window, player, i, self.players, self.scores)
            eliminated = self.shot(player, i, multiplier)
            print(self.segments)
            if len(self.players) < 2:
                return True
        return False

    def play(self):
        player, Round, multiplier = 0, 1, 1
        gameOver = False
        while not gameOver and Round <= self.max_round:
            if player == 0:
                print('#############\nRound {0}     #\n#############'.format(Round))
            # pygame.time.Clock().tick(30)
            # for event in pygame.event.get():
            #     if event.type == QUIT:
            #         pygame.quit()
            #         return
            gameOver = self.turn(self.players[player], multiplier)
            player += 1
            if player >= len(self.players):
                player = 0
                Round += 1
                if Round == 7:
                    multiplier = 2
                elif Round == 10:
                    multiplier = 3

        if gameOver:
            print('\n{0} wins!'.format(self.players[0]))
        else:
            if self.segments.count(max(self.segments)) == 1:
                print('\n{0} wins!'.format(self.players[self.segments.index(max(self.segments))]))
            else:
                winners = []
                for n, seg in enumerate(self.segments):
                    if seg == max(self.segments):
                        winners.append(self.players[n])
                out = '\n'
                for winner in winners[:-1]:
                    out += winner + ', '
                print(out[:-2] + ' and ' + winners[-1] + ' win!')

class RoundtheWorld:
    pass

class SnakesandLadders:
    pass

class DonkeyDerby:
    pass

class QuackShot:
    pass

[9, 17, 7, 20, 18, 10]