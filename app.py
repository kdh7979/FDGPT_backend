from flask import Flask, json, request, g, session

from src.middleware.cors import cors
from src.database.database import init_db
from config import config

from src.database.controller import create_chat, get_chat_all, get_chat_count, get_chat_n
from src.api.api import get_next_conversation, get_fraud_detection

from flask_socketio import SocketIO, join_room, leave_room, emit

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
    answer = get_next_conversation(model_id=room_id, conversation=[{"writer":unique_uid, "content":"안녕하세요."}])
    emit('receive_message', {'content': answer["content"], 'is_me': False}, to=unique_uid)
    create_chat(get_db(), writer=unique_uid, content="안녕하세요.", room_id=unique_uid)
    create_chat(get_db(), writer=room_id, content=answer["content"], room_id=unique_uid)
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
    create_chat(get_db(), writer=unique_uid, content=data['content'], room_id=unique_uid)
    emit('receive_message', {'content': data["content"], 'is_me': True}, to=unique_uid)
    answer = get_next_conversation(model_id=room_id, conversation=json.dumps(get_chat_all(get_db(), unique_uid)))

    create_chat(get_db(), writer=room_id, content=answer["content"], room_id=unique_uid)
    emit('receive_message', {'content': answer["content"], 'is_me': False}, to=unique_uid)

    n = get_chat_count(get_db(), unique_uid)
    if(n % 4) == 0 and n != 0:
        res = get_fraud_detection(conversation=get_chat_all(get_db(), unique_uid))
        if res["is_fraud"] == True:
            emit('alert', {"content": res["warning"]})

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
            "opponent_name": "멜룬멜룬",
            "product_name": "맬론",
            "product_price": 100000,
            "chat" : [{
                    "content": "안녕하세요.",
                    "is_me": True,
                }]
        }
    elif opponent_id == 2:
        res = {
            "opponent_name": "안아줘요",
            "product_name": "안아줘요 인형",
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
            "writer": "안아줘요",
            "description": "부드라미 인형 안아줘요 안아줘욥 날다람쥐 중형인형 입니다\n새상품이고\n여러개 구매 가능합니다 1.8 > 1.6 가격내림\n\n제발안아줘요 인형도 있어요 1.6 여러개 있음 즉입시 개당 1.5씩\n\n!!! 부드라미 햄스터 인형 1.8 > 1.6씩 2개 있음\n\n반택+0.2 편택+0.35\n여러 개 구매 우대하지만 개별도 문의받습니다 ㅠ 2개 이상 구매시 절충가능합니다",
            "chat_room_id": 2 # opponent_id랑 똑같음
        }
    return json.dumps(res)

@app.route('/status')
def status():
    return json.jsonify({'status': 'ok'})

if __name__ == "__main__":
    # socketio.run(app, "0.0.0.0", port=8081, debug=True, log_output=True)
    socketio.run(app, "0.0.0.0", port=8081, debug=True)