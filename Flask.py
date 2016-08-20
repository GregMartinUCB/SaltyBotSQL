# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 14:43:52 2016

@author: Greg
"""

import os
import sqlite3
from flask import (Flask, request, session, g, redirect,
                  url_for, abort, render_template, flash, jsonify)

from SaltyFunctions import *
from database import db_session
from models import Fight, Fighter


app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'Fighters.db'),
    SECRET_KEY='TheKey',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

fightId = None

#arguement is a SQLAlchemy row object, returns array of dictionaries
def FightHistoryToJson(fighterData, currentFightId):
    #Finds all fights that given fighter was in
    histories = db_session.query(Fight).filter(or_(Fight.fighter1_id ==fighterData.id,
                                                    Fight.fighter2_id == fighterData.id)).filter(Fight.id != currentFightId)
    
    appendedJsonHistory = []
    for fightHistory in histories:
        winLose = None
        #Must determine if the fighter was player 1 or player 2 and set bets occordingly
        if fightHistory.fighter1_id == fighterData.id:
            opponentId = fightHistory.fighter2_id
            betFor = fightHistory.bet1
            betAgainst = fightHistory.bet2
        else:
            opponentId = fightHistory.fighter1_id
            betFor = fightHistory.bet2
            betAgainst = fightHistory.bet1

        if fightHistory.winner_id == fighterData.id:
            winLose = True
        else:
            winLose = False

        historyJson = {'opponentName':db_session.query(Fighter).get(opponentId).name,
                        'winLose': winLose,
                        'betFor':betFor,
                        'betAgainst':betAgainst}
        appendedJsonHistory.append(historyJson)

        return appendedJsonHistory

#For closing the database session when the app closes down
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
    
@app.route('/')
def show_entries():
    
    return render_template('fighters.html')

@app.route('/fightData')
def GetFightData():

    currentFight = db_session.query(Fight).order_by(Fight.id.desc()).first()
    fighter = request.args.get('fighter', 0, type = int)

    if fighter == 1:
        fighterData = db_session.query(Fighter).get(currentFight.fighter1_id)
    else:
        fighterData = db_session.query(Fighter).get(currentFight.fighter2_id)

    history = FightHistoryToJson(fighterData, currentFight.id)

    jsonToSend = {'name':fighterData.name, 'averageWinRatio':fighterData.winRate,
                    'averageBetRatio': fighterData.betRatio,
                    'streak': fighterData.streak,
                    'fightHistory':history,
                    'fightNumber':currentFight.id}
    return jsonify(jsonToSend)
    
@app.route('/testFight')
def TestFight():
    #Using fight number 11 for test. Real one will get the current fight.
    currentFight = db_session.query(Fight).get(11)
    fighter = request.args.get('fighter', 0, type = int)

    if fighter == 1:
        fighterData = db_session.query(Fighter).get(currentFight.fighter1_id)
    else:
        fighterData = db_session.query(Fighter).get(currentFight.fighter2_id)

    history = FightHistoryToJson(fighterData, currentFight.id)

    jsonToSend = {'name':fighterData.name, 'averageWinRatio':fighterData.winRate,
                    'averageBetRatio': fighterData.betRatio,
                    'streak': fighterData.streak,
                    'fightHistory':history,
                    'fightNumber':currentFight.id}
    return jsonify(jsonToSend)

@app.route('/newFight')
def IsNewFight():

    fightId = request.args.get('fightId',0, type = int)
    currentFight = db_session.query(Fight).order_by(Fight.id.desc()).first()
    if(fightId == currentFight.id):
        return jsonify({'new':False})
    else:
        return jsonify({'new':True})
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')

    
