import time

def read_input(infile):
    while infile.empty():
        pass
    return infile.get()

def write_output(outfile, response):
    outfile.put(response)

def code(infile, outfile):
    num_player = int(read_input(infile))
    movelist_1 = [(5, 2), (5, 3), (5, 4), (5, 5)]
    movelist_2 = [(5, 8), (5, 7), (5, 6), (5, 5)]
    k = 0
    while True:
        read_msg = read_input(infile)
        if read_msg == "END":
            return # game end
        if num_player == 1:
            response = movelist_1[k] # edit this line
        else:
            response = movelist_2[k]
        time.sleep(2)
        write_output(outfile, response)
        k += 1
        # your bot has to update response to your next move

if __name__ == "__main__":
    code()