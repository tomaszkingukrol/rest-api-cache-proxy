from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class About(Resource):
    def get(self, path):
        response_body = {
            'type': 'GET',
            'name': path,
            'query': request.args
        }
        response_code = 200
        response_tag = {'Cache-Control-TTL': 15}
        return response_body, response_code, response_tag

    def post(self, path):
        response_body = {
            'type': 'POST',
            'name': path,
            'query': request.args
        }
        response_code = 200
        response_tag = {'Cache-Control-TTL': 15}
        return response_body, response_code, response_tag


api.add_resource(About, '/<path:path>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


