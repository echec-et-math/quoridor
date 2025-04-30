import requests
import json
import random as rd

from flask import Flask, request, jsonify, make_response

headers =  {"Content-Type":"application/json"}

app = Flask(__name__)

default_score_response2 = [
    {'opponent' : 'test', 'victory' : True},
    {'opponent' : 'test2', 'victory' : False}
]

@app.get("/")
def website_root():
    resp = make_response("Welcome to the Quoridor web server ! Please register at /register, submit your code at /submitcode and check your scores at /score !")
    return resp, 200

@app.get("/score")
def get_score():
    cookie = request.cookies.get("quoridor_user_id")
    # read ID from cookie jar
    # fetch scores from datasheet
    # build response in JSON
    if cookie == None:
        resp = make_response("You are not registered to the server yet !")
        return resp, 401
    else:
        resp = make_response()
        return jsonify(default_score_response2)

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
    resp = make_response("Sucessfully saved your code.")
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