# -*- coding: utf-8 -*-
"""
Created on Tue May  3 14:48:51 2016

@author: Greg
"""
import socket
from SaltyFunctions import FindNames
from SaltyFunctions import split_data
from SaltyFunctions import GetFighterStats


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

while 1:

    readBuffer=s.recv(1024).decode("UTF-8")
    if readBuffer.find ( 'PING' ) != -1:
        s.send ( bytes(('PONG ' + readBuffer.split() [ 1 ] + '\r\n'), "UTF-8"))


    if readBuffer.find('Bets are OPEN for ') != -1 and readBuffer.find('Team ') == -1:
        midfight = False
        try:
            players = split_data(readBuffer)
            name1, name2 = FindNames(players)
        except(NameError):
            print ("Program started mid fight. The program will record the next fight.\n")
        
        fighter1Stats = GetFighterStats("A-unagi")
        
        """
        Determines the average betting ratio if there are recorded entries for that fighter
        """
        if len(fighter1Stats) != 0:
            betRatios = [x[0]/(x[0]+x[1]) for x in fighter1Stats]
        
            averageBetRatio = 0
            for ratio in betRatios:
                averageBetRatio += ratio 
            averageBetRatio =averageBetRatio /len(betRatios)
        