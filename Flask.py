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

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
    
@app.route('/')
def show_entries():
    
    return render_template('fighters.html')

@app.route('/fightData')
def GetFightData():
    from SaltyFunctions import FightStats
    fighter = request.args.get('fighter', 0, type = int)
    
    print FightStats.fighter1

    if fighter == 1:
        return jsonify(FightStats.fighter1)
    if fighter == 2:
        return jsonify(FightStats.fighter2)
    else:
        return jsonify("No Fighter Found")
    
@app.route('/testFight')
def TestFight():
    from SaltyFunctions import FightStats
    FightStats.TestSetFighter()
    fighter = request.args.get('fighter', 0, type = int)
    if fighter == 1:
        return jsonify(FightStats.fighter1)
    if fighter == 2:
        return jsonify(FightStats.fighter2)
    else:
        return jsonify("No Fighter Found")
    
