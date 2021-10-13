from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from utils import conection
import json
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

#MODELS
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
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
 
db.create_all()
#MVC    
@app.route("/")
def index():
    #userr = User.query.filter_by(id=1).first().name
    context = {}
    context['item'] = "ejemplo"
    return jsonify(context)

@app.route("/new_game")
def new_game():
    try:
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
        reponse['sala'] = sala
        reponse['jugadores'] = jugadores
        return Response(reponse, status=201, mimetype='application/json')
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
        reponse['sala'] = sala
         
        return Response(reponse, status=201, mimetype='application/json')
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
    app.run(debug=True)    