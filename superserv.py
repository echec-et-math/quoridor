from threading import Thread
import random as rd
import os
import time

import exec_serv

from quoridor_server_constants import *

# TODO maybe autoflush the gamedb from too old games / automatically from time to time

main_database = "results/gamedb.txt"

def superserver():
    # pick a code for j1 and j2
    while True:
        threadlist = list()
        available_codes = [f for f in os.listdir("submissions") if os.path.isfile("submissions/" + f)]
        while len(available_codes) < 2:
            time.sleep(RECHECK_SUBMISSIONS_DELAY) # recheck submissions
            available_codes = [f for f in os.listdir("submissions") if os.path.isfile(f)]
        rd.shuffle(available_codes)
        for k in range(NB_PARALLEL_GAMES):
            # pick random file and remove extension
            if len(available_codes) < 2: # not enough submissions to continue
                break
            name1 = available_codes.pop()[:-3]
            name2 = available_codes.pop()[:-3]
            id = str(hex(rd.randint(1, 2**32)))
            threadlist.append(Thread(target=exec_serv.exec_server, args=[name1, name2, id])) # create game
            with open(main_database, "a") as main_db:
                main_db.write(f"{name1} {name2} {id}\n")
            threadlist[k].start()
        for k in range(len(threadlist)): # join blocks must happen after all threads have been started, otherwise it's not parallelized at all
            threadlist[k].join(timeout=SUBEXEC_TIMEOUT)
        time.sleep(DELAY_BETWEEN_GLOBAL_MATCHMAKING)

if __name__ == "__main__":
    superserver()