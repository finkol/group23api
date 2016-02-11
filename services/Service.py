from database import db_session
from models.Model import User, Result

from flask import request, jsonify


def register_user(user):
    db_session.add(user)
    db_session.flush()
    return user


def get_user_by_id(input_id):
    user = User.query.filter_by(id=input_id).first()
    if user is not None:
        return jsonify(user=user.get_object())
    else:
        return jsonify(user=None)


def get_user_by_name(input_name):
    user = User.query.filter_by(name=input_name).first()
    if user is not None:
        return jsonify(user=user.get_object())
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