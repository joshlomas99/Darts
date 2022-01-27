import pygame
from pygame.locals import QUIT
from pygameGUIs import updateScoreDemolition, drawDemolition

class InvalidScore(Exception):
    pass

def Score(scoreIn):
    if scoreIn[-1] == 'D':
        value, multiplier = int(scoreIn[:-1]), 2
    elif scoreIn[-1] == 'T':
        value, multiplier = int(scoreIn[:-1]), 3
    elif scoreIn[-1].isalpha():
        print(f'Invalid score: {scoreIn}')
        return False
    else:
        value, multiplier = int(scoreIn), 1
    if value >= 0 and value <= 20:
        return value*multiplier
    else:
        print(f'Invalid score: {value}')
        return False

class Demolition:
    def __init__(self, window, players, target=180):
        self.players = players
        self.scores = [target]*len(players)
        # os.environ['SDL_VIDEO_WINDOW_POS'] = "768,216"
        self.window = window

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
            x, y = pygame.mouse.get_pos()
            pygame.display.set_caption('{}, {}'.format(x, y))
            pygame.time.Clock().tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
            gameOver = self.turn(self.players[player])
            player += 1
            player %= 6

        print(f'{self.players[player - 1]} wins!')
        return

class Killer:
    pass

class RoundtheWorld:
    pass

class Shanghai:
    pass

class SnakesandLadders:
    pass

class DonkeyDerby:
    pass

class QuackShot:
    pass
