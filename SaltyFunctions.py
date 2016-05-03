# -*- coding: utf-8 -*-
"""
Created on Tue May  3 10:35:28 2016

@author: Greg
"""
import sqlite3

def RecordFightToDB(name1,name2,bet1,bet2,Winner):
    
    conn = sqlite3.connect('Fighters.db')

    c = conn.cursor()
    
    rowValues = (name1,name2,bet1,bet2,Winner)
    
    c.execute("INSERT INTO fights VALUES (?,?,?,?,?)", rowValues)
    
    conn.commit()
    conn.close()


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
