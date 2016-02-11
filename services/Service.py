from database import db_session
from models.Model import User, Result

from flask import request, jsonify


def register_user(user):
    db_session.add(user)
    db_session.flush()
    return user


def get_user(input_id):
    user = User.query.filter_by(id=input_id).first()
    return jsonify(user=user.get_object())

