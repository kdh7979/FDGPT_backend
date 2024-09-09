from flask import Flask, json, request, g, render_template, redirect, url_for, flash

from src.middleware.cors import cors
from src.database.database import init_db
from config import config

from src.database.controller import create_chat, create_chat_room, get_room, get_chat

from flask_socketio import SocketIO, join_room, leave_room, emit

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
    emit('message', data, broadcast=True, to=data['room_id'])

@socketio.on('createRoom')
def handle_createRoom(data):
    room_id = str(uuid.uuid4())
    join_room(room_id)
    create_chat_room(get_db(), room_id=room_id, room_name=data['roomName'])
    print(f'room created: {room_id}')
    emit('createdRoom', {'roomId' : room_id})

@socketio.on('join')
def handle_join(data):
    room_id = data['roomId']
    if get_room(get_db(), room_id) != False:
        join_room(room_id)
        emit('userJoined', {'room_id' : room_id, 'sid' : request.sid}, broadcast=True, to=room_id)
    else:
        emit('userFailedJoin')
        return redirect(url_for('index.html'))

@socketio.on('leave')
def handle_leave(data):
    room_id = data['roomId']
    leave_room(room_id)
    emit('userLeft', {'room_id' : room_id, 'sid' : request.sid}, broadcast=True, to=room_id)


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
    if room_id == False:
        flash('존재하지 않는 채팅방입니다.', 'error')
        return redirect(url_for('index'))
    else:
        return render_template('chat.html', room_id=room_id)

@app.route('/status')
def status():
    return json.jsonify({'status': 'ok'})

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=13242)