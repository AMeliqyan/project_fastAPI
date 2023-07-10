from fastapi import  Depends, Request, APIRouter
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import joinedload
from db import session
from models import *


router = APIRouter(
    prefix="/request",
    tags=["Request"]
)
# pntrel @st anvan
@router.get("/user_name_search/{name}")
def get_user_name(name: str, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    data = session.query(User).filter(User.name.like(f"{name}%")).all()
    return data


# harcum uxarkelu hamar
@router.post("/send_request")
def send_request(id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user_data = session.query(User).filter_by(email=current_user).first()
    send = Request(from_id=user_data.id, to_id=id)
    session.add(send)
    session.commit()
    return {"SMS": "Harcum@ uxarkvac e"}


# inc ekac harcumnner@
@router.get("/request")
def request(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user_data = session.query(User).filter_by(email=current_user).first()
    request = session.query(Request).filter_by(to_id=user_data.id).options(joinedload(Request.from_user)).all()
    return request


# @nkeranalu harcum@ yndunel
@router.post("/accept/{id}")
def accept(id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    accept = session.query(Request).get(id)
    data = Friend(user1_id=accept.from_id, user2_id=accept.to_id)
    session.add(data)
    session.delete(accept)
    session.commit()
    return {"SMS": "@ndunel e"}


# @nkeranalu harcum@ chexarkel
@router.delete("/decline/{id}")
def del_friend(id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    del_fr = session.query(Request).get(id)
    session.delete(del_fr)
    session.commit()
    return {"SMS": "jnjvel e"}
