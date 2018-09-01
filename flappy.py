'''
    Make the Game and let the Bot play it.
'''

from itertools import cycle
from bot import Bot

import random
import sys

import pygame
from pygame.locals import *

    #Initialize the bot
bot = Bot()

    #Game parameters
FPS = 60
SCREENWIDTH  = 288
SCREENHEIGHT = 512

    #Amount by which base can max shift from R to L
PIPEGAPSIZE = 100 # Gap between upper and lower part of a pipe
BASEY = SCREENHEIGHT*0.79

    #Image, sounds, hitmasks dictionaries
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

    #List of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = (
    #Red Bird
    (
        'assets/sprites/redbird-upflap.png',
        'assets/sprites/redbird-midflap.png',
        'assets/sprites/redbird-downflap.png',
    ),
    #Blue Bird
    (
        'assets/sprites/bluebird-upflap.png',
        'assets/sprites/bluebird-midflap.png',
        'assets/sprites/bluebird-downflap.png',
    ),
    #Yellow Bird
    (
        'assets/sprites/yellowbird-upflap.png',
        'assets/sprites/yellowbird-midflap.png',
        'assets/sprites/yellowbird-downflap.png',
    ), 
)

    #List of possible backgrounds
BACKGROUNDS_LIST = (
    'assets/sprites/backgrounds-day.png',
    'assets/sprites/backgrounds-night.png',
)

    #List of types of pipes
PIPES_LIST = (
    'assets/sprites/pipe-green.png',
    'assets/sprites/pipe-red.png',
)

    # Begin the game!

def main():
    global SCREEN, FPSCLOCK, bot
    #pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
    pygame.display.set_caption('Flappy Bird with Python AI v2.1')

        # Numbers sprites to display scores 
    IMAGES['numbers'] = (
        pygame.image.load('assets/sprites/0.png').convert_alpha(),
        pygame.image.load('assets/sprites/1.png').convert_alpha(),
        pygame.image.load('assets/sprites/2.png').convert_alpha(),
        pygame.image.load('assets/sprites/3.png').convert_alpha(),
        pygame.image.load('assets/sprites/4.png').convert_alpha(),
        pygame.image.load('assets/sprites/5.png').convert_alpha(),
        pygame.image.load('assets/sprites/6.png').convert_alpha(),
        pygame.image.load('assets/sprites/7.png').convert_alpha(),
        pygame.image.load('assets/sprites/8.png').convert_alpha(),
        pygame.image.load('assets/sprites/9.png').convert_alpha()
    )

        # 'Game Over' sprite
    IMAGES['gameover'] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
        # 'Welcome' message sprite 
    IMAGES['message'] = pygame.image.load('assets/sprites/message.png').convert_alpha()
        # base (ground) sprite
    IMAGES['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()

        # Configure sounds
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'
    
    SOUNDS['die']       =   pygame.mixer.Sound('assets/audio/die'+soundExt) 
    SOUNDS['hit']       =   pygame.mixer.Sound('assets/audio/hit'+soundExt)
    SOUNDS['point']     =   pygame.mixer.Sound('assets/audio/point'+soundExt)
    SOUNDS['swoosh']    =   pygame.mixer.Sound('assets/audio/swoosh'+soundExt)
    SOUNDS['wing']      =   pygame.mixer.Sound('assets/audio/wing'+soundExt)

    while True:
        #Select a random background sprite
        randBG = random.randint(0,len(BACKGROUNDS_LIST)-1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBG]).convert()

        #Now, select a random player sprite
        randPlayer = random.randing(0,len(PLAYERS_LIST) -1)
        IMAGES['player'] = (
            pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
        )
        
        #Select a random pipe sprite
        pipeIndex = random.randint(0,len(PIPES_LIST) -1)
        IMAGES['pipe'] = (
            pygame.transform.rotate(pygame.image.load(PIPES_LIST[pipeIndex]).convert_alpha(),180),
            pygame.image.load(PIPES_LIST[pipeIndex]).convert_alpha(),
        )

        # Hit mask for pipes and player

        HITMASKS['pipe'] = (
            getHitmask(IMAGES['pipe'][0]),
            getHitmask(IMAGES['pipe'][0]),
        )

        HITMASKS['player'] = (
            getHitmask(IMAGES['player'][0]),
            getHitmask(IMAGES['player'][1]),
            getHitmask(IMAGES['player'][2]),
        )

        movementInfo = ShowWelcomeAnimation()
        crashInfo = MainGame(movementInfo)
        ShowGameOverScreen(crashInfo)

