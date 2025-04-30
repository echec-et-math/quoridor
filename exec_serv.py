import os
from threading import Thread
import queue
import time

def exec_submission(module, infile, outfile):
    print("begin")
    try:
        import safety_preexec # not sure whether it will work after the previous imports
        module.code(infile, outfile)
    except Exception:
        print("Error while running code : ", module)
    
def readfrom(queue):
    if queue.empty():
        return None
    return queue.get()

def writeto(queue, msg):
    queue.put(msg)

def init_gamestate():
    gs = dict()
    gs['winner'] = 0
    gs['ended'] = False
    return gs # TODO not finished

def is_valid(gamestate, move):
    return len(move) > 10

def apply_move(gamestate, move):
    return gamestate

def log(movelist, end_status):
    return # TODO

def await_move_update_gamestate(gamestate, queue_in, queue_out):
    move = readfrom(queue_in)
    if move == None:
        return None, gamestate
    if not is_valid(gamestate, move):
        writeto(queue_out, "INVALID_MOVE")
        return False, gamestate
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
        gamestate = init_gamestate()
        move = "INIT"
        movelist = []
        while not gamestate['ended']: # main game loop
            # Update state to J1
            writeto(j1_out, move)
            move, gamestate = await_move_update_gamestate(gamestate, j1_in, j1_out)
            if move == None:
                # no move from j1
                writeto(j1_out, "END")
                writeto(j2_out, "END")
                log(movelist, "timeout1")
                return
            elif move == False:
                # invalid move from j1
                writeto(j1_out, "END")
                writeto(j2_out, "END")
                log(movelist, "invalid1")
                return
            movelist.append(move)
            writeto(j2_out, move)
            move, gamestate = await_move_update_gamestate(gamestate, j2_in, j2_out)
            if move == None:
                # no move from j2
                writeto(j1_out, "END")
                writeto(j2_out, "END")
                log(movelist, "timeout2")
                return
            elif move == False:
                # invalid move from j2
                writeto(j1_out, "END")
                writeto(j2_out, "END")
                log(movelist, "invalid2")
                return
            movelist.append(move)
        writeto(j1_out, "END")
        writeto(j2_out, "END")
        log(movelist, f"win{gamestate['winner']}")
        print("END SERVER")
    except Exception:
        print("Error while running")

if __name__ == "__main__":
    exec_server()