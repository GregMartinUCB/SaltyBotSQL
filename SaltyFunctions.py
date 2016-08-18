# -*- coding: utf-8 -*-
"""
Created on Tue May  3 10:35:28 2016

@author: Greg
"""
import sqlite3
from sqlalchemy import or_
import numpy as np
import datetime
from models import Fight, Fighter
from database import db_session


def RecordFightToDB(fighter1,fighter2,fight,Winner):
    
    #set current fight to false.
    fight.currentFight = False

    #Identify winner and save as foreign key
    if Winner == fighter1.name:
        fight.winner = fighter1
        fighter1.streak += 1
        fighter2.streak -= 1
    elif Winner == fighter2.name:
        fight.winner = fighter2
        fighter2.streak += 1
        fighter1.streak -= 1
    else:
        print ("Unable to match declared winner with a fighter.")
        return

    fight.time = datetime.datetime.now()
    #SQLAlchemey is similar to git, one must add then commit.
    #Unlike others once added the pk is created
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

#A Function to retrieve a fighters statistics
#Returns a Win rate between 0.0-1.0 and the average betting ratio, Also 0.0-1.0
def GetFighterStats(fighter):

    #This one statement took many iterations. Some Past Unsuccessful versions:
    #db_session.query(Fight).filter((Fight.fighter1_id == fighter.id) | (Fight.fighter1_id == fighter.id))
    history = db_session.query(Fight).filter(or_(Fight.fighter1_id == fighter.id, Fight.fighter2_id == fighter.id))

    betFor = []
    betAgainst = []
    winLose = []
    for pastFight in history:
        if pastFight.winner == fighter:
            winLose.append(1)
        else:
            winLose.append(0)

        #Matching the first or second bet as the for or against
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

#This function is so simple it probably isn't neccessary
def GetWinRate(winLose):
    return np.mean(winLose)


def TestRecordFightToDB():
    
    name1 = "test1"
    name2 = "test2"
    bet1 = 1
    bet2 = 2
    winner = "test1"
    
    RecordFightToDB(name1, name2, bet1, bet2, winner)

"""
This method extracts the important information from the irc stream
If the bets are opening then the information extracted will be the names
If the Bets are locked then the names and the amount bet will be extracted
"""

def split_data(data):
   
    if data.find('Bets are OPEN for ') != -1:
        name1_start = data.find('Bets are OPEN for ')+ 18
        data = data[name1_start:]
        
        name2_start = data.find(' vs ')+4       
        player1_data = data[0:name2_start - 4]
        player2_data = data[name2_start:data.find("! (")]   
    
    elif data.find('Bets are locked. '):
        name1_start = data.find('Bets are locked. ') + 17
        
        name2_start = data.find(", ") +2
            
        player1_data = data[name1_start:name2_start - 2]
        player2_data = data[name2_start:]
        
        if player2_data.find(":") != -1:
            player2_data = player2_data[:player2_data.find(":")]
    
    else:
        
        print ("Error, string to be split did not meet the requirments.")
    
    return [player1_data, player2_data] 
    


"""
A Method to print out a message with the match info
"""
def FindNames(players):
    if players[0].find('Team') == -1:
        name1 = players[0]
    if players[1].find('Team') == -1:
        name2 = players[1]
            
    if players[0].find('Team') != -1:
        print ("Player 1 is a team and will not be recorded.")
    if players[1].find('Team') != -1:
        print ("Player 2 is a team and will not be recorded.")
                
    print (players[0] + " vs " + players[1] + " Begin\n")
    
    try:
        return name1, name2
    except(UnboundLocalError):
        pass
    

def FindBets(player1Sentence, player2Sentence):
    bet1Start = player1Sentence.find('- $') + 3
    bet2Start = player2Sentence.find('- $') + 3
        
        
    bet1 = float(player1Sentence[bet1Start:].replace(',',''))
    bet2 = float(player2Sentence[bet2Start:].replace(',',''))
        
    return bet1, bet2

#Find and record the fighters' winning and or loosing streaks.
def FindStreak(player1String, player2String):

    start1 = player1String.find(' (')+2
    start2 = player2String.find(' (')+2

    end1 = player1String.find(') -')
    end2 = player2String.find(') -')

    try:
        streak1 = int(player1String[start1:end1])
        streak2 = int(player2String[start2:end2])
    except:
        print Exception.message
        print ''
        print player1String[start1:end1]
        print player1String[start1:end1]
        return

    return streak1, streak2

def CommitStreakData(fight, string1, string2):

    try:
        streak1, streak2 = FindStreak(string1, string2)
        fighter1 = db_session.query(Fighter).get(fight.fighter1_id)
        fighter2 = db_session.query(Fighter).get(fight.fighter2_id)

        fighter1.streak = streak1
        fighter2.streak = streak2

        db_session.add_all([fighter1,fighter2])
        db_session.commit()
    except(TypeError):
        print ("Error has occured when parsing the player string. " + 
                "Possibly no streak was presented. This happens in certain modes.")

    

    return

        