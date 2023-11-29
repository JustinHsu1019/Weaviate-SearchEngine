from flask import Flask, request
from flask_cors import CORS

from get_TopN import search_do
from call_ai import call_aied

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type, Qs-PageCode, Cache-Control'

@app.route("/")
def index():
    """Server 是否正常的確認頁面.
    """
    return "server is ready v1.1.0"

@app.route("/chat", methods=['POST', 'GET'])
def chat_bot():
    if request.method == 'POST':
        question = request.values.get("mess")

        if not question:
            response = "無問題 (無內容)"
        else:
            try:
                response = search_do(question)
                # response = call_aied(response_li, question)
            except Exception as e:
                print(f"get error: {e}")
                response = f"Error: {e}"

        return returnMsg(response)

    else:
        return "無問題 (GET)"

def returnMsg(response):
    print(response)
    return response

if __name__ == "__main__":
    app.run(threaded=True)
