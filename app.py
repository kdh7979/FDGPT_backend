from flask import Flask, json, request, g, render_template, redirect, url_for, flash

from src.middleware.cors import cors
from src.database.database import init_db
from config import config

from src.database.controller import create_chat, create_chat_room, get_room, get_chat

from flask_socketio import SocketIO, join_room, leave_room, emit

import uuid

def init_app():
    app = Flask(__name__)
    socketio = SocketIO(logger=True, engineio_logger=True, cors_allowed_origins="*")
    socketio.init_app(app)
    app.config["SECRET_KEY"] = config.SECRET_KEY

    cors.init_app(app)

    return app, socketio

app, socketio = init_app()
engine, get_db = init_db()

@socketio.on('message')
def handle_message(data):
    data = eval(data)
    create_chat(get_db(), writer=data['user'], chat=data['message'], room_id=data['roomId'])
    emit('message', data, broadcast=True, to=data['roomId'])

@socketio.on('createRoom')
def handle_createRoom(data):
    data = eval(data)   # eval(): string to dictionary
    room_id = str(uuid.uuid4())
    join_room(room_id)
    create_chat_room(get_db(), room_id=room_id, room_name=data['roomName'])
    emit('createdRoom', {'roomName' : data['roomName'], 'roomId' : room_id, 'user' : data['user']})

@socketio.on('join')
def handle_join(data):
    # notice : join할 때 chat 데이터를 로드하는게 아닌, chat/room_id 엔드포인트 접속 시 laod
    data = eval(data)
    room_id = data['roomId']
    if get_room(get_db(), room_id) != "NO_ROOM":    # ChatRoom이 db에 있을 시 실행
        join_room(room_id)
        emit('userJoined', {'room_id' : room_id, 'user' : data['user']}, broadcast=True, to=room_id)
    else:
        emit('userFailedJoin')
        return redirect(url_for('index'))

@socketio.on('leave')
def handle_leave(data):
    data = eval(data)
    room_id = data['roomId']
    leave_room(room_id)
    emit('userLeft', {'room_id' : room_id, 'user' : data['user']}, broadcast=True, to=room_id)  # 나간 당사자는 event를 받을 수 없음 (이미 나온 room에 보내기 때문)
    return redirect(url_for('index'))

@socketio.on('test')
def test(data):
    data = eval(data)
    chats = get_chat(get_db(), room_id=data['roomId'])
    emit('chats', {'chats' : str(chats)})

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
    room_id = get_room(get_db(), room_id)
    if room_id == "NO_ROOM":
        # flash('존재하지 않는 채팅방입니다.', 'error')
        return redirect(url_for('index'))
    else:
        chats = get_chat(get_db(), room_id=room_id)
        emit('chats', {'chats' : chats})
        return render_template('chat.html', room_id=room_id)

@app.route('/status')
def status():
    return json.jsonify({'status': 'ok'})

if __name__ == "__main__":
    socketio.run(app, "0.0.0.0", port=8081, debug=True)