def ShowWelcomeAnimation():

    '''
        Shows welcome screen animation to the game
    '''
        #Index of player to blip onscreen
    playerIndex = 0
    playerIndexGen = cycle([0,1,2,1])
        # Change the playerIndex every 5th iteration
    loopIter = 0

    playerx = int(SCREENWIDTH * 0.2)
    playery = int((SCREENHEIGHT-IMAGES['player'][0].get_height()) / 2) 

    messagey = int(SCREENHEIGHT * 0.12)
    messagex = int((SCREENWIDTH-IMAGES['message'].get_width()) / 2)

    basex = 0
        #Define amount of max shift
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

        #Player simple-harmonic osc values for up/down motion on welcome screen
    playerSHMVals = {'val':0, 'dir':1}

    while True:
        """
            >>>>>>>-------DEACTIVATED BECAUSE WE'RE USING A BOT-------<<<<<<<<<

        #Key press functionality
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                
                    #User started the game ! Play the first flap sound and return values for MainGame()!
                SOUNDS['wing'].play()
                return {
                    'playerY' : playery + playerSHMVals['val'],
                    'basex' : basex,
                    'playerIndexGen' : playerIndexGen,

                }
        """
        SOUNDS['wing'].play()    
        return {
                    'playery' : playery + playerSHMVals['val'],
                    'basex' : basex,
                    'playerIndexGen' : playerIndexGen,

        }

            #Adjust player's Y coordinate, index and base x-shift
        if (loopIter +1) % 5 == 0:
            playerIndex = next(playerIndexGen)
        loopIter = (loopIter+1) % 30
        basex = - ((-basex+4) % baseShift)
        PlayerSHM(playerSHMVals)

            # Draw the sprites
        SCREEN.blit(IMAGES['background'],(0,0))
        SCREEN.blit(IMAGES['player'][playerIndex],(playerx,playery + playerSHMVals['val']))
        SCREEN.blit(IMAGES['message'],(messagex,messagey))
        SCREEN.blit(IMAGES['base'],(basex,BASEY))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def MainGame(movementInfo):
    #Main game logic
    score = playerIndex = loopIter = 0
    playerIndexGen = movementInfo['playerIndexGen']

    playerx, playery = int(SCREENWIDTH * 0.2) , movementInfo['playery']
    
    basex = movementInfo['basex']
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

        # Create 2 new pipes to add to the upper and lower pipes
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
         {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
         {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]

    lowerPipes = [
         {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
         {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},

    ]

    pipeVelX = -4               # X-velocity of pipes
    playerVelY = -9             # Player's velocity along Y, same as playerFlapped
    playerMaxVelY = 10          # Max speed of descent
    playerMinVelY = -8          # Max speed of ascent
    playerAccY = 1              # Gravity, thou art a heartless bitch
    playerFlapAcc = -9          # Speed on Flap
    playerFlapped = False       # True when player flaps.

    while True:
        if -playerx + lowerPipes[0]['x'] > -30 :
            selectPipe = lowerPipes[0]
        else:
            selectPipe = lowerPipes[1]

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if (event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)):
                if playery > -2*IMAGES['player'][0].get_height():
                    playerVelY = playerFlapAcc
                    playerFlapped = True
                    SOUNDS['wing'].play()
        
        if bot.act(-playerx+selectPipe['x'], -playery+selectPipe['y'],playerVelY):
            if playery > -2*IMAGES['player'][0].get_height():
                    playerVelY = playerFlapAcc
                    playerFlapped = True
                    SOUNDS['wing'].play()

            # Check for a crash!
        crashTest = checkCrash({'x':playerx,'y':playery,'index':playerIndex}, upperPipes,lowerPipes)
        if crashTest[0]:
            # Update the Q-scores
            bot.update_scores()
            return{
                'y': playery,
                'groundCrash': crashTest[1],
                'basex': basex,
                'upperPipes' : upperPipes,
                'lowerPipes': lowerPipes,
                'score': score,
                'playerVelY': playerVelY,
            }

        # Check if player scored
        playerMidPos = playerx + IMAGES['player'][0].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4 :
                score += 1 #If player didn't hit it - score!
                SOUNDS['point'].play()
        
        # Change of base
        if (loopIter + 1) % 3 == 0:
            playerIndex = next(playerIndexGen)
        loopIter = (loopIter+1) % 30
        basex = -((-basex+100) % baseShift)

        #Movement by Player
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False
        playerHeight = IMAGES['player'][playerIndex].get_height()
        playery += min(playerVelY,BASEY-playery-playerHeight)

        # Progress game - move pipes left
        for upipe, lpipe in zip(upperPipes,lowerPipes):
            upipe['x'] += pipeVelX
            lpipe['x'] += pipeVelX
        
        # If first pipe is about to touch left edge of screen, add a new pipe
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # If first pipe gets out of bounds on left, remove it.
            if upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0)

        # Now draw the sprites
        SCREEN.blit(IMAGES['background'], (0.0))
        for upipe,lpipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0],(upipe['x'],upipe['y']))
            SCREEN.blit(IMAGES['pipe'][1],(lpipe['x'],lpipe['y']))
        