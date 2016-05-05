# -*- coding: utf-8 -*-
"""
Created on Tue May  3 09:54:53 2016

@author: Greg
"""

import socket
import os
from SaltyFunctions import split_data
from SaltyFunctions import FindNames
from SaltyFunctions import FindBets
from SaltyFunctions import RecordFightToDB




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
s.send(bytes(("PASS oauth:%s\r\n" % PASSWORD), "UTF-8"))
s.send(bytes(("NICK %s\r\n" % NICK), "UTF-8"))
s.send(bytes(("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME)), "UTF-8"))
s.send(bytes(("JOIN %s\r\n" % CHANNEL), "UTF-8"))

midfight = True
newMatch = True


print ("Welcome to Greg's Saltybet Tracker")
print (" ")

while 1:
    readBuffer=s.recv(1024).decode("UTF-8")
    if readBuffer.find ( 'PING' ) != -1:
       s.send ( bytes(('PONG ' + readBuffer.split() [ 1 ] + '\r\n'), "UTF-8"))
       
    #print (readBuffer)
       
    if readBuffer.find('Bets are OPEN for ') != -1 and readBuffer.find('Team ') == -1:
        midfight = False
        newMatch = True
        try:
            players = split_data(readBuffer)
            name1, name2 = FindNames(players)
            #fight = Fight(name1,name2)
            
            
        except(NameError):
            print ("Program started mid fight. The program will record the next fight.\n")
            
            
            
    if readBuffer.find('Bets are locked. ') != -1 and readBuffer.find('Team ') == -1 and midfight == False:
        
        fighter1String, fighter2String = split_data(readBuffer)
        bet1, bet2 = FindBets(fighter1String,fighter2String)
        
        print (fighter1String)
        print (fighter2String)       
       
    if readBuffer.find(' wins! Payouts to') != -1 and midfight == False and newMatch == True:
        winner= readBuffer[readBuffer.find('#saltybet :') + 11:readBuffer.find(' wins! Payouts to')]
        
        RecordFightToDB(name1,name2,bet1,bet2,winner)
        newMatch = False
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       