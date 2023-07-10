import random
import os
from fastapi import Depends, UploadFile, File, APIRouter
from models import *
from db import session
from fastapi_jwt_auth import AuthJWT


router = APIRouter(
    prefix="/image",
    tags=["Image"]
)

# nkar avelacnel
@router.post("/user_image")
def add_image_user(image: UploadFile = File(), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user_data = session.query(User).filter_by(email=current_user).first()
    image_file = image.file.read()
    img_name = f"images/{random.random()}-{image.filename}"
    with open(img_name, "wb") as f:
        f.write(image_file)
    img = Image(url=img_name, user_id=user_data.id)
    session.add(img)
    session.commit()
    return 'ok'


# /photos տեսնի իր նկարները
@router.get("/user_photos")
def get_image_user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user_data = session.query(User).filter_by(email=current_user).first()
    return session.query(Image).filter_by(id=user_data.id).all()


# /delete/{id} ջնջի նկարը
@router.delete("/del_photos/{id}")
def get_image_user(id: int):
    data = session.query(Image).get(id)
    os.remove(data.url)
    session.delete(data)
    session.commit()
    return {"ok"}
