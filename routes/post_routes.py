from db import session
from fastapi import  Depends, Body, APIRouter
from models import *
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import joinedload



router = APIRouter(
    prefix="/Post",
    tags=["Post"]
)
@router.post('/add-post')
def add_post(title: str = Body(), body: str = Body(), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()  # partadir login lini
    current_user = Authorize.get_jwt_subject()
    user_data = session.query(User).filter_by(email=current_user).first()
    post = Post(title=title, body=body, user_id=user_data.id)
    session.add(post)
    session.commit()
    return {"msg": "Successfully added"}


# /my-posts էջում ցուցադրել լոգին եղած user - ի post - երը։
@router.get("/my_posts")
def get_my_post(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()  # partadir login lini
    current_user = Authorize.get_jwt_subject()
    user_data = session.query(User).filter_by(email=current_user).first()
    data = session.query(Post).filter_by(user_id=user_data.id).options(joinedload(Post.post_like),
                                                                       joinedload(Post.post_comment)).all()
    return data


# /posts էջում ցուցադրել բոլոր user - ների post - երը։
@router.get("/posts")
def get_post(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()  # partadir login lini
    return session.query(Post).options(joinedload(Post.post_like), joinedload(Post.post_comment)).all()


# Ստեղծել post - ին comment գրելու և like -ի  հնարավորություն։

@router.post("/post_comment")
def post_comment(post_id: int = Body(), text: str = Body(), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user_data = session.query(User).filter_by(email=current_user).first()
    comment = Post_comment(post_id=post_id, user_id=user_data.id, text=text)
    session.add(comment)
    session.commit()
    return {"SMS": "ADD"}


@router.post("/post_like/{post_id}")
def like_post(post_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user_data = session.query(User).filter_by(email=current_user).first()
    data = session.query(Post_like).filter_by(post_id=post_id, user_id=user_data.id).first()

    print(data)
    if data:
        new_like = Post_like(post_id=post_id, user_id=user_data.id)
        session.add(new_like)
        session.commit()
        return {"sms": "add"}
    else:
        session.delete(data)
        session.commit()
        return {"SMS": "del"}
