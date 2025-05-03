from threading import Thread
import queue
import time
import importlib

from quoridor_server_constants import *

def exec_submission(submission, infile, outfile):
    #try:
    submission.code(infile, outfile)
    #except Exception:
    #print("Error while running code : ", submission)
    
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
    return True # len(move) > 10

def apply_move(gamestate, move):
    return gamestate

def log(filename, msg):
    with open("results/" + filename + ".txt", "a") as f_results:
        f_results.write(msg + '\n')

# multi-move approach :
# while not queue_in.is_empty():
#    move = queue_in.get()

NOMOVE = 0
INVALID = 1
OK = 2

def await_move_update_gamestate(gamestate, queue_in):
    time.sleep(PLAYER_MOVE_TIMEOUT)
    move = readfrom(queue_in)
    if move == None:
        return NOMOVE, None, gamestate
    if not is_valid(gamestate, move):
        return INVALID, move, gamestate
    gamestate = apply_move(gamestate, move)
    return OK, move, gamestate

def exec_server(name1, name2, game_id):
    #print("START SERVER")
    try:
        f1 = importlib.import_module("submissions." + name1)
        f2 = importlib.import_module("submissions." + name2)
        j1_in, j1_out, j2_in, j2_out = queue.Queue(maxsize=10), queue.Queue(maxsize=10), queue.Queue(maxsize=10), queue.Queue(maxsize=10)
        #print("Queues created")
        t1 = Thread(target=exec_submission, args=[f1, j1_out, j1_in])
        t2 = Thread(target=exec_submission, args=[f2, j2_out, j2_in])
        #print("Threads created")
        t1.start()
        t2.start()
        #print("Threads started")
        j1_out.put("1") # player number
        j2_out.put("2") # player number
        gamestate = init_gamestate()
        move = "INIT"
        k = 0
        while not gamestate['ended'] and k < 10: # main game loop
            # Update state to J1
            writeto(j1_out, move)
            errtype, move, gamestate = await_move_update_gamestate(gamestate, j1_in)
            if errtype == NOMOVE:
                # no move from j1
                writeto(j1_out, "END")
                writeto(j2_out, "END")
                log(game_id, "timeout1")
                return
            elif errtype == INVALID:
                # invalid move from j1
                writeto(j1_out, "END")
                writeto(j2_out, "END")
                log(game_id, f"invalid1 : {move}")
                return
            log(game_id, move)
            writeto(j2_out, move)
            errtype, move, gamestate = await_move_update_gamestate(gamestate, j2_in)
            if errtype == NOMOVE:
                # no move from j2
                writeto(j1_out, "END")
                writeto(j2_out, "END")
                log(game_id, "timeout2")
                return
            elif errtype == INVALID:
                # invalid move from j2
                writeto(j1_out, "END")
                writeto(j2_out, "END")
                log(game_id, f"invalid2 : {move}")
                return
            log(game_id, move)
            k += 1
        writeto(j1_out, "END")
        writeto(j2_out, "END")
        log(game_id, f"win{gamestate['winner']}")
        #print("END SERVER")
    except Exception:
        print("Error while running")

if __name__ == "__main__":
    exec_server()