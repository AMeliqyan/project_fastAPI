import datetime

from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from db import session
from models import User

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

# Ստեղծել հնարավորություն user - ին բլոկելու
@router.post("/block/{id}")
def block_time(id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user = session.query(User).filter_by(id=id).first()
    dt = datetime.datetime.now() + datetime.timedelta(minutes=5)
    user.block_time = dt
    session.commit()
    return 'block'
