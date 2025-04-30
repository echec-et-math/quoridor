def read_input(infile):
    while infile.empty():
        pass
    return infile.get()

def write_output(outfile, response):
    outfile.put(response)

def play_move(infile, outfile, response):
    write_output(outfile, response)
    serv_response = read_input(infile)
    print(serv_response)
    return serv_response == "OK"

def code(infile, outfile):
    num_player = int(read_input(infile))
    response = "I'm J1"
    while True:
        read_msg = read_input(infile)
        if read_msg == "END":
            return
        while not play_move(infile, outfile, response):
            # your bot has to update response to your next move
            # your are stuck in this loop while your move is invalid
            response = "new move because previous invalid"

if __name__ == "__main__":
    code()