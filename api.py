from flask import Flask, jsonify, g, request
from flask_restful import Api, Resource
from database import init_db

from services.parsers.Parser import parse_user, parse_result
from services.Service import register_user, get_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'twoPointtwoLeyndo'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

api = Api(app)
init_db()


class UserApi(Resource):
    def get(self):
        id = request.args['id']
        print "id: " + str(id)
        return get_workout_line_bundle(id)

    def post(self):
        user = parse_user()
        user = register_user(user)
        return get_user(user.id)


api.add_resource(UserApi,
                 '/api/user')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)