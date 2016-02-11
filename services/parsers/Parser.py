from flask import request

from models.Model import User, Result


def parse_user():
    user = User()
    user.name = request.json.get('name')
    user.age = request.json.get('age')
    user.sex = request.json.get('sex')

    return user


def parse_result():
    result = Result()
    result.user_id = request.json.get('user_id')
    result.number_of_drinks = request.json.get('number_of_drinks')
    result.reaction_time = request.json.get('reaction_time')
    result.distance_from_centre = request.json.get('distance_from_centre')

    return result
