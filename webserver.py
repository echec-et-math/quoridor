import requests
import json
import random as rd

from flask import Flask, request, jsonify, make_response

headers =  {"Content-Type":"application/json"}

app = Flask(__name__)

default_score_response = [
    {'opponent' : 'alice', 'victory' : True},
    {'opponent' : 'bob', 'victory' : False}
]

default_score_response2 = [
    {'opponent' : 'test', 'victory' : True},
    {'opponent' : 'test2', 'victory' : False}
]

@app.get("/")
def website_root():

    return 200

@app.get("/score")
def get_score():
    cookie = request.cookies.get("quoridor_user_id")
    # read ID from cookie jar
    # fetch scores from datasheet
    # build response in JSON
    if cookie == None:
        return jsonify(default_score_response) # TODO
    else:
        return jsonify(default_score_response2)

@app.post("/submitcode")
def submit_code():
    resp = make_response("Not implemented yet.")
    return jsonify(resp), 500

@app.get("/register")
def create_cookie_id():
    # generate random ID
    # build according cookie
    # add cookie to jar
    cookie = request.cookies.get("quoridor_user_id")
    if cookie == None:
        resp = make_response("Successfully registered.")
        resp.set_cookie("quoridor_user_id", hex(rd.randint(1, 2**128)))
        return resp, 200
    else:
        # user already exists
        resp = make_response("You are already registered !")
        return resp, 403

@app.get("/unregister")
def unregister():
    cookie = request.cookies.get("quoridor_user_id")
    if cookie != None:
        resp = make_response("Successfully unregistered.")
        resp.delete_cookie("quoridor_user_id")
        return resp, 200
    else:
        # user doesn't exist
        resp = make_response("You never registered before !")
        return resp, 403