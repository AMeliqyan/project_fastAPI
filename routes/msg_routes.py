from fastapi import APIRouter
from fastapi import  Depends,  Body
from fastapi_jwt_auth import AuthJWT
from db import session
from models import *


router = APIRouter(
    prefix="/messenger",
    tags=["Messeng"]
)
# namak avelacnel
@router.post("/message")
def post_message(text: str = Body(), to_id: int = Body(), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user_data = session.query(User).filter_by(email=current_user).first()
    sms = Message(text=text, to_id=to_id, from_id=user_data.id)
    session.add(sms)
    session.commit()
    return {"ok"}
