from fastapi import APIRouter, Body, HTTPException
from fastapi import Depends
from fastapi_jwt_auth import AuthJWT

from db import session
from models import *
from passlib.context import CryptContext

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password): #passwordi kodavorman hamar
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):# stugelu hamar passwordi chishta te voch
    return pwd_context.verify(plain_password, hashed_password)


@router.post('/register')
def register(name: str = Body(), surname: str = Body(), email: str = Body(), password: str = Body()):
    user = User(name=name, surname=surname, email=email, password=get_password_hash((password)))
    session.add(user)
    session.commit()
    return {"message": "success"}


@router.post('/login')
def login(email: str = Body(), password: str = Body(), Authorize: AuthJWT = Depends()):
    user = session.query(User).filter_by(email=email).first()
    dt = datetime.datetime.now()
    if not user:
        raise HTTPException(status_code=401, detail="wrong email")
    elif not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Wrong password")
    elif dt < user.block_time:
        raise HTTPException(status_code=401, detail="user blocked")
    access_token = Authorize.create_access_token(subject=user.email)
    Authorize.set_access_cookies(access_token)
    return {"access_token": access_token}


@router.get('/profile')
def profile(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()  # stgum e toqn ka te voch
    current_user = Authorize.get_jwt_subject()
    user_data = session.query(User).filter_by(email=current_user).first()
    return {"user": user_data}


# passwordi popoxutyun
@router.put("/user_password")
def put_user(old_password: str = Body(), new_password: str = Body(), repeat_password: str = Body(),
             Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user_data = session.query(User).filter_by(email=current_user).first()
    if verify_password(old_password, user_data.password) and new_password == repeat_password:
        user_data.password = get_password_hash(new_password)
        session.commit()
        return "put"
    else:
        return HTTPException(detail="error", status_code=400)


@router.delete('/logout')
def logout(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    Authorize.unset_jwt_cookies()
    return {"msg": "Successfully logout"}
