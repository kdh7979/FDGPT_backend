from flask import Flask, json, request, g, render_template

from src.middleware.cors import cors
from src.database.database import init_db
from config import config

from src.database.controller import create_chat, create_chat_room

from flask_socketio import SocketIO, join_room, emit


def init_app():
    app = Flask(__name__)
    socketio = SocketIO(app)
    app.config["SECRET_KEY"] = config.SECRET_KEY

    # app에 뭔가 더 추가하고 싶은게 있으면 여기에 추가
    cors.init_app(app)

    return app, socketio

app, socketio = init_app()
engine, get_db = init_db()

@socketio.on('message')
def handle_message(data):
    print('Received message:', data)
    emit('message', data)



# 연결이 끊어질때 db close
@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chatting():
    return render_template('chat.html')

@app.route('/status')
def status():
    return json.jsonify({'status': 'ok'})

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=13242)