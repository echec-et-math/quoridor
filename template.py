def read_input(infile):
    while infile.empty():
        pass
    return infile.get()

def write_output(outfile, response):
    outfile.put(response)

def code(infile, outfile):
    num_player = int(read_input(infile))
    swap = True
    while True:
        read_msg = read_input(infile)
        if read_msg == "END":
            return # game end
        if swap:
            response = "MOVE UP" # edit this line
        else:
            response = "MOVE DOWN"
        swap = not swap
        write_output(outfile, response)
        # your bot has to update response to your next move

if __name__ == "__main__":
    code()