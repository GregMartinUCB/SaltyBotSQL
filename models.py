from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime, Table
from database import Base
from sqlalchemy.orm import relationship




class Fighter(Base):
    __tablename__ = 'Fighter'
    id = Column(Integer, primary_key = True)
    name = Column(String(75), unique = True)
    winRate = Column(Float())
    betRatio = Column(Float())
    streak = Column(Integer())



    def __init__(self, name = None):
        self.name = name

class Fight(Base):
    __tablename__ = 'Fight'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime())
    bet1 = Column(Integer())
    bet2 = Column(Integer())

    winner_id = Column(Integer, ForeignKey('Fighter.id'))
    fighter1_id = Column(Integer, ForeignKey('Fighter.id'))
    fighter2_id = Column(Integer, ForeignKey('Fighter.id'))
    fighter1 = relationship("Fighter", foreign_keys = [fighter1_id])
    fighter2 = relationship("Fighter", foreign_keys = [fighter2_id])
    winner = relationship("Fighter",foreign_keys = [winner_id])

    def __init__(self, fighter1=None, fighter2=None):
        self.fighter1 = fighter1
        self.fighter2 = fighter2
        self.currentFight = True

    def __repr__(self):
        return '<User %r>' % (self.name)

