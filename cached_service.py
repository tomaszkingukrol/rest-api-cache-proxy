from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class About(Resource):
    def get(self, path):
        response_body = {
            'name': path,
        }
        response_code = 200
        response_tag = {'Cache-Control-TTL': 15}
        return response_body, response_code, response_tag


api.add_resource(About, '/<path>')

if __name__ == '__main__':
    app.run(host='127.0.0.100', port=5000, debug=True)