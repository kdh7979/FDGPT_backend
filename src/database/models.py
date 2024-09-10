from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey

from src.database.database import engine

Base = declarative_base()

class ChatRoom(Base):
    __tablename__ = "chat_rooms" # 여기에 테이블 이름
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(String)
    room_name = Column(String)

class Chat(Base):
    __tablename__ = "chat"
    id = Column(Integer, primary_key=True, index=True)
    writer = Column(String)
    chat = Column(String)
    room_id = Column(String)
    created_at = Column(DateTime, server_default=current_timestamp())


# 데이터베이스 생성
Base.metadata.create_all(bind=engine)