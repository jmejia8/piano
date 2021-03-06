import pygame
from pygame.locals import *
from classes import Background, Block, RedLine, scales, get_icon
from data import tile_positions, sound_keys, sounds, key_map
from gameio import csv_result, PianoSession
from settings import settings
from itertools import islice
import os
import sys
import time

# Bitmask values for evaluation
EVAL_NOTE  = 2
EVAL_SCALE = 4
EVAL_TIME  = 8

def nex_blocks(session):
    """Get next four blocks from session and map them to a list of Block objects
    """
    def gen_blocks(note_tuple):
        # index, note
        return Block(tile_positions[note_tuple[1][0], note_tuple[0]], note_tuple[1][0], note_tuple[1][1])
    return list(map(gen_blocks, enumerate(islice(session, 4))))

def eval_key(block, evaluated, note, scale, correspondence):
    """Compute the evaluation of a click"""
    res = 0
    if note == block.note:
        res |= EVAL_NOTE
    if scale == block.scale:
        res |= EVAL_SCALE
    if not evaluated:
        res |= EVAL_TIME

    how, when, where = correspondence

    correct = True
    if how: 
        correct &= note == block.note
    if when: 
        correct &= not evaluated
    if where: 
        correct &= scale == block.scale



    return res, correct

def gen_essay(blocks):
    """Given a list of block objects return the evaluation matrix for this essay
    """
    return [
        (block.note, block.scale)
        for block in blocks
    ]

def display_info(session, screen, clock):
    # Info screen variables
    infoscreens  = session.get_infoscreens()
    num_infos    = len(infoscreens)
    current_info = 0

    # Info screen
    while True:
        # tick to 60 fps
        clock.tick(60)
        # Handle events
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == 27:
                # ESC key, exit game
                return
            elif event.type == KEYDOWN and event.unicode in sound_keys:
                # Valid key, validate input and update essay evaluation matrix
                note = key_map[event.unicode][0]

                if note == 'C':
                    current_info += 1
                    if current_info == num_infos:
                        break
                elif note == 'B' and current_info == num_infos-1:
                    current_info = 0
            elif event.type == QUIT:
                # Handles window close button
                return
        else:
            screen.blit(infoscreens[current_info].image, infoscreens[current_info].rect)

            pygame.display.flip()
            continue
        break

def main(session):
    """Main entry point of this game, keeps the game loop"""
    # Initialize screen
    pygame.init()
    # the game screen, pass FULLSCREEN to fullscreen
    screen = pygame.display.set_mode((800, 600))
    # Game icon
    pygame.display.set_icon(get_icon())
    # Game title
    pygame.display.set_caption('Piano')

    # Fill background
    background = Background()

    # Blit everything to the screen
    clock = pygame.time.Clock()

    # Display info screens
    display_info(session, screen, clock)

    # Blocks
    blocks = nex_blocks(session)
    # The red line
    redline = RedLine(380, 460, 2)
    # First scale (corresponding to first block)
    scale = scales[blocks[0].scale]

    # Gane loop variables
    move         = True # controls redline motion speed
    column       = -1 # stores current column given by the clock
    progress     = float('-inf') # register progress of redline
    evaluated    = False # A flag that indicates if this column has been evaluated
    evaluation   = [] # Essay evaluation matrix
    essay        = gen_essay(blocks)
    criteria     = session.get_criteria()
    essay_num    = 1
    countScreen  = 1
    passLevel    = False
    startTime    = time.time()
    firstTime    = True 

    HOW   = criteria in [3,  7, 11, 15] 
    WHEN  = criteria in [9, 11, 13, 15]
    WHERE = criteria in [5,  7, 13, 15]

    new_column = 0
    new_progress = progress

    # Event loop
    while True:
        # tick to 60 fps
        clock.tick(60)
        # Handle events
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == 27:
                # ESC key, exit game
                return
            elif event.type == KEYDOWN and event.unicode in sound_keys and column>-1:
                clicked_note, clicked_scale = key_map[event.unicode]
                score, correct_ans = eval_key(
                    blocks[column],
                    evaluated,
                    clicked_note,
                    clicked_scale,
                    (HOW, WHEN, WHERE)
                )

                evaluation.append([
                    essay_num,
                    blocks[column].note if not evaluated else None,
                    blocks[column].scale if not evaluated else None,
                    clicked_note,
                    clicked_scale,
                    score,
                    1,
                    time.time(),
                    score + 1,
                    time.time() - startTime
                ])
                startTime = time.time()
                
                if not evaluated :
                    if correct_ans:
                        sounds[key_map[event.unicode]].play()
                    else:
                        passLevel = False
                        countScreen = 1
                    

                    if  not WHEN:
                        new_column = (new_column + 1) % 4

                        if new_column == 0:
                            new_progress = 0
                            progress = 1

                evaluated = True
            elif event.type == QUIT:
                # Handles window close button
                return

        # Move the redline
        if move:

            if WHEN:
                new_progress = redline.move()
                new_column = redline.get_column()


        if progress != new_progress: # progress has changed
            # Essay finished, report to session
            if new_progress < progress:
                session.results += csv_result(evaluation)
                blocks     = nex_blocks(session)
                essay      = gen_essay(blocks)
                evaluation = []
                essay_num += 1
                countScreen += 1

                if countScreen > 10:
                    passLevel   = True
                    countScreen = 1

                if passLevel:
                    session.session['level'] += 1
                    break

                if not blocks :
                    break

                if WHEN and not evaluated:
                    passLevel = False
                    countScreen = 1

            progress = new_progress

        # Change the column and the scale
        if new_column != column and new_column > -1:
            if firstTime:
                startTime = time.time()
                firstTime = False
            if not evaluated and column > -1: # Send an empty evaluation
                evaluation.append([
                    essay_num,
                    blocks[column].note,
                    blocks[column].scale,
                    None,
                    None,
                    0,
                    0,
                    0,
                    0,
                    0,
                ])
                passLevel = False
            evaluated = False
            column = new_column
            scale = scales[blocks[column].scale]


        # Paint background
        screen.fill((255, 255, 255))
        screen.blit(background.image, background.rect)

        # Paint blocks
        if HOW:
            for block in blocks:
                screen.blit(block.image, block.rect)

        # Paint the redline
        if WHEN:
            screen.blit(redline.image, redline.rect)
        # Paint the scale
        if WHERE:
            screen.blit(scale.image, scale.rect)

        # Send everything to screen
        pygame.display.flip()

        # Alternate readline motion
        move = not move


if __name__ == '__main__':
    with PianoSession() as piano_session:
        main(piano_session)
