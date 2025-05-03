import itertools
import requests
import json
import random as rd

from flask import Flask, request, jsonify, make_response

headers =  {"Content-Type":"application/json"}

app = Flask(__name__)
# port is 5000
# remember to create the submissions folder

main_database = "results/gamedb.txt"

###########
## Fonctions de lecture de fichiers 

def fetch_database(id):
    # Find all games associated to this id
    with open(main_database, "r") as main_db:
        gamelist = main_db.readlines()
    res = []
    for g in gamelist:
        g = g[:-1] # remove trailing endline
        j1, j2, gameid = tuple(g.split(" "))
        if j1 == id: res.append((gameid, j1, j2, 1))
        elif j2 == id: res.append((gameid, j1, j2, 2))
    return res

def fetch_game(id):
    # Read game log associated to this id
    try: # file might not exist if the game was just created : unlikely but possible
        with open("results/" + str(id) + ".txt", "r") as gamefile:
            movelist = gamefile.readlines()
            return movelist
    except FileNotFoundError:
        print("Game not found !")
        return None

###########
## Fonctions d'affichage

def game_to_HTML(gameid, name1, name2, movelist, playerslot):
    if playerslot == 1:
        titles = """<tr>
        <th>YOU</th>
        <th>OPPONENT</th>
        </tr>"""
    else:
        titles = """<tr>
        <th>OPPONENT</th>
        <th>YOU</th>
        </tr>"""
    res = f"""<p>RESULTS FOR GAME {gameid}, {name1} vs {name2} :</p><table style="width:100%">{titles}"""
    for k in range(len(movelist) // 2):
        m, n = movelist[2*k], movelist[2*k + 1]
        res += f"<tr><td>{m}</td><td>{n}</td></tr>"
    if len(movelist) % 2 == 1:
        res += f"<tr><td>{movelist[-1]}</td></tr>"
    return res + "</table>" # TODO edit <p> header with color and game status

def game_in_progress_HTML(gameid, name1, name2):
    return f"""<p>RESULTS FOR GAME {gameid}, {name1} vs {name2} : STARTING NOW</p>"""

def build_HTML_scoresheet(id):  # wrapper pour assembler toutes les parties d'un joueur
    res = """<!DOCTYPE html>
<html>
<style>
table, th, td {
  border:1px solid black;
}
</style>
<body><h2>SCORES FOR PLAYER """ + str(id) + " :</h2>"
    gamelist = fetch_database(id)
    for id, n1, n2, ps in gamelist:
        ml = fetch_game(id)
        if ml == None:
            res += game_in_progress_HTML(id, n1, n2)
        else:
            res += game_to_HTML(id, n1, n2, ml, ps)
    return res + """</body>
    </html>"""

###########
## Fonctions de l'API

@app.get("/")
def website_root():
    resp = make_response("Welcome to the Quoridor web server ! Please register at /register, unregister at /unregister submit your code at /submitcode and check your scores at /score !")
    return resp, 200

@app.get("/score")
def get_score():
    id = request.cookies.get("quoridor_user_id")
    # read ID from cookie jar
    # fetch scores from datasheet
    # build response in JSON
    if id == None:
        resp = make_response("You are not registered to the server yet !")
        return resp, 401
    else:
        resp = make_response()
        return build_HTML_scoresheet(id)

@app.get("/submitcode")
def submitcode_get():
    resp = make_response("""<form action="submitcode" method="post" enctype=multipart/form-data>
    Code file : <input id="fileupload" name="submission" type="file" />
    <input type="submit" value="Submit">
</form>""")
    return resp, 200

@app.post("/submitcode")
def submitcode_post():
    cookie = request.cookies.get("quoridor_user_id")
    if cookie == None:
        resp = make_response("You are not registered to the server yet !")
        return resp, 401
    submission = request.files.get("submission")
    if submission == None:
        resp = make_response("No file sent.")
        return resp, 400
    submission.save("submissions/" + cookie + ".py")
    resp = make_response("Successfully saved your code.")
    return resp, 201


@app.get("/register")
def create_cookie_id():
    # generate random ID
    # build according cookie
    # add cookie to jar
    cookie = request.cookies.get("quoridor_user_id")
    if cookie == None:
        id = hex(rd.randint(1, 2**32))
        resp = make_response("Successfully registered as : " + str(id))
        resp.set_cookie("quoridor_user_id", id)
        return resp, 201
    else:
        # user already exists
        resp = make_response("You are already registered as " + str(cookie) + " !")
        return resp, 403

@app.get("/unregister")
def unregister():
    cookie = request.cookies.get("quoridor_user_id")
    if cookie != None:
        resp = make_response("Successfully unregistered.")
        resp.delete_cookie("quoridor_user_id")
        return resp, 201
    else:
        # user doesn't exist
        resp = make_response("You never registered before !")
        return resp, 403