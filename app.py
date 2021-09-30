from flask import Flask, request
from pymongo import MongoClient
    
app = Flask(__name__)

@app.route("/")
def index():
    return "Doubt back end welcome !"

@app.route("/new_game")
def new_game(request):
    client = MongoClient("mongodb+srv://new_user1:new_user123@cluster0.3rxb9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    #create new game with request parms
    # example -> print(request.args.get("n"))
    return "New game created"
