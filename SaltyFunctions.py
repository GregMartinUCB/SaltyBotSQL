# -*- coding: utf-8 -*-
"""
Created on Tue May  3 10:35:28 2016

@author: Greg
"""
import sqlite3

class FightStats:
    fighter1 = {'name':None,
                'fightHistory': None,
                'averageWinRatio':None,
                'averageBetRatio':None}
    fighter2 = fighter1

    @staticmethod
    def GetFighterStats(name):
    
        conn = sqlite3.connect('Fighters.db')
    
        c = conn.cursor()
        
        try:
            c.execute("""SELECT CASE 
                WHEN name1 = ? then Bet1
                WHEN name2 = ? THEN Bet2
            END
            "BetFor",
            CASE 
                WHEN name1 = ? then Bet2
                WHEN name2 = ? THEN Bet1
            END
            "BetAgainst",
            CASE
                WHEN winner = ? THEN "Won"
                ELSE "Lost"
            END
            "Result"
            FROM fights WHERE name1 = ? OR name2 =?""", (name,name,name,name,name,name,name))
            
            fighterStats = c.fetchall()
        except():
            print ("No Records of this fighter!")
        if fighterStats == []:
            print ("No Records of this fighter!")
        else:
            print (fighterStats)
            
        
        conn.close()
        return fighterStats    

    """
    Determines the average betting ratio if there are recorded entries for that fighter
    """
    @staticmethod
    def GetAverageRatio(fighterStats):
        
        if len(fighterStats) != 0:
            betRatios = [x[0]/(x[0]+x[1]) for x in fighterStats]
        
            averageBetRatio = 0
            for ratio in betRatios:
                averageBetRatio += ratio 
            averageBetRatio =averageBetRatio /len(betRatios)
            
            return averageBetRatio
        else:
            return 0
            
    """
    Count adds up all the wins. the count is then divided by the length of the fights list.
    """
    @staticmethod
    def GetWinRatio(fighterStats):
        count = 0
        if len(fighterStats) != 0:
            for fight in fighterStats:
                if fight[2] == 'Won':
                    count+=1
        
            return count/len(fighterStats)
        else:
            return 0
    


    
    """
    Returns a list of Tuples. Tuple entries are (Bet For, Bet Against, Win/lose)
    The index of the list is fight number
    """
    
    
    @staticmethod
    def SetFightStats(name1,name2):

        fighter1 = FightStats.GetFighterStats(name1)
        fighter2 = FightStats.GetFighterStats(name2)
        
        FightStats.fighter1['name'] = name1
        FightStats.fighter1['fightHistory'] = fighter1
        FightStats.fighter1['averageWinRatio'] = FightStats.GetAverageRatio(fighter1)
        FightStats.fighter1['averageBetRatio'] = FightStats.GetWinRatio(fighter1)
        
        FightStats.fighter2['name'] = name2
        FightStats.fighter2['fightHistory'] = fighter2
        FightStats.fighter2['averageWinRatio'] = FightStats.GetAverageRatio(fighter2)
        FightStats.fighter2['averageBetRatio'] = FightStats.GetWinRatio(fighter2)

    @staticmethod
    def PrintFighterStats():
        
        if FightStats.fighter1['fightHistory'] != []:
            print (FightStats.fighter1['name'] + "'s Stats:")
            print ("Number of fights recorded: "+ str(len(FightStats.fighter1['fightHistory'])))
            print ("Win Ratio: "+ str(FightStats.fighter1['averageWinRatio']))
            print ("Betting Ratio: "+ str(FightStats.fighter1['averageBetRatio']))
            print ("")
        if FightStats.fighter2['fightHistory'] != []:
            print (FightStats.fighter2['name'] + "'s Stats:")
            print ("Number of fights recorded: "+ str(len(FightStats.fighter2['fightHistory'])))
            print ("Win Ratio: "+ str(FightStats.fighter2['averageWinRatio']))
            print ("Betting Ratio: "+ str(FightStats.fighter2['averageBetRatio']))
            print ("")
            
    @staticmethod
    def TestPrintFighterStats():
        FightStats.PrintFighterStats("Wonder woman revolutions")
        FightStats.PrintFighterStats("Ssj goku z2 ex")
    
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
