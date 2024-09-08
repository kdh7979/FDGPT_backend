from sqlalchemy.orm import Session
from src.database.models import ChatRoom, Chat

# 아래 설계한 컨트롤러를 만들어 넣기
# def create_user(db: Session, user: Users, commit : bool = True):
#     db.add(user)
#     if commit:
#         db.commit()
#     return user

# def get_user_by_id(db: Session, user_id: int):
#     return db.query(Users).filter(Users.id == user_id).first()

# TODO 
# def create_chat_room : 채팅방 만들기
def create_chat_room(db: Session, room_id: str, room_name: str):
    chat_room = ChatRoom(room_id = room_id, room_name = room_name)
    db.add(chat_room)
    db.commit()
    return chat_room

# def create_chat : 채팅 만들기
def create_chat(db: Session, chat: str, room_id:str):
    chat = Chat(chat=chat, room_id=room_id)
    db.add(chat)
    db.commit()
    return chat

# def load_chat : DB에서 채팅 데이터 가져오기
def load_chat(db: Session, room_id: int):
    return db.query(Chat).filter(Chat.room_id == room_id).last().chat
