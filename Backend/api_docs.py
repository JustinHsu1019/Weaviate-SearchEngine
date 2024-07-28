from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import timedelta
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from flask_restx import Api, Resource, fields
import traceback
from jwt.algorithms import HMACAlgorithm

from utils.weaviate_op import search_do
from utils.call_ai import call_aied
import utils.config_log as config_log

config, logger, CONFIG_PATH = config_log.setup_config_and_logging()
config.read(CONFIG_PATH)

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type, Qs-PageCode, Cache-Control'

JWT_SECRET_KEY = config.get("JWT", 'Secret')
custom_algorithms = {
    "http://www.w3.org/2001/04/xmldsig-more#hmac-sha256": HMACAlgorithm(HMACAlgorithm.SHA256)
}
jwt.register_algorithm("http://www.w3.org/2001/04/xmldsig-more#hmac-sha256", HMACAlgorithm(HMACAlgorithm.SHA256))

limiter = Limiter(
    get_remote_address,
    app=app
)

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'JWT 認證, 請輸入 token (前端串接請記得加上 Bearer)'
    }
}

api = Api(app, version='1.0', title='Swagger UI',
          description='Swagger UI',
          authorizations=authorizations,
          security='Bearer Auth'
          )

ns = api.namespace('api', description='Chatbot operations')

model = api.model('ChatRequest', {
    'message': fields.String(required=True, description='The message to the chatbot')
})

@ns.route("/")
class HealthCheck(Resource):
    @api.doc('health_check')
    def get(self):
        """Server health check."""
        response = jsonify("server is ready")
        response.status_code = 200
        return response

@ns.route("/chat")
class ChatBot(Resource):
    @api.doc('chat_bot')
    @api.expect(model)
    @api.header('Authorization', 'Bearer {JWT Token}', required=True)
    @limiter.limit("15 per minute")
    def post(self):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                response = jsonify({"message": "Missing Authorization header"})
                response.status_code = 401
                return response
        except:
            response = jsonify({"message": "Missing Authorization header"})
            response.status_code = 401
            return response

        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        else:
            token = auth_header

        try:
            if token == "":
                response = jsonify({"message": "Missing token"})
                response.status_code = 401
                return response
        except:
            response = jsonify({"message": "Missing token"})
            response.status_code = 401
            return response

        try:
            decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms=["http://www.w3.org/2001/04/xmldsig-more#hmac-sha256"], audience="front-end-url")
            email = decoded.get("Email")
            user_id = decoded.get("UserId")
            role = decoded.get("Role")
            print(email)
            print(user_id)
            print(role)
        except jwt.InvalidAlgorithmError as e:
            response = jsonify({"message": "Invalid algorithm error"})
            response.status_code = 401
            return response
        except jwt.ExpiredSignatureError as e:
            response = jsonify({"message": "Token expired"})
            response.status_code = 401
            return response
        except jwt.InvalidAudienceError as e:
            response = jsonify({"message": "Invalid audience error"})
            response.status_code = 401
            return response
        except Exception as e:
            response = jsonify({"message": "Invalid token"})
            response.status_code = 401
            return response

        question = request.json.get("message")
        alpha = 0.5

        if not question:
            response = jsonify({"llm": "無問題", "retriv": "無檢索"})
            response.status_code = 200
            return response
        else:
            try:
                response_li = search_do(question, alp=alpha)
                response = call_aied(response_li, question)

                if not isinstance(response, str):
                    response = str(response)
                if not isinstance(response_li, str):
                    response_li = str(response_li)

            except Exception as e:
                response = jsonify({"message": "Internal Server Error"})
                response.status_code = 500
                return response

        try:
            response = jsonify({"llm": response, "retriv": response_li})
            response.status_code = 200
            return response
        except TypeError as e:
            response = jsonify({"message": "Internal Server Error"})
            response.status_code = 500
            return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
