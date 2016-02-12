import os
from flask import Flask, jsonify, g, request
from flask_restful import Api, Resource
from database import init_db

from services.parsers.Parser import parse_user, parse_result
from services.Service import register_user, get_user_by_id, get_user_by_name, get_result_by_id, register_result, \
    get_result_by_user_name, get_result_by_user_id, get_result_by_age, get_result_by_sex, get_image_by_user_name, \
    get_image_by_age, get_image_by_sex

app = Flask(__name__)
app.config['SECRET_KEY'] = 'twoPointtwoLeyndo'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

api = Api(app)
init_db()


class UserApi(Resource):
    def get(self):
        if 'id' in request.args:
            id = request.args['id']
            return get_user_by_id(id)

        elif 'name' in request.args:
            name = request.args['name']
            return get_user_by_name(name)

    def post(self):
        user = parse_user()
        user = register_user(user)
        return get_user_by_id(user.id)


api.add_resource(UserApi,
                 '/api/user')


class ResultApi(Resource):
    def get(self):
        if 'id' in request.args:
            id = request.args['id']
            return get_result_by_id(id)

        return None

    def post(self):
        result = parse_result()
        result = register_result(result)
        return get_result_by_id(result.id)


api.add_resource(ResultApi,
                 '/api/result')


class HistoryApi(Resource):
    def get(self):
        if 'user_id' in request.args:
            id = request.args['user_id']
            return get_result_by_user_id(id)
        elif 'sex' in request.args:
            sex = request.args['sex']
            return get_result_by_sex(sex)
        elif 'age' in request.args:
            age = request.args['age']
            return get_result_by_age(age)
        elif 'user_name' in request.args:
            user_name = request.args['user_name']
            return get_result_by_user_name(user_name)
        return None

api.add_resource(HistoryApi,
                 '/api/history')


class ImageApi(Resource):
    def get(self):
        if 'sex' in request.args:
            sex = request.args['sex']
            return get_image_by_sex(sex)
        elif 'age' in request.args:
            age = request.args['age']
            return get_image_by_age(age)
        elif 'user_name' in request.args:
            user_name = request.args['user_name']
            return get_image_by_user_name(user_name)
        return None

api.add_resource(ImageApi,
                 '/api/image')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 2500))
    app.run(host='0.0.0.0', port=port, debug=True)