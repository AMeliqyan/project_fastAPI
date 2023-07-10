from fastapi import APIRouter
from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import joinedload

from db import session
from models import *

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


# friend/2 էջում ցույց տալ  2 user - ի նկարները, փոստերը, անձնական տվյալները, ընկերները և այլն :
@router.get("/friend/{id}")
def friend_2(id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    info = session.query(User).filter_by(id=id).one()
    images = session.query(Image).filter_by(user_id=id).all()
    post = session.query(Post).filter_by(user_id=id).all()
    friend = session.query(Friend).filter(Friend.user2_id == id or Friend.user1_id == id).options(
        joinedload(Friend.user1), joinedload(Friend.user2)).all()
    return info, images, post, friend


# @nkeroj jnjel@
@router.delete("/friend/{id}")
def del_friend(id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    friend = session.query(Friend).get(id)
    session.delete(friend)
    session.commit()
    return "delete"
