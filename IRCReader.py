# -*- coding: utf-8 -*-
"""
Created on Tue May  3 09:54:53 2016

@author: Greg
"""

import socket
import os
import datetime
import numpy as np
from SaltyFunctions import split_data
from SaltyFunctions import FindNames
from SaltyFunctions import FindBets
from models import Fight, Fighter
from database import db_session


def RecordFightToDB(fighter1,fighter2,fight,Winner):
    
    #set current fight to false.
    fight.currentFight = False
    #Identify winner and save as foreign key
    if Winner == fighter1.name:
        fight.winner = fighter1
    elif Winner == fighter2.name:
        fight.winner = fighter2
    else:
        print ("Unable to match declared winner with a fighter.")
        return

    fight.time = datetime.datetime.now()
    db_session.add(fight)

    #determine ratios and averages
    avgBetRatio1, winRate1 = GetFighterStats(fighter1)
    avgBetRatio2, winRate2 = GetFighterStats(fighter2)

    #Save fighter values.
    fighter1.winRate = winRate1
    fighter1.betRatio = avgBetRatio1
    fighter2.winRate = winRate2
    fighter2.betRatio = avgBetRatio2

    db_session.add_all([fighter1,fighter2])
    db_session.commit()

def GetFighterStats(fighter):

    history = Fight.query.filter(Fight.fighter1 == fighter | Fight.fighter2 == fighter)

    betFor = []
    betAgainst = []
    winLose = []
    for pastFight in history:
        if pastFight.winner == fighter:
            winLose.append(1)
        else:
            winLose.append(0)

        if pastFight.fighter1 == fighter:
            betFor.append(pastFight.bet1)
            betAgainst.append(pastFight.bet2)
        else:
            betFor.append(pastFight.bet2)
            betAgainst.append(pastFight.bet1)

    avgBetRatio = GetAverageBetRatio(betFor, betAgainst)
    winRate = GetWinRate(winLose)

    return avgBetRatio, winRate

def GetAverageBetRatio(betFor, betAgainst):
    betRatios = []
    for i in range(len(betFor)):
        betRatios.append(betFor[i]/float(betFor[i]+betAgainst[i]))

    return np.mean(betRatios)

def GetWinRate(winLose):

    return np.mean(winLose)



"""
Log in information.
"""
with open('confidential.txt','r') as loginInfo:
    nickname = loginInfo.readline().replace('\n','')
    password = loginInfo.readline().replace('\n','')


HOST="irc.twitch.tv"
PORT=6667
NICK=nickname
IDENT=nickname
REALNAME=nickname
CHANNEL="#saltybet"
PASSWORD=password #From http://twitchapps.com/tmi/


s=socket.socket( )
s.connect((HOST, PORT))
s.send(bytes(("PASS oauth:%s\r\n" % PASSWORD)))
s.send(bytes(("NICK %s\r\n" % NICK)))
s.send(bytes(("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))))
s.send(bytes(("JOIN %s\r\n" % CHANNEL)))

midfight = True
newMatch = True
fighter1 = None
fighter2 = None
fight = None


print ("Welcome to Greg's Saltybet Tracker")
print (" ")

while 1:
    readBuffer=s.recv(1024).decode("UTF-8")
    
    if readBuffer.find ( 'PING' ) != -1:
        try:
            s.send ( bytes(('PONG ' + readBuffer.split() [ 1 ] + '\r\n'), "UTF-8"))
        except TypeError:
            s.send ( bytes('PONG ' + readBuffer.split() [ 1 ] + '\r\n'))

    #print (readBuffer)
       
    if readBuffer.find('Bets are OPEN for ') != -1 and readBuffer.find('Team ') == -1:
        midfight = False
        newMatch = True
        try:
            players = split_data(readBuffer)
            name1, name2 = FindNames(players)
            
            #Find the fighter by name, if none found make one and add it.
            if Fighter.query.filter(Fighter.name == name1).count()>0:
                fighter1 = Fighter.query.filter(Fighter.name == name1).first()
            else:
                fighter1 = Fighter(name1)
                db_session.add(fighter1)
            
            if Fighter.query.filter(Fighter.name == name2).count()>0:
                fighter2 = Fighter.query.filter(Fighter.name == name2).first()
            else:
                fighter2 = Fighter(name2)
                db_session.add(fighter2)
            
            db_session.commit()
            fight = Fight(fighter1.id, fighter2.id)
            db_session.add(fight)
            db_session.commit()

        except(NameError):
            print ("Program started mid fight. The program will record the next fight.\n")
            
            
            
    if readBuffer.find('Bets are locked. ') != -1 and readBuffer.find('Team ') == -1 and midfight == False:
        
        fighter1String, fighter2String = split_data(readBuffer)
        bet1, bet2 = FindBets(fighter1String,fighter2String)
        fight.bet1 = bet1
        fight.bet2 = bet2
        db_session.add(fight)
        db_session.commit()

        print (fighter1String)
        print (fighter2String)       
       
    if readBuffer.find(' wins! Payouts to') != -1 and midfight == False and newMatch == True:
        winner= readBuffer[readBuffer.find('#saltybet :') + 11:readBuffer.find(' wins! Payouts to')]
        
        RecordFightToDB(fighter1,fighter2,fight,winner)
        newMatch = False
       






       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       