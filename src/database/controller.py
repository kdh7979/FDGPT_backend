from sqlalchemy.orm import Session
from src.database.models import ChatRoom, Chat

# def create_chat : 채팅 만들기
def create_chat(db: Session, writer: str, chat: str, room_id:str):
    chat = Chat(writer=writer, chat=chat, room_id=room_id)
    db.add(chat)
    db.commit()
    return chat

# def get_chat : DB에서 채팅 데이터 가져오기
def get_chat_all(db: Session, room_id: str):
    chats = db.query(Chat).filter(Chat.room_id == room_id).all()
    if chats == None:
        return []
    else:
        chat_data = []
        for i in chats:
            res = {}
            res["writer"] = i.writer
            res["chat"] = i.chat
            res["time"] = i.created_at
            chat_data.append(res)   # chat_data: [{"writer":"who", "chat":"chat content", "time", "chatting 시각"}, {...}, ...]
        return chat_data

def get_chat_n(db: Session, room_id: str, n: int):
    chats = db.query(Chat).filter(Chat.room_id == room_id).limit(n).all()
    if chats == None:
        return []
    else:
        chat_data = []
        for i in chats:
            res = {}
            res["writer"] = i.writer
            res["chat"] = i.chat
            res["time"] = i.created_at
            chat_data.append(res)   # chat_data: [{"writer":"who", "chat":"chat content", "time", "chatting 시각"}, {...}, ...]
        return chat_data

def get_chat_count(db: Session, room_id: str):
    count = db.query(Chat).filter(Chat.room_id == room_id).count()
    return count