# -*- coding: utf-8 -*-
"""
Created on Tue May  3 14:48:51 2016

@author: Greg
"""
import socket
from SaltyFunctions import FindNames
from SaltyFunctions import split_data, FightStats


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

try:
    s.send(bytes(("PASS oauth:%s\r\n" % PASSWORD)))
    s.send(bytes(("NICK %s\r\n" % NICK)))
    s.send(bytes(("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))))
    s.send(bytes(("JOIN %s\r\n" % CHANNEL)))
except TypeError as e:
    s.send(bytes(("PASS oauth:%s\r\n" % PASSWORD), 'utf8'))
    s.send(bytes(("NICK %s\r\n" % NICK), 'utf8'))
    s.send(bytes(("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME)), 'utf8'))
    s.send(bytes(("JOIN %s\r\n" % CHANNEL), 'utf8'))

midfight = True



while 1:
    try:
        
        readBuffer=s.recv(1024).decode("UTF-8")
        if readBuffer.find ( 'PING' ) != -1:
            try:
                s.send ( bytes(('PONG ' + readBuffer.split() [ 1 ] + '\r\n'), "UTF-8"))
            except:
                s.send ( bytes(('PONG ' + readBuffer.split() [ 1 ] + '\r\n')))
    
        if readBuffer.find('Bets are OPEN for ') != -1 and readBuffer.find('Team ') == -1:
            midfight = False
            try:
                players = split_data(readBuffer)
                name1, name2 = FindNames(players)
            except(NameError):
                print ("Program started mid fight. The program will record the next fight.\n")
            
                     
            
            FightStats.SetFightStats(name1, name2)
            FightStats.PrintFighterStats()
            
            
    except Exception as e:
        print (e)