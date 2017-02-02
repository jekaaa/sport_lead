from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
    Boolean,
    Float,
    )
from sqlalchemy.orm import (
    relationship
)


from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    #name = Column(Text)
    login = Column(Text)
    password = Column(Text)
    #photo = Column(BLOB)
    #city = Column(Text)
    #age = Column(Integer)

class Participant(Base):
    __tablename__ = 'participant'
    eventId = Column(Integer, ForeignKey('event.id'))
    id = Column(Integer, primary_key=True)
    first_name = Column(Text)
    middle_name = Column(Text)
    last_name = Column(Text)
    age = Column(Integer)
    sex = Column(Boolean)
    weight = Column(Float)
    team = Column(Text)

    event = relationship("Event", backref="participants")

class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    weight = Column(Text)
    numberTable = Column(Integer)
    name = Column(Text)
    city = Column(Text)
    date = Column(Text)
    dateEnd = Column(Text)
    groupNumber = Column(Integer)
    description = Column(Text)
    building = Column(Text)
    address = Column(Text)
    scoreWin = Column(Integer)
    scoreDraw = Column(Integer)
    scoreLose = Column(Integer)
    kindId = Column(Integer,ForeignKey('kind.id'))
    typeId = Column(Integer,ForeignKey('type.id'))
    userId = Column(Integer,ForeignKey('user.id'))

    kind = relationship("KindOfSport",backref = "events")
    type = relationship("TypeTournament",backref = "events")
    user = relationship("User",backref = "events")


class KindOfSport(Base):
    __tablename__ = 'kind'
    id = Column(Integer, primary_key=True)
    name = Column(Text)

class TypeTournament(Base):
    __tablename__ = 'type'
    id = Column(Integer, primary_key=True)
    name = Column(Text)

class Game(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    #name = Column(Text)
    eventId = Column(Integer,ForeignKey('event.id'))
    date = Column(Text)
    playerOne = Column(Text)
    playerTwo = Column(Text)
    playerOneScore = Column(Integer)
    playerTwoScore = Column(Integer)

    event = relationship("Event",backref = "games")
    #def __json__(self,request):
    #    return {'foo':1}

class PlayOff(Base):
    __tablename__ = 'play-off'
    id = Column(Integer, primary_key=True)
    #name = Column(Text)
    eventId = Column(Integer,ForeignKey('event.id'))
    date = Column(Text)
    playerOne = Column(Text)
    playerTwo = Column(Text)
    playerOneScore = Column(Integer)
    playerTwoScore = Column(Integer)
    stage = Column(Integer)

    event = relationship("Event",backref = "play-offs")
#class Set(Base):
#    __tablename__ = 'set'
#    id = Column(Integer, primary_key=True)
#    gameId = Column(Integer,ForeignKey('game.id'))
#    pointPlayerOne = Column(Integer)
#    pointPlayerTwo = Column(Integer)

#    game = relationship("Game",backref = "sets")

class Table(Base):
    __tablename__ = 'table'
    id = Column(Integer, primary_key=True)
    eventId =  Column(Integer,ForeignKey('event.id'))
    position = Column(Integer)
    name = Column(Text)
    games = Column(Integer)
    wins = Column(Integer)
    draws = Column(Integer)
    lose = Column(Integer)
    goalsScored = Column(Integer)
    goalsAgainst = Column(Integer)
    score = Column(Integer)

    event = relationship("Event",backref = "tables")

class GroupTable(Base):
    __tablename__ = 'grouptable'
    id = Column(Integer, primary_key=True)
    eventId = Column(Integer, ForeignKey('event.id'))
    position = Column(Integer)
    name = Column(Text)
    games = Column(Integer)
    wins = Column(Integer)
    draws = Column(Integer)
    lose = Column(Integer)
    goalsScored = Column(Integer)
    goalsAgainst = Column(Integer)
    score = Column(Integer)
    nameGroup = Column(Text)

    event = relationship("Event", backref="grouptables")

class RaceTable(Base):
    __tablename__ = "race"
    id = Column(Integer, primary_key=True)
    eventId = Column(Integer, ForeignKey('event.id'))
    position = Column(Integer)
    name = Column(Text)
    score = Column(Text)

    event = relationship("Event", backref="racetables")

class Favorites(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True)
    userId = Column(Integer,ForeignKey('user.id'))
    eventId = Column(Integer, ForeignKey('event.id'))

    user = relationship("User",backref="favorites")
    event = relationship("Event",backref="favorites")