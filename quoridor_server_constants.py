PLAYER_MOVE_TIMEOUT = 0.1
# in seconds, the allowed time to input a move.
#The server waits for this amount of time no matter what, even if a move was inputted before the timeout.

NB_PARALLEL_GAMES = 10 # max instances allowed at the same time

RECHECK_SUBMISSIONS_DELAY = 60 # in seconds : time to wait to recheck the submissions file, if not enough files

SUBEXEC_TIMEOUT = 300 # in seconds : time for a whole match thread to be considered as crashed

DELAY_BETWEEN_GLOBAL_MATCHMAKING = 5 # in seconds : delay before restarting another global matchmaking session