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

# def get_chat : DB에서 채팅 데이터 가져오기
def get_chat(db: Session, room_id: int):
    last_chat = db.query(Chat).filter(Chat.room_id == room_id).last()
    if last_chat == None:
        return
    else:
        return last_chat.chat


# def get_room : DB에서 채팅방 아이디가 있는지 확인
def get_room(db: Session, room_id: str):
    room = db.query(ChatRoom).filter(ChatRoom.room_id == room_id).first()
    if room==None:
        print(f"{room_id} not found in db")
        return False
    else:
        return room.room_id