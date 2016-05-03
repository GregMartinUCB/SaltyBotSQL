# -*- coding: utf-8 -*-
"""
Created on Tue May  3 09:02:37 2016

@author: Greg
"""

import sqlite3

conn = sqlite3.connect('Fighters.db')

c = conn.cursor()

c.execute('''CREATE TABLE fights 
            (Name1 text, Name2 text, Bet1 REAL, Bet2 REAL, Winner TEXT)''')

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()                    

