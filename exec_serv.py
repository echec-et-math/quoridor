#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 16:43:52 2025

@author: GrandLatapon
"""

import os
from threading import Thread
import queue
import time

def exec_submission(module, infile, outfile):
    print("begin")
    module.code(infile, outfile)
    outfile.put("end")
    
def readfrom(queue):
    while queue.empty():
        pass
    return queue.get()

def writeto(queue, msg):
    queue.put(msg)

def is_valid(gamestate, move):
    return len(move) > 10

def apply_move(gamestate, move):
    return gamestate

def await_for_valid_move_and_update_gamestate(gamestate, queue_in, queue_out):
    move = readfrom(queue_in)
    while not is_valid(gamestate, move):
        writeto(queue_out, "INVALID_MOVE")
        move = readfrom(queue_in)
    writeto(queue_out, "OK")
    print("Found valid move :", move)
    gamestate = apply_move(gamestate, move)
    return move, gamestate

def exec_server():
    print("START SERVER")
    import submission_base as f1
    import submission_base2 as f2
    try:
        j1_in, j1_out, j2_in, j2_out = queue.Queue(maxsize=10), queue.Queue(maxsize=10), queue.Queue(maxsize=10), queue.Queue(maxsize=10)
        print("Queues created")
        t1 = Thread(target=exec_submission, args=[f1, j1_out, j1_in])
        t2 = Thread(target=exec_submission, args=[f2, j2_out, j2_in])
        print("Threads created")
        t1.start()
        t2.start()
        print("Threads started")
        j1_out.put("1") # player number
        j2_out.put("2") # player number
        time_start_loop = time.time()
        MAX_TIME = 5
        elapsed = 0
        gamestate = "TODO"
        move = "INIT"
        game_ended = False
        while elapsed < MAX_TIME and not game_ended: # main game loop
            elapsed = time.time() - time_start_loop
            # Update state to J1
            writeto(j1_out, move)
            move, gamestate = await_for_valid_move_and_update_gamestate(gamestate, j1_in, j1_out)
            writeto(j2_out, move)
            move, gamestate = await_for_valid_move_and_update_gamestate(gamestate, j2_in, j2_out)
        writeto(j1_out, "END")
        writeto(j2_out, "END")
        print("END SERVER")
    except Exception:
        print("Error while running")

if __name__ == "__main__":
    exec_server()