from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import timedelta
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import jwt
from flask_restx import Api, Resource, fields

from utils.weaviate_op import search_do
from utils.call_ai import call_aied
import utils.config_log as config_log

config, logger, CONFIG_PATH = config_log.setup_config_and_logging()
config.read(CONFIG_PATH)

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type, Qs-PageCode, Cache-Control'

api = Api(app, version='1.0', title='AllPass API',
          description='AllPass API',
          )

ns = api.namespace('api', description='Chatbot operations')

JWT_SECRET_KEY = config.get("JWT", 'Secret')
JWT_ISSUER = config.get("JWT", 'Issuer')
JWT_AUDIENCE = config.get("JWT", 'Audience')

limiter = Limiter(
    get_remote_address,
    app=app
)

model = api.model('ChatRequest', {
    'mess': fields.String(required=True, description='The message to the chatbot')
})

@ns.route("/")
class HealthCheck(Resource):
    @api.doc('health_check')
    def get(self):
        """Server health check."""
        return "server is ready"

@ns.route("/chat")
class ChatBot(Resource):
    @api.doc('chat_bot')
    @api.expect(model)
    @limiter.limit("15 per minute")
    def post(self):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Missing or invalid Authorization header"}), 401

        token = auth_header.split(" ")[1]
        try:
            decoded_token = jwt.decode(
                token,
                JWT_SECRET_KEY,
                algorithms=["HS256"],
                issuer=JWT_ISSUER,
                audience=JWT_AUDIENCE
            )
            email = decoded_token.get("Email")
            user_id = decoded_token.get("UserId")
            role = decoded_token.get("Role")
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({"message": f"Invalid token: {e}"}), 401

        question = request.json.get("mess")
        alpha = 0.5

        if not question:
            response = "無問題"
            response_li = "無檢索"
        else:
            try:
                response_li = search_do(question, alp=alpha)
                response = call_aied(response_li, question)
            except Exception as e:
                print(f"get error: {e}")
                response = f"Error: {e}"

        return jsonify({"llm": response, "retriv": response_li})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, threaded=True)
