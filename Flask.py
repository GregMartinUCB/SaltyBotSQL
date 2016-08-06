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
from SaltyFunctions import FightStats

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

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
    
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
    
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
        
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print ('Initialized the database.')
    
@app.route('/')
def show_entries():
    
    return render_template('fighters.html')

@app.route('/fightData')
def GetFightData():
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
    FightStats.TestSetFighter()
    fighter = request.args.get('fighter', 0, type = int)
    if fighter == 1:
        return jsonify(FightStats.fighter1)
    if fighter == 2:
        return jsonify(FightStats.fighter2)
    else:
        return jsonify("No Fighter Found")
    
