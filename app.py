from flask import Flask, json, request, g, render_template, redirect, url_for

from src.middleware.cors import cors
from src.database.database import init_db
from config import config

from src.database.controller import create_chat, create_chat_room

from flask_socketio import SocketIO, join_room, emit

import uuid


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
    create_chat(get_db(), chat=data['message'], room_id=data['room_id'])
    emit('message', data, to=data['room_id'])

@socketio.on('join')
def handle_join(data):
    room_id = str(uuid.uuid4())
    print("received data to join:", data, room_id)
    print(f"SID: {request.sid} is trying to join room {room_id}")
    join_room(room_id)
    create_chat_room(get_db(), room_id=room_id, room_name=data['roomName'])
    return redirect(url_for("chatting", room_id=room_id))



# 연결이 끊어질때 db close
@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat/<room_id>')
def chatting(room_id):
    return render_template('chat.html', room_id=room_id)

@app.route('/status')
def status():
    return json.jsonify({'status': 'ok'})

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=13242)