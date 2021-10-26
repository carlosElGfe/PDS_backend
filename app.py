from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from pymongo import MongoClient
from utils import conection
import json
from datetime import datetime

app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

#MODELS
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    joined = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    def __repr__(self):
        return '<User %r>' % self.name
    
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    players = db.Column(db.Integer, unique=False, nullable=False, default=1)
    def __repr__(self):
        return '<game %r>' % str(self.id)

class GameUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'),nullable=False) 
    jugador_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False) 
    game = db.relationship('Game',
        backref=db.backref('usergames', lazy=True))
    user = db.relationship('User',
        backref=db.backref('usergames', lazy=True))
    def __repr__(self):
        return '<gameuser %r>' % str(self.id)

class GameData(db.model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'),nullable=False) 
    jugador_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False) 
    target_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False) 
    game = db.relationship('Game',
        backref=db.backref('usergames', lazy=True))
    jugador = relationship("User", foreign_keys=[jugador_id]) 
    target = relationship("User", foreign_keys=[target_id])
    def __repr__(self):
        return '<Gamedata %r>' % str(self.id)
    

#fiend request
class UserUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jugador_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False) 
    target_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False) 
    state = db.Column(db.Boolean, default=False)
    jugador = relationship("User", foreign_keys=[jugador_id])
    target = relationship("User", foreign_keys=[target_id])
    def __repr__(self):
        return '<Friend Status %r>' % str(self.id)
 
db.create_all()
#MVC    
@app.route("/")
def index():
    #userr = User.query.filter_by(id=1).first().name
    context = {}
    return Response(context, status=200, mimetype='application/json')

@app.route("/login")
def login():
    try:
        # localhost:5000/login?username=john
        #COLLECT THE PARAMS IN THE PYTHON CODE
        name = request.args.get('username')
        
        targer_user = User.query.filter_by(name = name).first()
        
        reponse = {}
        reponse['user_id'] = targer_user.id
         
        return jsonify(reponse)
    except ValueError:
        return Response("Error", status=400, mimetype='application/json')

@app.route("/new_game")
def new_game():
    try:
        
        #  localhost:5000/new_game?current_id=1&players=4&sala=33
        
        #COLLECT THE PARAMS IN THE PYTHON CODE
        sala = request.args.get('sala')
        jugadores = request.args.get('players')
        my_id = request.args.get('current_id')
        current_user = User.query.filter_by(id = int(my_id)).first()
        
        #CREATE THE GAME
        game = Game(id=int(sala), players=int(jugadores))
        
        #RELATE THE GAME TO A USER (current)
        gameuser = GameUser(game = game, user = current_user)
        
        db.session.add(game)
        db.session.add(gameuser)
        db.session.commit()
        
        #STAGE THE CHANGES
        
        #GENERATE RESPONSE
        reponse = {}
        reponse[sala] = sala
        reponse['jugadores'] = jugadores
        return Response(reponse, status=201, mimetype='application/json')
    except ValueError:
        return Response("Error", status=400, mimetype='application/json')
    
@app.route("/new_user")
def new_user():
    try:
        #  localhost:5000/new_user?username=pedro
        
        #COLLECT THE PARAMS IN THE PYTHON CODE
        user_name = request.args.get('username')
        
        #RELATE THE GAME TO A USER (current)
        new_user = User(name = user_name)
        db.session.add(new_user)
        
        #STAGE THE CHANGES
        db.session.commit()
        
        #GENERATE RESPONSE
        reponse = {}
        return Response(reponse, status=201, mimetype='application/json')
    except Exception:
        return Response("Error", status=400, mimetype='application/json')

@app.route("/games")
def games():
    try:
        #  localhost:5000/games?my_id=1
        
        #COLLECT THE PARAMS IN THE PYTHON CODE
        my_id = int(request.args.get('my_id'))
        
        #RELATE THE GAME TO A USER (current)
        games_ids = GameUser.query.filter_by(jugador_id = my_id).distinct()
        resp = {}
        for value in games_ids:
            buff = []
            ganembuffer = Game.query.filter_by(id = value.game_id).first()
            buff.append(value.game_id)
            buff.append(ganembuffer.players)
            buff.append(ganembuffer.created)
            resp[value.game_id] = (buff)
            print(value.game_id)
        respp = {}
        respp[str(resp)] = resp
        return Response(respp, status=201, mimetype='application/json')
    except ValueError:
        return Response("Error", status=400, mimetype='application/json')

