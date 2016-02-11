import os
from flask import Flask, jsonify, g, request
from flask_restful import Api, Resource
from database import init_db

from services.parsers.Parser import parse_user, parse_result
from services.Service import register_user, get_user_by_id, get_user_by_name, get_result_by_id, register_result

app = Flask(__name__)
app.config['SECRET_KEY'] = 'twoPointtwoLeyndo'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

api = Api(app)
init_db()


class UserApi(Resource):
    def get(self):
        if 'id' in request.args:
            print "bla2"
            id = request.args['id']
            print "id: " + str(id)
            return get_user_by_id(id)

        elif 'name' in request.args:
            print "bla"
            name = request.args['name']
            print "name: " + str(name)
            return get_user_by_name(name)

    def post(self):
        user = parse_user()
        print user.name
        user = register_user(user)
        return get_user_by_id(user.id)


api.add_resource(UserApi,
                 '/api/user')


class ResultApi(Resource):
    def get(self):
        if 'id' in request.args:
            id = request.args['id']
            print "id: " + str(id)
            return get_result_by_id(id)

        elif 'name' in request.args:
            print "bla"
            name = request.args['name']
            print "name: " + str(name)
            return get_user_by_name(name)

    def post(self):
        result = parse_result()
        result = register_user(result)
        return get_result_by_id(result.id)


api.add_resource(ResultApi,
                 '/api/result')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 2500))
    app.run(host='0.0.0.0', port=port, debug=True)