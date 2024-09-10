
from flask import Flask, json, request, g, session

from src.middleware.cors import cors
from src.database.database import init_db
from config import config

from src.database.controller import create_chat, get_chat_all, get_chat_count, get_chat_n

from flask_socketio import SocketIO, join_room, leave_room, emit

import requests

def init_app():
    app = Flask(__name__)
    socketio = SocketIO(logger=True, engineio_logger=True, cors_allowed_origins="*")
    socketio.init_app(app)
    app.config["SECRET_KEY"] = config.SECRET_KEY

    cors.init_app(app)

    return app, socketio


app, socketio = init_app()
engine, get_db = init_db()

# 연결이 끊어질때 db close
@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@socketio.on('join')
def handle_join(data):
    room_id = data['room_id']
    unique_uid = request.sid
    join_room(unique_uid) # 2389dhwdbajhdawjd
    session['room_id'] = room_id # 1 or 2

@socketio.on('leave')
def handle_leave(data):
    unique_uid = request.sid
    leave_room(unique_uid)
    session.clear()

@socketio.on('send_message')    # When got message from user
def handle_message(data):
    unique_uid = request.sid
    room_id = session['room_id']
    create_chat(get_db(), writer=unique_uid, chat=data['content'], room_id=unique_uid)
    emit('receive_message', {'content': data["content"], 'is_me': True}, to=unique_uid)
    answer = requests.post('/api/inference/conversation', json={
        "model_id": room_id,
        "conversation": get_chat_all(get_db(), unique_uid) # 과거 대화 기록 다 가져와서 넣기
    })
    create_chat(get_db(), writer=room_id, chat=answer, room_id=unique_uid)
    emit('receive_message', {'content': answer["content"], 'is_me': False}, to=unique_uid)

    n = get_chat_count(get_db(), unique_uid)
    if(n % 4) == 0 and n != 0:
        answer = requests.post('/api/inference/fraud_detect', json={
            "conversation" : get_chat_n(4)
        })

@app.route('/api/items', methods=['GET'])
def items():
    items = [
		{
			"title": "불량 멜룬",
			"location": "UNIST",
			"timestamp": "1분 전",
			"price": 100000,
			"item_id": 1
		},
		{
			"title": "안아줘요 인형",
			"location": "엘리아스",
			"timestamp": "1분 전",
			"price": 100000,
			"item_id": 2
		},
	]
    return json.dumps(items)

@app.route('/api/chat/<opponent_id>', methods=['GET'])   # opponent_id : GPT's id
def chat(opponent_id):
    res = {}
    opponent_id = int(opponent_id)
    if opponent_id == 1:
        res = {
            "opponent_name": "멜룬멜룬1",
            "product_name": "맬론",
            "product_price": 100000,
            "chat" : [{
                    "content": "안녕하세요.",
                    "is_me": True,
                }]
        }
    elif opponent_id == 2:
        res = {
            "opponent_name": "멜룬멜룬2",
            "product_name": "맬론",
            "product_price": 100000,
            "chat" : [{
                    "content": "안녕하세요.",
                    "is_me": True,
                }]
        }
    return json.dumps(res)


@app.route('/api/item/<item_id>', methods=['GET'])
def item_detail(item_id):
    item_id = int(item_id)
    res = {}
    if item_id == 1:
        res = {
            "title": "멜론",
            "location": "UNIST",
            "timestamp": "1분 전",
            "price": 100000,
            "writer": "멜룬멜룬",
            "description": "불법 유통한 멜?루 입니다.\n불량한 멜룬 아닙니다.\n\n너무 멜룬멜룬 하지 않아 식용 가능 합니다. \n\n멜룬다고.",
            "chat_room_id": 1 # opponent_id랑 똑같음
        }
    elif item_id == 2:
        res = {
            "title": "안아줘요 인형",
            "location": "엘리아스",
            "timestamp": "1분 전",
            "price": 100000,
            "writer": "멜룬멜룬",
            "description": "불법 유통한 멜?루 입니다.\n불량한 멜룬 아닙니다.\n\n너무 멜룬멜룬 하지 않아 식용 가능 합니다. \n\n멜룬다고.",
            "chat_room_id": 2 # opponent_id랑 똑같음
        }
    return json.dumps(res)


# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/chat/<room_id>')
# def chatting(room_id):
#     room_id = get_room(get_db(), room_id)
#     if room_id == "NO_ROOM":
#         # flash('존재하지 않는 채팅방입니다.', 'error')
#         return redirect(url_for('index'))
#     else:
#         chats = get_chat_all(get_db(), room_id=room_id)
#         emit('chats', {'chats' : chats})
#         return render_template('chat.html', room_id=room_id)

@app.route('/status')
def status():
    return json.jsonify({'status': 'ok'})

if __name__ == "__main__":
    socketio.run(app, "0.0.0.0", port=8081, debug=True)