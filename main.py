from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from models import *
from routes import *

app = FastAPI()


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


app.include_router(user_routes.router)
app.include_router(admin_routes.router)
app.include_router(auth_routes.router)
app.include_router(msg_routes.router)
app.include_router(request_routes.router)
app.include_router(post_routes.router)
app.include_router(image_routes.router)

