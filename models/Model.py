from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Numeric, Time
from sqlalchemy.orm import relationship, backref
from database import Base
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import func
import datetime


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    sex = Column(String(5), unique=False)
    age = Column(Integer, unique=False)

    results = relationship("Result")

    def __init__(self, name=None, sex=None, age=None):
        self.name = name
        self.sex = sex
        self.age = age

    def __repr__(self):
        return '<User ' + str(self.id) + ' %r>' % self.name

    def get_object(self):
        return {'id': self.id, 'name': self.name, 'sex': self.sex, 'age': self.age}

    def get_object_with_results(self):
        results_templist = []
        for i in self.results:
            results_templist.append(i.get_object())
        user_object = self.get_object()
        user_object.update({'results': results_templist})
        return user_object

    def get_results(self):
        results_templist = []
        for i in self.results:
            results_templist.append(i.get_object())
        return results_templist


class Result(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), unique=False)
    reaction_time = Column(Numeric(asdecimal=False), unique=False)
    distance_from_centre = Column(Numeric(asdecimal=False), unique=False)
    number_of_drinks = Column(Integer, unique=False)
    timestamp = Column(DateTime(timezone=False), unique=False, default=datetime.datetime.now)

    user = relationship('User', foreign_keys='Result.user_id')

    def __init__(self, user_id=None, reaction_time=None, distance_from_centre=None, number_of_drinks=None):
        self.user_id = user_id
        self.reaction_time = reaction_time
        self.distance_from_centre = distance_from_centre
        self.number_of_drinks = number_of_drinks

    def __repr__(self):
        return '<Result ' + str(self.id) + ' %r>' % self.user_id

    def get_object(self):
        return {'id': self.id, 'user_id': self.user_id, 'reaction_time': self.reaction_time,
                'distance_from_centre': self.distance_from_centre, 'number_of_drinks': self.number_of_drinks}

    def get_object_with_user(self):
        result_object = self.get_object()
        result_object.update({'user': self.user.get_object()})
        return result_object


