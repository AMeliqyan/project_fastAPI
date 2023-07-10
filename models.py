import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from db import Base, engine


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    password = Column(String)
    posts = relationship("Post", backref="user")
    block_time = Column(DateTime, default=datetime.datetime.utcnow())


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    post_like = relationship("Post_like", backref="post.id")
    post_comment = relationship("Post_comment", backref="post.id")


class Post_like(Base):
    __tablename__ = "post_like"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE", onupdate="CASCADE"))
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))


class Post_comment(Base):
    __tablename__ = "post_comment"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE", onupdate="CASCADE"))
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    text = Column(String)


class Request(Base):
    __tablename__ = "request"
    id = Column(Integer, primary_key=True)
    from_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    to_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    from_user = relationship('User', primaryjoin="Request.from_id==User.id")


class Friend(Base):
    __tablename__ = "friend"
    id = Column(Integer, primary_key=True)
    user1_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    user2_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    user1 = relationship('User', primaryjoin="Friend.user1_id==User.id")
    user2 = relationship('User', primaryjoin="Friend.user2_id==User.id")


class Image(Base):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))


class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True)
    from_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    to_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    text = Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow())


Base.metadata.create_all(engine)

# join grum enq en paragayum erb erkrord classi verabervox payman petqe stugenq
