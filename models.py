﻿from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime
from database import Base
from sqlalchemy.orm import relationship

class Fighter(Base):
    __tablename__ = 'fighter'
    id = Column(Integer, primary_key = True)
    name = Column(String(75), unique = True)
    winRate = Column(Float())
    betRatio = Column(Float())

    fights = relationship("Fight", backref="fighter")

    def __init__(self, name = None):
        self.name = name

class Fight(Base):
    __tablename__ = 'fight'
    id = Column(Integer, primary_key=True)
    currentFight = Column(Boolean())
    time = Column(DateTime())
    fighter1_id = Column(Integer, ForeignKey('fighter.id'))
    fighter2_id = Column(Integer, ForeignKey('fighter.id'))
    

    bet1 = Column(Integer())
    bet2 = Column(Integer())
    winner_id = Column(Integer, ForeignKey('fighter.id'))

    def __init__(self, fighter1=None, fighter2=None):
        self.fighter1 = fighter1
        self.fighter2 = fighter2
        self.currentFight = True

    def __repr__(self):
        return '<User %r>' % (self.name)

