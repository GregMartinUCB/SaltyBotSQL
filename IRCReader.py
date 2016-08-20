# -*- coding: utf-8 -*-
"""
Created on Tue May  3 09:54:53 2016

@author: Greg
"""

import socket
import os
from SaltyFunctions import split_data, FindNames, GetAverageBetRatio, GetFighterStats
from SaltyFunctions import FindBets, GetWinRate, RecordFightToDB, CommitStreakData
from models import Fight, Fighter
from database import db_session




"""
Log in information. Stored in confidential.txt which is ignored by git
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
        #This try and except is neccessary for switching between python 2.7 and 3
        #Python 3 needs the second arguement for bytes function
        try:
            s.send ( bytes(('PONG ' + readBuffer.split() [ 1 ] + '\r\n'), "UTF-8"))
        except TypeError:
            s.send ( bytes('PONG ' + readBuffer.split() [ 1 ] + '\r\n'))

    #print (readBuffer)
      
    #Filter out team matches. Unable to determine individual fighters from teams
    if readBuffer.find('Bets are OPEN for ') != -1 and readBuffer.find('Team ') == -1:
        midfight = False
        newMatch = True
        try:
            #Split the string and find the fighter's names
            players = split_data(readBuffer)
            name1, name2 = FindNames(players)
            
            #Find the fighter by name, if none found make one and add it.
            #This query assumes that a fighters name is Unique. This is unverified but highly likely
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
            fight = Fight(fighter1, fighter2)
            db_session.add(fight)
            db_session.commit()

        except(Exception):
            print Exception.message
            print ("Program started mid fight. The program will record the next fight.\n")
            
            
            
    if readBuffer.find('Bets are locked. ') != -1 and readBuffer.find('Team ') == -1 and midfight == False:
        
        #Find bet info from string
        fighter1String, fighter2String = split_data(readBuffer)
        bet1, bet2 = FindBets(fighter1String,fighter2String)
        fight.bet1 = bet1
        fight.bet2 = bet2

        #Add fight to database then commit the streaks
        db_session.add(fight)
        CommitStreakData(fight, fighter1String, fighter2String)
        db_session.commit()

        print (fighter1String)
        print (fighter2String)
               
    if readBuffer.find(' wins! Payouts to') != -1 and midfight == False and newMatch == True:
        winner= readBuffer[readBuffer.find('#saltybet :') + 11:readBuffer.find(' wins! Payouts to')]
        
        print winner + ' Won!'

        RecordFightToDB(fighter1,fighter2,fight,winner)
        newMatch = False
       






       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       