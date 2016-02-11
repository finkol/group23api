from database import db_session
from models.Model import User, Result
from sqlalchemy import func

from flask import request, jsonify


def register_user(user):
    db_session.add(user)
    db_session.flush()
    return user


def get_user_by_id(input_id):
    user = User.query.filter_by(id=input_id).first()
    number_of_drinks = db_session.query(func.max(Result.number_of_drinks)).filter(Result.user_id == user.id).scalar()
    if user is not None:
        return_user = user.get_object_with_results()
        return_user.update({'number_of_drinks': number_of_drinks})
        return jsonify(user=return_user)
    else:
        return jsonify(user=None)


def get_user_by_name(input_name):
    user = User.query.filter_by(name=input_name).first()
    number_of_drinks = db_session.query(func.max(Result.number_of_drinks)).filter(Result.user_id == user.id).scalar()
    if user is not None:
        return_user = user.get_object_with_results()
        return_user.update({'number_of_drinks': number_of_drinks})
        return jsonify(user=return_user)
    else:
        return jsonify(user=None)


def register_result(result):
    db_session.add(result)
    db_session.flush()
    return result


def get_result_by_id(input_id):
    result = Result.query.filter_by(id=input_id).first()
    if result is not None:
        return jsonify(result=result.get_object())
    else:
        return jsonify(result=None)


def get_result_by_user_name(input_name):
    user = User.query.filter_by(name=input_name).first()
    if user is not None:
        return jsonify(results=user.get_results())
    else:
        return jsonify(result=None)


def get_result_by_user_id(input_id):
    user = User.query.filter_by(id=input_id).first()
    if user is not None:
        return jsonify(results=user.get_results())
    else:
        return jsonify(result=None)


def get_result_by_sex(input_sex):
    user = User.query.filter_by(sex=input_sex).first()
    if user is not None:
        return jsonify(results=user.get_results())
    else:
        return jsonify(result=None)


def get_result_by_age(input_age):
    user = User.query.filter_by(age=input_age).first()
    if user is not None:
        return jsonify(results=user.get_results())
    else:
        return jsonify(result=None)