@app.route("/join")
def join():
    try:
        #COLLECT THE PARAMS IN THE PYTHON CODE
        sala = request.args.get('sala')
        my_id = request.args.get('current_id')
        current_user = User.query.filter_by(id = int(my_id)).first()
        
        #FIND THE GAME
        game = Game.query.filter_by(id = int(sala)).first()
                
        #RELATE THE GAME TO A USER (current)
        gameuser = GameUser(game = game, user = current_user)
        db.session.add(gameuser)
        
        #STAGE THE CHANGES
        db.session.commit()
        
        #GENERATE RESPONSE
        reponse = {}
        reponse[str("juego usuario creado con extipo")] = sala
         
        return Response(reponse, status=201, mimetype='application/json')
    except ValueError:
        return Response("Error", status=400, mimetype='application/json')

@app.route("/add_friend")
def add_friend():
    try:
        my_id = request.args.get('current_id')
        target_id = request.args.get('target_id')
        current_user = User.query.filter_by(id = int(my_id)).first()
        target_user = User.query.filter_by(id = int(target_id)).first()
        
        #CREATE the user user instance
        useruser = UserUser( jugador = current_user, target = target_user)
        db.session.add(useruser)
        
        #STAGE THE CHANGES
        db.session.commit()
        reponse = {}
        reponse['current'] = my_id
        reponse['target'] = target_id
        reponse['status'] = False
        reponse['id'] = useruser.id
        return jsonify(reponse)
    except ValueError:
        return Response("Error", status=400, mimetype='application/json')
        
@app.route("/accept_friend_request")
def accept_friend_request():
    try:
        my_id = request.args.get('current_id')
        target_id = request.args.get('target_id')
        current_user = User.query.filter_by(id = int(my_id)).first()
        target_user = User.query.filter_by(id = int(target_id)).first()
        
        #Fetch and update the user user instance
        useruser = UserUser.query.filter_by(jugador = current_user, target = target_user).first()
        
        useruser.status= True
        
        #STAGE THE CHANGES
        db.session.commit()
        reponse = {}
        reponse['current'] = my_id
        reponse['target'] = target_id
        reponse['status'] = True
        return jsonify(reponse)
    except ValueError:
        return Response("Error", status=400, mimetype='application/json')
        
@app.route("/get_friends")
def get_friends():
    try:
        my_id = request.args.get('current_id')
        current_user = User.query.filter_by(id = int(my_id)).first()
        
        #Fetch and update the user user instance
        userusers = UserUser.query.filter_by(jugador = current_user, state = True).all()
        reponse = {}
        cont = 1
        for i in userusers:
            reponse[str(cont)] = i.name
        reponse['current'] = my_id
        return jsonify(reponse)
    except ValueError:
        return Response("Error", status=400, mimetype='application/json')
    
@app.route("/get_friends_not_accepted")
def get_friends_not_accepted():
    try:
        my_id = request.args.get('current_id')
        current_user = User.query.filter_by(id = int(my_id)).first()
        
        #Fetch and update the user user instance
        userusers = UserUser.query.filter_by(jugador = current_user, state = False).all()
        reponse = {}
        cont = 1
        for i in userusers:
            reponse[str(cont)] = i.name
        reponse['current'] = my_id
        return jsonify(reponse)
    except ValueError:
        return Response("Error", status=400, mimetype='application/json')
   
    
@app.route("/invite")
def invite():
    try:
        #COLLECT THE PARAMS IN THE PYTHON CODE
        sala = request.args.get('sala')
        target_id = request.args.get('target_id')
        targer_user = User.query.filter_by(id = int(target_id)).first()
        
        #FIND THE GAME
        game = Game.query.filter_by(id = int(sala)).first()
                
        #RELATE THE GAME TO A USER (current)
        gameuser = GameUser(game = game, user = targer_user)
        db.session.add(gameuser)
        
        #STAGE THE CHANGES
        db.session.commit()
        
        #GENERATE RESPONSE
        reponse = {}
        reponse['sala'] = "Target invited succesfully!"
         
        return Response(reponse, status=201, mimetype='application/json')
    except ValueError:
        return Response("Error", status=400, mimetype='application/json')

@app.route("/jugada")
def jugada():
    #TODO terminar esta ruta para poder jugar sobre una sala
    sala = request.args.get('sala')
    current = request.args.get('current')
    target = request.args.get('target')
    target = request.args.get('target')
    reponse = {}
    reponse['sala'] = sala
    reponse['current'] = current
    reponse['target'] = current
    
    #create new game with request parms
    # example -> print(request.args.get("n"))
    try:
        return Response(reponse, status=201, mimetype='application/json')
    except Exception:
        return Response("Error", status=400, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=False)    